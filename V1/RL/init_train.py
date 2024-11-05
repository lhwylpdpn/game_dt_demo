import os
import sys
import time
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from buildpatrol import BuildPatrol
from schedule import schedule
from strategy.single_RL_agent import Q_Agent
from strategy.single_RL_agent import Random_Agent
from strategy.single_RL_agent import PPO_Agent

from V1.test.demo_show import game
from PPO import PPO
import copy
from datetime import datetime

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

    sch.performance.end()
    res_json=sch.send_update()
    sch.performance.static()
    replay(state_init,res_json)
    return sch.agent_1.q_table
#
def replay(state,json_=os.path.abspath(os.path.join(os.path.dirname(__file__)))+'/../for_qiangye.json'):
    game_obj=game(state)
    game_obj.game_init()
    game_obj.run(json_)


def train_ppo():




    print("============================================================================================")

    ####### initialize environment hyperparameters ######
    env_name = "liutest"


    max_ep_len = 2000                   # max timesteps in one episode
    train_loop = 20    # break training loop if timeteps > max_training_timesteps

    print_freq = max_ep_len * 10        # print avg reward in the interval (in num timesteps)
    log_freq = max_ep_len * 2           # log avg reward in the interval (in num timesteps)
    save_model_freq = int(1e5)          # save model frequency (in num timesteps)

    action_std = 0.6                    # starting std for action distribution (Multivariate Normal)
    action_std_decay_rate = 0.05        # linearly decay action_std (action_std = action_std - action_std_decay_rate)
    min_action_std = 0.1                # minimum action_std (stop decay after action_std <= min_action_std)
    action_std_decay_freq = int(2.5e5)  # action_std decay frequency (in num timesteps)
    #####################################################

    ## Note : print/log frequencies should be > than max_ep_len

    ################ PPO hyperparameters ################
    update_timestep = max_ep_len * 4      # update policy every n timesteps
    K_epochs = 80               # update policy for K epochs in one PPO update

    eps_clip = 0.2          # clip parameter for PPO
    gamma = 0.99            # discount factor

    lr_actor = 0.0003       # learning rate for actor network
    lr_critic = 0.001       # learning rate for critic network

    random_seed = 0         # set random seed if required (0 = no random seed)
    #####################################################

    print("training environment name : " + env_name)


    # state space dimension
    state_dim = 2# todo 看真实

    # action space dimension

    action_dim = 3#todo 看真实

    ###################### logging ######################

    #### log files for multiple runs are NOT overwritten
    log_dir = "PPO_logs"
    if not os.path.exists(log_dir):
          os.makedirs(log_dir)

    log_dir = log_dir + '/' + env_name + '/'
    if not os.path.exists(log_dir):
          os.makedirs(log_dir)

    #### get number of log files in log directory
    run_num = 0
    current_num_files = next(os.walk(log_dir))[2]
    run_num = len(current_num_files)

    #### create new log file for each run
    log_f_name = log_dir + '/PPO_' + env_name + "_log_" + str(run_num) + ".csv"

    print("current logging run number for " + env_name + " : ", run_num)
    print("logging at : " + log_f_name)
    #####################################################

    ################### checkpointing ###################
    run_num_pretrained = 0      #### change this to prevent overwriting weights in same env_name folder

    directory = "PPO_preTrained"
    if not os.path.exists(directory):
          os.makedirs(directory)

    directory = directory + '/' + env_name + '/'
    if not os.path.exists(directory):
          os.makedirs(directory)


    checkpoint_path = directory + "PPO_{}_{}_{}.pth".format(env_name, random_seed, run_num_pretrained)
    print("save checkpoint path : " + checkpoint_path)
    #####################################################


    ############# print all hyperparameters #############
    print("--------------------------------------------------------------------------------------------")
    # print("max training timesteps : ", max_training_timesteps)
    print("max timesteps per episode : ", max_ep_len)
    print("model saving frequency : " + str(save_model_freq) + " timesteps")
    print("log frequency : " + str(log_freq) + " timesteps")
    print("printing average reward over episodes in last : " + str(print_freq) + " timesteps")
    print("--------------------------------------------------------------------------------------------")
    print("state space dimension : ", state_dim)
    print("action space dimension : ", action_dim)
    print("--------------------------------------------------------------------------------------------")
    print("Initializing a discrete action space policy")
    print("--------------------------------------------------------------------------------------------")
    print("PPO update frequency : " + str(update_timestep) + " timesteps")
    print("PPO K epochs : ", K_epochs)
    print("PPO epsilon clip : ", eps_clip)
    print("discount factor (gamma) : ", gamma)
    print("--------------------------------------------------------------------------------------------")
    print("optimizer learning rate actor : ", lr_actor)
    print("optimizer learning rate critic : ", lr_critic)
    print("============================================================================================")

    ################# training procedure ################

    # initialize a PPO agent
    ppo_agent = PPO(state_dim, action_dim, lr_actor, lr_critic, gamma, K_epochs, eps_clip)

    # track total training time
    start_time = datetime.now().replace(microsecond=0)
    print("Started training at (GMT) : ", start_time)

    print("============================================================================================")

    # logging file
    log_f = open(log_f_name,"w+")
    log_f.write('episode,timestep,reward\n')

    # printing and logging variables
    print_running_reward = 0
    print_running_episodes = 0

    log_running_reward = 0
    log_running_episodes = 0

    time_step = 0
    i_episode = 0


    print("game_info============================================================================================")

    path=os.path.abspath(os.path.join(os.path.dirname(__file__)))
    src_path=path+"/../data.json"
    state_init = BuildPatrol(src_path).load_data()
    state_init=data_init(state_init)
    sch=schedule(state_init)
    sch.agent_1 = PPO_Agent(ppo_agent=ppo_agent)
    sch.agent_2 = Random_Agent()
    sch.timeout_tick=200
    battle_res = []

    # training loop
    while time_step <= train_loop:

        sch.game.reset()
        sch.game.start()
        state = sch.game.get_current_state()
        state_dict = sch.state_to_dict(state)
        sch.init_state = state_dict

        #todo 这个地方需要完全自定义处理





        while sch.tick < sch.timeout_tick and not sch.game_over:
            sch.tick += 1
            sch.next()#
            #todo 这个地方调用next,
            print(sch.state)
            time.sleep(100)
        game_res = sch.game.check_game_over()[1]
        if game_res == 0:  # 怪兽胜利
            sch.agent_1.update_q_value(reward=-2)  # 去更新 .update_q_value(reward=-2)
        if game_res == 1:  # 英雄胜利
            sch.agent_1.update_q_value(reward=1)  # 去更新 .update_q_value(reward= 1)
        if game_res == 2:  # 平局
            sch.agent_1.update_q_value(reward=-1)  # 去更新 .update_q_value(reward= -1)
        battle_res.append(game_res)
        sch.tick = 0





        for t in range(1, max_ep_len+1):

            # select action with policy
            action = ppo_agent.select_action(state)
            state, reward, done, _ = env.step(action)

            # saving reward and is_terminals
            ppo_agent.buffer.rewards.append(reward)
            ppo_agent.buffer.is_terminals.append(done)

            time_step +=1
            current_ep_reward += reward

            # update PPO agent
            if time_step % update_timestep == 0:
                ppo_agent.update()

            # if continuous action space; then decay action std of ouput action distribution
            if has_continuous_action_space and time_step % action_std_decay_freq == 0:
                ppo_agent.decay_action_std(action_std_decay_rate, min_action_std)

            # log in logging file
            if time_step % log_freq == 0:

                # log average reward till last episode
                log_avg_reward = log_running_reward / log_running_episodes
                log_avg_reward = round(log_avg_reward, 4)

                log_f.write('{},{},{}\n'.format(i_episode, time_step, log_avg_reward))
                log_f.flush()

                log_running_reward = 0
                log_running_episodes = 0

            # printing average reward
            if time_step % print_freq == 0:

                # print average reward till last episode
                print_avg_reward = print_running_reward / print_running_episodes
                print_avg_reward = round(print_avg_reward, 2)

                print("Episode : {} \t\t Timestep : {} \t\t Average Reward : {}".format(i_episode, time_step, print_avg_reward))

                print_running_reward = 0
                print_running_episodes = 0

            # save model weights
            if time_step % save_model_freq == 0:
                print("--------------------------------------------------------------------------------------------")
                print("saving model at : " + checkpoint_path)
                ppo_agent.save(checkpoint_path)
                print("model saved")
                print("Elapsed Time  : ", datetime.now().replace(microsecond=0) - start_time)
                print("--------------------------------------------------------------------------------------------")

            # break; if the episode is over
            if done:
                break

        print_running_reward += current_ep_reward
        print_running_episodes += 1

        log_running_reward += current_ep_reward
        log_running_episodes += 1

        i_episode += 1

    log_f.close()
    env.close()

    # print total training time
    print("============================================================================================")
    end_time = datetime.now().replace(microsecond=0)
    print("Started training at (GMT) : ", start_time)
    print("Finished training at (GMT) : ", end_time)
    print("Total training time  : ", end_time - start_time)
    print("============================================================================================")





def clac_rewards(state):
    """

    :param state: 传入整个state镜像
    :return: 返回奖励制
    """


if __name__ == '__main__':
    #table=train_agent(num_episodes=1)
    train_ppo()




