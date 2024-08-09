# -*- coding:utf-8 -*-
"""
@author HU
@date 20245-07-23
"""
from pprint import pprint
from models.hero import Hero
from models.monster import Monster
from models.skill import Skill
from models.skilldetail import SkillDetail
from models.skilleffect import SkillEffect
from models.map import Map, Land
from test_hero_data import origin_hero_data
from test_map_data import origin_map_data
from test_monster_data import origin_monster_data


class BuildPatrol():
    
    @staticmethod
    def build_heros(origin_hero_data):  # 返回英雄的对象
        heros = []
        for each in origin_hero_data:
            _hero = Hero(**each)
            skills = []
            for skill in each.get("skills"):
                skill_detail = SkillDetail(**skill)
                for each_skill_effect in skill.get("effects"):
                    skill_effect = SkillEffect(**each_skill_effect)
                    skill_detail.effects_add(skill_effect)
                skills.append(skill_detail)
            _hero.set_skills(skills)
            _hero.load_init_unActiveSkill()
            heros.append(_hero)
        return heros

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
    def build_monster(origin_monster_data): # 返回monster的对象
        monsters = []
        for each in origin_monster_data:
            monster = Monster(**each)
            skills = []
            for skill in each.get("skills"):
                skill_detail = SkillDetail(**skill)
                for each_skill_effect in skill.get("effects"):
                    skill_effect = SkillEffect(**each_skill_effect)
                    skill_detail.effects_add(skill_effect)
                skills.append(skill_detail)
            monster.set_skills(skills)
            monster.load_init_unActiveSkill()
            monsters.append(monster)
        return monsters

        
if __name__ == "__main__":
    map = BuildPatrol.build_map(origin_map_data)    # map
    heros = BuildPatrol.build_heros(origin_hero_data)  # heros
    monster = BuildPatrol.build_monster(origin_monster_data)# monster 
    each_back_skill = heros[0].get_back_skills(monster[0], SkillDetail(**{"DefaultSkills":1}))
    print(each_back_skill)
    if each_back_skill:
        state = {"hero": heros, "monster":monster, "maps": map}
        heros[0].func_attack(enemys=[monster[0]], skill=each_back_skill[0], attack_point=monster[0].position, state=state, is_back_atk=True)
    #map.list_land_postion()
    #map.set_land_pass(8,1,5)
    #print(heros[0].dict())
    #heros[0].move_position(8,1,5,map)
    #print(heros[1].dict())
    #print(heros[1].is_death)
    #print(heros[1].is_alive)
    #print(monster[0].dict())
    #print(monster[1].dict())
    #print(map.dict())
    #print(map.view_from_z_dict())
    #print(map.get_land_from_xy(8,1))
    