import time

from test_hero_data import origin_hero_data  # 后续通过api获取前端传递的数据
from test_map_data import origin_map_data  # 后续通过api获取前端传递的数据
from test_monster_data import origin_monster_data  # 后续通过api获取前端传递的数据
from buildpatrol import BuildPatrol
import schedule
from V1.test.demo_show import generate_state
from V1.test.demo_show import generate_state

class test_process:
    def __init__(self):
        map = BuildPatrol.build_map(origin_map_data)  # map
        heros = BuildPatrol.build_heros(origin_hero_data)  # heros
        monster = BuildPatrol.build_monster(origin_monster_data)
        self.state = {"map": map, "hero": heros, "monster": monster}
        generate_state(self.state)


    def test(self):
        for i in range(len(self.state['hero'])):
            #print(self.state['hero'][i].dict().keys())
            #print(self.state['hero'][i].dict()['DogBase'])
            self.state['hero'][i].set_DogBase(1000)
            self.state['hero'][i].set_JumpHeight([100])
            pass
        for i in range(len(self.state['monster'])):
            #print(self.state['monster'][i].dict().keys())
            #print(self.state['monster'][i].dict()['DogBase'])
            self.state['monster'][i].set_DogBase(1000)
            self.state['monster'][i].set_JumpHeight([100])
            pass
        for i in range(len(self.state['map'].dict())):
            for j in range(len(self.state['map'].dict()[i])):
                pass


    def run(self):

        sch = schedule.schedule(self.state)
        sch.start()
        sch.run()
        update = sch.send_update()
        sch.performance.static()




if __name__ == '__main__':
    a=test_process()