import random
#准备一个计算伤害的函数，传入释动的对象，受动动对象，返回伤害值
def damage(attacker,defender,skill):

    if attacker.__class__.__name__.lower()=='hero':
        #英雄的属性
        attacker_HP=attacker.HP
        attacker_Atk=attacker.Atk
        attacker_Def=defender.Def
        attacker_Velocity=attacker.Velocity
        attacker_skill_coefficient=skill.coefficient
        attacker_x=attacker.x
        attacker_y=attacker.y
        attacker_z=attacker.z
        attacker_critBase=attacker.critBase
    if defender.__class__.__name__.lower()=='Monster':

        #对手的属性
        defender_HP=defender.HP
        defender_Atk=defender.Atk
        defender_Def=defender.Def
        defender_Velocity=defender.Velocity
        defender_x=defender.x
        defender_y=defender.y
        defender_z=defender.z

    #防御值二次计算

    attacker_Def=attacker_Def*(3)

    #计算加成系数
    if attacker_z>defender_z:
        attacker_Atk=attacker_Atk*(1+0.05)
        defender_Def=defender_Def*(1-0.05)
        attacker_critBase=attacker_critBase*(1+0.05)
    if attacker_z<defender_z:
        attacker_Atk=attacker_Atk*(1-0.05)
        defender_Def=defender_Def*(1+0.05)
        attacker_critBase=attacker_critBase*(1-0.05)



    damage=0
    #计算伤害
    #(((攻击值 x 技能系数) x 加成系数 - 防御值) x 防御系数 x 暴击系数 ) x 伤害控制系数 - 护盾伤害减免)
    damage=attacker_Atk*attacker_skill_coefficient
    return damage

if __name__ == '__main__':
    #damage(hero,monster)

    #产生一个30% 概率 出现0.3 ,70%出现0 的随机数
    print(random.choices([0,1],[0.7,0.3]))