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
# step0 调度接到外部的开始请求，传入初始地图，传入初始角色，传入计算信息
# step1 调度开始游戏,调用棋盘初始化游戏
# step2 调度开始自增计时器
# step3 调度获取棋盘中可用游戏角色的ap
# step3.5 获取当前状态
# step4 判断能整除谁的时候，使用棋子调用决策树获得行动
# step4.5 调用棋盘执行行动
# step4.6 获得行动后的状态，计算状态差异，组织数据存储
# step5 检查游戏是否结束
# step6 如果游戏结束，产生内容序列

class schedule:

    def __init__(self, state):

        self.hero_list = state['hero']
        self.state = state['map']
        self.monster_list = state['monster']
        self.game = game_broad(hero=self.hero_list, maps=self.state, monster=self.monster_list)
        self.agent_1 = agent()
        self.agent_2 = agent()
        self.timeout_tick = 1200
        self.tick = 0
        self.record_update_dict = {}
        self.record_error_dict = {}
        self.action_dict= {}
        self.ap_parm=20 # 特定设置，代表一个tick增加速度/20 个ap
        self.ap_limit=100 # 游戏设置，代表每满足100个ap就动一次
        self.game_over=False
        self.init_state=None# 特定用于给强爷传输初始状态
        ##统计
        self.performance=performance()

    def start(self):
        self.game.start()

    def run(self):
        self.performance.event_start('get_current_state')
        state = self.game.get_current_state()
        state_dict = self.state_to_dict(state) #todo  优化性能
        self.init_state=state_dict
        self.performance.event_end('get_current_state')

        while self.tick < self.timeout_tick and not self.game_over:
            self.tick += 1
            self.next()

        self.performance.end()
        return self.game.check_game_over()[1]
    def next(self):
        self.performance.event_start('get_current_state')
        state=self.game.get_current_state()
        state_dict = self.state_to_dict(state)
        self.performance.event_end('get_current_state')
        alive_hero = self.game.get_current_alive_hero()
        #todo  同tick 的顺序问题，同tick的时候是不是有排序


        for hero in alive_hero:
            # hero是一个对象，想获得它的类名
            alive_hero_class = hero.__class__.__name__.lower()
            alive_hero_id=hero.HeroID
            #向上取整

            once_tick=math.ceil(self.ap_limit/(hero.Velocity/self.ap_parm))
            #print('once_tick',self.tick,once_tick)
            if self.tick % once_tick == 0:
                # 查看hero的队列
                if alive_hero_class == 'hero':
                    self.performance.event_start('schedule_choose_action')
                    actions = self.agent_1.choice_hero_act(hero, state)
                    print('tick',self.tick,'调度获得的行动list: 英雄', alive_hero_id)
                    self.performance.event_end('schedule_choose_action')
                if alive_hero_class == 'monster':
                    self.performance.event_start('schedule_choose_action')
                    actions = self.agent_2.choice_monster_act(hero, state)
                    print('tick',self.tick,'调度获得的行动list: 怪兽', alive_hero_id)
                    self.performance.event_start('schedule_choose_action')

                for action in actions:
                    action_result=True
                    print('调度行动',self.tick,'id',alive_hero_id,'class',alive_hero_class)
                    self.performance.event_start('game_action')
                    if hero.__class__.__name__.lower() == 'hero':
                        action_result=self.game.hero_action(hero, action)
                    else:
                        action_result=self.game.monster_action(hero, action)
                    if not action_result: #如果动作失败，直接跳出本次动作链路
                        print('调度行动-接到动作失败',self.tick,'id',alive_hero_id,'class',alive_hero)
                        break
                    self.performance.event_end('game_action')
                    self.performance.event_start('get_current_state')
                    new_state = self.game.get_current_state()
                    new_state_dict=self.state_to_dict(new_state)
                    self.performance.event_end('get_current_state')

                    self.performance.event_start('record')
                    action['id']=alive_hero_id
                    action['class']=alive_hero_class
                    self._record(action, state_dict, new_state_dict)
                    self.performance.event_end('record')
                    self.performance.event_start('get_current_state')
                    state = new_state
                    state_dict=self.state_to_dict(state)
                    self.performance.event_end('get_current_state')
                self.performance.event_start('check_game_over')
                if self.game.check_game_over()[0]:
                    self.performance.event_end('check_game_over')
                    print('战斗结束了！！！！',self.game.check_game_over()[1])
                    self.game_over=True

                    return
                self.performance.event_end('check_game_over')


    #增加一个state静态化的方法
    def state_to_dict(self,state):
        #self.performance.event_start('get_current_state_to_dict')
        map=copy.deepcopy(state['map'])
        hero=copy.deepcopy(state['hero'])
        monster=copy.deepcopy(state['monster'])

        if type(map)!=list:
            map=[map]
        if type(hero)!=list:
            hero=[hero]
        if type(monster)!=list:
            monster=[monster]

        map_dict={}
        hero_dict={}
        monster_dict={}

        for i in range(len(map)):
            map_dict[i]=map[i].dict(for_view=True)
        for h in hero:
            hero_dict[h.HeroID]=h.dict(for_view=True)
        for m in monster:
            monster_dict[m.HeroID]=m.dict(for_view=True)
        #self.performance.event_end('get_current_state_to_dict')
        return {'map':map_dict,'hero':hero_dict,'monster':monster_dict}


    def _record(self,action,before_state,after_state):
        update_dict=Deepdiff_modify(before_state,after_state)

        print('调度显示的变化',update_dict)
        if self.record_update_dict.get(self.tick) is None:
            self.record_update_dict[self.tick]={'action':[],'state':[]}#初始化
        self.record_update_dict[self.tick]['action'].append(action)
        self.record_update_dict[self.tick]['state'].append(update_dict)
        self.record_update_dict[self.tick]['tick']=self.tick

    def send_update(self):


        #打印测试
        # for key in self.record_update_dict.keys():
        #     print('第',key,'tick 行动')
        #     print('行动',self.record_update_dict[key]['action'])
        #     print('状态',self.record_update_dict[key]['state'])
        #self.record_update_dict=self.record_update_dict.values()
        result=[i for i in self.record_update_dict.values()]
        result={'init_state':self.init_state,'update':result}
        result=json.dumps(result)
        print('给强爷',result)
        return result


def main(state):
    sch = schedule(state)
    sch.start()
    sch.run()
    update = sch.send_update()
    sch.performance.static()
    return update

def save_result_to_view(data, path):
    with open(path, 'w') as file:
        #json.dump(data, file)
        file.write(data)
    return


if __name__ == '__main__':
    ## python schedule.py src_path result_path
    a=time.time()
    src_path = sys.argv[1] if len(sys.argv) > 2 else "data.json"        # 源文件地址
    result_file = sys.argv[2] if len(sys.argv) >= 3 else "result.json"   # result地址

    state = BuildPatrol(src_path).load_data()                          # 初始化对象

    # map = BuildPatrol.build_map(origin_map_data)  # map
    # heros = BuildPatrol.build_heros(origin_hero_data)  # heros
    # monster = BuildPatrol.build_monster(origin_monster_data)
    # # heros[0].set_x(1)
    # # heros[0].set_y(1)
    # # heros[0].set_z(1)
    # # heros[0].set_Atk(1000)
    # # heros[0].set_RoundAction(1)


    # state={"map": map, "hero": heros, "monster": monster}
    result = main(state)
    save_result_to_view(result, result_file)
    print('总时间',time.time()-a)



