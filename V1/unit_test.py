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

    def data_init_fanji(self,state):
        p_all = state['maps'].view_from_y_dict().keys()
        p_all = list(p_all)
        for p in state['maps'].view_from_y_dict().keys():
            if p[0] > 4 or p[2] > 4:
                state['maps'].set_land_no_pass(p[0], p[1], p[2], 1)
        for p in state['maps'].view_from_y_dict().keys():
            # if state['map'].view_from_y_dict()[p]['Block'] != 0:
            #     p_all.remove(p)
            if not state['maps'].land_can_pass(p[0], p[1], p[2]):
                p_all.remove(p)
        state['hero'] = [_ for _ in state['hero'] if _.HeroID == 5002]
        state['monster'] = [_ for _ in state['monster'] if _.Quality == 2]

        for i in range(len(state['hero'])):

            p = random.choice(p_all)
            p_all.remove(p)

            tmp_skills = [82]

            state['hero'][i].set_AvailableSkills(tmp_skills)

            state['hero'][i].set_x(p[0])
            state['hero'][i].set_y(p[1])
            state['hero'][i].set_z(p[2])
        for i in range(len(state['monster'])):

            p = random.choice(p_all)
            p_all.remove(p)
            monster_random_Atk = random.randint(80,80)
            state['monster'][i].set_Atk(monster_random_Atk)

            # tmp_skills = [82]
            #
            # state['monster'][i].set_AvailableSkills(tmp_skills)

            state['monster'][i].set_x(p[0])
            state['monster'][i].set_y(p[1])
            state['monster'][i].set_z(p[2])
        return state

    def data_init(self,state):
        for i in range(len(state['hero'])):

            #hero_random_RoundAction = random.randint(5, 5)
            #hero_random_JumpHeight = [random.randint(15, 15)]
            #hero_random_DogBase = random.randint(5, 5)
            #hero_random_HP = random.randint(500, 500)
            #hero_random_Atk = random.randint(200, 200)

            # self.state['hero'][i].set_RoundAction(hero_random_RoundAction)
            # self.state['hero'][i].set_JumpHeight(hero_random_JumpHeight)
            # self.state['hero'][i].set_DogBase(hero_random_DogBase)
            # self.state['hero'][i].set_Hp(hero_random_HP)
            # self.state['hero'][i].set_Atk(hero_random_Atk)
            pass
        for i in range(len(state['monster'])):

            hero_random_Atk = random.randint(135, 135)

            state['monster'][i].set_Atk(hero_random_Atk)
        self.state=state
        return state

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
    obj_.data_init_fanji(obj_.state)
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
    main()
