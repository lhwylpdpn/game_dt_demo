import os
import sys
import json
import time
import configparser
from schedule.strategy.game import Game as game_broad
from schedule.strategy.agent import Agent as agent
# from test_hero_data import origin_hero_data  # 后续通过api获取前端传递的数据
# from test_map_data import origin_map_data  # 后续通过api获取前端传递的数据
# from test_monster_data import origin_monster_data  # 后续通过api获取前端传递的数据
import copy
import math
from schedule.utils.tools import Deepdiff_modify
from schedule.utils.tools import performance
from log.log import log_manager


# step0 调度接到外部的开始请求，传入初始地图，传入初始角色，传入计算信息
# step1 调度开始游戏,调用棋盘初始化游戏
# step2 调度开始自增计时器
# step3 调度获取棋盘中可用游戏角色的ap
# step3.5 获取当前状态
# step4 判断能整除谁的时候，使用棋子调用决策树获得行动
# step4.5 调用棋盘执行行动
# step5 检查游戏是否结束
# step6 如果游戏结束，产生内容序列

# 需要在刷新了各项配置文件后，引用game，game里用到了配置文件的内容


class schedule:

    def __init__(self, left_hero,right_hero,state, battle_id=0):

        self.battle_id = battle_id
        self.redis_expiration_time = 7 * 24 * 60 * 60
        self.hero_list = left_hero
        self.state = state
        self.monster_list = right_hero

        self.game = game_broad(hero=self.hero_list, maps=self.state, monster=self.monster_list, attachment=None,setting=None)
        self.agent_1 = agent()
        self.agent_2 = agent()
        self.timeout_tick = 2000
        self.tick = 0
        self.record_update_dict = {}
        self.record_update_dict_update = {}  # 测试用
        self.record_error_dict = {}
        self.action_dict = {}
        self.ap_parm = 30  # 特定设置，代表一个tick增加速度/20 个ap
        self.ap_limit = 100  # 游戏设置，代表每满足100个ap就动一次
        self.game_over = False
        self.init_state = None  # 特定用于给强爷传输初始状态
        ##统计



        self.performance = performance()


        self.performance.event_start('get_current_state')
        state = self.game.get_current_state()
        state_dict = self.state_to_dict(state)  # todo  优化性能

        self.init_state = state_dict
        self.performance.event_end('get_current_state')

        alive_hero = self.game.get_current_alive_hero()
        # 初始化 英雄: 行动回合
        # self.hero_next_action_round = {hero.HeroID: math.ceil(self.ap_limit / (hero.Velocity / self.ap_parm)) for hero in alive_hero}
        self.hero_next_action_round = []
        for hero in alive_hero:
            self.hero_next_action_round.append(
                {
                    "id": hero.HeroID,
                    "speed": math.ceil(self.ap_limit / (hero.Velocity / self.ap_parm)),
                    "class": hero.__class__.__name__.lower()
                }
            )
    def start(self):
        self.performance.event_start('game_start')
        self.game.start()
        self.performance.event_end('game_start')


    def single_run(self,fun_,client,card_action_list):
        alive_hero = self.game.get_current_alive_hero()
        #根据alive_hero里每个hero.Velocity 重新排序alive_hero
        alive_hero.sort(key=lambda x: x.Velocity, reverse=True)
        state = self.game.get_current_state()
        state_dict = self.state_to_dict(state)
        self.fun_=fun_
        self.client=client
        self.max_action_num =float('inf')
        self.temp_action_num = 0
        self.temp_hero_num = float('inf')
        self.max_hero_num = 0

        for __action in card_action_list:
            hero=__action['hero obj']
            if hero.camp == 'p1':
                action_result = self.game.hero_action(hero, action)

            else:
                action_result = self.game.monster_action(hero, action)

            if not action_result:  # 如果动作失败，直接跳出本次动作链路
                break
            if isinstance(action_result, dict):
                action_result = [action_result]
            new_state = self.game.get_current_state()
            new_state_dict = self.state_to_dict(new_state)

            for action in action_result:

                if self.game.check_game_over()[0]:
                    self.game_over = True
                    self.max_action_num = 0
                    self.temp_action_num = 0
                    self.temp_hero_num = 0
                    self.max_hero_num = 0
                action['id'] = hero.HeroID
                action['unique_id'] = hero.unique_id
                action['class'] = hero.camp
                action['step']=hero['step']
                self._record(action, state_dict, new_state_dict)
                self.tick += 1
                if self.game_over:
                    return self.game_over
                # 每次实际行动就自增tick加1，这样1个tick代表一次行动
            state = new_state
            state_dict = self.state_to_dict(state)

        #为了返回roundover 单独增加的计数器
        self.max_hero_num=len(alive_hero)
        self.temp_hero_num=0
        for hero in alive_hero:
            self.temp_hero_num+=1
            if hero.is_death:  # 同一个tick里也可能，后轮到的英雄被先轮到的打死
                continue
            actions=None
            if hero.camp == 'p1':
                self.performance.event_start('schedule_choose_action')
                actions = self.agent_1.choice_hero_act(hero, state, self.performance)
                # print('tick', self.tick, '调度获得的行动list: 英雄', alive_hero_id, actions)
                # log_manager.add_log({'stepname':'调度获得的行动list','tick':self.tick,'hero':alive_hero_id,'class':alive_hero_class,'actions':actions})
                self.performance.event_end('schedule_choose_action')
            if hero.camp == 'p2':
                self.performance.event_start('schedule_choose_action')
                actions = self.agent_2.choice_monster_act(hero, state, self.performance)
                # print('tick', self.tick, '调度获得的行动list: 怪兽', alive_hero_id, actions)
                # log_manager.add_log({'stepname':'调度获得的行动list','tick':self.tick,'hero':alive_hero_id,'class':alive_hero_class,'actions':actions})
                self.performance.event_end('schedule_choose_action')
            self.max_action_num=len(actions)
            self.temp_action_num=0
            for action in actions:
                self.temp_action_num+=1
                action_result=[]
                self.performance.event_start('game_action')
                if hero.camp == 'p1':
                    action_result = self.game.hero_action(hero, action)

                else:
                    action_result = self.game.monster_action(hero, action)
                self.performance.event_end('game_action')

                if not action_result:  # 如果动作失败，直接跳出本次动作链路
                    break
                if isinstance(action_result, dict):
                    action_result = [action_result]
                self.performance.event_start('get_current_state')
                new_state = self.game.get_current_state()
                new_state_dict = self.state_to_dict(new_state)
                self.performance.event_end('get_current_state')

                for action in action_result:

                    if self.game.check_game_over()[0]:
                        self.game_over=True
                        self.max_action_num=0
                        self.temp_action_num=0
                        self.temp_hero_num=0
                        self.max_hero_num=0

                    action['id'] = hero.HeroID
                    action['unique_id'] = hero.unique_id
                    action['class'] = hero.camp
                    action['step']=hero['step']
                    self._record(action, state_dict, new_state_dict)
                    self.tick+=1
                    if self.game_over:
                        return  self.game_over
                    #每次实际行动就自增tick加1，这样1个tick代表一次行动
                self.performance.event_start('get_current_state')
                state = new_state
                state_dict = self.state_to_dict(state)
                self.performance.event_end('get_current_state')

    def run(self):

        while self.tick < self.timeout_tick and not self.game_over:
            self.tick += 1
            self.next()
        self.performance.end()
        self.performance.tick = self.tick
        return self.game.check_game_over()[1]




    def next(self):


        self.performance.event_start('get_current_alive_hero')
        alive_hero = self.game.get_current_alive_hero()
        self.performance.event_end('get_current_alive_hero')
        # todo  同tick 的顺序问题，同tick的时候是不是有排序

        alive_hero_ids = [_.HeroID for _ in alive_hero]
        self.hero_next_action_round = [_ for _ in self.hero_next_action_round if _["id"] in alive_hero_ids]

        have_action_status = False
        for hero in alive_hero:
            if hero.is_death:  # 同一个tick里也可能，后轮到的英雄被先轮到的打死
                continue
            once_tick = math.ceil(self.ap_limit / (hero.Velocity / self.ap_parm))
            if self.tick % once_tick == 0:
                have_action_status=True
        if have_action_status:
            self.performance.event_start('get_current_state')
            state = self.game.get_current_state()

            state_dict = self.state_to_dict(state)

            self.performance.event_end('get_current_state')
        else:
            return self.game.get_current_state()

        for hero in alive_hero:
            # hero是一个对象，想获得它的类名
            # print('tick',self.tick,'调度当前拿到的活着hero', hero.__class__.__name__.lower(), hero.HeroID,)
            # log_manager.add_log({'stepname':'拿到的存活的英雄','tick':self.tick,'hero':hero.HeroID,'class':hero.__class__.__name__.lower()})
            if hero.is_death:  # 同一个tick里也可能，后轮到的英雄被先轮到的打死
                continue
            alive_hero_class = hero.__class__.__name__.lower()
            alive_hero_id = hero.HeroID
            # 向上取整
            once_tick = math.ceil(self.ap_limit / (hero.Velocity / self.ap_parm))
            # print('once_tick',self.tick,hero.Velocity,once_tick,hero.__class__.__name__.lower(), hero.HeroID,)

            if self.tick % once_tick == 0:
                print(
                    f"----------------------------------------- tick: {self.tick}, role: {hero.HeroID}  ----------------------------------------- ")
                self.performance.event_start('focus')
                #print('focus',type(state),state)

                focus = hero.focus(state)
                self.performance.event_end('focus')
                # 查看hero的队列
                if alive_hero_class == 'hero':
                    self.performance.event_start('schedule_choose_action')
                    actions = self.agent_1.choice_hero_act(hero, state, self.performance)
                    #print('tick', self.tick, '调度获得的行动list: 英雄', alive_hero_id, actions)
                    # log_manager.add_log({'stepname':'调度获得的行动list','tick':self.tick,'hero':alive_hero_id,'class':alive_hero_class,'actions':actions})
                    self.performance.event_end('schedule_choose_action')
                if alive_hero_class == 'monster':
                    self.performance.event_start('schedule_choose_action')
                    actions = self.agent_2.choice_monster_act(hero, state, self.performance)
                    #print('tick', self.tick, '调度获得的行动list: 怪兽', alive_hero_id, actions)
                    # log_manager.add_log({'stepname':'调度获得的行动list','tick':self.tick,'hero':alive_hero_id,'class':alive_hero_class,'actions':actions})
                    self.performance.event_end('schedule_choose_action')
                self.performance.event_start('un_focus')
                un_focus = hero.un_focus(state)

                # 计算行动顺序
                target_item = None
                for h in self.hero_next_action_round:
                    if h["id"] == hero.HeroID:
                        h["speed"] += once_tick
                        target_item = h
                        self.hero_next_action_round.remove(h)

                self.hero_next_action_round.sort(key=lambda x: (x['speed'], x['id']))
                # 再次判断 同一ticker里，后续英雄是否死亡
                alive_hero_ids = [_.HeroID for _ in alive_hero if _.Hp > 0]
                self.hero_next_action_round = [_ for _ in self.hero_next_action_round if _["id"] in alive_hero_ids]
                self.hero_next_action_round = [target_item] + self.hero_next_action_round

                # action_order = [f"{_['id']}({_['speed']})" for _ in self.hero_next_action_round]
                # print(f" ===>>>   所有英雄未来行动顺序: {', '.join(action_order)}")
                sequence = copy.deepcopy(self.hero_next_action_round)
                # 增加特定初始动作，用于显示移动情况
                move_ = [{"action_type": "MOVE_START", "sequence": sequence}]

                actions = focus + move_ + actions + un_focus
                self.performance.event_end('un_focus')
                # print('tick',self.tick,'合并后调度获得的行动list: 总', alive_hero_id,actions)
                # log_manager.add_log({'stepname':'合并后调度获得的行动list','tick':self.tick,'hero':alive_hero_id,'class':alive_hero_class,'actions':actions})
                for action in actions:
                    # print('调度行动',self.tick,'id',alive_hero_id,'class',alive_hero_class,action)
                    action_result=[]
                    self.performance.event_start('game_action')
                    if hero.__class__.__name__.lower() == 'hero':
                        action_result = self.game.hero_action(hero, action)

                    else:
                        action_result = self.game.monster_action(hero, action)
                    self.performance.event_end('game_action')
                    log_manager.add_log({'stepname': '调度行动-接到动作结果', 'tick': self.tick, 'hero': alive_hero_id,
                                         'class': alive_hero_class, 'action_result': action_result})
                    if not action_result:  # 如果动作失败，直接跳出本次动作链路
                        # print('调度行动-接到动作失败',self.tick,'id',alive_hero_id,'class',alive_hero)
                        log_manager.add_log(
                            {'stepname': '调度行动-接到动作失败', 'tick': self.tick, 'hero': alive_hero_id,
                             'class': alive_hero_class})
                        break
                    if isinstance(action_result, dict):
                        action_result = [action_result]
                    self.performance.event_start('get_current_state')
                    new_state = self.game.get_current_state()
                    new_state_dict = self.state_to_dict(new_state)
                    self.performance.event_end('get_current_state')

                    for action in action_result:


                        self.performance.event_start('record')
                        action['unique_id'] = _.unique_id
                        # action['class'] = alive_hero_class
                        if action['action_type'] != 'SKILL_82':  # 反击
                            action['id'] = alive_hero_id
                            action['class'] = alive_hero_class
                        self._record(action, state_dict, new_state_dict)

                    self.performance.event_end('record')
                    self.performance.event_start('get_current_state')
                    state = new_state
                    state_dict = self.state_to_dict(state)
                    self.performance.event_end('get_current_state')

                # 2024-10-21 调整存储redis结构

                self.performance.event_start('check_game_over')
                if self.game.check_game_over()[0]:
                    # print('战斗结束了！！！！',self.game.check_game_over()[1])
                    log_manager.add_log(
                        {'stepname': '战斗结束了', 'tick': self.tick, 'game_over': self.game.check_game_over()[1]})
                    self.performance.event_end('check_game_over')
                    self.game_over = True
                    if self.record_update_dict.get(self.tick) is not None:
                        #self.record_update_dict[self.tick]['sequence'] = self.hero_next_action_round
                        self.save_result_to_redis(self.record_update_dict[self.tick])

                    return state
                self.performance.event_end('check_game_over')
        if self.record_update_dict.get(self.tick) is not None:
            self.record_update_dict[self.tick]['sequence'] = self.hero_next_action_round
            self.save_result_to_redis(self.record_update_dict[self.tick])
    # 增加一个state静态化的方法

        return state
    def state_to_dict(self, state):
        # from pympler import asizeof
        # from utils.tools import print_object_details
        # state_size = asizeof.asizeof(state['maps'])
        # print_object_details(state['maps'])
        # print(f"当前 map state 占用内存: {state_size} 字节")
        # state_size = asizeof.asizeof(state['hero'])
        # print_object_details(state['hero'])
        #
        # print(f"当前 hero state 占用内存: {state_size} 字节")
        # state_size = asizeof.asizeof(state['monster'])
        # print(f"当前 monster state 占用内存: {state_size} 字节")
        # state_size = asizeof.asizeof(state['attachment'])
        # print(f"当前 attachment state 占用内存: {state_size} 字节")
        # state_size = asizeof.asizeof(state['setting'])
        # print(f"当前 setting state 占用内存: {state_size} 字节")

        map = copy.deepcopy(state['maps'])
        hero = copy.deepcopy(state['hero'])
        monster = copy.deepcopy(state['monster'])

        #
        # attachment = copy.deepcopy(state['attachment'])
        # setting=copy.deepcopy(state['setting'])

        if type(map) != list:
            map = [map]
        if type(hero) != list:
            hero = [hero]
        if type(monster) != list:
            monster = [monster]
        # if type(attachment) != list:
        #     attachment = [attachment]
        # if type(setting)!=list:
        #     setting=[setting]

        map_dict = {}
        hero_dict = {}
        monster_dict = {}
        # map3_dict = {}
        # map4_dict = {}

        for i in range(len(map)):
            map_dict[i] = map[i].dict(for_view=True)
        for h in hero:
            hero_dict[h.HeroID] = h.dict(for_view=True)
        for m in monster:
            monster_dict[m.HeroID] = m.dict(for_view=True)
        # for a in attachment:
        #     #attachment_dict[a.MapID] = a.dict()
        #     if a.Layer == 3:
        #         map3_dict[a.MapID] = a.dict()
        #     if a.Layer == 4:
        #         map4_dict[a.MapID] = a.dict()
        res = {'map': map_dict, 'hero': hero_dict, 'monster': monster_dict,
               #'map3': map3_dict, "map4":map4_dict,
               #'attachment': attachment_dict,
               #"setting":setting
                }
        del map
        del hero
        del monster
        # del attachment
        # del setting

        return res

    # def state_to_dict_new(self,state):
    #     if type(state['map'])!=list:
    #         map=[state['map']]
    #     else:
    #         map=state['map']
    #     if type(state['hero'])!=list:
    #         hero=[state['hero']]
    #     else:
    #         hero=state['hero']
    #     if type(state['monster'])!=list:
    #         monster=[state['monster']]
    #     else:
    #         monster=state['monster']
    #
    #     map_dict={}
    #     hero_dict={}
    #     monster_dict={}
    #     for i in range(len(map)):
    #         map_dict[i]=map[i].dict(for_view=True)
    #     for h in hero:
    #         hero_dict[h.HeroID]=h.dict(for_view=True)
    #     for m in monster:
    #         monster_dict[m.HeroID]=m.dict(for_view=True)
    #     res = json.dumps({'map': map_dict, 'hero': hero_dict, 'monster': monster_dict})
    #     return json.loads(res)
    def _record(self, action, before_state, after_state):
        # self.performance.event_start('record_detail')
        update_dict = Deepdiff_modify(before_state, after_state)
        if self.tick not in self.record_update_dict:
            self.record_update_dict[self.tick] = {'action': [],'state': [], 'tick': 0,'step': 'auto_fight', 'gameover': False}
        self.record_update_dict[self.tick]['action']=action
        self.record_update_dict[self.tick]['state'].append(update_dict)
        self.record_update_dict[self.tick]['tick'] = self.tick
        self.record_update_dict[self.tick]['step'] = action['step']
        self.record_update_dict[self.tick]['gameover'] = self.game_over
        if self.temp_action_num==self.max_action_num and self.temp_hero_num==self.max_hero_num:
            #如果是最后一个英雄的最后一个动作,就roundover是True
            self.record_update_dict[self.tick]['roundover'] =True
        else:
            self.record_update_dict[self.tick]['roundover'] = False
        self.fun_(self.client,self.client.player.playerId,self.record_update_dict[self.tick])
        #todo 调用彬哥

    def save_result_to_redis(self):


        print('这里是返回动作',self.record_update_dict)
        #redis_client.rpush(redis_key_2, json.dumps(record_update_dict))


def main(state, battle_id, out_file_name):
    sch = schedule(state, battle_id)
    sch.start()
    sch.run()
    update = sch.send_update(out_file_name)
    sch.performance.static()
    return update


def save_result_to_view(data, path):
    with open(path, 'w') as file:
        # json.dump(data, file)
        file.write(data)
    return



if __name__ == '__main__':
    ## python schedule.py src_path result_path
    a = time.time()
    src_path = sys.argv[1] if len(sys.argv) > 2 else "data.json"  # 源文件地址
    result_file = sys.argv[2] if len(sys.argv) >= 3 else "result.json"  # result地址
    battle_id = sys.argv[3] if len(sys.argv) >= 4 else 0  # battle_id
    state = BuildPatrol(src_path).load_data()  # 初始化对象
    # state={"map": map, "hero": heros, "monster": monster}
    main(state, battle_id, result_file)
    # save_result_to_view(result, result_file)
    # print('总时间',time.time()-a)
