from test_hero_data import origin_hero_data  # 后续通过api获取前端传递的数据
from test_map_data import origin_map_data  # 后续通过api获取前端传递的数据
from test_monster_data import origin_monster_data  # 后续通过api获取前端传递的数据
from buildpatrol import BuildPatrol
import schedule

class test_process:
    def __init__(self):
        map = BuildPatrol.build_map(origin_map_data)  # map
        heros = BuildPatrol.build_heros(origin_hero_data)  # heros
        monster = BuildPatrol.build_monster(origin_monster_data)
        self.state = {"map": map, "hero": heros, "monster": monster}

    def random(self):
        for k in self.state['hero'][0].dict().keys():
            print(k)

if __name__ == '__main__':
    a = test_process()
    a.random()