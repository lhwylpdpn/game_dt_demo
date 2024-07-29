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
                # getattr(_hero, f"set_skid{i}")(skill_detail)
            # pprint(_hero.dict_short())
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
        monster = Monster(**origin_monster_data)
        skills = []
        for skill in origin_monster_data.get("skills"):
            skill_detail = SkillDetail(**skill)
            for each_skill_effect in skill.get("effects"):
                skill_effect = SkillEffect(**each_skill_effect)
                skill_detail.effects_add(skill_effect)
            skills.append(skill_detail)
        monster.set_skills(skills)
        return [monster,]

        
if __name__ == "__main__":
    #map = BuildPatrol.build_map(origin_map_data)    # map
    heros = BuildPatrol.build_heros(origin_hero_data)  # heros
    monster = BuildPatrol.build_monster(origin_monster_data)# monster 
    #map.list_land_postion()
    print(heros[1].dict_short())
    #print(monster[0].dict_short())