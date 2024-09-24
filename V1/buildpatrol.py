# -*- coding:utf-8 -*-
"""
@author HU
@date 20245-07-23
"""
import json
import copy
from pprint import pprint
from models.hero import Hero
from models.monster import Monster
from models.skill import Skill
from models.skilldetail import SkillDetail
from models.skilleffect import SkillEffect
from models.map import Map, Land
from models.teamflag import TeamFlag
# from test_hero_data import origin_hero_data
# from test_map_data import origin_map_data
# from test_monster_data import origin_monster_data


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
        return {"map": self.build_map(src_json_data.get("map")), 
                "hero": heros,
                "monster": monsters
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
                skill_detail = SkillDetail(**skill)
                for each_skill_effect in skill.get("effects"):
                    skill_effect = SkillEffect(**each_skill_effect)
                    skill_detail.effects_add(skill_effect)
                skills.append(skill_detail)
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

        
if __name__ == "__main__":
    state = BuildPatrol("data.json").load_data()
    state["maps"] = state["map"]
    # print(len(state.get("monster")))
    # hero = state.get("hero")[0] #
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

    #hero = state.get("hero")[1]
    hero = state.get("hero")[1]
    monster = state.get("monster")[-1]
    # hero2.set_AvailableSkills([82])
    print(hero.skills)

    skill = monster.get_skill_by_id(77)
   
    hero.move_position(3,1,4, state=state)
    monster.move_position(3,1,3, state=state)
    print("use skill_82 test:", skill)
    print( monster.func_attack(enemys=[hero], 
                        skill=skill, 
                        attack_point=hero.position, 
                        state=state))

    


    
