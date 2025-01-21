import os
import sys
import json
import time
from strategy.game import Game as game_broad
from strategy.agent import Agent as agent
from buildpatrol import BuildPatrol
import copy
import math
from utils.tools import Deepdiff_modify
from utils.tools import performance



#1、初始化schedule 对象
#2、调用set 预处理动作
#3、调用run函数开始处理，run函数会先处理预处理动作
#4、每生成一个动作返回一下内容


#todo 新增一个批量给预处理动作对函数 ing
#todo 改造run函数先处理预处理动作 ing
#todo 改造agent对调用关系 ok
#todo 改造一个单调返回的函数
#todo 改造一个简单策略
#todo 回合阶段怎么回的

################################
#todo 要考虑回合超时的问题

class schedule:

    def __init__(self, state, battle_id=0):

        self.battle_id = battle_id
        #self.redis_expiration_time = 7 * 24 * 60 * 60
        self.hero_p1 = state['hero_p1']
        self.state = state['maps']
        self.hero_p2 = state['hero_p2']
        self.game = game_broad(hero=self.hero_p1, maps=self.state, monster=self.hero_p2)
        self.agent_p1 = agent()
        self.agent_p2 = agent()
        self.timeout_tick = 200000
        self.tick = 0
        self.record_update_dict = {}
        self.record_update_dict_update = {}  # 测试用
        self.record_error_dict = {}
        self.action_dict = {}
        self.ap_parm = 30  # 特定设置，代表一个tick增加速度/20 个ap
        self.ap_limit = 100  # 游戏设置，代表每满足100个ap就动一次
        self.game_over = False
        self.init_state = None  # 特定用于给强爷传输初始状态
        self.pre_defined_actions=[]
        ##统计



        self.performance = performance()
        self.performance.event_start('get_current_state')
        state = self.game.get_current_state()
        state_dict = self.state_to_dict(state)
        self.init_state = state_dict
        self.performance.event_end('get_current_state')
        alive_hero = self.game.get_current_alive_hero()

    def start(self):
        self.performance.event_start('game_start')
        self.game.start()
        self.performance.event_end('game_start')

    def run_pre_defined_actions(self,actions_list):
        #合并预执行的动作
        self.pre_defined_actions+=actions_list

        #todo 这里执行循环根据英雄，执行了这些动作了，更新了state


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
            if hero.is_death:  # 同一个tick里也可能，后轮到的英雄被先轮到的打死
                continue
            alive_hero_class = hero.camp #todo 根据虎哥返回内容这里调整
            alive_hero_id = hero.HeroID
            # 向上取整
            once_tick = math.ceil(self.ap_limit / (hero.Velocity / self.ap_parm))
            # print('once_tick',self.tick,hero.Velocity,once_tick,hero.__class__.__name__.lower(), hero.HeroID,)

            if self.tick % once_tick == 0:
                # 查看hero的队列
                if alive_hero_class == 'p1':
                    self.performance.event_start('schedule_choose_action')
                    actions = self.agent_p1.choice_hero_act(hero, state, self.performance)
                    self.performance.event_end('schedule_choose_action')
                if alive_hero_class == 'p2':
                    self.performance.event_start('schedule_choose_action')
                    actions = self.agent_p2.choice_monster_act(hero, state, self.performance)
                    self.performance.event_end('schedule_choose_action')

                for action in actions:
                    # print('调度行动',self.tick,'id',alive_hero_id,'class',alive_hero_class,action)
                    action_result=[]
                    self.performance.event_start('game_action')
                    if hero.__class__.__name__.lower() == 'hero':
                        action_result = self.game.hero_action(hero, action)

                    else:
                        action_result = self.game.monster_action(hero, action)
                    self.performance.event_end('game_action')

                    if not action_result:  # 如果动作失败，直接跳出本次动作链路
                        # print('调度行动-接到动作失败',self.tick,'id',alive_hero_id,'class',alive_hero)
                        break
                    if isinstance(action_result, dict):
                        action_result = [action_result]
                    self.performance.event_start('get_current_state')
                    new_state = self.game.get_current_state()
                    new_state_dict = self.state_to_dict(new_state)
                    self.performance.event_end('get_current_state')

                    for action in action_result:


                        self.performance.event_start('record')
                        action['id'] = alive_hero_id
                        action['class'] = alive_hero_class
                        self._record(action, state_dict, new_state_dict)

                    self.performance.event_end('record')
                    self.performance.event_start('get_current_state')
                    state = new_state
                    state_dict = self.state_to_dict(state)
                    self.performance.event_end('get_current_state')

                self.performance.event_start('check_game_over')
                if self.game.check_game_over()[0]:
                    # print('战斗结束了！！！！',self.game.check_game_over()[1])
                    self.performance.event_end('check_game_over')
                    self.game_over = True
                    if self.record_update_dict.get(self.tick) is not None:
                        self.save_result_to_redis(self.record_update_dict[self.tick])

                    return state
                self.performance.event_end('check_game_over')
        if self.record_update_dict.get(self.tick) is not None:
            self.save_result_to_redis(self.record_update_dict[self.tick])

        return state

    def save_result_to_redis(self, record_update_dict):

        redis_key_2 = "battle_id:" + str(self.battle_id)
        #todo 看怎么给彬哥

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
        attachment = copy.deepcopy(state['attachment'])
        setting=copy.deepcopy(state['setting'])

        if type(map) != list:
            map = [map]
        if type(hero) != list:
            hero = [hero]
        if type(monster) != list:
            monster = [monster]
        if type(attachment) != list:
            attachment = [attachment]
        if type(setting)!=list:
            setting=[setting]

        map_dict = {}
        hero_dict = {}
        monster_dict = {}
        map3_dict = {}
        map4_dict = {}

        for i in range(len(map)):
            map_dict[i] = map[i].dict(for_view=True)
        for h in hero:
            hero_dict[h.HeroID] = h.dict(for_view=True)
        for m in monster:
            monster_dict[m.HeroID] = m.dict(for_view=True)
        for a in attachment:
            #attachment_dict[a.MapID] = a.dict()
            if a.Layer == 3:
                map3_dict[a.MapID] = a.dict()
            if a.Layer == 4:
                map4_dict[a.MapID] = a.dict()
        res = {'map': map_dict, 'hero': hero_dict, 'monster': monster_dict, 
               'map3': map3_dict, "map4":map4_dict,
               #'attachment': attachment_dict,
               "setting":setting}
        del map
        del hero
        del monster
        del attachment
        del setting

        return res

    def _record(self, action, before_state, after_state):
        # self.performance.event_start('record_detail')
        update_dict = Deepdiff_modify(before_state, after_state)

        if self.record_update_dict.get(self.tick) is None:
            self.record_update_dict[self.tick] = {'action': [], 'state': []}  # 初始化
        self.record_update_dict[self.tick]['action'].append(action)
        #print('record',self.record_update_dict[self.tick]['action'])
        self.record_update_dict[self.tick]['state'].append(update_dict)
        self.record_update_dict[self.tick]['tick'] = self.tick
        # self.performance.event_end('record_detail')



def main(state, battle_id):
    sch = schedule(state, battle_id)
    sch.start()
    sch.run()
    sch.performance.static()

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
