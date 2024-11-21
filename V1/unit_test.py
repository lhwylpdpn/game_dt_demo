import os
import time
from strategy.single_RL_agent import Random_Agent
from buildpatrol import BuildPatrol
import schedule
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# 显示每一列的全部内容
pd.set_option('display.max_colwidth', 1000)

class test_process:
    def __init__(self,init_state=None):
        if init_state is None:
            self.state = BuildPatrol('data.json').load_data()
        else:
            self.state = init_state

    def run(self):

        sch = schedule.schedule(self.state)
        sch.timeout_tick=50
        sch.agent_1 = Random_Agent()
        sch.agent_2 = Random_Agent()
        sch.start()
        sch.run()
        self.return_data = sch.send_update()
        return self.return_data


def test_tool(init_state):
    obj_=test_process(init_state=init_state) #传入state可以直接
    res=obj_.run()
    return res


if __name__ == '__main__':
    test_tool(init_state=None)
