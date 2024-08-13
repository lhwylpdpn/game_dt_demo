import time

from test_hero_data import origin_hero_data  # 后续通过api获取前端传递的数据
from test_map_data import origin_map_data  # 后续通过api获取前端传递的数据
from test_monster_data import origin_monster_data  # 后续通过api获取前端传递的数据
from buildpatrol import BuildPatrol
import schedule
from V1.test.demo_show import game
import random
import copy
class test_process:
    def __init__(self):
        map = BuildPatrol.build_map(origin_map_data)  # map
        heros = BuildPatrol.build_heros(origin_hero_data)  # heros
        monster = BuildPatrol.build_monster(origin_monster_data)
        self.state = {"map": map, "hero": heros, "monster": monster}
    def data_init(self):
        p_all = self.state['map'].view_from_y_dict().keys()
        p_all = list(p_all)
        for p in self.state['map'].view_from_y_dict().keys():
            if self.state['map'].view_from_y_dict()[p]['Block'] != 1:
                p_all.remove(p)


        for i in range(len(self.state['hero'])):


            hero_random_RoundAction = random.randint(0, 3)
            hero_random_JumpHeight = [random.randint(1,1)]
            hero_random_DogBase = random.randint(0, 2)
            hero_random_HP = random.randint(0, 10000)
            hero_random_Atk = random.randint(0, 1000)

            p = random.choice(p_all)
            p_all.remove(p)
            tmp_skills=copy.deepcopy(self.state['hero'][i].dict()['AvailableSkills'])
            for j in self.state['hero'][i].dict()['AvailableSkills']:
                if random.random()>0.5:
                    tmp_skills.remove(j)
            if 200 not in tmp_skills:
                tmp_skills.append(200)
            print('hero',self.state['hero'][i].dict()['HeroID'])
            print('hero_random_RoundAction', hero_random_RoundAction)
            print('hero_random_JumpHeight', hero_random_JumpHeight)
            print('hero_random_DogBase', hero_random_DogBase)
            print('hero_random_HP', hero_random_HP)
            print('hero_random_Atk', hero_random_Atk)
            print('p', p)

            self.state['hero'][i].set_AvailableSkills(tmp_skills)
            self.state['hero'][i].set_RoundAction(hero_random_RoundAction)
            self.state['hero'][i].set_JumpHeight(hero_random_JumpHeight)
            self.state['hero'][i].set_DogBase(hero_random_DogBase)
            self.state['hero'][i].set_Hp(hero_random_HP)
            self.state['hero'][i].set_Atk(hero_random_Atk)
            #随机选地图的一个位置给到英雄
            self.state['hero'][i].set_x(p[0])
            self.state['hero'][i].set_y(p[1])
            self.state['hero'][i].set_z(p[2])
        for i in range(len(self.state['monster'])):

            monster_random_RoundAction = random.randint(0, 3)
            monster_random_JumpHeight = [random.randint(5, 10)]
            monster_random_DogBase = random.randint(0,100 )
            monster_random_HP = random.randint(0, 10000)
            monster_random_Atk = random.randint(0, 1000)
            p = random.choice(p_all)
            p_all.remove(p)
            tmp_skills = copy.deepcopy(self.state['monster'][i].dict()['AvailableSkills'])
            print('tmp_skills',tmp_skills)
            for j in self.state['monster'][i].dict()['AvailableSkills']:
                if random.random() > 0.5:
                    tmp_skills.remove(j)
            if 200 not in tmp_skills:
                tmp_skills.append(200)
            print('monster',self.state['monster'][i].dict()['HeroID'])
            print('monster_random_RoundAction', monster_random_RoundAction)
            print('monster_random_JumpHeight', monster_random_JumpHeight)
            print('monster_random_DogBase', monster_random_DogBase)
            print('monster_random_HP', monster_random_HP)
            print('monster_random_Atk', monster_random_Atk)
            print('p', p)
            self.state['monster'][i].set_AvailableSkills(tmp_skills)
            self.state['monster'][i].set_RoundAction(monster_random_RoundAction)
            self.state['monster'][i].set_JumpHeight(monster_random_JumpHeight)
            self.state['monster'][i].set_DogBase(monster_random_DogBase)
            self.state['monster'][i].set_Hp(monster_random_HP)
            self.state['monster'][i].set_Atk(monster_random_Atk)

            self.state['monster'][i].set_x(p[0])
            self.state['monster'][i].set_y(p[1])
            self.state['monster'][i].set_z(p[2])


    #创建固定参数
    def pygame_init(self):
        self.game_obj=game(self.state)
        self.game_obj.game_init()

    def run(self):

        sch = schedule.schedule(self.state)
        sch.start()
        res=sch.run()
        self.return_data = sch.send_update()
        sch.performance.static()
        return res

    def game_run(self):
        self.game_obj.run(self.return_data)


    def over_state(self):
        for i in range(len(self.state['hero'])):
            print('hero',self.state['hero'][i].dict()['HeroID'],'HP',self.state['hero'][i].dict()['Hp'])
        for i in range(len(self.state['monster'])):
            print('monster',self.state['monster'][i].dict()['HeroID'],'HP',self.state['monster'][i].dict()['Hp'])


if __name__ == '__main__':
    res=[]
    for i in range(1):
        obj_=test_process()
        obj_.data_init()
        obj_.pygame_init()
        res.append(obj_.run())
        obj_.over_state()
        obj_.game_run()
    print(res)
