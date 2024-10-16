import os
import time
import matplotlib.pyplot as plt

# from test_hero_data import origin_hero_data  # 后续通过api获取前端传递的数据
# from test_map_data import origin_map_data  # 后续通过api获取前端传递的数据
# from test_monster_data import origin_monster_data  # 后续通过api获取前端传递的数据
from buildpatrol import BuildPatrol
import schedule
from V1.test.demo_show import game
import random
import copy
import pandas as pd
import json
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# 显示每一列的全部内容
pd.set_option('display.max_colwidth', 1000)

from V1.strategy.single_RL_agent import Agent as SingleRLAgent

class test_process:
    def __init__(self):

        self.state = BuildPatrol("data.json").load_data()
        print('state',self.state)


    def map_change(self):
        p_all = self.state['map'].view_from_y_dict().keys()
        p_all = list(p_all)
        #在一张图上画出来这个p_all


        for p in self.state['map'].view_from_y_dict().keys():
            if p[0]>6:
                self.state['map'].set_land_no_pass(p[0],p[1],p[2],5)
            if p[2]>6:
                self.state['map'].set_land_no_pass(p[0],p[1],p[2],5)
        # # 提取 x, y, z（高度）的值
        # x = [p[0] for p in p_all]
        # z = [self.state['map'].view_from_y_dict()[p]['Block'] for p in p_all]  # 表示是否有占用
        # y = [p[2] for p in p_all]
        #
        # plt.figure(figsize=(8, 6))
        # scatter = plt.scatter(x, y, c=z, cmap='viridis', s=100)
        #
        # # 添加颜色条
        # plt.colorbar(scatter, label='block value')
        #
        # # 添加标题和标签
        # plt.title('')
        # plt.xlabel('X Coordinate')
        # plt.ylabel('Y Coordinate')
        #
        # # 显示图形
        # plt.grid()
        # plt.show()
        # time.sleep(1000)




    def data_init(self):
        p_all = self.state['map'].view_from_y_dict().keys()
        p_all = list(p_all)
        for p in self.state['map'].view_from_y_dict().keys():
            if self.state['map'].view_from_y_dict()[p]['Block'] != 1:
                p_all.remove(p)
        print(self.state['hero'],self.state['monster'])
        self.state['hero'] =[_ for _ in self.state['hero'] if _.HeroID==5002]
        self.state['monster'] = [_ for _ in self.state['monster'] if _.Quality==2]
        print(self.state['hero'],self.state['monster'])

        for i in range(len(self.state['hero'])):

            hero_random_RoundAction = random.randint(5,5)
            hero_random_JumpHeight = [random.randint(15,15)]
            hero_random_DogBase = random.randint(5,5)
            hero_random_HP = random.randint(500,500)
            hero_random_Atk = random.randint(200,200)
            #
            p = random.choice(p_all)
            p_all.remove(p)
            # tmp_skills=copy.deepcopy(self.state['hero'][i].dict()['AvailableSkills'])
            # print('tmp_skills',tmp_skills)
            # # for j in self.state['hero'][i].dict()['AvailableSkills']:
            # #     if random.random()>0.5:
            # #         tmp_skills.remove(j)
            # # if 200 not in tmp_skills:
            # #     tmp_skills.append(200)
            # #print('原始技能',self.state['hero'][i].dict())
            tmp_skills=[77]
            # #print('hero',self.state['hero'][i].dict()['HeroID'])
            # print('hero_random_RoundAction', hero_random_RoundAction)
            # print('hero_random_JumpHeight', hero_random_JumpHeight)
            # print('hero_random_DogBase', hero_random_DogBase)
            # print('hero_random_HP', hero_random_HP)
            # print('hero_random_Atk', hero_random_Atk)
            #
            # # if i == 0:
            # #     p=(2,1,6)
            # # if i==1:
            # #     p=(3,1,16)
            self.state['hero'][i].set_AvailableSkills(tmp_skills)
            self.state['hero'][i].set_RoundAction(hero_random_RoundAction)
            self.state['hero'][i].set_JumpHeight(hero_random_JumpHeight)
            self.state['hero'][i].set_DogBase(hero_random_DogBase)
            self.state['hero'][i].set_Hp(hero_random_HP)
            self.state['hero'][i].set_Atk(hero_random_Atk)
            # # #随机选地图的一个位置给到英雄
            # # print('p', p)
            self.state['hero'][i].set_x(p[0])
            self.state['hero'][i].set_y(p[1])
            self.state['hero'][i].set_z(p[2])

        for i in range(len(self.state['monster'])):

            monster_random_RoundAction = random.randint(5,5)
            monster_random_JumpHeight = [random.randint(15,15)]
            monster_random_DogBase = random.randint(5,5 )
            monster_random_HP = random.randint(500, 500)
            monster_random_Atk = random.randint(200, 200)
            p = random.choice(p_all)
            p_all.remove(p)
            #tmp_skills = copy.deepcopy(self.state['monster'][i].dict()['AvailableSkills'])
            #print('tmp_skills',tmp_skills)
            # for j in self.state['monster'][i].dict()['AvailableSkills']:
            #     if random.random() > 0.5:
            #         tmp_skills.remove(j)
            # if 200 not in tmp_skills:
            #     tmp_skills.append(200)
            #tmp_skills = [77, 78, 88]
            # print('monster',self.state['monster'][i].dict()['HeroID'])
            # print('monster_random_RoundAction', monster_random_RoundAction)
            # print('monster_random_JumpHeight', monster_random_JumpHeight)
            # print('monster_random_DogBase', monster_random_DogBase)
            # print('monster_random_HP', monster_random_HP)
            # print('monster_random_Atk', monster_random_Atk)

            #self.state['monster'][i].set_AvailableSkills(tmp_skills)
            self.state['monster'][i].set_RoundAction(monster_random_RoundAction)
            self.state['monster'][i].set_JumpHeight(monster_random_JumpHeight)
            self.state['monster'][i].set_DogBase(monster_random_DogBase)
            self.state['monster'][i].set_Hp(monster_random_HP)
            self.state['monster'][i].set_Atk(monster_random_Atk)
            # self.state['monster'][i].set_Def(monster_random_Def)
            # if i==0:
            #     p=(19,5,18)
            # if i==1:
            #     p=(12,7,8)
           # print('p', p)
            self.state['monster'][i].set_x(p[0])
            self.state['monster'][i].set_y(p[1])
            self.state['monster'][i].set_z(p[2])

        print(self.state)
        #time.sleep(5)

    #创建固定参数
    def pygame_init(self):
        self.game_obj=game(self.state)
        self.game_obj.game_init()

    def run(self,out_file_name='for_qiangye.json'):

        sch = schedule.schedule(self.state)
        sch.agent_1=SingleRLAgent()
        sch.agent_2=SingleRLAgent()
        sch.timeout_tick=3000
        sch.start()
        res=sch.run()
        self.return_data = sch.send_update(out_file_name)
        sch.performance.static()
        return res


    def game_run(self,json=None):
        if json!=None:
            self.return_data=json
        self.game_obj.run(self.return_data)
        self.game_obj.over_state()

    def over_state(self):
        for i in range(len(self.state['hero'])):
            print('hero',self.state['hero'][i].dict()['HeroID'],'HP',self.state['hero'][i].dict()['Hp'])
        for i in range(len(self.state['monster'])):
            print('monster',self.state['monster'][i].dict()['HeroID'],'HP',self.state['monster'][i].dict()['Hp'])


def main():
    log_file_path = os.getcwd() + '/log/logs.json'
    with open(log_file_path, 'w') as f:
        f.write('')
    obj_=test_process()
    obj_.map_change()
    obj_.data_init()
    #obj_.pygame_init()
    obj_.run()
    #obj_.game_run()
    #time.sleep(100)


if __name__ == '__main__':

    main()
    #todo:调整地图大小