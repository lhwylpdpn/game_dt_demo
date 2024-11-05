import game_info
import agent

def train_agent(num_episodes):





    game = game_info.game()
    agent_liu = agent.randomAgent('小刘', game)
    agent_qiang = agent.QLearningAgent('强爷', game)

    res=[]
    # 运行多次游戏
    for i_episode in range(num_episodes):
        # 开始新的游戏
        game.reset()
        game.start()
        game.next()

        print(f'第{i_episode}次游戏')

        while True:
            agent_liu.act_hero = agent_liu.get_action_hero(game.get_current_herolist('小刘'))
            action = agent_liu.choice_act(game.state)
            game.action_to_state(agent_liu.act_hero, action)
            game_status, team = game.check_game_over()


            if game_status:
                agent_qiang.update_q_value(reward=-1)#失败不能给0 ，给0是表示学习不到任何内容
                res.append(team)
                break

            game.next()
            state = game.state

            action = agent_qiang.get_action(state)
            game.action_to_state(agent_qiang.act_hero, action)
            game_status, team = game.check_game_over()
            if game_status:
                agent_qiang.update_q_value(reward=1)
                res.append(team)
                break
            game.next()
        #print(f'第{i_episode}次游戏')
        print('游戏结束时候的 agent_qiang.q_table',agent_qiang.q_table)
    return  res
if __name__ == '__main__':
    res=train_agent(300)
    #通过MC反复训练，获得一个针对随机操作的Q表，然后通过Q表来进行决策就行，Q表就是可以用来决策对model了
    #打印胜利次数可以看到，只有前几次小刘能胜利，战斗次数多了，都是强爷胜利了


    print('小刘胜利次数',res.count('小刘'))
    print('强爷胜利次数',res.count('强爷'))





#定义一个接口
{
state: {
    [[
    [{HP:300,type:5..},{HP:300,type:5..},{{HP:300,type:5..}],
    [{HP:300,type:5..},{HP:300,type:5..},{{HP:300,type:5..}],
    ],
        [
    [{HP:300,type:5..},{HP:300,type:5..},{{HP:300,type:5..}],
    [{HP:300,type:5..},{HP:300,type:5..},{{HP:300,type:5..}],
    ],
[
    [{HP:300,type:5..},{HP:300,type:5..},{{HP:300,type:5..}],
    [{HP:300,type:5..},{HP:300,type:5..},{{HP:300,type:5..}],
    ]]
    },

hero_list: {
    [
    {
    name: '小刘',
    team: 1,
    x: 1,
    y: 1,
    z: 3,
    hp: 100,
    ap: 100,
    atk: 10,
    distance: 5,
    defense: 0,

    skill:{'atk':20,'distance':5,'limit':2,'current':0},
    deaded: False
    },
    {
    name: '小刘',
    team: 1,
    x: 1,
    y: 1,
        z: 3,
    hp: 100,
    mp: 100,
    atk: 10,
    skill:{'atk':20,'distance':5,'limit':2,'current':0},
    deaded: False
    },
    {
    name: '小刘',
    team: 2,
    x: 1,
    y: 1,
        z: 3,
    hp: 100,
    mp: 100,
    atk: 10,
    skill:{'atk':20,'distance':5,'limit':2,'current':0},
    deaded: False
    }
    ]
    }

}
name,id,teamid,hp,ap,atk,atk_distance,defense,运气,灵巧,move_distance,move_distance_y,skill{}