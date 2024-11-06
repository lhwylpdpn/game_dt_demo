import json

from utils.strategy_utils.range import Range
import time
import random
from RL.Q_lerning import QLearningAgent
from RL.PPO import PPO
import numpy as np
class Q_Agent(QLearningAgent):


    def action_transition(self,allow_actions):
        res=[]
        for key in allow_actions:
            for action in allow_actions[key]:
                if type(action)==dict:
                    res.append(action)
                if type(action)==list:
                    for _ in action:
                        res.append(_)

        #结构清理，返回训练需要的结构和事实结构
        res_train=[]

        for r in res:
            if r['action_type'] in ['LEFT','RIGHT','BOTTOM','TOP']:
                res_train.append({k: v for k, v in r.items() if k  in ['action_type']})
            elif 'SKILL' in r['action_type']:
                res_train.append({k: v for k, v in r.items() if k  in ['action_type']})
            elif 'WAIT' in r['action_type']:
                res_train.append({k: v for k, v in r.items()})
            else:
                res_train.append({k: v for k, v in r.items()})

        return res,res_train
    def swap_specific_keys(self, d, key1, key2):
        d2 = {}
        if key1 not in d or key2 not in d:
            raise KeyError("Both keys must exist in the dictionary.")

        d2[key1], d2[key2] = d[key2], d[key1]
        d2["map"] = d["map"]
        return d2

    def add_maps_block(self, state):
        maps = state["maps"]
        for m in [state["hero"] + state["monster"]]:
            m.move_position(m.position, state["maps"])

    def choice_hero_act(self, hero, state,performance=None):
        print('RL agent------------------------------')
        hero = hero.dict()
        allow_actions = Range(state=state, role=hero).simple_strategy()
        actions,train_actions=self.action_transition(allow_actions)
        #随机选择train_actions中的某一个，然后用这个序号选择actions
        state_={}

        state_['hero'] = [_.dict() for _ in state['hero']]
        state_['monster']=[_.dict() for _ in state['monster']]
        state_['map'] =state['map'].dict()
        state_['attachment']=[_.dict() for _ in state['attachment']]
        train_actions=[json.dumps(action,sort_keys=True) for action in train_actions]
        state_=json.dumps(state_,sort_keys=True)
        res = self.get_action(state=state_, action_list=train_actions)
        index = train_actions.index(res)
        res=actions[index]
        print('------------------------------')
        return [res]

    def choice_monster_act(self, hero, state,performance=None):
        state = self.swap_specific_keys(state, "hero", "monster")
        hero = hero.dict()
        # enemies = [_.dict() for _ in state["monster"]]
        # maps = state["map"].view_from_y_dict()
        # maps = Attack().convert_maps(maps)
        # teammates = [_.dict() for _ in state["hero"] if _.HeroID != hero["HeroID"]]
        allow_actions = Range(state=state, role=hero).simple_strategy()
        actions, train_actions = self.action_transition(allow_actions)
        # 随机选择train_actions中的某一个，然后用这个序号选择actions
        res = random.choice(train_actions)
        index = train_actions.index(res)
        res = actions[index]
        print('返回的', res)
        print('------------------------------')
        return [res]


