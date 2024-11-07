import copy
import time

from utils.config import bass_class
import pandas as pd
import os
import configparser

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
def get_data_from_csv(filename):
    cf = configparser.ConfigParser()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    cf.read(path + '/../config/conf.ini', encoding='utf-8')
    team_strategy = cf.get('strategy', 'team_strategy')
    df=pd.DataFrame()
    team_strategy_str=''
    #1 快速完成关卡 2 目标取得高分 3 谨慎稳步推进
    if str(team_strategy)=="1":
        team_strategy_str="快速完成关卡"
    elif str(team_strategy)=="2":
        team_strategy_str="目标取得高分"
    elif str(team_strategy)=="3":
        team_strategy_str="谨慎稳步推进"
    else:
        pass
    df=pd.read_csv(filename)
    df = df[df['type'] == team_strategy_str]
    return df


class strategy_params:
    def __init__(self):
        self.data_type = [1,2] # 1是越小越好，2是越大越好
        self.base_class = bass_class
        self.action_strategy = {}
        self.selection_strategy = {}
        #self.team_strategy = '快速完成关卡'
        ####选择逃跑策略================================================================================================
        self.selection_strategy["escape"] = {}
        self.selection_strategy["escape"]["is_health_below_threshold"]={'weight': 0.4} #0.4代表40%
        ####选择攻击对象的策略================================================================================================
        self.action_strategy["atk_target"] = {}
        ####优先攻击最近的敌人
        self.action_strategy["atk_target"]["nearest"] = {'score': [0,1], 'desc': '优先攻击最近的敌人', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 1}
        ####优先攻击百分比血量最少的敌人
        self.action_strategy["atk_target"]["min_hp"] = {'score': [0,1], 'desc': '优先攻击百分比血量最少的敌人', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 1}
        ####优先攻击攻击力最高的敌人
        self.action_strategy["atk_target"]["max_atk"] = {'score': [0,1], 'desc': '优先攻击攻击力最高的敌人', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 2}
        ####优先攻击防御力最低的敌人
        self.action_strategy["atk_target"]["min_def"] = {'score': [0,1], 'desc': '优先攻击防御力最低的敌人', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 1}
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

        ###选择攻击方式的策略================================================================================================
        self.action_strategy["atk_type"] = {}
        ####优先使用技能攻击
        self.action_strategy["atk_type"]["skill"] = {'score': [0,1], 'desc': '优先使用技能攻击', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先使用普通攻击
        self.action_strategy["atk_type"]["normal"] = {'score': [0,1], 'desc': '优先使用普通攻击', 'weight': 0.2, 'clac_type': 'exclusive'}
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
        self.action_strategy["move_position"]["atk_multi"] = {'score': [0,1], 'desc': '优先移动到普通攻击可以攻击到复数敌人的位置', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 2}
        ####优先移动到不会被更多敌人攻击的位置
        #被攻击到人越少，分数越高
        self.action_strategy["move_position"]["no_atk"] = {'score': [0,1], 'desc': '优先移动到不会被更多敌人攻击的位置', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 1}
        ####优先占领制高点，目标地点-当前地点的高度差越大，分数越高
        self.action_strategy["move_position"]["high"] = {'score': [0,1], 'desc': '优先占领制高点', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 2}
        ####选择移动路径策略================================================================================================
        self.action_strategy["move_path"] = {}
        ####优先最短路线
        self.action_strategy["move_path"]["shortest"] = {'score': [0,1], 'desc': '优先最短路线', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 1}
        ####优先不进入敌人的警戒范围
        ###进入敌人警戒范围的点越多，分值越低
        self.action_strategy["move_path"]["no_warning"] = {'score': [0,1], 'desc': '优先不进入敌人的警戒范围', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 1}
        ####选择辅助策略================================================================================================
        self.action_strategy["assist"] = {}
        ####优先使用单体治疗技能
        self.action_strategy["assist"]["single_heal"] = {'score': [0,1], 'desc': '优先使用单体治疗技能', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 2}
        ####优先使用群体治疗技能
        self.action_strategy["assist"]["group_heal"] = {'score': [0,1], 'desc': '优先使用群体治疗技能', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 2}
        ####优先使用持续治疗技能
        self.action_strategy["assist"]["sustain_heal"] = {'score': [0,1], 'desc': '优先使用持续治疗技能', 'weight': 0.2, 'clac_type': 'normalized', 'data_type': 2}
        ####优先针对防守型职业使用治疗技能
        self.action_strategy["assist"]["assist_career_defense"] = {'score': [0,1], 'desc': '优先针对防守型职业使用治疗技能', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先针对攻击型职业使用治疗技能
        self.action_strategy["assist"]["assist_career_attack"] = {'score': [0,1], 'desc': '优先针对攻击型职业使用治疗技能', 'weight': 0.2, 'clac_type': 'exclusive'}
        ####优先针对自己加血
        self.action_strategy["assist"]["self_heal"] = {'score': [0,1], 'desc': '优先针对自己加血', 'weight': 0.2, 'clac_type': 'exclusive'}


    def set_team_strategy(self,type_name):
        self.team_strategy = type_name
    def get_strategy_params(self,base_class_value:int):

        real_action_strategy  =copy.deepcopy(self.action_strategy)
        real_selection_strategy = copy.deepcopy(self.selection_strategy)
        if base_class_value ==10000:
            real_selection_strategy["escape"]["is_health_below_threshold"]['weight'] = 0.4
            w_tmp = {}
            k_count_1=len(real_action_strategy.keys())
            for k in real_action_strategy.keys():
                w_tmp[k] = round(1/k_count_1,4)
                k_count_2=len(real_action_strategy[k].keys())
                for k1 in real_action_strategy[k].keys():
                    real_action_strategy[k][k1]['weight'] =round(w_tmp[k]/k_count_2,4)

        elif base_class_value in (1,2,3,4,5):

            df=get_data_from_csv(os.path.dirname(os.path.abspath(__file__))+'/weight.csv')
            df['hero']  = df['hero'].astype(int)
            df = df[df['hero'].isin([1,2,3,4,5])]
            df=df[df['hero']==base_class_value]
            # for k in self.selection_strategy:
            #     for k1 in self.selection_strategy[k]:
            #         if k1 in df.columns:
            #             real_selection_strategy[k][k1]['weight'] = df[k1].iloc[0]
            #             continue
            #强制逃跑0.4先
            for k in self.action_strategy:
                for k1 in self.action_strategy[k]:
                    if k1 in df.columns:
                        real_action_strategy[k][k1]['weight'] = df[k1].iloc[0]
                        continue


        else:
            real_action_strategy,real_selection_strategy = None,None
        return real_action_strategy,real_selection_strategy




    def get_special_case_1(self):
        #做一个全部weight是none的，开始手动填写，最后检查是否还有none
        real_action_strategy  =copy.deepcopy(self.action_strategy)
        real_selection_strategy = copy.deepcopy(self.selection_strategy)
        for i in real_action_strategy.keys():
            for j in real_action_strategy[i].keys():
                real_action_strategy[i][j]['weight'] =None
        ####逃跑血量
        real_selection_strategy["escape"]["is_health_below_threshold"]['weight'] = 0.4
        ####优先攻击最近的敌人
        real_action_strategy["atk_target"]["nearest"]['weight'] = 0.2
        ####优先攻击百分比血量最少的敌人
        real_action_strategy["atk_target"]["min_hp"]['weight'] = 0.2
        ####优先攻击攻击力最高的敌人
        real_action_strategy["atk_target"]["max_atk"]['weight'] = 0.2
        ####优先攻击防御力最低的敌人
        real_action_strategy["atk_target"]["min_def"]['weight'] = 0.2
        ####优先攻击支援型职业
        real_action_strategy["atk_target"]["career_support"]['weight'] = 0.2
        ####优先攻击攻击型职业
        real_action_strategy["atk_target"]["career_attack"]['weight'] = 0.2
        ####优先攻击防御型职业
        real_action_strategy["atk_target"]["career_defense"]['weight'] = 0.2
        ####优先攻击非精英单位
        real_action_strategy["atk_target"]["non_elite"]['weight'] = 0.2
        ####优先攻击精英单位
        real_action_strategy["atk_target"]["elite"]['weight'] = 0.2
        ####优先使用技能攻击
        real_action_strategy["atk_type"]["skill"]['weight'] = 0.2
        ####优先使用普通攻击
        real_action_strategy["atk_type"]["normal"]['weight'] = 0.2
        ####优先对攻击力最高的敌人使用单体攻击技能
        real_action_strategy["atk_type"]["single_max_atk"]['weight'] = 0.2
        ####优先对防御力最高的敌人使用单体攻击技能
        real_action_strategy["atk_type"]["single_max_def"]['weight'] = 0.2
        ####优先对支援型职业使用单体攻击技能
        real_action_strategy["atk_type"]["single_career_support"]['weight'] = 0.2
        ####优先对攻击型职业使用单体攻击技能
        real_action_strategy["atk_type"]["single_career_attack"]['weight'] = 0.2
        ####优先对防御型职业使用单体攻击技能
        real_action_strategy["atk_type"]["single_career_defense"]['weight'] = 0.2
        ####优先移动到普通攻击可以攻击到更多敌人的位置
        real_action_strategy["move_position"]["atk_multi"]['weight'] = 0.2
        ####优先移动到不会被更多敌人攻击的位置
        real_action_strategy["move_position"]["no_atk"]['weight'] = 0.2
        ####优先占领制高点，目标地点-当前地点的高度差越大，分数越高
        real_action_strategy["move_position"]["high"]['weight'] = 0.2
        ####优先最短路线
        real_action_strategy["move_path"]["shortest"]['weight'] = 0.2
        ####优先不进入敌人的警戒范围
        ###进入敌人警戒范围的点越多，分值越低

        real_action_strategy["move_path"]["no_warning"]['weight'] = 0.2
        ####优先使用单体治疗技能
        real_action_strategy["assist"]["single_heal"]['weight'] = 0.2
        ####优先使用群体治疗技能
        real_action_strategy["assist"]["group_heal"]['weight'] = 0.2
        ####优先使用持续治疗技能
        real_action_strategy["assist"]["sustain_heal"]['weight'] = 0.2
        ####优先针对防守型职业使用治疗技能
        real_action_strategy["assist"]["career_defense"]['weight'] = 0.2
        ####优先针对攻击型职业使用治疗技能
        real_action_strategy["assist"]["career_attack"]['weight'] = 0.2
        ####优先针对自己加血
        real_action_strategy["assist"]["self_heal"]['weight'] = 0.2

        #检查所有key的weight是不是都不是none
        for i in real_action_strategy.keys():
            for j in real_action_strategy[i].keys():
                if real_action_strategy[i][j]['weight'] == None:
                    print('存在未配置都项,[',str(i),'],[',str(j),']')


class simple_strategy_params:
    def __init__(self):
        self.demo_step_dict = {
            "action": {
                "enemy": {
                    "normal": bool, #普通攻击
                    "skill": {
                        "any_attack": bool,#任意可以对敌人释放的技能
                        "attack": int,  # 0单体攻击技能，1群体攻击技能
                        "de_buff": int,  # 0单体减益技能，1群体减益技能
                        "select": []  # 指定对技能ID，可以是多个
                    },
                    "item": {
                        "attack": [0, 1], # 0单体攻击物品 1群体攻击物品
                        "de_buff": [0, 1], # 0单体减益物品 ，1 群体减益物品
                        "select": [] #具体物品id
                    }
                },
                "us": {
                    "skill": {
                        "any": bool,  # 可以对我方释放的技能
                        "any_heal": int,  # 0单体，1群体
                        "any_buff": int,  # 0单体，1群体
                        "select": []  # 技能ID
                    },
                    "item": {
                        "any": bool,
                        "any_heal": [0, 1],
                        "any_buff": [0, 1],
                        "select": []  # 物品ID

                    }
                }
            },
            "target": {
                "character": {
                    "any": bool,  #任意职业、位置
                    "type": int,  # 传入具体int 1 2 3 代表 ["any", "前卫", "后卫"]
                    "geo": int,  # 传入具体int  1 2 3 4 5 代表 ["any", "攻击型","防守型"，"治疗型"，"辅助型"]
                    "role": int, #  传入具体int  1 2 3 4 5 代表 ["近身持续输出", "近身爆发输出"，"远程输出","魔法输出","治疗辅助"]
                    "select": []  # baseclassID [1]代表战士
                },
                "role_type": int  # boss 0 普通 1

            },
            "filter": {
                "hp": {
                    "max_hp": bool,
                    "min_hp": bool,
                    "max_perc_hp": bool,
                    "min_perc_hp": bool,
                    "hp_below": float, # 0.3
                    "hp_above": float # 0.7
                },
                "status": {
                    "any_buff": [], #todo 定义bufferid ,定义每个buffer和类别对关系
                    # BUFF_ADD_HP,
                    # BUFF_ADD_ATK,
                    # BUFF_ADD_DEF,
                    # BUFF_ROUND_ACTION
                    # 护盾暂无

                    "any_de_buff": [],  # todo 待定
                    "no_status": bool # 代表是否有任何buffer  ，
                },
                "distance": str,  # MIN / MAX
                "count": int,# 1人以上，就传入 1
                "value": {
                    "p_attack": str,  # MIN / MAX
                    "m_attack": str,  # MIN / MAX
                    "p_defense": str,  # MIN / MAX
                    "m_defense": str,  # MIN / MAX
                    "speed": str,  # MIN / MAX
                },
                "limit": {
                    # TODO 行为限制
                }
            }
        }

    def get_strategy_params(self,hero_id:int):
        _res_list=[]
        if hero_id==5002:
            res_dict = {}
            res_dict['action']={}
            res_dict['action']['enemy']={}
            res_dict['action']['enemy']['skill']={}
            res_dict['action']['enemy']['skill']['select']=[78]
            res_dict['target']={}
            res_dict['target']['character']={}
            res_dict['target']['character']['any']=True
            res_dict['filter']={}
            res_dict['filter']['count']=2
            _res_list.append(res_dict)

        if hero_id==5003:
            res_dict={}
            res_dict['action']={}
            res_dict['action']['enemy']={}
            res_dict['action']['enemy']['skill']={}
            res_dict['action']['enemy']['skill']['select']=[88]
            res_dict['target']={}
            res_dict['target']['character']={}
            res_dict['target']['character']['any']=True
            res_dict['filter']={}
            res_dict['filter']['hp']={}
            res_dict['filter']['hp']['hp_below']=0.5
            _res_list.append(res_dict)

        return _res_list





if __name__ == '__main__':
    obj= strategy_params()
    print(obj.get_strategy_params(2))