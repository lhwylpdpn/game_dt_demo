import copy
from utils.config import bass_class
#生成一个固定对参数字典,然后每个英雄都用这个字典产生一个参数字典
#再网上都是针对这个字典的模版封装
#最终每个英雄和怪物都有一个字典，作为英雄的属性初始化进去
#####
#score: 归一化后的范围
#normalized: 归一化的方法，根据当前state的情况里的数据进行归一化
#exclusive: 互斥的方法，根据当前state的情况里符合条件的为score[1]，不符合条件的为score[0]

#得到分数后*权重，然后根据权重数加和，得到最终的结果
#action_strategy: 选择行动策略用于函数内
#selection_strategy: 选择tree上的判断策略 用于tree上
#####
class strategy_params:
    def __init__(self):

        self.base_class = bass_class
        self.action_strategy = {}
        self.selection_strategy = {}
        ####选择逃跑策略================================================================================================
        self.selection_strategy["escape"] = {}
        self.selection_strategy["escape"]["is_health_below_threshold"]={'weight': 0.4} #0.4代表40%

        ####选择攻击对象的策略================================================================================================
        self.action_strategy["atk_target"] = {}
        ####优先攻击最近的敌人
        self.action_strategy["atk_target"]["nearest"] = {'score': [0,1], 'desc': '优先攻击最近的敌人', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先攻击百分比血量最少的敌人
        self.action_strategy["atk_target"]["min_hp"] = {'score': [0,1], 'desc': '优先攻击百分比血量最少的敌人', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先攻击攻击力最高的敌人
        self.action_strategy["atk_target"]["max_atk"] = {'score': [0,1], 'desc': '优先攻击攻击力最高的敌人', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先攻击防御力最低的敌人
        self.action_strategy["atk_target"]["min_def"] = {'score': [0,1], 'desc': '优先攻击防御力最低的敌人', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先攻击支援型职业
        self.action_strategy["atk_target"]["career_support"] = {'score': [0,1], 'desc': '优先攻击支援型职业', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先攻击攻击型职业
        self.action_strategy["atk_target"]["career_attack"] = {'score': [0,1], 'desc': '优先攻击攻击型职业', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先攻击防御型职业
        self.action_strategy["atk_target"]["career_defense"] = {'score': [0,1], 'desc': '优先攻击防御型职业', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先攻击非精英单位
        self.action_strategy["atk_target"]["non_elite"] = {'score': [0,1], 'desc': '优先攻击非精英单位', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先攻击精英单位
        self.action_strategy["atk_target"]["elite"] = {'score': [0,1], 'desc': '优先攻击精英单位', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####尽量不攻击敌人
        self.action_strategy["atk_target"]["no_atk"] = {'score': [0,float('-inf')], 'desc': '尽量不攻击敌人', 'weight': 0.2, 'clac_type': 'exclusive'}
        ###避免在非战斗状态下攻击敌人
        self.action_strategy["atk_target"]["no_combat_no_atk"] = {'score': [0,float('-inf')], 'desc': '避免在非战斗状态下攻击敌人', 'weight': 0.2, 'clac_type': 'exclusive'}

        ###选择攻击方式的策略================================================================================================
        self.action_strategy["atk_type"] = {}
        ####优先使用技能攻击
        self.action_strategy["atk_type"]["skill"] = {'score': [0,1], 'desc': '优先使用技能攻击', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先使用普通攻击
        self.action_strategy["atk_type"]["normal"] = {'score': [0,1], 'desc': '优先使用普通攻击', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先对攻击力最高的敌人使用单体攻击技能
        self.action_strategy["atk_type"]["single_max_atk"] = {'score': [0,1], 'desc': '优先对攻击力最高的敌人使用单体攻击技能', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先对防御力最高的敌人使用单体攻击技能
        self.action_strategy["atk_type"]["single_max_def"] = {'score': [0,1], 'desc': '优先对防御力最高的敌人使用单体攻击技能', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先对支援型职业使用单体攻击技能
        self.action_strategy["atk_type"]["single_career_support"] = {'score': [0,1], 'desc': '优先对支援型职业使用单体攻击技能', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先对攻击型职业使用单体攻击技能
        self.action_strategy["atk_type"]["single_career_attack"] = {'score': [0,1], 'desc': '优先对攻击型职业使用单体攻击技能', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先对防御型职业使用单体攻击技能
        self.action_strategy["atk_type"]["single_career_defense"] = {'score': [0,1], 'desc': '优先对防御型职业使用单体攻击技能', 'weight': 0.2, 'clac_type': 'exclusive'}

        ####选择移动位置策略================================================================================================
        self.action_strategy["move_position"] = {}
        ####优先移动到普通攻击可以攻击到更多敌人的位置
        #攻击到人越多，分数越高
        self.action_strategy["move_position"]["atk_multi"] = {'score': [0,1], 'desc': '优先移动到普通攻击可以攻击到复数敌人的位置', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先移动到不会被更多敌人攻击的位置
        #被攻击到人越少，分数越高
        self.action_strategy["move_position"]["no_atk"] = {'score': [0,1], 'desc': '优先移动到不会被更多敌人攻击的位置', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先占领制高点，目标地点-当前地点的高度差越大，分数越高
        self.action_strategy["move_position"]["high"] = {'score': [0,1], 'desc': '优先占领制高点', 'weight': 0.2, 'clac_type': 'normalized'}
        ####选择移动路径策略================================================================================================
        self.action_strategy["move_path"] = {}
        ####优先最短路线
        self.action_strategy["move_path"]["shortest"] = {'score': [0,1], 'desc': '优先最短路线', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先不进入敌人的警戒范围
        ###进入敌人警戒范围的点越多，分值越低
        self.action_strategy["move_path"]["no_warning"] = {'score': [0,1], 'desc': '优先不进入敌人的警戒范围', 'weight': 0.2, 'clac_type': 'normalized'}
        ####选择辅助策略================================================================================================
        self.action_strategy["assist"] = {}
        ####优先使用单体治疗技能
        self.action_strategy["assist"]["single_heal"] = {'score': [0,1], 'desc': '优先使用单体治疗技能', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先使用群体治疗技能
        self.action_strategy["assist"]["group_heal"] = {'score': [0,1], 'desc': '优先使用群体治疗技能', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先使用持续治疗技能
        self.action_strategy["assist"]["sustain_heal"] = {'score': [0,1], 'desc': '优先使用持续治疗技能', 'weight': 0.2, 'clac_type': 'normalized'}
        ####优先针对防守型职业使用治疗技能
        self.action_strategy["assist"]["career_defense"] = {'score': [0,1], 'desc': '优先针对防守型职业使用治疗技能', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先针对攻击型职业使用治疗技能
        self.action_strategy["assist"]["career_attack"] = {'score': [0,1], 'desc': '优先针对攻击型职业使用治疗技能', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先针对自己加血
        self.action_strategy["assist"]["self_heal"] = {'score': [0,1], 'desc': '优先针对自己加血', 'weight': 0.2, 'clac_type': 'exclusive'}

    def get_strategy_params(self,base_class_value:int):

        real_action_strategy  =copy.deepcopy(self.action_strategy)
        real_selection_strategy = copy.deepcopy(self.selection_strategy)
        #print('real_action_strategy',real_action_strategy)
        #print('real_selection_strategy',real_selection_strategy)
        if base_class_value==1:#战士
            real_selection_strategy["escape"]["is_health_below_threshold"]['weight'] = 0.4
            real_action_strategy["atk_target"]["nearest"]['weight'] = 0.2
            real_action_strategy["atk_target"]["min_hp"]['weight'] = 0.2
            real_action_strategy["atk_target"]["max_atk"]['weight'] = 0.2
            real_action_strategy["atk_target"]["min_def"]['weight'] = 0.2
            real_action_strategy["atk_target"]["career_support"]['weight'] = 0.2
            real_action_strategy["atk_target"]["career_attack"]['weight'] = 0.2
            real_action_strategy["atk_target"]["career_defense"]['weight'] = 0.2
            real_action_strategy["atk_target"]["non_elite"]['weight'] = 0.2
            real_action_strategy["atk_target"]["elite"]['weight'] = 0.2
            real_action_strategy["atk_target"]["no_atk"]['weight'] = 0.2
            real_action_strategy["atk_target"]["no_combat_no_atk"]['weight'] = 0.2
            real_action_strategy["atk_type"]["skill"]['weight'] = 0.2
            real_action_strategy["atk_type"]["normal"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_max_atk"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_max_def"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_career_support"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_career_attack"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_career_defense"]['weight'] = 0.2
            real_action_strategy["move_position"]["atk_multi"]['weight'] = 0.2
            real_action_strategy["move_position"]["no_atk"]['weight'] = 0.2
            real_action_strategy["move_position"]["high"]['weight'] = 0.2
            real_action_strategy["move_path"]["shortest"]['weight'] = 0.2
            real_action_strategy["move_path"]["no_warning"]['weight'] = 0.2
            real_action_strategy["assist"]["single_heal"]['weight'] = 0.2
            real_action_strategy["assist"]["group_heal"]['weight'] = 0.2
            real_action_strategy["assist"]["sustain_heal"]['weight'] = 0.2
            real_action_strategy["assist"]["career_defense"]['weight'] = 0.2
            real_action_strategy["assist"]["career_attack"]['weight'] = 0.2
            real_action_strategy["assist"]["self_heal"]['weight'] = 0.2
        elif base_class_value == 2:#弓箭手
            real_selection_strategy["escape"]["is_health_below_threshold"]['weight'] = 0.4
            real_action_strategy["atk_target"]["nearest"]['weight'] = 0.2
            real_action_strategy["atk_target"]["min_hp"]['weight'] = 0.2
            real_action_strategy["atk_target"]["max_atk"]['weight'] = 0.2
            real_action_strategy["atk_target"]["min_def"]['weight'] = 0.2
            real_action_strategy["atk_target"]["career_support"]['weight'] = 0.2
            real_action_strategy["atk_target"]["career_attack"]['weight'] = 0.2
            real_action_strategy["atk_target"]["career_defense"]['weight'] = 0.2
            real_action_strategy["atk_target"]["non_elite"]['weight'] = 0.2
            real_action_strategy["atk_target"]["elite"]['weight'] = 0.2
            real_action_strategy["atk_target"]["no_atk"]['weight'] = 0.2
            real_action_strategy["atk_target"]["no_combat_no_atk"]['weight'] = 0.2
            real_action_strategy["atk_type"]["skill"]['weight'] = 0.2
            real_action_strategy["atk_type"]["normal"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_max_atk"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_max_def"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_career_support"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_career_attack"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_career_defense"]['weight'] = 0.2
            real_action_strategy["move_position"]["atk_multi"]['weight'] = 0.2
            real_action_strategy["move_position"]["no_atk"]['weight'] = 0.2
            real_action_strategy["move_position"]["high"]['weight'] = 0.2
            real_action_strategy["move_path"]["shortest"]['weight'] = 0.2
            real_action_strategy["move_path"]["no_warning"]['weight'] = 0.2
            real_action_strategy["assist"]["single_heal"]['weight'] = 0.2
            real_action_strategy["assist"]["group_heal"]['weight'] = 0.2
            real_action_strategy["assist"]["sustain_heal"]['weight'] = 0.2
            real_action_strategy["assist"]["career_defense"]['weight'] = 0.2
            real_action_strategy["assist"]["career_attack"]['weight'] = 0.2
            real_action_strategy["assist"]["self_heal"]['weight'] = 0.2
        elif base_class_value == 3:#治疗
            real_selection_strategy["escape"]["is_health_below_threshold"]['weight'] = 0.4
            real_action_strategy["atk_target"]["nearest"]['weight'] = 0.3444
            real_action_strategy["atk_target"]["min_hp"]['weight'] = 0.2
            real_action_strategy["atk_target"]["max_atk"]['weight'] = 0.2
            real_action_strategy["atk_target"]["min_def"]['weight'] = 0.2
            real_action_strategy["atk_target"]["career_support"]['weight'] = 0.2
            real_action_strategy["atk_target"]["career_attack"]['weight'] = 0.2
            real_action_strategy["atk_target"]["career_defense"]['weight'] = 0.2
            real_action_strategy["atk_target"]["non_elite"]['weight'] = 0.2
            real_action_strategy["atk_target"]["elite"]['weight'] = 0.2
            real_action_strategy["atk_target"]["no_atk"]['weight'] = 0.2
            real_action_strategy["atk_target"]["no_combat_no_atk"]['weight'] = 0.2
            real_action_strategy["atk_type"]["skill"]['weight'] = 0.2
            real_action_strategy["atk_type"]["normal"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_max_atk"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_max_def"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_career_support"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_career_attack"]['weight'] = 0.2
            real_action_strategy["atk_type"]["single_career_defense"]['weight'] = 0.2
            real_action_strategy["move_position"]["atk_multi"]['weight'] = 0.2
            real_action_strategy["move_position"]["no_atk"]['weight'] = 0.2
            real_action_strategy["move_position"]["high"]['weight'] = 0.2
            real_action_strategy["move_path"]["shortest"]['weight'] = 0.2
            real_action_strategy["move_path"]["no_warning"]['weight'] = 0.2
            real_action_strategy["assist"]["single_heal"]['weight'] = 0.2
            real_action_strategy["assist"]["group_heal"]['weight'] = 0.2
            real_action_strategy["assist"]["sustain_heal"]['weight'] = 0.2
            real_action_strategy["assist"]["career_defense"]['weight'] = 0.2
            real_action_strategy["assist"]["career_attack"]['weight'] = 0.2
            real_action_strategy["assist"]["self_heal"]['weight'] = 0.3
        else:
            real_action_strategy,real_selection_strategy = None,None
        return real_action_strategy,real_selection_strategy
if __name__ == '__main__':
    obj= strategy_params()
    print(obj.get_strategy_params(1))
