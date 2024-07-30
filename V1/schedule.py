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
            print('hero1', hero.__class__.__name__.lower())

        # print('tick',self.tick)
        for hero in alive_hero:
            # hero是一个对象，想获得它的类名
            alive_hero_name = hero.__class__.__name__.lower()
            print('alive_hero_name', alive_hero_name)
            if self.tick % hero.Velocity == 0:
                # 查看hero的队列
                if hero.__class__.__name__.lower() == 'hero':
                    actions = self.agent_1.choice_hero_act(hero, state)
                if hero.__class__.__name__.lower() == 'monster':
                    actions = self.agent_2.choice_monster_act(hero, state)
                print('choose action', actions)
                for action in actions:
                    self.game.action(action)
                    new_state = self.game.get_current_state()
                    self._record(action, state, new_state)
                    state = new_state
                if self.game.check_game_over():
                    break

    def _record(self, action, before_state, after_state):
        print('action', action)
        print('before_state', before_state)
        print('after_state', after_state)


if __name__ == '__main__':
    map = BuildPatrol.build_map(origin_map_data)  # map
    heros = BuildPatrol.build_heros(origin_hero_data)  # heros
    monster = BuildPatrol.build_monster(origin_monster_data)
    sch = schedule(state={"map": map, "hero": heros, "monster": monster})
    sch.run()
