import os
import sys
import time
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from buildpatrol import BuildPatrol
from schedule import schedule
from strategy.single_RL_agent import Q_Agent
from strategy.single_RL_agent import Random_Agent
from V1.test.demo_show import game


import copy


def data_init(state):
    p_all = state['map'].view_from_y_dict().keys()
    p_all = list(p_all)

    for p in state['map'].view_from_y_dict().keys():
        if p[0] > 4 or p[2]>4:
            state['map'].set_land_no_pass(p[0], p[1], p[2], 5)
    for p in state['map'].view_from_y_dict().keys():
        if state['map'].view_from_y_dict()[p]['Block'] != 1:
            p_all.remove(p)
    state['hero'] = [_ for _ in state['hero'] if _.HeroID == 5002]
    state['monster'] = [_ for _ in state['monster'] if _.Quality == 2]
    # 提取 x, y, z（高度）的值
    #
    # import matplotlib.pyplot as plt
    #
    # x = [p[0] for p in p_all]
    # z = [state['map'].view_from_y_dict()[p]['Block'] for p in p_all]  # 表示是否有占用
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
    for i in range(len(state['hero'])):
        # hero_random_RoundAction = random.randint(5, 5)
        # hero_random_JumpHeight = [random.randint(15, 15)]
        # hero_random_DogBase = random.randint(5, 5)
        # hero_random_HP = random.randint(500, 500)
        # hero_random_Atk = random.randint(200, 200)
        # #
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
        tmp_skills = [77]
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
        state['hero'][i].set_AvailableSkills(tmp_skills)
        # state['hero'][i].set_RoundAction(hero_random_RoundAction)
        # state['hero'][i].set_JumpHeight(hero_random_JumpHeight)
        # state['hero'][i].set_DogBase(hero_random_DogBase)
        # state['hero'][i].set_Hp(hero_random_HP)
        # state['hero'][i].set_Atk(hero_random_Atk)
        # # #随机选地图的一个位置给到英雄
        # # print('p', p)
        state['hero'][i].set_x(p[0])
        state['hero'][i].set_y(p[1])
        state['hero'][i].set_z(p[2])

    for i in range(len(state['monster'])):
        # monster_random_RoundAction = random.randint(5, 5)
        # monster_random_JumpHeight = [random.randint(15, 15)]
        # monster_random_DogBase = random.randint(5, 5)
        # monster_random_HP = random.randint(500, 500)
        # monster_random_Atk = random.randint(200, 200)
        p = random.choice(p_all)
        p_all.remove(p)
        # tmp_skills = copy.deepcopy(self.state['monster'][i].dict()['AvailableSkills'])
        # print('tmp_skills',tmp_skills)
        # for j in self.state['monster'][i].dict()['AvailableSkills']:
        #     if random.random() > 0.5:
        #         tmp_skills.remove(j)
        # if 200 not in tmp_skills:
        #     tmp_skills.append(200)
        # tmp_skills = [77, 78, 88]
        # print('monster',self.state['monster'][i].dict()['HeroID'])
        # print('monster_random_RoundAction', monster_random_RoundAction)
        # print('monster_random_JumpHeight', monster_random_JumpHeight)
        # print('monster_random_DogBase', monster_random_DogBase)
        # print('monster_random_HP', monster_random_HP)
        # print('monster_random_Atk', monster_random_Atk)

        # self.state['monster'][i].set_AvailableSkills(tmp_skills)
        # self.state['monster'][i].set_RoundAction(monster_random_RoundAction)
        # self.state['monster'][i].set_JumpHeight(monster_random_JumpHeight)
        # self.state['monster'][i].set_DogBase(monster_random_DogBase)
        # self.state['monster'][i].set_Hp(monster_random_HP)
        # self.state['monster'][i].set_Atk(monster_random_Atk)
        # self.state['monster'][i].set_Def(monster_random_Def)
        # if i==0:
        #     p=(19,5,18)
        # if i==1:
        #     p=(12,7,8)
        # print('p', p)
        state['monster'][i].set_x(p[0])
        state['monster'][i].set_y(p[1])
        state['monster'][i].set_z(p[2])
    return state

def train_agent(num_episodes):
    # 初始化游戏和agent
    # 1、加载游戏
    # 2、初始化游戏
    # 3、定义agent 训练一个针对随机的agent
    # 4、定义rewards 试着分步奖励
    # 5、反复跑，怎么存储model下次好加载
    path=os.path.abspath(os.path.join(os.path.dirname(__file__)))
    src_path=path+"/../data.json"
    state_init = BuildPatrol(src_path).load_data()
    state_init=data_init(state_init)
    sch=schedule(state_init)
    sch.agent_1 = Q_Agent()
    sch.agent_2 = Random_Agent()
    sch.timeout_tick=500
    battle_res = []



    res=[]
    for i_episode in range(num_episodes):
        # 开始新的游
        print('episodes',i_episode)
        sch.game.reset()
        sch.game.start()
        state = sch.game.get_current_state()
        state_dict = sch.state_to_dict(state)
        sch.init_state=state_dict

        while sch.tick < sch.timeout_tick and not sch.game_over:
            sch.tick+=1
            sch.next()

        game_res=sch.game.check_game_over()[1]
        if game_res==0:#怪兽胜利
            sch.agent_1.update_q_value(reward=-2) #去更新 .update_q_value(reward=-2)
        if game_res==1: # 英雄胜利
            sch.agent_1.update_q_value(reward=1) #去更新 .update_q_value(reward= 1)
        if game_res==2: # 平局
            sch.agent_1.update_q_value(reward=-1)#去更新 .update_q_value(reward= -1)
        battle_res.append(game_res)
        sch.tick = 0
    print('总共训练到的state类别是:',len(sch.agent_1.q_table.keys()))
    print('总共训练到的各个类别的平均分是:',sum(sch.agent_1.q_table.values())/len(sch.agent_1.q_table.keys()))

    print('战场情况:胜利次数--'+str(sum([1 for _ in battle_res if _==0])))
    print('战场情况:失败次数--'+str(sum([1 for _ in battle_res if _==1])))
    print('战场情况:平局次数--'+str(sum([1 for _ in battle_res if _==2])))


    res_json=sch.send_update()
    sch.performance.static()
    #replay(state_init,res_json)
    return sch.agent_1.q_table
#
def replay(state,json_=os.path.abspath(os.path.join(os.path.dirname(__file__)))+'/../for_qiangye.json'):
    game_obj=game(state)
    game_obj.game_init()
    game_obj.run(json_)
if __name__ == '__main__':
    table=train_agent(num_episodes=10)


