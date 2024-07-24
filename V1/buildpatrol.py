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



def build_hero(origin_hero_data):
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
        heros.append(_hero)
    return heros


def build_map(origin_map_data):
    map = Map(*Map.find_map_size(origin_map_data))
    
        
if __name__ == "__main__":
    # heros = build_hero(origin_hero_data)
    # for each_h in heros:
    #     pprint(each_h.dict())
    build_map(origin_map_data)