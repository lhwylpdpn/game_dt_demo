import json
import time
from strategy.game import Game as game_broad
from strategy.agent import Agent as agent
from buildpatrol import BuildPatrol
from test_hero_data import origin_hero_data  # 后续通过api获取前端传递的数据
from test_map_data import origin_map_data  # 后续通过api获取前端传递的数据
from test_monster_data import origin_monster_data  # 后续通过api获取前端传递的数据
import copy
import jsondiff
import math
import pandas as pd
from deepdiff import DeepDiff
import re
import dictdiffer


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


class performance:
    def __init__(self):
        self.start_time = time.time()
        self.result = {}
        self.tag_time={}
        self.event_count={}
    def event_start(self, event_name):
        self.tag_time[event_name]=time.time()
    def event_end(self, event_name):
        use_time=time.time()-self.tag_time[event_name]
        self.result[event_name]=use_time if self.result.get(event_name) is None else self.result[event_name]+use_time
        self.event_count[event_name]=self.event_count[event_name]+1 if self.event_count.get(event_name) is not None else 1
        self.tag_time[event_name]=None

    def end(self):
        self.result['total_time']=time.time()-self.start_time
        self.event_count['total_time']=1


    def static(self):
        #计算各类事件的平均时间转成df
        df=pd.DataFrame(self.result.items(),columns=['event','time'])
        #合并每个事件的次数
        df['count']=df['event'].apply(lambda x:self.event_count[x])
        df['avg_time']=df['time']/df['count']
        print(df)


class schedule:

    def __init__(self, state):

        self.hero_list = state['hero']
        self.state = state['map']
        self.monster_list = state['monster']
        self.game = game_broad(hero=self.hero_list, maps=self.state, monster=self.monster_list)
        self.agent_1 = agent()
        self.agent_2 = agent()
        self.timeout_tick = 100
        self.tick = 0
        self.record_update_dict = {}
        self.record_error_dict = {}
        self.action_dict= {}
        self.ap_parm=20 # 特定设置，代表一个tick增加速度/20 个ap
        self.ap_limit=100 # 游戏设置，代表每满足100个ap就动一次
        self.game_over=False
        ##统计
        self.performance=performance()

    def start(self):
        self.game.start()

    def run(self):

        while self.tick < self.timeout_tick and not self.game_over:
            self.tick += 1
            self.next()

        self.performance.end()
    def next(self):
        self.performance.event_start('get_current_state')
        state=self.game.get_current_state()
        state_dict = self.state_to_dict(state)
        self.performance.event_end('get_current_state')
        alive_hero = self.game.get_current_alive_hero()



        for hero in alive_hero:
            # hero是一个对象，想获得它的类名
            alive_hero_name = hero.__class__.__name__.lower()
            #向上取整

            once_tick=math.ceil(self.ap_limit/(hero.Velocity/self.ap_parm))
            #print('once_tick',self.tick,once_tick)
            if self.tick % once_tick == 0:
                # 查看hero的队列
                if hero.__class__.__name__.lower() == 'hero':
                    self.performance.event_start('schedule_choose_action')
                    actions = self.agent_1.choice_hero_act(hero, state)
                    print('tick',self.tick,'调度获得的行动list: 英雄', hero.HeroID, actions)
                    self.performance.event_end('schedule_choose_action')
                if hero.__class__.__name__.lower() == 'monster':
                    self.performance.event_start('schedule_choose_action')
                    actions = self.agent_2.choice_monster_act(hero, state)
                    print('tick',self.tick,'调度获得的行动list: 怪兽', hero.MonsterId, actions)
                    self.performance.event_start('schedule_choose_action')

                for action in actions:
                    self.performance.event_start('game_action')
                    if hero.__class__.__name__.lower() == 'hero':
                        self.game.hero_action(hero, action)
                    else:
                        self.game.monster_action(hero, action)
                    self.performance.event_end('game_action')
                    self.performance.event_start('get_current_state')
                    new_state = self.game.get_current_state()
                    new_state_dict=self.state_to_dict(new_state)
                    self.performance.event_end('get_current_state')

                    self.performance.event_start('record')
                    self._record(action, state_dict, new_state_dict)
                    self.performance.event_end('record')
                    self.performance.event_start('get_current_state')
                    state = new_state
                    state_dict=self.state_to_dict(state)
                    self.performance.event_end('get_current_state')
                self.performance.event_start('check_game_over')
                if self.game.check_game_over():
                    self.performance.event_end('check_game_over')
                    self.game_over=True
                    return
                self.performance.event_end('check_game_over')


    #增加一个state静态化的方法
    def state_to_dict(self,state):
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
            map_dict[i]=map[i].dict()
        for h in hero:
            hero_dict[h.HeroID]=h.dict()
        for m in monster:
            monster_dict[m.MonsterId]=m.dict()
        return {'map':map_dict,'hero':hero_dict,'monster':monster_dict}

    def _record(self,action,before_state,after_state):
        #update_dict=jsondiff.diff(before_state,after_state)
        update_dict=Deepdiff_modify(before_state,after_state)
        if self.record_update_dict.get(self.tick) is None:
            self.record_update_dict[self.tick]={'action':[],'state':[]}#初始化

        self.record_update_dict[self.tick]['action'].append(action)
        self.record_update_dict[self.tick]['state'].append(update_dict)

    def send_update(self):


        #打印测试
        for key in self.record_update_dict.keys():
            print('第',key,'tick 行动')
            print('行动',self.record_update_dict[key]['action'])
            print('状态',self.record_update_dict[key]['state'])


        return self.record_update_dict


def Deepdiff_modify(before,after):
    diff_types = [
        "dictionary_item_added",
        "dictionary_item_removed",
        "values_changed",
        "iterable_item_added",
        "iterable_item_removed",
        "attribute_added",
        "attribute_removed",
        "type_changes",
        "set_item_added",
        "set_item_removed",
    ]

    res=DeepDiff(before,after)
    diff_type=res.keys()
    res=res.to_dict()
    # print('对比结果',jsondiff.diff(before,after))
    # print('对比结果2',list(dictdiffer.diff(before, after)))
    return list(dictdiffer.diff(before, after))



if __name__ == '__main__':
    map = BuildPatrol.build_map(origin_map_data)  # map
    heros = BuildPatrol.build_heros(origin_hero_data)  # heros
    monster = BuildPatrol.build_monster(origin_monster_data)
    heros[0].set_x(1)
    heros[0].set_y(1)
    heros[0].set_z(1)
    heros[0].set_Atk(20)
    heros[0].set_max_step(100)
    #heros[0].set_max_step(3)
    sch = schedule(state={"map": map, "hero": heros, "monster": monster})
    sch.run()
    update=sch.send_update()
    sch.performance.static()


    # s="['monster'][1173]['hateBase'][1173]"
    # #针对字符串转抽取其中的monster，1173，hateBase，1173,不带括号
    # import re
    # res=re.findall(r'\[(.*?)\]',s)
    # print(len(res),type(res))