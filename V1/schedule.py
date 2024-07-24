
import time
import game_info as game_broad
import agent as agent



#step1 调度决定开始游戏
#step2 调度开始自增计时器
#step3 调度获取棋盘中可用游戏角色的ap
#step3.5 获取当前状态
#step4 判断能整除谁的时候，使用棋子调用决策树获得行动
#step4.5 调用棋盘执行行动
#step4.6 获得行动后的状态，计算状态差异，组织数据存储
#step5 检查游戏是否结束
#step6 如果游戏结束，产生内容序列



class schedule:

    def __init__(self,hero_list,state):
        self.hero_list=hero_list
        self.state=state
        self.game=game_broad.game(hero=self.hero_list,state=self.state)
        self.agent_1=agent.randomAgent(name='a1',self.game)
        self.agent_2=agent.randomAgent(name='a2',self.game)
        self.timeout_tick=100000
        self.tick=0
    def start(self):
        self.game.start
    def run(self):

        while self.tick<self.timeout_tick:
            self.tick+=1
            self.next()
            time.sleep(0.1)

    def next(self):
        state=self.game.get_current_state()
        alive_hero=self.game.get_current_alive_hero()
        for hero in alive_hero:
            if self.tick%hero.ap==0:
                #查看hero的队列
                if hero.team==1:
                    action=self.agent_1.choice_act(state)
                else:
                    action=self.agent_2.choice_act(state)
                self.game.action_to_state(hero,action)
                new_state=self.game.get_current_state()
                self._record(action,state,new_state)
                state=new_state
                if self.game.check_game_over():
                    break

    def _record(self,action,before_state,after_state):

        pass


def schedule_api(hero_list,state):
    sch=schedule(hero_list,state)
    sch.start()
    sch.run()
    return sch