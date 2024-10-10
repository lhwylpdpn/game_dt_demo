from V1.utils.strategy_utils.range import Range
import time
import random
class Agent(object):


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