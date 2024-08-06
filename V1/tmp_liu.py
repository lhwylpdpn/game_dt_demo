from buildpatrol import BuildPatrol
from utils.damage import damage
from test_hero_data import origin_hero_data  # 后续通过api获取前端传递的数据
from test_monster_data import origin_monster_data  # 后续通过api获取前端传递的数据
#
# demo_skill['劈砍'] = 201
# demo_skill['战士普攻'] = 200
# demo_skill['弓箭手普攻'] = 300
# demo_skill['穿杨'] = 301
# demo_skill['上前一步'] = 302
if __name__ == '__main__':
    heros = BuildPatrol.build_heros(origin_hero_data)  # heros
    monsters = BuildPatrol.build_monster(origin_monster_data)
    for  h  in heros:
        for s in h.skills:
            print('技能',s.SkillId,damage(h, monsters[0], s))