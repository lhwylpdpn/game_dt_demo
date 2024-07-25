# -*- coding:utf-8 -*-
"""
@author HU
@date 20245-07-23
"""
from pprint import pprint
from models.hero import Hero
from models.skill import Skill
from models.skilldetail import SkillDetail
from models.skilleffect import SkillEffect
from models.map import Map, Land
from test_hero_data import origin_hero_data
from test_map_data import origin_map_data


class BuildPatrol():
    
    @staticmethod
    def build_heros(origin_hero_data):  # 返回英雄的对象
        heros = []
        for each in origin_hero_data:
            _hero = Hero(**each)
            for i in range(len(each.get("skills"))):
                each_skill_data = each.get("skills")[i]
                skill_detail = SkillDetail(**each_skill_data)
                for each_skill_effect in each_skill_data.get("effects"):
                    skill_effect =SkillEffect(**each_skill_effect)
                    skill_detail.effects_add(skill_effect)
                getattr(_hero, f"set_skid{i}")(skill_detail)
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
    def build_monster(): # 返回monster的对象
        return

        
if __name__ == "__main__":
    #map = BuildPatrol.build_map(origin_map_data)    # map
    heros = BuildPatrol.build_heros(origin_hero_data)  # heros
    #monsters = BuildPatrol.build_monster()# monster 
    