import time
from strategy.game import Game as game_broad
from strategy.agent import Agent as agent
from buildpatrol import BuildPatrol
from test_hero_data import origin_hero_data  # 后续通过api获取前端传递的数据
from test_map_data import origin_map_data  # 后续通过api获取前端传递的数据
from test_monster_data import origin_monster_data  # 后续通过api获取前端传递的数据


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
        self.timeout_tick = 100000
        self.tick = 0
        self.record_update_dict = {}
        self.record_error_dict = {}
        self.action_dict= {}

    def start(self):
        self.game.start()

    def run(self):

        while self.tick < self.timeout_tick:
            self.tick += 100000
            self.next()
            time.sleep(0.1)

    def next(self):
        state = self.game.get_current_state()
        alive_hero = self.game.get_current_alive_hero()


        for hero in alive_hero:
            # hero是一个对象，想获得它的类名
            alive_hero_name = hero.__class__.__name__.lower()
            print('schedule alive_hero_name', alive_hero_name)
            if self.tick % hero.Velocity == 0:
                # 查看hero的队列
                if hero.__class__.__name__.lower() == 'hero':
                    actions = self.agent_1.choice_hero_act(hero, state)
                if hero.__class__.__name__.lower() == 'monster':
                    actions = self.agent_2.choice_monster_act(hero, state)
                print('schedule choose action', actions)
                for action in actions:
                    self.game.action(action)
                    new_state = self.game.get_current_state()
                    self._record(action, state, new_state)
                    state = new_state
                if self.game.check_game_over():
                    break

    def _record(self,action,before_state,after_state):


        b_map=before_state['map']
        b_hero=before_state['hero']
        b_monster=before_state['monster']
        a_map=after_state['map']
        a_hero=after_state['hero']
        a_monster=after_state['monster']

        if type(b_map)!=list:
            b_map=[b_map]
        if type(b_hero)!=list:
            b_hero=[b_hero]
        if type(b_monster)!=list:
            b_monster=[b_monster]
        if type(a_map)!=list:
            a_map=[a_map]
        if type(a_hero)!=list:
            a_hero=[a_hero]
        if type(a_monster)!=list:
            a_monster=[a_monster]

        a_hero_dict={}
        for hero in a_hero:
            a_hero_dict[hero.sn]=hero.dict()
        b_hero_dict={}
        for hero in b_hero:
            b_hero_dict[hero.sn]=hero.dict()

        hero_update_dict={k: a_hero_dict[k] for k in a_hero_dict if k in b_hero_dict and a_hero_dict[k] != b_hero_dict[k]}
        hero_error_dict_diff_a={k: a_hero_dict[k] for k in a_hero_dict if k not in b_hero_dict}
        hero_error_dict_diff_b={k: b_hero_dict[k] for k in b_hero_dict if k not in a_hero_dict}
        hero_error_dict={**hero_error_dict_diff_a,**hero_error_dict_diff_b}


        a_map_dict={}
        for i in range(len(a_map)):
            a_map_dict[i]={}
            for each in a_map[i].dict():
                a_map_dict[i][each['sn']]=each
        b_map_dict={}
        for i in range(len(b_map)):
            b_map_dict[i]={}
            for each in b_map[i].dict():
                b_map_dict[i][each['sn']]=each

        map_update_dict={k: a_map_dict[k] for k in a_map_dict if k in b_map_dict and a_map_dict[k] != b_map_dict[k]}
        map_error_dict_diff_a={k: a_map_dict[k] for k in a_map_dict if k not in b_map_dict}
        map_error_dict_diff_b={k: b_map_dict[k] for k in b_map_dict if k not in a_map_dict}
        map_error_dict={**map_error_dict_diff_a,**map_error_dict_diff_b}

        a_monster_dict={}
        for monster in a_monster:
            a_monster_dict[monster.sn]=monster.dict()
        b_monster_dict={}
        for monster in b_monster:
            b_monster_dict[monster.sn]=monster.dict()

        monster_update_dict={k: a_monster_dict[k] for k in a_monster_dict if k in b_monster_dict and a_monster_dict[k] != b_monster_dict[k]}
        monster_error_dict_diff_a={k: a_monster_dict[k] for k in a_monster_dict if k not in b_monster_dict}
        monster_error_dict_diff_b={k: b_monster_dict[k] for k in b_monster_dict if k not in a_monster_dict}
        monster_error_dict={**monster_error_dict_diff_a,**monster_error_dict_diff_b}

        update_dict={'hero':hero_update_dict,'map':map_update_dict,'monster':monster_update_dict}
        error_dict={'hero':hero_error_dict,'map':map_error_dict,'monster':monster_error_dict}
        print('schedule after action update_dict',update_dict)
        print('schedule after action error_dict',error_dict)
        self.record_update_dict[self.tick]=update_dict
        self.record_error_dict[self.tick]=error_dict
        self.action_dict[self.tick]=action

    def send_update(self):
        return self.record_update_dict,self.action_dict

if __name__ == '__main__':
    map = BuildPatrol.build_map(origin_map_data)  # map
    heros = BuildPatrol.build_heros(origin_hero_data)  # heros
    monster = BuildPatrol.build_monster(origin_monster_data)
    sch = schedule(state={"map": map, "hero": heros, "monster": monster})
    sch.run()
    update,action=sch.send_update()
    for k,v in update.items():
        print('schdule update给强爷的state',k,v)
        print('schdule update给强爷的action',k,action[k])



