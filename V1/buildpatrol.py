# -*- coding:utf-8 -*-
"""
@author HU
@date 20245-07-23
"""
import json
import copy
import pickle
from pprint import pprint
from models.hero import Hero
from models.monster import Monster
from models.skill import Skill
from models.effect import Effect
from models.map import Map, Land
from models.teamflag import TeamFlag
from models.attachment import Attachment


class BuildPatrol():

    def __init__(self, src_data_path):
        self.src_data_path = src_data_path
    
    def load_data(self):
        with open(self.src_data_path, 'r') as file:
            src_json_data = json.load(file)
        heros = self.build_object(src_json_data.get("hero"), hero_or_monster="hero")
        monsters = self.build_object(src_json_data.get("monster"), hero_or_monster="monster")
        TeamFlag.search_teammate(heros)
        TeamFlag.search_teammate(monsters)
        _map = self.build_map(src_json_data.get("map"))     # 初始化地图
        attachments =  self.map_load_attachment(src_json_data, _map) # 地图加载附着物
        return {"map": _map, 
                "hero": heros,
                "monster": monsters,
                "attachment": attachments
                }

    @staticmethod
    def build_object(origin_hero_data, hero_or_monster):  # 
        m_h_obj_list = []
        buff_unit_dis = [] # 全队连携的buff
        Object_Class = Hero if hero_or_monster == "hero" else Monster
        for each in origin_hero_data:
            m_h_obj = Object_Class(**each)
            skills = []
            for skill in each.get("skills"):
                _skill = Skill(**skill)
                for each_effect in skill.get("effects"):
                    _effect = Effect(**each_effect)
                    _skill.effects_add(_effect)
                skills.append(_skill)
            m_h_obj.set_skills(skills)
            buffs = m_h_obj.load_init_unActiveSkill() # 返回全队的连携
            buff_unit_dis.extend(buffs)
            m_h_obj_list.append(m_h_obj)
        
        # 加载给全部队友的buff
        for each_buff_unit_dis in buff_unit_dis: # 所有的连携 
            for each in m_h_obj_list:
                if each_buff_unit_dis.buff_from != each: #  不是自己的技能，需要加一下
                    each.add_buff_object(copy.deepcopy(each_buff_unit_dis))
        
        return m_h_obj_list

    @staticmethod
    def build_map(origin_map_data):  # 返回加载地块的MAP对象
        map = Map(*Map.find_map_size(origin_map_data))
        for each in origin_map_data:
            position = each.get("position")
            land = Land(**each)
            map.load_land(*position, land)
        # pprint(map.view_from_y())
        return map
    
    @staticmethod
    def map_load_attachment(origin_attachment_data, map_obj): # 加载地图附着物
        # 第二层 无
        # 第三层 地块的相关buff
        # 第四层  拒马， 火药桶， 宝箱
        attachments = []
        for each in origin_attachment_data.get("map_3", []) + origin_attachment_data.get("map_4", []) : 
            new_attach = Attachment(**each)
            attachments.append(new_attach)
            _effects = []
            for each_effect in each.get("effects"):
                _effect = Effect(**each_effect)
                _effects.append(_effect)
            new_attach.set_effects(_effects)
            map_obj.load_attachment(new_attach)
    
        return attachments


def test_atk_bomb(stats):
    hero = state.get("hero")[0] #
    state["maps"] = state["map"]
    hero.move_position(15,13,11, state=stats)
    map_ = state.get("map")
    bomb = state.get("attachment")[2]
    map_.attack_attachment( wage_object=hero, 
                            skill=hero.skills[0], 
                            attachment=bomb, stats=stats)


def pickle_state(state):
    
    file = "break.data"
    # with open(file, "wb") as file_obj: 
    #     state_pickle =  pickle.dump(state, file_obj)

    with open(file, "rb") as file_obj:
        new_state = pickle.load(file_obj)


if __name__ == "__main__":
    state = BuildPatrol("data.json").load_data()
    file = "break.data"
    
    with open(file, "wb") as file_obj: 
        state_pickle =  pickle.dump(state, file_obj)
        
    with open(file, "rb") as file_obj:
        new_state = pickle.load(file_obj)

    # state_pickle =  pickle.dumps(state)
    # new_state = pickle.loads(state_pickle)  

    print(new_state)

    # state['maps'] = state['map']
    # #test_atk_bomb(state)
    # for each in state.get("hero") + state.get("monster"):
    #     each.move_position(*each.position, state)
    # map_ = state.get("map")
    # for p in state['map'].view_from_y_dict().keys():
    #     print(p, "land_can_pass", state['map'].land_can_pass(p[0],p[1],p[2]))

    
    # state["maps"] = state["map"]
    # print(len(state.get("monster")))
    # hero2 = state.get("hero")[2]
    # hero2.move_position(3,1,4, state=state)
    # hero.move_position(3,1,3, state=state)
    # print(hero.hero_or_monster())
    # print(hero.BaseClassID)
    # monster = state.get("monster")[0]
    # monster.move_position(3,1,4, state=state)
    
    # monster.func_attack(enemys=[hero], 
    #                     skill=skill, 
    #                     attack_point=hero.position, 
    #                     state=state)
    
    # print("use skill_104 test:", skill)
    # skill = hero.get_skill_by_id(104)
    # hero.focus(state=state)
    # print(hero.Hp)
    # hero.set_Hp(100)
    # print(hero.Hp)
    # for e in hero.un_focus(state=state):
    #     hero.trigger_buff(e)
    # print(hero.Hp)

    # hero0 = state.get("hero")[1
    # ]
    # hero1 = state.get("hero")[0]
    # monster0 = state.get("monster")[0]
    # monster1 = state.get("monster")[1]
    # hero2.set_AvailableSkills([82])
    # print(hero0.skills)

    # skill = hero0.get_skill_by_id(78)
   
    # hero0.move_position(3,1,6, state=state)
    # monster0.move_position(3,1,4, state=state)
    # monster1.move_position(3,1,3, state=state)
    # hero0.after_atk_skill(enemys=[monster0,monster1], skill=skill, attack_point=[3,1,5], state=state)
    # print("use skill_79 test:", skill)
    # print( hero0.friend_treatment(
    #     friends=[hero1], 
    #                     skill=skill, 
    #                     attack_point=hero1.position, 
    #                     state=state))
    # print(hero1.dict())

    


    
