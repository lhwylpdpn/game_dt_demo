
import numpy as np

class QLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate
        self.q_table = {}  # initialize Q-table
        self.episode = []

    def get_q_value(self, state, action):
        #如果遇到一个新的状态，就将这个状态加入到q表，并且置为0
        #print(type(state),type(action),'test')
        if (state, action) not in self.q_table:
            print('这里有一次重新state，get_q_value',state,action)
            self.q_table[(state, action)] = 0.0
        return self.q_table[(state, action)]

    #MC-RL 只更新结局，反推步骤奖励
    def update_q_value(self, reward):
        # update Q values based on the reward received at the end of an episode
        for state, action in reversed(self.episode):
            if (state, action) not in self.q_table:
                self.q_table[(state, action)] = 0
            self.q_table[(state, action)] = self.alpha * (reward + self.gamma * self.q_table[(state, action)]) + (1 - self.alpha) * self.q_table[(state, action)]
        self.episode = []  # reset the episode list
    def get_action(self, state,action_list):
        # epsilon-greedy policy

        if np.random.uniform(0, 1) < self.epsilon:
            # explore: choose a random action
            action = np.random.choice(action_list)
        else:
            # exploit: choose the action with max Q value for the current state
            #只能从当前state内游戏规则允许的动作中选择
            q_values = {action: self.get_q_value(state, action) for action in action_list}
            max_q_value = max(q_values.values())
            # if multiple actions have the max Q value, randomly choose one of them
            actions_with_max_q_value = [action for action, q_value in q_values.items() if q_value == max_q_value]
            action = np.random.choice(actions_with_max_q_value)

        self.episode.append((state, action))  # add the state-action pair to the episode list
        return action