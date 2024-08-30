#一个策略模版


#生成一个固定对参数字典,然后每个英雄都用这个字典产生一个参数字典
#再网上都是针对这个字典的模版封装
#最终每个英雄和怪物都有一个字典，作为英雄的属性初始化进去
aciton_strategy = {}

####选择攻击对象的策略================================================================================================
aciton_strategy["atk_target"] = {}
####优先攻击最近的敌人
aciton_strategy["atk_target"]["nearest"] = {'score': [0,1], 'desc': '优先攻击最近的敌人', 'weight': 0.2, 'clac_type': 'normalized'}
####优先攻击百分比血量最少的敌人
aciton_strategy["atk_target"]["min_hp"] = {'score': [0,1], 'desc': '优先攻击百分比血量最少的敌人', 'weight': 0.2, 'clac_type': 'normalized'}
####优先攻击攻击力最高的敌人
aciton_strategy["atk_target"]["max_atk"] = {'score': [0,1], 'desc': '优先攻击攻击力最高的敌人', 'weight': 0.2, 'clac_type': 'normalized'}
####优先攻击防御力最低的敌人
aciton_strategy["atk_target"]["min_def"] = {'score': [0,1], 'desc': '优先攻击防御力最低的敌人', 'weight': 0.2, 'clac_type': 'normalized'}
####优先攻击支援型职业
aciton_strategy["atk_target"]["career_support"] = {'score': [0,1], 'desc': '优先攻击支援型职业', 'weight': 0.2, 'clac_type': 'exclusive'}
####优先攻击攻击型职业
aciton_strategy["atk_target"]["career_attack"] = {'score': [0,1], 'desc': '优先攻击攻击型职业', 'weight': 0.2, 'clac_type': 'exclusive'}
####优先攻击防御型职业
aciton_strategy["atk_target"]["career_defense"] = {'score': [0,1], 'desc': '优先攻击防御型职业', 'weight': 0.2, 'clac_type': 'exclusive'}
####优先攻击非精英单位
aciton_strategy["atk_target"]["non_elite"] = {'score': [0,1], 'desc': '优先攻击非精英单位', 'weight': 0.2, 'clac_type': 'exclusive'}
####优先攻击精英单位
aciton_strategy["atk_target"]["elite"] = {'score': [0,1], 'desc': '优先攻击精英单位', 'weight': 0.2, 'clac_type': 'exclusive'}
####尽量不攻击敌人
aciton_strategy["atk_target"]["no_atk"] = {'score': [0,float('-inf')], 'desc': '尽量不攻击敌人', 'weight': 0.2, 'clac_type': 'normalized'}
###避免在非战斗状态下攻击敌人
aciton_strategy["atk_target"]["no_combat_no_atk"] = {'score': [0,float('-inf')], 'desc': '避免在非战斗状态下攻击敌人', 'weight': 0.2, 'clac_type': 'normalized'}



def test():

if __name__ == '__main__':
    test()