class PPO_Agent():

    def __init__(self,ppo_agent):
        self.agent=ppo_agent
    def action_transition(self,allow_actions):
        res=[]
        for key in allow_actions:
            for action in allow_actions[key]:
                if type(action)==dict:
                    res.append(action)
                if type(action)==list:
                    for _ in action:
                        res.append(_)

        #结构清理，返回训练需要的结构和事实结构
        res_train=[]

        for r in res:
            if r['action_type'] in ['LEFT','RIGHT','BOTTOM','TOP']:
                res_train.append({k: v for k, v in r.items() if k  in ['action_type']})
            elif 'SKILL' in r['action_type']:
                res_train.append({k: v for k, v in r.items() if k  in ['action_type']})
            elif 'WAIT' in r['action_type']:
                res_train.append({k: v for k, v in r.items()})
            else:
                res_train.append({k: v for k, v in r.items()})

        return res,res_train
    def swap_specific_keys(self, d, key1, key2):
        d2 = {}
        if key1 not in d or key2 not in d:
            raise KeyError("Both keys must exist in the dictionary.")

        d2[key1], d2[key2] = d[key2], d[key1]
        d2["map"] = d["map"]
        return d2

    def add_maps_block(self, state):
        maps = state["maps"]
        for m in [state["hero"] + state["monster"]]:
            m.move_position(m.position, state["maps"])

    def choice_hero_act(self, hero, state,performance=None):
        print('RL agent------------------------------')
        hero = hero.dict()
        allow_actions = Range(state=state, role=hero).simple_strategy()
        actions,train_actions=self.action_transition(allow_actions)
        #随机选择train_actions中的某一个，然后用这个序号选择actions
        state_ = {}

        state_['hero'] = [_.dict() for _ in state['hero']]
        state_['monster'] = [_.dict() for _ in state['monster']]
        state_['map'] = state['map'].dict()
        state_['attachment'] = [_.dict() for _ in state['attachment']]
        train_actions=[json.dumps(action,sort_keys=True) for action in train_actions]

        state_=self.convert_state_to_tensor(state_)
        res = self.agent.select_action(state_)
        print(res)
        index = train_actions.index(res)
        res=actions[index]
        print('选择的动作',res)
        print('------------------------------')
        return [res]

    def choice_monster_act(self, hero, state,performance=None):
        state = self.swap_specific_keys(state, "hero", "monster")
        hero = hero.dict()
        # enemies = [_.dict() for _ in state["monster"]]
        # maps = state["map"].view_from_y_dict()
        # maps = Attack().convert_maps(maps)
        # teammates = [_.dict() for _ in state["hero"] if _.HeroID != hero["HeroID"]]
        allow_actions = Range(state=state, role=hero).simple_strategy()
        actions, train_actions = self.action_transition(allow_actions)
        # 随机选择train_actions中的某一个，然后用这个序号选择actions
        res = random.choice(train_actions)
        index = train_actions.index(res)
        res = actions[index]
        print('返回的', res)
        print('------------------------------')
        return [res]

    def convert_state_to_tensor(self,state_dict):
        print(state_dict)

        def flatten_dict(d, parent_key='', sep='_'):
            items = []
            if isinstance(d, list):
                for index, item in enumerate(d):
                    if isinstance(item, dict):
                        items.extend(flatten_dict(item, f"{parent_key}{sep}{index}", sep=sep).items())
                    elif isinstance(item, (int, float)):  # 直接保留数值
                        items.append((f"{parent_key}{sep}{index}", item))
            elif isinstance(d, dict):
                for k, v in d.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else k
                    if isinstance(v, (dict, list)):
                        items.extend(flatten_dict(v, new_key, sep=sep).items())
                    elif isinstance(v, (int, float)):  # 只保留数值类型
                        items.append((new_key, v))
            return dict(items)

        flattened_dict = flatten_dict(state_dict)
        values = [v for k, v in flattened_dict.items()]
        return np.array(values, dtype=np.float32)


class Random_Agent(object):


    def action_transition(self,allow_actions):
        res=[]
        for key in allow_actions:
            for action in allow_actions[key]:
                if type(action)==dict:
                    res.append(action)
                if type(action)==list:
                    for _ in action:
                        res.append(_)

        #结构清理，返回训练需要的结构和事实结构
        res_train=[]

        for r in res:
            if r['action_type'] in ['LEFT','RIGHT','BOTTOM','TOP']:
                res_train.append({k: v for k, v in r.items() if k  in ['action_type']})
            elif 'SKILL' in r['action_type']:
                res_train.append({k: v for k, v in r.items() if k  in ['action_type']})
            elif 'WAIT' in r['action_type']:
                res_train.append({k: v for k, v in r.items()})
            else:
                res_train.append({k: v for k, v in r.items()})

        return res,res_train
    def swap_specific_keys(self, d, key1, key2):
        d2 = {}
        if key1 not in d or key2 not in d:
            raise KeyError("Both keys must exist in the dictionary.")

        d2[key1], d2[key2] = d[key2], d[key1]
        d2["map"] = d["map"]
        return d2

    def add_maps_block(self, state):
        maps = state["maps"]
        for m in [state["hero"] + state["monster"]]:
            m.move_position(m.position, state["maps"])

    def choice_hero_act(self, hero, state,performance=None):
        print('RL agent------------------------------')
        hero = hero.dict()
        allow_actions = Range(state=state, role=hero).simple_strategy()
        actions,train_actions=self.action_transition(allow_actions)
        #随机选择train_actions中的某一个，然后用这个序号选择actions
        res = random.choice(train_actions)
        index = train_actions.index(res)
        res=actions[index]
        print('返回的',res)
        print('------------------------------')

        return [res]

    def choice_monster_act(self, hero, state,performance=None):
        state = self.swap_specific_keys(state, "hero", "monster")
        hero = hero.dict()
        # enemies = [_.dict() for _ in state["monster"]]
        # maps = state["map"].view_from_y_dict()
        # maps = Attack().convert_maps(maps)
        # teammates = [_.dict() for _ in state["hero"] if _.HeroID != hero["HeroID"]]
        allow_actions = Range(state=state, role=hero).simple_strategy()
        actions, train_actions = self.action_transition(allow_actions)
        # 随机选择train_actions中的某一个，然后用这个序号选择actions
        res = random.choice(train_actions)
        index = train_actions.index(res)
        res = actions[index]
        print('返回的', res)
        print('------------------------------')
        return [res]