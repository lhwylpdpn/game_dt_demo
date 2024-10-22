import os
import sys
import json
import time
from strategy.game import Game as game_broad
from strategy.agent import Agent as agent
from buildpatrol import BuildPatrol
# from test_hero_data import origin_hero_data  # 后续通过api获取前端传递的数据
# from test_map_data import origin_map_data  # 后续通过api获取前端传递的数据
# from test_monster_data import origin_monster_data  # 后续通过api获取前端传递的数据
import copy
import math
from utils.tools import Deepdiff_modify
from utils.tools import performance
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
import redis
import configparser

cf = configparser.ConfigParser()
path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
cf.read(path + '/config/conf.ini', encoding='utf-8')

redis_host = cf.get('redis', 'host')
redis_port = cf.get('redis', 'port')
redis_db_index = cf.get('redis', 'index')
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db_index, decode_responses=True)


class schedule:

    def __init__(self, state, battle_id=0):

        self.battle_id = battle_id
        self.redis_expiration_time = 7 * 24 * 60 * 60
        self.hero_list = state['hero']
        self.state = state['map']
        self.monster_list = state['monster']
        self.game = game_broad(hero=self.hero_list, maps=self.state, monster=self.monster_list)
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

    def start(self):
        self.performance.event_start('game_start')
        self.game.start()
        self.performance.event_end('game_start')

    def run(self):
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

        while self.tick < self.timeout_tick and not self.game_over:
            self.tick += 1
            self.next()
        self.performance.end()
        self.performance.tick = self.tick
        return self.game.check_game_over()[1]

    def next(self):
        self.performance.event_start('get_current_state')
        state = self.game.get_current_state()
        state_dict = self.state_to_dict(state)
        self.performance.event_end('get_current_state')

        self.performance.event_start('get_current_alive_hero')
        alive_hero = self.game.get_current_alive_hero()
        self.performance.event_end('get_current_alive_hero')
        # todo  同tick 的顺序问题，同tick的时候是不是有排序

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

                focus = hero.focus(state)
                self.performance.event_end('focus')

                # 增加特定初始动作，用于显示移动情况
                move_ = [{"action_type": "MOVE_START"}]
                # 查看hero的队列

                if alive_hero_class == 'hero':
                    self.performance.event_start('schedule_choose_action')
                    actions = self.agent_1.choice_hero_act(hero, state, self.performance)
                    print('tick', self.tick, '调度获得的行动list: 英雄', alive_hero_id, actions)
                    # log_manager.add_log({'stepname':'调度获得的行动list','tick':self.tick,'hero':alive_hero_id,'class':alive_hero_class,'actions':actions})
                    self.performance.event_end('schedule_choose_action')
                if alive_hero_class == 'monster':
                    self.performance.event_start('schedule_choose_action')
                    actions = self.agent_2.choice_monster_act(hero, state, self.performance)
                    print('tick', self.tick, '调度获得的行动list: 怪兽', alive_hero_id, actions)
                    # log_manager.add_log({'stepname':'调度获得的行动list','tick':self.tick,'hero':alive_hero_id,'class':alive_hero_class,'actions':actions})
                    self.performance.event_end('schedule_choose_action')
                self.performance.event_start('un_focus')
                un_focus = hero.un_focus(state)
                actions = focus + move_ + actions + un_focus
                self.performance.event_end('un_focus')

                # print('tick',self.tick,'合并后调度获得的行动list: 总', alive_hero_id,actions)
                # log_manager.add_log({'stepname':'合并后调度获得的行动list','tick':self.tick,'hero':alive_hero_id,'class':alive_hero_class,'actions':actions})
                for action in actions:

                    # print('调度行动',self.tick,'id',alive_hero_id,'class',alive_hero_class,action)
                    self.performance.event_start('game_action')
                    if hero.__class__.__name__.lower() == 'hero':
                        action_result = self.game.hero_action(hero, action)
                    else:
                        action_result = self.game.monster_action(hero, action)
                    self.performance.event_end('game_action')
                    # print('调度行动-接到动作结果',self.tick,'id',alive_hero_id,'class',alive_hero,action_result)
                    log_manager.add_log({'stepname': '调度行动-接到动作结果', 'tick': self.tick, 'hero': alive_hero_id,
                                         'class': alive_hero_class, 'action_result': action_result})
                    if not action_result:  # 如果动作失败，直接跳出本次动作链路
                        # print('调度行动-接到动作失败',self.tick,'id',alive_hero_id,'class',alive_hero)
                        log_manager.add_log(
                            {'stepname': '调度行动-接到动作失败', 'tick': self.tick, 'hero': alive_hero_id,
                             'class': alive_hero_class})
                        break

                    self.performance.event_start('get_current_state')
                    new_state = self.game.get_current_state()
                    new_state_dict = self.state_to_dict(new_state)
                    self.performance.event_end('get_current_state')

                    self.performance.event_start('record')
                    action_result['id'] = alive_hero_id
                    action_result['class'] = alive_hero_class
                    self._record(action_result, state_dict, new_state_dict)
                    self.performance.event_end('record')

                    self.performance.event_start('get_current_state')
                    state = new_state
                    state_dict = self.state_to_dict(state)
                    self.performance.event_end('get_current_state')

                target_item = None
                for h in self.hero_next_action_round:
                    if h["id"] == hero.HeroID:
                        h["speed"] += once_tick
                        target_item = h
                        self.hero_next_action_round.remove(h)

                self.hero_next_action_round.sort(key=lambda x: x['speed'])
                self.hero_next_action_round = [target_item] + self.hero_next_action_round

                action_order = [f"{_['id']}({_['speed']})" for _ in self.hero_next_action_round]
                # print(f" ===>>>   所有英雄未来行动顺序: {', '.join(action_order)}")

                # 2024-10-21 调整存储redis结构

                self.performance.event_start('check_game_over')
                if self.game.check_game_over()[0]:
                    # print('战斗结束了！！！！',self.game.check_game_over()[1])
                    log_manager.add_log(
                        {'stepname': '战斗结束了', 'tick': self.tick, 'game_over': self.game.check_game_over()[1]})
                    self.performance.event_end('check_game_over')
                    self.game_over = True
                    if self.record_update_dict.get(self.tick) is not None:
                        self.record_update_dict[self.tick]['sequence'] = self.hero_next_action_round
                        self.save_result_to_redis(self.record_update_dict[self.tick])

                    return
                self.performance.event_end('check_game_over')
        if self.record_update_dict.get(self.tick) is not None:
            self.record_update_dict[self.tick]['sequence'] = self.hero_next_action_round
            self.save_result_to_redis(self.record_update_dict[self.tick])

    # 增加一个state静态化的方法
    def state_to_dict(self, state):
        map = copy.deepcopy(state['map'])
        hero = copy.deepcopy(state['hero'])
        monster = copy.deepcopy(state['monster'])
        if type(map) != list:
            map = [map]
        if type(hero) != list:
            hero = [hero]
        if type(monster) != list:
            monster = [monster]

        map_dict = {}
        hero_dict = {}
        monster_dict = {}
        for i in range(len(map)):
            map_dict[i] = map[i].dict(for_view=True)
        for h in hero:
            hero_dict[h.HeroID] = h.dict(for_view=True)
        for m in monster:
            monster_dict[m.HeroID] = m.dict(for_view=True)
        del map
        del hero
        del monster
        res = {'map': map_dict, 'hero': hero_dict, 'monster': monster_dict}
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
        # self.performance.event_end('record_detail')
        log_manager.add_log(
            {'stepname': '调度记录change变化', 'tick': self.tick, 'action': action, 'update_dict': update_dict})
        if self.record_update_dict.get(self.tick) is None:
            self.record_update_dict[self.tick] = {'action': [], 'state': []}  # 初始化
        self.record_update_dict[self.tick]['action'].append(action)
        self.record_update_dict[self.tick]['state'].append(update_dict)
        self.record_update_dict[self.tick]['tick'] = self.tick
        # self.performance.event_end('record_detail')

    def send_update(self, out_file_name='for_qiangye.json'):

        self.performance.event_start('send_update')
        result = [i for i in self.record_update_dict.values()]
        result = {'init_state': self.init_state, 'update': result}
        result = json.dumps(result)
        # print('给强爷',result)
        save_result_to_view(result, out_file_name)
        redis_key = "battle_id:" + str(self.battle_id) + ":status"
        res = {'tick': self.tick, 'total_time': self.performance.result['total_time']}
        res = json.dumps(res)
        redis_client.set(redis_key, res, ex=self.redis_expiration_time)
        self.performance.event_end('send_update')
        return result

    def save_result_to_redis(self, record_update_dict):

        redis_key_2 = "battle_id:" + str(self.battle_id)
        print('rpush',json.dumps(record_update_dict))
        redis_client.rpush(redis_key_2, json.dumps(record_update_dict))


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
