from utils.tools import random_choices
import random
#准备一个计算伤害的函数，传入释动的对象，受动动对象，返回伤害值
def damage(attacker,defender,skill):



    demo_skill={}
    demo_skill['劈砍'] = 78
    demo_skill['战士普攻'] = 77
    demo_skill['弓箭手普攻'] = 86
    demo_skill['穿杨'] = 87
    demo_skill['上前一步'] = 88
    demo_skill['集中'] = 92
    demo_skill['反击斩']=81
    demo_skill['箭雨']=89

    if skill.SkillId == demo_skill['反击斩']:
        res=random_choices({0:0.5,1:0.5}) #0 反击生效  1 反击不生效
        if res==1:
            return {'damage':0,'miss':0}
    #####-------------------------------------------------------------------
    #####这里负责取值，不负责计算




    #英雄的属性
    attacker_HP=attacker.Hp
    attacker_PhysicalAtk=attacker.Atk
    attacker_PhysicalDef=defender.Def
    attacker_Velocity=attacker.Velocity
    attacker_x=attacker.x
    attacker_y=attacker.y
    attacker_z=attacker.z
    attacker_MagicalDef=attacker.MagicalDef
    attacker_MagicalAtk=attacker.MagicalAtk
    attacker_Luck=attacker.Luck
    attacker_Agile=attacker.Agile
    attacker_level=1
    attacker_hitrate=100

    attacker_hitrate=attacker.BUFF_HIT_RATE #



    #对手的属性
    defender_HP=defender.Hp
    defender_PhysicalAtk=defender.Atk
    defender_PhysicalDef=defender.Def
    defender_Velocity=defender.Velocity
    defender_x=defender.x
    defender_y=defender.y
    defender_z=defender.z
    defender_MagicalDef=defender.MagicalDef
    defender_MagicalAtk=defender.MagicalAtk
    defender_Luck=defender.Luck
    defender_Agile=defender.Agile
    defender_level=1
    #####-------------------------------------------------------------------



    #####-------------------------------------------------------------------
    ##这里负责封装二阶的变量

    attacker_skill_coefficient = 1  #技能伤害系数
    if skill.SkillId==demo_skill['战士普攻']:
        attacker_skill_coefficient=float(skill.get_effect_by_key('ATK').param[1])/100 # 100%物理伤害
    if skill.SkillId==demo_skill['劈砍']:
        attacker_skill_coefficient=float(skill.get_effect_by_key('ATK').param[1])/100 # 85%物理伤害
    if skill.SkillId==demo_skill['弓箭手普攻']:
        attacker_skill_coefficient=float(skill.get_effect_by_key('ATK_FORMULA_1').param[1])/100 #65%(物理+敏捷)的物理伤害
    if skill.SkillId==demo_skill['穿杨']:
        attacker_skill_coefficient=float(skill.get_effect_by_key('ATK').param[1])/100 #对范围内的敌人造成150%普攻的物理伤害
    if skill.SkillId==demo_skill['上前一步']:
        attacker_skill_coefficient=float(skill.get_effect_by_key('ATK').param[1])/100  #给指定范围内的目标以50%的伤害
    if skill.SkillId==demo_skill['箭雨']:
        attacker_skill_coefficient=float(skill.get_effect_by_key('ATK').param[1])/100 # 130%物理伤害
    if skill.SkillId==demo_skill['反击斩']:
        attacker_skill_coefficient=float(skill.get_effect_by_key('ATK_BACK').param[1])/100 # 100%物理伤害
    attacker_Def=attacker_PhysicalDef # 防御值
    if False: #todo 这里需要知道技能的是物理伤害还是魔法伤害，当前判断假设是物理伤害都
        attacker_Def=defender_MagicalDef
    defender_Def=defender_PhysicalDef
    if False: #todo 这里需要知道技能的是物理伤害还是魔法伤害，当前判断假设是物理伤害都
        defender_Def=defender_MagicalDef

    attacker_ATK=attacker_PhysicalAtk#攻击值  这里要根据不同技能增加
    if skill.SkillId==demo_skill['弓箭手普攻']:
        attacker_ATK=(attacker_PhysicalAtk+attacker_Agile)

    #被动防御加成
    if True: #这里不做任何处理了,因为技能的被动防御变化是从面板获得了，也就是技能传到这里的时候已经是最终的数值了
        defender_passiveDefenseBonus=0


    defender_Def_position_bonus=0
    attacker_ATK_position_bonus=0
    #位置加成
    if attacker_z>defender_z:
        attacker_ATK_position_bonus=0.05
        defender_Def_position_bonus=-0.05
    if attacker_z<defender_z:
        attacker_ATK_position_bonus=-0.05
        defender_Def_position_bonus=0.05
    defender_Def=defender_Def*(1+defender_passiveDefenseBonus)*(1+defender_Def_position_bonus)


    #攻击加成系数
    attacker_Atk_bonusCoefficient=0
    defender_ATK_bonusCoefficient=0
    if attacker_z>defender_z:
        attacker_Atk_bonusCoefficient=0.05
        defender_ATK_bonusCoefficient=-0.05
    if attacker_z<defender_z:
        attacker_Atk_bonusCoefficient=-0.05
        defender_ATK_bonusCoefficient=0.05
    #防御系数
    attacker_DefenseCoefficient=1
    defender_DefenseCoefficient=1

    attacker_critBase_bonus=0.05 if attacker_y>defender_y else -0.05
    #暴击率
    #attacker_critBase=attacker_Luck**0.5*2-defender_Luck**0.5*0.5+attacker_critBase_bonus
    if skill.get_effect_by_key('TAG_CRIT') is None:
        attacker_critBase=0 # 没有暴击效果的技能 暴击加成等于0 ，最终计算伤害的时候维持*100%
    else:
        attacker_critBase = 0.25 + attacker_critBase_bonus
        #随机一个0.1到0.5的加成,也就按暴击率计算一个要不0加成要不随机10%到50%的加成
        attacker_critBase=random_choices({0:1-attacker_critBase,random.randint(10,50)/100:attacker_critBase}) #0 未暴击 1 暴击
    #伤害控制系数
    damageControlCoefficient=1 #todo 分技能,暂时没有
    #护盾伤害减免
    shieldDamageReduction=0 #todo 分技能,暂时没有


    #####-------------------------------------------------------------------

    #####-------------------------------------------------------------------
    ##这里负责封装三阶变量
    basedamage=attacker_ATK*attacker_skill_coefficient
    print('basedamage',basedamage)

    level2damage=(basedamage*(1+attacker_Atk_bonusCoefficient)-defender_Def)*defender_DefenseCoefficient*(1+attacker_critBase)
    if skill.SkillId == demo_skill['反击斩']:
        print('反2击','basedamage',basedamage,'attacker_Atk_bonusCoefficient',attacker_Atk_bonusCoefficient,'defender_Def',defender_Def,'defender_DefenseCoefficient',defender_DefenseCoefficient,'attacker_critBase',attacker_critBase)
    print('中途输出', 'basedamage', basedamage, 'attacker_Atk_bonusCoefficient', attacker_Atk_bonusCoefficient,
          'defender_Def', defender_Def, 'defender_DefenseCoefficient', defender_DefenseCoefficient, 'attacker_critBase',
          attacker_critBase)

    print('level2damage',level2damage)
    #print('level2damage',level2damage)
    damage=level2damage*damageControlCoefficient-shieldDamageReduction
    damage=round(damage,2)
    print('damage',damage)


    #####-------------------------------------------------------------------


    #####-------------------------------------------------------------------
    #这里单独算回避率
    #回避率
    attacker_hitratebonus=0#todo 根据技能调整
    if attacker_hitrate is not None:
        attacker_hitratebonus+=attacker_hitrate

    defender_avoidancebonus=0#todo 根据技能调整
    #avoidance=4+(defender_Velocity-attacker_Agile)*0.5*12+(defender_level-attacker_level)**0.5+defender_avoidancebonus-attacker_hitratebonus
    avoidance=0.1+defender_avoidancebonus-attacker_hitratebonus #2024-08-07 修改
    #最终伤害
    #回避率高于100%则是100%

    avoidance=100 if avoidance>100 else avoidance
    avoidance=0 if avoidance<0 else avoidance
    miss=random_choices({0:1-avoidance/100,1:avoidance/100}) #0 回避失败，所以命中 1 回避成功，所以没命中


    if skill.get_effect_by_key('TAG_HIT') is not None: # 有必中效果的技能,miss=0 #
        miss=0

    if damage<0: #伤害小于0，伤害为0
        damage=0

    if miss==1:
        damage=0
    print('miss',miss)
    res={'damage':damage,'miss':miss}
    return res

if __name__ == '__main__':

    #产生一个30% 概率 出现0.3 ,70%出现0 的随机数
    print(random_choices({0:0.5,1:0.5}))

