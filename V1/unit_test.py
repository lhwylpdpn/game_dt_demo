import os
import time

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

class test_process:
    def __init__(self):

        self.state = BuildPatrol("data.json").load_data()

    def data_init(self):
        p_all = self.state['map'].view_from_y_dict().keys()
        p_all = list(p_all)



        for p in self.state['map'].view_from_y_dict().keys():
            if self.state['map'].view_from_y_dict()[p]['Block'] != 1:
                p_all.remove(p)


        for i in range(len(self.state['hero'])):

            #
            # hero_random_RoundAction = random.randint(20,20)
            hero_random_JumpHeight = [random.randint(15,15)]
            # hero_random_DogBase = random.randint(100,100)
            # hero_random_HP = random.randint(1000,10000)
            hero_random_Atk = random.randint(250,250)
            #
            # p = random.choice(p_all)
            # p_all.remove(p)
            # tmp_skills=copy.deepcopy(self.state['hero'][i].dict()['AvailableSkills'])
            # print('tmp_skills',tmp_skills)
            # # for j in self.state['hero'][i].dict()['AvailableSkills']:
            # #     if random.random()>0.5:
            # #         tmp_skills.remove(j)
            # # if 200 not in tmp_skills:
            # #     tmp_skills.append(200)
            # #print('原始技能',self.state['hero'][i].dict())
            # #tmp_skills=[86]
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
            # # self.state['hero'][i].set_AvailableSkills(tmp_skills)
            # self.state['hero'][i].set_RoundAction(hero_random_RoundAction)
            #
            #
            self.state['hero'][i].set_JumpHeight(hero_random_JumpHeight)
            # self.state['hero'][i].set_DogBase(hero_random_DogBase)
            # self.state['hero'][i].set_Hp(hero_random_HP)
            self.state['hero'][i].set_Atk(hero_random_Atk)
            # # #随机选地图的一个位置给到英雄
            # # print('p', p)
            # self.state['hero'][i].set_x(p[0])
            # self.state['hero'][i].set_y(p[1])
            # self.state['hero'][i].set_z(p[2])
            pass
        for i in range(len(self.state['monster'])):

            monster_random_RoundAction = random.randint(20,30)
            monster_random_JumpHeight = [random.randint(5,5)]
            monster_random_DogBase = random.randint(10,10 )
            monster_random_HP = random.randint(1350, 1350)
            monster_random_Atk = random.randint(88, 88)
            monster_random_Def = random.randint(10, 10)
            p = random.choice(p_all)
            p_all.remove(p)
            tmp_skills = copy.deepcopy(self.state['monster'][i].dict()['AvailableSkills'])
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
            # self.state['monster'][i].set_RoundAction(monster_random_RoundAction)
            self.state['monster'][i].set_JumpHeight(monster_random_JumpHeight)
            # self.state['monster'][i].set_DogBase(monster_random_DogBase)
            # self.state['monster'][i].set_Hp(monster_random_HP)
            self.state['monster'][i].set_Atk(monster_random_Atk)
            # self.state['monster'][i].set_Def(monster_random_Def)
            # if i==0:
            #     p=(19,5,18)
            # if i==1:
            #     p=(12,7,8)
           # print('p', p)
           #  self.state['monster'][i].set_x(p[0])
           #  self.state['monster'][i].set_y(p[1])
           #  self.state['monster'][i].set_z(p[2])



    #创建固定参数
    def pygame_init(self):
        self.game_obj=game(self.state)
        self.game_obj.game_init()

    def run(self,out_file_name='for_qiangye.json'):

        sch = schedule.schedule(self.state)
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


    def genarate_test_data_for_single_hero(self,basecalssid,skill_id):

        #删除掉其他的英雄
        update_hero=[]
        update_monster = []
        for i in range(len(self.state['hero'])):
            if self.state['hero'][i].dict()['BaseClassID']==int(basecalssid):
                update_hero.append(self.state['hero'][i])

        for i in range(len(self.state['monster'])):
            if self.state['monster'][i].dict()['Quality']==int(2):
                update_monster.append(self.state['monster'][i])

        self.state['hero']=update_hero
        self.state['monster']=[update_monster[0]]#只要一个怪物即可
        p_all = self.state['map'].view_from_y_dict().keys()
        p_all = list(p_all)
        for p in self.state['map'].view_from_y_dict().keys():
            if self.state['map'].view_from_y_dict()[p]['Block'] != 1:
                p_all.remove(p)
        for i in range(len(self.state['hero'])):
            if self.state['hero'][i].dict()['BaseClassID']==int(basecalssid):
                hero_random_RoundAction = random.randint(5,5)
                hero_random_JumpHeight = [random.randint(15,15)]
                hero_random_DogBase = random.randint(100,100)
                hero_random_HP = random.randint(1000,1000)
                hero_random_Atk = random.randint(150,150)
                self.state['hero'][i].set_RoundAction(hero_random_RoundAction)
                self.state['hero'][i].set_JumpHeight(hero_random_JumpHeight)
                self.state['hero'][i].set_DogBase(hero_random_DogBase)
                self.state['hero'][i].set_Hp(hero_random_HP)
                self.state['hero'][i].set_HpBase(hero_random_HP)
                self.state['hero'][i].set_Atk(hero_random_Atk)
                if type(skill_id)!=list:
                    skill_id=[skill_id]
                self.state['hero'][i].set_AvailableSkills(skill_id)

        self.state['monster'][0].set_x(self.state['hero'][0].dict()['position'][0]+1)
        self.state['monster'][0].set_y(self.state['hero'][0].dict()['position'][1])
        self.state['monster'][0].set_z(self.state['hero'][0].dict()['position'][2])
        self.state['monster'][0].set_Atk(100)

