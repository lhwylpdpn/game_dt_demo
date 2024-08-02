import random
#准备一个计算伤害的函数，传入释动的对象，受动动对象，返回伤害值
def damage(attacker,defender,skill):

    #####-------------------------------------------------------------------
    #####这里负责取值，不负责计算

    #英雄的属性
    attacker_HP=attacker.Hp
    attacker_PhysicalAtk=attacker.Atk #todo 这个再看取什么
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

    attacker_skill_coefficient = 1.5   #todo 这里要根据不同技能增加
    attacker_Def=attacker_PhysicalDef # 防御值
    if True: #todo 这里需要知道技能的是物理伤害还是魔法伤害，当前判断假设是魔法伤害
        attacker_Def=defender_MagicalDef
    defender_Def=defender_PhysicalDef
    if True: #todo 这里需要知道技能的是物理伤害还是魔法伤害，当前判断假设是魔法伤害
        defender_Def=defender_MagicalDef

    attacker_ATK=attacker_PhysicalAtk#攻击值 #todo 这里要根据不同技能增加
    defender_ATK=defender_PhysicalAtk#攻击值 #todo 这里要根据不同技能增加

    #被动防御加成
    if True: #todo 这里要根据不同技能增加
        attacker_passiveDefenseBonus=(1+0.25*random.choices([0,1],[0.75,0.25])[0])
    if True: #todo 这里要根据不同技能增加
        defender_passiveDefenseBonus=(1+0.25*random.choices([0,1],[0.75,0.25])[0])

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
    #暴击系数
    attacker_critBase=attacker_Luck**0.5*2-defender_Luck**0.5*0.5+attacker_critBase_bonus
    attacker_critBase+=304 #todo 分技能算技能带来的变化数字
    #暴击
    #伤害控制系数
    damageControlCoefficient=1 #todo 分技能
    #护盾伤害减免
    shieldDamageReduction=0 #todo 分技能


    #####-------------------------------------------------------------------

    #####-------------------------------------------------------------------
    ##这里负责封装三阶变量
    basedamage=attacker_ATK*attacker_skill_coefficient
    level2damage=(basedamage*(1+attacker_Atk_bonusCoefficient)-defender_Def)*defender_DefenseCoefficient*attacker_critBase
    damage=level2damage*damageControlCoefficient-shieldDamageReduction



    #####-------------------------------------------------------------------


    #####-------------------------------------------------------------------
    #这里单独算回避率
    #回避率
    attacker_hitratebonus=0.05#todo 根据技能调整
    defender_avoidancebonus=0.05#todo 根据技能调整
    avoidance=4+(defender_Velocity-attacker_Agile)*0.5*12+(defender_level-attacker_level)**0.5+defender_avoidancebonus-attacker_hitratebonus
    #最终伤害
    #回避率高于100%则是100%
    avoidance=100 if avoidance>100 else avoidance
    miss=random.choices([0,1],[1-avoidance/100,avoidance/100])[0] #0 回避失败，所以命中 1 回避成功，所以没命中
    if miss==1:
        damage=0
    res={'damage':damage,'miss':miss}
    return res

if __name__ == '__main__':
    #damage(hero,monster)

    #产生一个30% 概率 出现0.3 ,70%出现0 的随机数
    print(random.choices([0,1],[0.7,0.3])[0])
