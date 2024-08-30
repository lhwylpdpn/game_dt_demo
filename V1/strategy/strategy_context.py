#一个策略模版


#生成一个固定对参数字典,然后每个英雄都用这个字典产生一个参数字典
#再网上都是针对这个字典的模版封装
#最终每个英雄和怪物都有一个字典，作为英雄的属性初始化进去


#####
#score: 归一化后的范围
#normalized: 归一化的方法，根据当前state的情况里的数据进行归一化
#exclusive: 互斥的方法，根据当前state的情况里符合条件的为score[1]，不符合条件的为score[0]

#得到分数后*权重，然后根据权重排序，得到最终的结果
#####

aciton_strategy = {}
selection_strategy = {}
####选择逃跑策略================================================================================================
selection_strategy["escape"] = {}
selection_strategy["escape"]["is_health_below_threshold"]={'weight': 0.4} #0.4代表40%

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
aciton_strategy["atk_target"]["no_atk"] = {'score': [0,float('-inf')], 'desc': '尽量不攻击敌人', 'weight': 0.2, 'clac_type': 'exclusive'}
###避免在非战斗状态下攻击敌人
aciton_strategy["atk_target"]["no_combat_no_atk"] = {'score': [0,float('-inf')], 'desc': '避免在非战斗状态下攻击敌人', 'weight': 0.2, 'clac_type': 'exclusive'}

###选择攻击方式的策略================================================================================================
aciton_strategy["atk_type"] = {}
####优先使用技能攻击
aciton_strategy["atk_type"]["skill"] = {'score': [0,1], 'desc': '优先使用技能攻击', 'weight': 0.2, 'clac_type': 'normalized'}
####优先使用普通攻击
aciton_strategy["atk_type"]["normal"] = {'score': [0,1], 'desc': '优先使用普通攻击', 'weight': 0.2, 'clac_type': 'normalized'}
####优先对攻击力最高的敌人使用单体攻击技能
aciton_strategy["atk_type"]["single_max_atk"] = {'score': [0,1], 'desc': '优先对攻击力最高的敌人使用单体攻击技能', 'weight': 0.2, 'clac_type': 'exclusive'}
####优先对防御力最高的敌人使用单体攻击技能
aciton_strategy["atk_type"]["single_max_def"] = {'score': [0,1], 'desc': '优先对防御力最高的敌人使用单体攻击技能', 'weight': 0.2, 'clac_type': 'exclusive'}
####优先对支援型职业使用单体攻击技能
aciton_strategy["atk_type"]["single_career_support"] = {'score': [0,1], 'desc': '优先对支援型职业使用单体攻击技能', 'weight': 0.2, 'clac_type': 'exclusive'}
####优先对攻击型职业使用单体攻击技能
aciton_strategy["atk_type"]["single_career_attack"] = {'score': [0,1], 'desc': '优先对攻击型职业使用单体攻击技能', 'weight': 0.2, 'clac_type': 'exclusive'}
####优先对防御型职业使用单体攻击技能
aciton_strategy["atk_type"]["single_career_defense"] = {'score': [0,1], 'desc': '优先对防御型职业使用单体攻击技能', 'weight': 0.2, 'clac_type': 'exclusive'}

####选择移动位置策略================================================================================================
aciton_strategy["move_position"] = {}
####优先移动到普通攻击可以攻击到更多敌人的位置
#攻击到人越多，分数越高
aciton_strategy["move_position"]["atk_multi"] = {'score': [0,1], 'desc': '优先移动到普通攻击可以攻击到复数敌人的位置', 'weight': 0.2, 'clac_type': 'normalized'}
####优先移动到不会被更多敌人攻击的位置
#被攻击到人越少，分数越高
aciton_strategy["move_position"]["no_atk"] = {'score': [0,1], 'desc': '优先移动到不会被更多敌人攻击的位置', 'weight': 0.2, 'clac_type': 'normalized'}
####优先占领制高点，目标地点-当前地点的高度差越大，分数越高
aciton_strategy["move_position"]["high"] = {'score': [0,1], 'desc': '优先占领制高点', 'weight': 0.2, 'clac_type': 'normalized'}
####选择移动路径策略================================================================================================
aciton_strategy["move_path"] = {}
####优先最短路线
aciton_strategy["move_path"]["shortest"] = {'score': [0,1], 'desc': '优先最短路线', 'weight': 0.2, 'clac_type': 'normalized'}
####优先不进入敌人的警戒范围
###进入敌人警戒范围的点越多，分值越低
aciton_strategy["move_path"]["no_warning"] = {'score': [0,1], 'desc': '优先不进入敌人的警戒范围', 'weight': 0.2, 'clac_type': 'normalized'}
####选择辅助策略================================================================================================
aciton_strategy["assist"] = {}
####优先使用单体治疗技能
aciton_strategy["assist"]["single_heal"] = {'score': [0,1], 'desc': '优先使用单体治疗技能', 'weight': 0.2, 'clac_type': 'normalized'}
####优先使用群体治疗技能
aciton_strategy["assist"]["group_heal"] = {'score': [0,1], 'desc': '优先使用群体治疗技能', 'weight': 0.2, 'clac_type': 'normalized'}
####优先使用持续治疗技能
aciton_strategy["assist"]["sustain_heal"] = {'score': [0,1], 'desc': '优先使用持续治疗技能', 'weight': 0.2, 'clac_type': 'normalized'}
####优先针对防守型职业使用治疗技能
aciton_strategy["assist"]["career_defense"] = {'score': [0,1], 'desc': '优先针对防守型职业使用治疗技能', 'weight': 0.2, 'clac_type': 'exclusive'}
####优先针对攻击型职业使用治疗技能
aciton_strategy["assist"]["career_attack"] = {'score': [0,1], 'desc': '优先针对攻击型职业使用治疗技能', 'weight': 0.2, 'clac_type': 'exclusive'}
####优先针对自己加血
aciton_strategy["assist"]["self_heal"] = {'score': [0,1], 'desc': '优先针对自己加血', 'weight': 0.2, 'clac_type': 'exclusive'}

def test():
    print(aciton_strategy)
    print(selection_strategy)

if __name__ == '__main__':
    test()