def single_skill_test_main(basecalssid,skill_id,pygame_init=True):
    obj_=test_process()


    obj_.genarate_test_data_for_single_hero(basecalssid=basecalssid,skill_id=skill_id)
    if pygame_init:
        obj_.pygame_init()
    obj_.run(out_file_name='for_qiangye_skill_'+str(skill_id)+'.json')
    if pygame_init:
        obj_.game_run()

def main():
    log_file_path = os.getcwd() + '/log/logs.json'
    with open(log_file_path, 'w') as f:
        f.write('')
    obj_=test_process()
    obj_.data_init()
    #obj_.pygame_init()
    obj_.run()
    #obj_.game_run()
    #time.sleep(100)


def replay():
    obj_=test_process()
    #obj_.data_init()
    obj_.pygame_init()

    #从文件里读取转成json
    with open('result.json', 'r', encoding='utf-8') as file:
        json_reload = file.read()
    obj_.game_run(json=json_reload)

if __name__ == '__main__':

    #清空log文件


    # # #
    # # #
    # # #
    # skill_list=list(demo_skill.values())
    # print(skill_list)
    # #skill_list=[77]
    # # # # #暂时有bug的技能
    # skill_list.remove(79)
    # #skill_list.remove(81) #带概率的后面统一测试
    # skill_list.remove(82)
    # skill_list.remove(85)# 需要改
    # skill_list.remove(99)
    #
    #
    # #
    # # #通过的技能
    # # skill_list.remove(91)
    # # skill_list.remove(92)
    # # skill_list.remove(88)
    # # skill_list.remove(90)
    # # skill_list.remove(77)
    # # skill_list.remove(78)
    # # skill_list.remove(80)
    # # skill_list.remove(83)
    # # skill_list.remove(84)
    # # skill_list.remove(85)
    # # skill_list.remove(86)
    # # skill_list.remove(96)
    # #
    # # skill_list.remove(78)
    # # skill_list.remove(97)
    # # skill_list.remove(98)
    # # skill_list.remove(99)
    # # skill_list.remove(100)
    # # skill_list.remove(101)
    # # skill_list.remove(102)
    # # skill_list.remove(103)
    # #
    # #
    # skill_list=[79,81,82,85,99]
    # #
    # #
    # for skill_id in skill_list:
    #      single_skill_test_main(basecalssid=1,skill_id=skill_id,pygame_init=False)
    #main()
    replay()