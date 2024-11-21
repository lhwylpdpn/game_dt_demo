# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-08-01

"""
import json
import copy
import traceback
from itertools import product
from utils.damage import damage
from utils.heal import heal
from utils.tools import random_choices
from utils.tools import round_up_2_integer
from .map import Map, Land
from .buff import Buff
from .attachment import Attachment
from .teamflag import TeamFlag
from .baseclass import BaseClass

class Hero():
    
    def __init__(self, **kwargs):
        # 基本属性
        self.__HeroID = int(kwargs.get("HeroID", None))
        self.__protagonist = kwargs.get("protagonist", 0)          # 是否是主角
        self.__AvailableSkills = kwargs.get("AvailableSkills", []) # 可用的技能     #
        self.__RoundAction = kwargs.get("RoundAction", None)       # 行动步数
        self.__JumpHeight = kwargs.get("JumpHeight", [])           # 跳跃的高度 
        self.__skills =  kwargs.get("skills", [])                  # 技能
        self.__DogBase = kwargs.get("DogBase", None)               # 警戒-初始
        self.__BaseClassID = kwargs.get("BaseClassID", None)       # 职业
        self.__Element = kwargs.get("Element", 0)                  # 元素属性
        self.__BaseClass = BaseClass(**kwargs.get("BaseClass", {})) # 职业
        # 初始数值
        self.__HpBase = kwargs.get("Hp", None)                       #生命-初始
        self.__Hp = kwargs.get("Hp", None)                           #生命
        
        self.__AtkBase = kwargs.get("Atk", None)                     #攻击-初始
        self.__Atk = kwargs.get("Atk", None)                         #攻击
        
        self.__DefBase = kwargs.get("Def", None)                     #防御-初始
        self.__Def = kwargs.get("Def", None)                         #防御

        self.__MagicalAtkBase = kwargs.get("MagicalAtk", None)       #魔法攻击-初始
        self.__MagicalAtk = kwargs.get("MagicalAtk", None)           #魔法攻击

        self.__MagicalDefBase = kwargs.get("MagicalDef", None)       #魔法防御-初始
        self.__MagicalDef = kwargs.get("MagicalDef", None)           #魔法防御

        self.__AgileBase = kwargs.get("Agile", None)                 #敏捷-初始
        self.__Agile = kwargs.get("Agile", None)                     #敏捷

        self.__VelocityBase = kwargs.get("Velocity", None)           #速度-初始   行动力
        self.__Velocity = kwargs.get("Velocity", None)               #速度-初始   行动力
        
        self.__LuckBase = kwargs.get("Luck", None)                   #运气-初始
        self.__Luck = kwargs.get("Luck", None)                       #运气
        self.__Quality = kwargs.get("Quality", 0)                    # 是否 boss
        self.__team = kwargs.get("team", None)                       # 所属队伍
        
        # position 位置
        self.__position = kwargs.get("position")                               #  坐标
        self.__avali_move_p_list = kwargs.get("avali_move_p_list", [])         #  可移动范围
        self.__shoot_p_list = kwargs.get("shoot_p_list", [])                   #  可攻击范围
        self.__atk_effect_p_list = kwargs.get("atk_effect_p_list", [])         #  攻击效果范围

        #### buff
        self.__buff = []                                                       # 带的buff

        self.fields =  ["HeroID", "protagonist", "AvailableSkills", "RoundAction", "JumpHeight", "skills",
            "DogBase", "BaseClassID", "Element", "BaseClass", "Hp", "HpBase", "Atk",  "Def", "MagicalAtk",
            "MagicalDef",  "Agile",  "Velocity", "Quality", "team",
            "Luck", "position", "buff",
            "avali_move_p_list", "shoot_p_list", "atk_effect_p_list"
            ]
        ### unit_hero
        self.__unit_skill_buff = []                                             # 连携攻击增加的buf(每行动一次，重新组织一次此数据)
        self.__Block = 2                                                        # 地块站立的属性 hero 为2， monster 为 3
        # UnitDistance 
        self.__UnitDistance = kwargs.get("UnitDistance", 1)                     # 连携距离
        # 自己的数据统计
        self.__focus_times = 0                                                  # 被选中的次数
        # 回合内是否移动变量
        self.is_move = False

    def hero_or_monster(self):
        "HERO or MONSER"
        return self.__class__.__name__.upper()
    
    def is_hero(self):
        return True
    
    def get_fields(self):
        return self.fields
    
    def join_game(self, state, init_position=True): # 进入战局
        self.move_position(*self.position, state, init_position)
        return self
    
    def __get_need_trigger_buff(self, is_before_action=True): # 获取自己需要每次触发的buff
        _buf = []
        for _ in self.__buff:
            if _.is_need_trigger and _.is_before_action==is_before_action:
                _buf.append(_)
        return _buf

    def focus(self, state):
        # 被选中
        self.__focus_times += 1     # 被选中次数 + 1
        self.is_move = False
        self.check_buff()           # 减少buff
        map_obj = state.get("maps")
        map_obj.h_m_focus(self)
        bufff_s = []
        for each in self.__get_need_trigger_buff(is_before_action=True):
            bufff_s.append({"action_type": f"EFFECT_{each.buff_id}", "buff":each})
        self.reduce_buff_round_action() # 减少buff的round action
        return bufff_s 
    
    def un_focus(self, state):
        # 取消选中
        bufff_s = []
        for each in self.__get_need_trigger_buff(is_before_action=False):
            bufff_s.append({"action_type": f"EFFECT_{each.buff_id}", "buff":each})
        if not self.is_move: # 回合内是否移动了
            for each in self.skills:
                if each.is_dont_move_media_self_skill(): # 回合内不移动治疗自己
                    for each_e in each.effects:
                        tmp_buff = None
                        if "ADD_HP" == each_e.key:
                            tmp_buff = Buff.create_buff(self, buff_id=each_e.id, buff_key=each_e.key, param=each_e.param[1:], BuffType=each_e.BuffType)
                        else:
                            if each_e.key != "IS_WAIT":
                                print("[ERROR] need add ", each_e.key)
                        if tmp_buff:
                            bufff_s.append({"action_type": f"EFFECT_{tmp_buff.buff_id}", "buff":tmp_buff}) 
        map_obj = state.get("maps")
        map_obj.h_m_unfocus(self)
        self.is_move = False
        return bufff_s
    
    def __get_friends(self, state):
        all_friends = state['hero'] if self in state['hero'] else state['monster'] # 找到己方的所有人, 包括自己
        return [_ for _ in all_friends if _.is_alive]

    def leve_game(self, state): # 退出战局
        map_obj = state.get('maps')
        map_obj.exit(self)
        self.team.leve_game(self)
        friends = self.__get_friends(state)
        # 由于我给加上的buff，都要去掉（主要是连携 NEAR）
        for each in friends: 
            for each_buff in each.buff:
                if each_buff.buff_from == self:
                    each_buff.make_invalid(each)
                    each.__buff.remove(each_buff)
        
        print(f"{self.HeroID} is Killed, leve game.")
        return self

    def dict(self, fields=[], for_view=False):
        if not fields:
            fields = copy.deepcopy(self.fields)
        data = {}
        if "skills" in fields:
            data["skills"] = []
            fields.remove("skills")
            for each in self.__getattribute__("skills"):
                if each.is_avaliable():
                    data["skills"].append(each.dict(for_view=for_view))
        if "buff" in fields:
            data["buff"] = []
            fields.remove("buff")
            for each in self.__getattribute__("buff"):
                if each.is_avaliable() and each.is_buff():
                    data["buff"].append(each.dict(for_view=for_view))
        data.update({field: self.__getattribute__(field) for field in fields})
        if "team" in fields:
            if self.team:
                data["team"] = self.team.dict()
            else:
                data["team"] = []
        if "BaseClass" in fields:
            data["BaseClass"]  = self.__BaseClass.dict()
        # if for_view:
        #     data['position'] = list(trans_postion(*data["position"]))
        return data         
    
    @property
    def HeroID(self): # 
        return self.__HeroID
    
    def set_HeroID(self, HeroID):
        self.__HeroID = HeroID
        return self
    
    @property
    def UnitDistance(self):
        return self.__UnitDistance
    
    def set_UnitDistance(self, v):
        self.__UnitDistance = v
        return self
    
    @property
    def buff(self): # 
        return self.__buff

    @property
    def team(self): # 
        return self.__team
    
    def set_team(self, v):
        self.__team = v
        return self
    
    @property
    def Quality(self):
        return self.__Quality

    @property
    def set_Quality(self, V):
        self.__Quality = V
        return self

    def dict_short(self):
        data = super().dict_short()
        data["Quality"] = self.Quality
        return data

    @property
    def protagonist(self): # 
        return self.__protagonist
    
    def set_protagonist(self, v):
        self.__protagonist = v
        return self
    
    @property
    def AvailableSkills(self):
        return self.__AvailableSkills
    
    def set_AvailableSkills(self, AvailableSkills):
        self.__AvailableSkills = AvailableSkills
        return self
    
    @property
    def RoundAction(self):
        return self.__RoundAction
    
    def set_RoundAction(self, RoundAction):
        self.__RoundAction = RoundAction
        return self
    
    @property
    def Element(self):
        return self.__Element
    
    def set_Element(self, Element):
        self.__Element = Element
        return self
    
    @property
    def JumpHeight(self):
        return self.__JumpHeight
    
    def set_JumpHeight(self, JumpHeight):
        self.__JumpHeight = JumpHeight
        return self
    
    @property
    def skills(self):
        skills = []
        for each in self.__skills: # 通过 AvailableSkills 判断
            if each.SkillId in self.AvailableSkills:
                skills.append(each)
        return skills
    
    def get_skill_by_id(self, skill_id):
        for each in self.skills:
            if each.SkillId == skill_id:
                return each
        return None
    
    def set_skills(self, v):
        self.__skills = v
        return self

    @property
    def Block(self):
        return self.__Block
    
    def set_Block(self, v):
        self.__Block = v
        return self
    
    def skills_add(self, skill):
        self.__skills.append(skill)
        return self
    
    @property
    def HpBase(self): # 最高血量
        return self.__HpBase
    
    def set_HpBase(self,v): # 最高血量
        self.__HpBase = v
        return self
    
    @property
    def Hp(self):
        return self.__Hp
    
    def set_Hp(self, Hp):
        self.__Hp = round_up_2_integer(Hp)
        print(self.HeroID ,"Hp <curent>: ", self.__Hp)
        return self
    
    def Hp_damage(self, damage_res): # 被攻击，掉血
        damage = sum([_.get("damage") for _ in damage_res]) 
        print(self.HeroID ,"Hp <before>: ", self.Hp)
        print(self.HeroID ,"Hp <damage>: ", damage)
        _t_hp = self.Hp - damage
        return self.set_Hp(float("%.2f"%_t_hp) if _t_hp >= 0 else 0) # 血量

    def Hp_add(self, heal_res): # 被治疗or suck，涨Hp
        hp = sum([_.get("heal") for _ in heal_res])
        print(self.HeroID ,"Hp <before>: ", self.Hp)
        print(self.HeroID ,"Hp <hp add>: ", hp)
        _t_hp = self.Hp + hp
        return self.set_Hp(float("%.2f"%_t_hp) if _t_hp <= self.HpBase else self.HpBase) # 血量
    
    def Hp_suck(self, damage):  # 攻击别人，自己吸血
        # TODO damage 需要吸血多少，需要处理
        return self.Hp_add(damage)
    
    @property
    def AtkBase(self):
        return self.__AtkBase

    @property
    def Atk(self):
        return self.__Atk
    
    def set_Atk(self, Atk):
        self.__Atk = round_up_2_integer(Atk)
        return self
    
    @property
    def DefBase(self):
        return self.__DefBase

    @property
    def Def(self):
        return self.__Def
    
    def set_Def(self, Def):
        self.__Def = round_up_2_integer(Def)
        return self

    @property
    def MagicalAtkBase(self):
        return self.__MagicalAtkBase

    @property
    def MagicalAtk(self):
        return self.__MagicalAtk
    
    def set_MagicalAtk(self, v):
        self.__MagicalAtk = round_up_2_integer(v)
        return self
    
    @property
    def MagicalDefBase(self):
        return self.__MagicalDefBase
    
    @property
    def MagicalDef(self):
        return self.__MagicalDef
    
    def set_MagicalDef(self, MagicalDef):
        self.__MagicalDef = round_up_2_integer(MagicalDef)
        return self
    
    @property
    def AgileBase(self):
        return self.__AgileBase

    @property
    def Agile(self):
        return self.__Agile
    
    def set_Agile(self, Agile):
        self.__Agile = round_up_2_integer(Agile)
        return self
    
    @property
    def VelocityBase(self):
        return self.__VelocityBase

    @property
    def Velocity(self):
        return self.__Velocity
    
    def set_Velocity(self, Velocity):
        self.__Velocity = round_up_2_integer(Velocity)
        return self

    @property
    def BaseClassID(self):
        return self.__BaseClassID
    
    def set_BaseClassID(self, v):
        self.__BaseClassID = v
        return self
    
    @property
    def BaseClass(self):
        return self.__BaseClass
    
    def set_BaseClass(self, v):
        self.__BaseClass = v
        return self

    @property
    def DogBase(self):
        return self.__DogBase
    
    def set_DogBase(self, DogBase):
        self.__DogBase = DogBase
        return self
    
    def get_dog_range(self, state): # 警戒范围
        map_object = state.get("maps")
        drange = []
        if self.is_alive:
            for x, z in product(range(-self.__DogBase, self.__DogBase + 1), repeat=2):
                if abs(x) + abs(z) <= self.__DogBase:
                    try:
                        p_x, p_z = self.x + x, self.z + z
                        p_y = map_object.get_y_from_xz(p_x, p_z)
                        if p_y is not None:
                            drange.append(tuple([p_x, p_y, p_z]))
                    except Exception:
                        pass
        return drange
                
    @property
    def LuckBase(self):
        return self.__LuckBase

    @property
    def Luck(self):
        return self.__Luck
    
    def set_Luck(self, v): 
        self.__Luck = v
        return self

    @property
    def x(self):
        return self.__position[0]
    
    def set_x(self, p_x):
        self.__position[0]= p_x
        return self
    
    @property
    def y(self):
        return self.__position[1]
    
    def set_y(self, p_y):
        self.__position[1]= p_y
        return self
    
    @property
    def z(self):
        return self.__position[2]
    
    def set_z(self, p_z):
        self.__position[2]= p_z
        return self   
    
    @property
    def position(self):
        return self.__position

    def set_position(self,x,y,z):
        return self.set_x(x).set_y(y).set_z(z)
    
    def __buff_value(self, buff_key):
        value = None
        for each in self.__buff:
            if each.buff_key == buff_key:
                if value is not None:
                    value += int(each.buff_value)
                else:
                    value = int(each.buff_value)
        return value

    @property
    def BUFF_HIT_RATE(self): # 增加{0}的命中率
        return self.__buff_value(buff_key="BUFF_HIT_RATE")

    @property
    def BUFF_MISS_HIT(self): # {0}%机率使攻击无效，并持续{0}行动回合
        return self.__buff_value(buff_key="BUFF_MISS_HIT")

    @property
    def BUFF_MAX_ATK_DISTANCE(self): # 攻击范围最大值增加{0}格，并持续{0}行动回合
        return self.__buff_value(buff_key="BUFF_MAX_ATK_DISTANCE")
    
    def add_buff_object(self, buff_obj): # 增加普通buff object
        buff_obj.make_effective(self)
        self.__buff.append(buff_obj)
        return buff_obj

    def add_buff(self, buff_id,  buff_key, param, buff_percent=None, BuffType=None): # 增加普通buff
        buff = Buff.create_buff(self, buff_id, buff_key, param, buff_percent=buff_percent, BuffType=BuffType)
        buff.make_effective(self) # buff生效
        self.__buff.append(buff)
        return buff

    def check_buff(self): # 回合结束后，检查buff的加成
        for each in self.__buff:
            if not each.is_avaliable:
                each.make_invalid(self)
                self.__buff.remove(each)
        return self
    
    def add_unit_buff(self, buff_id, buff_key, param, BuffType=None): # 增加连携buff
        buff = Buff.create_buff(self, buff_id, buff_key, param, BuffType=BuffType)
        buff.make_effective(self)
        self.__unit_skill_buff.append(buff)
        return buff
    
    def remove_unit_buff(self, state): # 去除连携buff
        friends = self.__get_friends(state)
        for each_f in friends:
            for each in each_f.__unit_skill_buff:
                each.make_invalid(each_f)
            each_f.__unit_skill_buff = []
        return 

    @property
    def avali_move_p_list(self):
        return self.__avali_move_p_list
    
    def set_avali_move_p_list(self, v):
        self.__avali_move_p_list = v
        return self 

    @property
    def shoot_p_list(self):
        return self.__shoot_p_list
    
    def set_shoot_p_list(self, v):
        self.__shoot_p_list = v
        return self 

    @property
    def atk_effect_p_list(self):
        return self.__atk_effect_p_list
    
    def set_atk_effect_p_list(self, v):
        self.__atk_effect_p_list = v
        return self 

    def is_position_ok(self, x, y, z, state):
        map_obj = state['maps']
        return map_obj.land_can_pass(x, y, z)
    
    def check_team(self, state): # 检查是否需要合并队伍
        print("*****************检查是否需要合并队伍")
        if not self.is_alive:
            print("已经死亡，不需要队伍合并")
            return self
        enter_other_team_dog_range = TeamFlag.get_should_combine_team(self, state)
                    
        if enter_other_team_dog_range:
            new_team = TeamFlag.choose_team(self, state, enter_other_team_dog_range)
            TeamFlag.recombine_team(self.team, new_team)
            del new_team
        
        return self
    
    def move_position(self, x, y, z, state, init_position=False):
        print("MOVE>>:", self.HeroID, f"from <{self.position}>计划移动到<[{x}, {y}, {z}]>")
        map_obj = state['maps']
        if not map_obj.land_can_pass(x, y, z):
            raise Exception(f"<ERROR>:({x}, {y}, {z}) 不能通过.")
        map_obj.exit(self)            # 离开当前地块
        map_obj.enter(x,y,z, self, init_position)    # 进入新地块, 返回宝箱
        self.set_x(x).set_y(y).set_z(z)       # 设置新位置
        self.is_move = True
        print("MOVE>>:", self.HeroID, f"移动到<{self.position}>")
        self.remove_unit_buff(state)          # 先卸载连携buff
        self.load_unit_buff(state)            # 加载新的连携buff
        if not init_position : #初始化位置时候，不做队伍检查
            self.check_team(state)
        return self

    @property
    def is_death(self):
        return self.Hp <= 0
    
    @property
    def is_alive(self):
        return not self.is_death
    
    def remove_debuff(self):
        for each in self.buff:
            if each.buff_key in ["DEBUFF_ROUND_ACTION_BACK"] :
                each.make_invalid(self)
        return self
    
    def get_back_attack_Skills(self): # 获取反击攻击技能
        skill = []
        for _ in self.skills:
            if _.is_back_attack_skill():
                skill.append(_)
        return skill
    
    def get_back_skills(self, enemy, attach_skill): # 获取反击技能
        skill = []
        for _ in self.get_back_attack_Skills():
            if "ATK_BACK" in _.avaliable_effects():
                # 是默认技能， 默认技能攻击时候触发
                if attach_skill.is_default_skill():
                    if _.is_default_hit() or _.is_hit():
                        skill.append(_)
                # 不是默认技能，其他技能攻击时候触发
                if not attach_skill.is_default_skill():
                    if _.is_skill_hit() or _.is_hit():
                        skill.append(_)
            if "DEBUFF_ROUND_ACTION_BACK" in _.avaliable_effects() and _.is_hit():
                effect = _.get_effect_by_key("DEBUFF_ROUND_ACTION_BACK")
                if random_choices({True:int(effect.param[0])/100.0, False:1 - int(effect.param[0])/100.0}): # 几率判断
                    enemy.add_buff(buff_id=effect.id, buff_key="DEBUFF_ROUND_ACTION_BACK",
                                   param=effect.param[1:], buff_percent=effect.param[0], BuffType=effect.BuffType)
        print("get back skill:", len(skill), skill)
        return skill

    def load_init_unActiveSkill(self): # load  buff
        # 初始的时候，增加非主动，非被动触发的技能, 不是被普通攻击 , 不是连携技能
        buffs_unit_dis = []
        for each_skill in self.skills:
            if each_skill.is_buff(): 
                for each in each_skill.effects:
                    buff = self.add_buff(buff_id=each.id, buff_key=each.key, param=each.param, BuffType=each.BuffType)
                    if "BUFF_UNIT_DISTANCE" == each.key: # 寻找可以全队连携的buff
                        buffs_unit_dis.append(buff)
        return buffs_unit_dis

    def get_unit_skill(self): # 获取连携攻击
        unit_skills = []
        for each_skill in self.skills:
            if each_skill.is_unit_skill(): 
               unit_skills.append(each_skill)
        return unit_skills
                
    def __search_near_friends(self, range, state):
        near_friends = []
        for each in self.__get_friends(state):
            if abs(self.x - each.x) + abs(self.z - each.z) <= int(range): # 在范围内
                near_friends.append(each)
        return near_friends   
    
    def load_unit_buff(self, state): # 加载连携攻击
        # 我身边的位置 几格之内有队友
        """
        @ value 几格
        @ state 场景 {"hero":{}, "monster":{}, "maps": map}
        """
        for each in self.__get_friends(state):
            unit_skill = each.get_unit_skill() # 获取连携攻击
            for each_skill in unit_skill:
                # 确定连携的范围
                buff_range = each_skill.get_effect_by_key("ADD_BUFF_RANGE")
                if buff_range is None: buff_range = 0
                else: buff_range = buff_range.param[1]
                near_friends = self.__search_near_friends(buff_range, state)
                if len(near_friends) >1: # 多于一个人才可以连携 (自己一个人不算哈)
                    for friend in near_friends:
                        for e_skill in each_skill.effects:
                            friend.add_unit_buff(buff_id=e_skill.id, buff_key=e_skill.key, param=e_skill.param)
        return  self               
                    
    def __get_unit_num(self, skill, state): # 获取连携数据
        unit_num = 1
        if skill.is_default_skill(): # 普通攻击时候 才考虑连携
            near_frinds = self.__search_near_friends(self.UnitDistance, state)
            unit_num = len(near_frinds)
        return unit_num
                         
    def prepare_attack(self, skill): # 被攻击之前，加载主动技能 (作为 施动者 )
        effect_ids = skill.make_effective(self)
        return effect_ids

    def judge_direction(self, enemy): # 判断敌人在 上下左右，一级斜
        if enemy.x == self.x: # x 轴相等
            if enemy.z > self.z: # 敌人在上面
                return "UP"
            else: # 敌人在上面
                return "DOWN"
        elif enemy.z == self.z: # z 轴相等
            if enemy.x > self.x: # 敌人在右侧
                return "RIGHT"
            else: # 敌人在左侧
                return "LEFT"
        return "OTHER"


    def calc_move_point(self, direction, move_value): # 向某个方向移动几步的，返回新位置 
        move_x, move_y, move_z = self.position
        if direction == "UP":
            move_z = move_z + move_value 
        elif direction == "DOWN":
            move_z = move_z - move_value
        elif direction == "RIGHT":
            move_x = move_x + move_value
        elif direction == "LEFT":
            move_x = move_x - move_value
        else:
            pass
        return move_x, move_y, move_z

    def skill_move_position(self, move_value, direction, state): 
        """ 向某个方向移动几步 """
        
        if direction == "OTHER":
            print("方向:OTHER, 不移动")
            return self
        map_obj = state.get("maps")
        position_ok = None
        print(f"{self.HeroID} 计划从 {self.position} 移动 {move_value} 步，方向{direction}")
        
        for steps in range(1, move_value + 1):    # 找到具体的位置
            move_x, move_y, move_z = self.calc_move_point(direction, steps)
            move_x, move_z  = map_obj.correct_map_bonus(move_x, move_z)
            move_y = map_obj.get_y_from_xz(move_x, move_z)
            if self.is_position_ok(move_x, move_y, move_z, state):
                position_ok = [move_x, move_y, move_z]
            else:
                break
        
        if position_ok:
            print(f"{self.HeroID} 实际从 {self.position} {direction} 移动 { steps } 步,到 {position_ok} 点")
            self.move_position(*position_ok, state)
        else:
            print(f"{self.HeroID} 实际从{self.position} 移动 0 步")
            
        return self
    
    def __use_skill(self, skill):
        if not skill.use_skill(self).is_avaliable(): # 使用次数减少 后 判断技能是否还是可用的
            self.__AvailableSkills.remove(skill.skillId)
        return self
    
    def sort_enemys(self, enemys, reverse=False): # 对敌人进行排序
        """
        reverse : "False" 由近到远排序, "True" 由远到近排序
        """

        def distance(p1, p2):
            return abs(p1.x - p2.x) + abs(p1.z - p2.z)

        enemys.sort(key=lambda e_n:distance(self, e_n), reverse=reverse)
        return enemys
    
    def after_atk_skill(self, enemys=[], skill=None, attack_point=[], state=None): # 使用攻击技能后
        self.__use_skill(skill)
        # 判断自己是否向敌人移动 #TODO
        if "MOVE_SELF2TARGET" in skill.avaliable_effects():
            print("use: MOVE_SELF2TARGET 自己向敌人移动")
            move_value = skill.get_effect_by_key("MOVE_SELF2TARGET").param # 移动距离
            enemys = self.sort_enemys(enemys) #对敌人 由近及远排序
            direction = self.judge_direction(enemys[0])
            self.skill_move_position(int(move_value[0]), direction, state)
        # 判断敌人是否向自己移动 
        if "MOVE_TARGET2SELF" in skill.avaliable_effects():
            print("use: MOVE_TARGET2SELF 敌人向自己移动")
            move_value = skill.get_effect_by_key("MOVE_TARGET2SELF").param # 移动距离
            enemys = self.sort_enemys(enemys) #对敌人 由近及远排序
            for each_e in enemys: 
                direction = each_e.judge_direction(enemys[0])
                each_e.skill_move_position(int(move_value[0]), direction, state)
        # 击退几格
        if "REPEL_TARGET" in skill.avaliable_effects():
            print("use: REPEL_TARGET 被击退几格")
            direction = self.judge_direction(Hero(position=attack_point, HeroID='0')) # 攻击点即敌人在的方向
            move_value = skill.get_effect_by_key("REPEL_TARGET").param # 移动距离
            enemys = self.sort_enemys(enemys, reverse=True) #对敌人 由远及近排序
            for each_e in enemys: 
                each_e.skill_move_position(int(move_value[0]), direction, state)
        return self
         
    def after_medical_skill(self, friends=[], skill=None, state=None): # 使用治疗技能之后
        self.__use_skill(skill)
        if "BUFF_ADD_HP" in skill.avaliable_effects(): 
            effect = skill.get_effect_by_key("BUFF_ADD_HP")
            if random_choices({True:int(effect.param[0])/100.0, False:1 - int(effect.param[0])/100.0}): # 几率判断
                for each in friends:
                    buff = Buff.create_buff(hero_or_monster=self, buff_id=effect.id,
                        buff_key="BUFF_ADD_HP", param=effect.param[1:], 
                        buff_percent=effect.param[0], BuffType=effect.BuffType)
                    each.add_buff_object(buff)
        if "BUFF_HP" in skill.avaliable_effects(): 
            effect = skill.get_effect_by_key("BUFF_HP")
            for each in friends:
                buff = Buff.create_buff(hero_or_monster=self, buff_id=effect.id, buff_key="BUFF_HP", 
                   param=effect.param, buff_percent=effect.param[0], BuffType=effect.BuffType)
                each.add_buff_object(buff)
        if "ADD_HP_FORMULA_2" in skill.avaliable_effects():
            effect = skill.get_effect_by_key("ADD_HP_FORMULA_2")
            for each in friends:
                buff = Buff.create_buff(hero_or_monster=self, buff_id=effect.id, buff_key="ADD_HP_FORMULA_2", 
                   param=effect.param, BuffType=effect.BuffType)
                each.add_buff_object(buff)
        if "BUFF_MAGICAL_DEF" in skill.avaliable_effects(): 
            print("use: BUFF_MAGICAL_DEF")
            effect = skill.get_effect_by_key("BUFF_MAGICAL_DEF")
            for each in friends:
                buff = Buff.create_buff(hero_or_monster=self, buff_id=effect.id, buff_key="BUFF_MAGICAL_DEF", 
                   param=effect.param, BuffType=effect.BuffType)
                each.add_buff_object(buff)
        if "BUFF_DEF" in skill.avaliable_effects(): 
            print("use: BUFF_DEF")
            effect = skill.get_effect_by_key("BUFF_DEF")
            for each in friends:
                buff = Buff.create_buff(hero_or_monster=self, buff_id=effect.id, buff_key="BUFF_DEF", 
                   param=effect.param, BuffType=effect.BuffType)
                each.add_buff_object(buff)
        return self

    def before_be_attacked(self, skill):                # 被攻击之前，加载被动技能(作为被攻击对象)
        effect_ids = []
        for each_skill in self.skills:
            if each_skill.is_back_NA_skill():           # 加载反应技能
                if skill.is_default_skill():            # 技能是默认技能
                    if each_skill.is_default_hit() or each_skill.is_hit():  # 被默认技能攻击 or 被攻击 
                        effect_ids.extend(each_skill.make_effective(self))
                if not skill.is_default_skill():        # 不是默认技能攻击
                    if each_skill.is_hit() or each_skill.is_skill_hit() :   # 被技能攻击时候触发  or 被攻击 
                        effect_ids.extend(each_skill.make_effective(self))
        return effect_ids
    
    def after_be_attacked(self, skill):                # 被攻击之后，卸载被动技能(作为被攻击对象)
        for each_skill in self.skills:
            if each_skill.is_back_NA_skill():           # 卸载反应技能
                if skill.is_default_skill():            # 技能是默认技能
                    if each_skill.is_default_hit() or each_skill.is_hit():  # 被默认技能攻击 or 被攻击 
                        each_skill.make_invalid(self)
                if not skill.is_default_skill():        # 不是默认技能攻击
                    if each_skill.is_hit() or each_skill.is_skill_hit() :   # 被技能攻击时候触发  or 被攻击 
                        each_skill.make_invalid(self)
        return self
    
    def reduce_buff_round_action(self): # 每次行动后，减少buff中的round_action
        for each in self.__buff:
            each.reduce_round_action()
        return self

    def dont_move(self): # 移动不移动
        return self
    
    # 被动技能使攻击失效
    def is_miss_hit(self, attach_skill):
        
        def __is_miss(skill):
            effect = skill.get_effect_by_key("MISS_DAMAGE")
            return effect.id, random_choices({True:int(effect.param[0])/100.0, False:1 - int(effect.param[0])/100.0})

        for each_skill in self.skills:
            if each_skill.is_miss_damage(): # 是使攻击失效技能
                # 默认技能
                if each_skill.is_default_hit() and attach_skill.is_default_skill():
                   return __is_miss(each_skill)
                # 都是非默认技能
                if (not each_skill.is_default_hit()) and (not attach_skill.is_default_skill()):
                    return __is_miss(each_skill)
                # 被攻击
                if each_skill.is_hit():
                    return __is_miss(each_skill)
        
        return None, False
    
    def is_in_hitline_range(self, range_line_value,  enemy, state): # 
        """
        range_line_value 以我为原点,朝向敌人线性延伸{0｜0}
        enemy 目标敌人，即方向
        """
        if self.judge_direction(enemy) in ("UP", "DOWN", "LEFT", "RIGHT"):
            if abs(self.x - enemy.x) + abs(self.z - enemy.z) <= int(range_line_value): # 在范围内
                return True
        return False
    
    def is_in_hitcross_range(self,  gap, radis, enemy, state): # 
        """
        range_line_value 以我为原点,朝向敌人线性延伸{0｜0}
        enemy 目标敌人，即方向
        """
        if self.judge_direction(enemy) in ("UP", "DOWN", "LEFT", "RIGHT"):
            if int(gap)<= abs(self.x - enemy.x) + abs(self.z - enemy.z) <= int(radis): # 在范围内
                return True
        return False
 
    def is_in_hit_range(self, gap, radis, enemy, state):
        huff_dis = abs(self.x - enemy.x) + abs(self.z - enemy.z)
        if huff_dis <= int(radis) and huff_dis > gap:
            return True
        else:
            return False

    # 反击敌人， 以我为原点，是否在反击的技能范围之内
    def is_in_backskill_range(self, back_skill, enemy, state):
        # "ATK_DISTANCE" 攻击距离
        # "HIT_LINE",    生效范围(线),    以我为原点,朝向敌人线性延伸{0｜0}
        # "HIT_RANGE",   生效范围(菱形),  以我为原点延伸{0｜0}
        
        if "ATK_DISTANCE" not in back_skill.avaliable_effects(): # 没有攻击距离
            return True
        else: #有攻击距离 
            effect = back_skill.get_effect_by_key("ATK_DISTANCE")
            l_in_range,r_in_range,cross_in_range = False, False, False
            # 高度影响攻击范围, 高低差每{0}格，最大攻击范围加{0}格, 暂时不处理
            # if "ADD_ATK_DISTANCE" in back_skill.avaliable_effects():
            #     pass
            if "HIT_LINE" in back_skill.avaliable_effects():
                _eff = back_skill.get_effect_by_key("HIT_LINE")
                range_line_value =  _eff.param[1] + 1
                l_in_range = self.is_in_hitline_range(range_line_value,  enemy, state)
            if "HIT_RANGE" in back_skill.avaliable_effects(): # 高度影响范围
                _eff = back_skill.get_effect_by_key("HIT_RANGE")
                gap, radis = _eff.param[0], _eff.param[1] 
                r_in_range = self.is_in_hit_range(gap, radis, enemy, state)
            if "HIT_LINE" not in back_skill.avaliable_effects() and\
                "HIT_RANGE" not in back_skill.avaliable_effects():# 自己为中心点，十字x格
                gap, radis = effect.param[0], effect.param[1] 
                cross_in_range = self.is_in_hitcross_range(int(gap), int(radis), enemy, state)
            if not l_in_range and not r_in_range and not cross_in_range: # 没有在范围内
                return False
            else:
                if "CHANGE_ATK_DISTANCE" in back_skill.avaliable_effects(): # 攻击范围限制高度，高低差{0}内生效
                    _eff = back_skill.get_effect_by_key("CHANGE_ATK_DISTANCE")
                    if abs(enemy.y - self.y) <= int(_eff.param[0]):
                        return True
                    else:
                        return False
                else: # 没有高度影响范围
                    return True
        return True
    
    @staticmethod
    def effect_format_data(hero_or_monster, effect_id):
        return {
                    "role":  hero_or_monster.hero_or_monster().lower(),
                    "role_id": hero_or_monster.HeroID,
                    "effect_id": effect_id
                }
    
    def __damage(self, attacker, defender, skill, unit_num):  # 计算伤害 
        _res = damage(attacker=attacker, defender=defender, skill=skill, unit_num=unit_num) 
        for _ in _res: # 向上取整
            _["damage"] = round_up_2_integer(_["damage"])
            _["pre_damage"] = round_up_2_integer(_["pre_damage"])
        return _res
        
    def back_attack(self, enemy, skill=None, attack_point=[]):
        """ 反击
            @enemys       被攻击敌人对象列表
            @skill        使用的技能对象
            @attack_point 技能释放点位
        """

        def back_format_data(res, skill, attack_point, effect_ids):
            return {
                    "action_type" : f"SKILL_{skill.SkillId}",
                    "atk_range": [tuple(attack_point)],  # 攻击范围
                    "atk_position": tuple(attack_point), # 攻击位置
                    "release_range": [tuple(attack_point)], # 释放范围
                    "damage": res, 
                    "effects": [Hero.effect_format_data(enemy, _) for _ in effect_ids],
                    "id": self.HeroID,
                    "class": self.hero_or_monster().lower()
                }
             
        print(self.HeroID ,"(^ ^)反击(^ ^)")
        effect_ids = self.prepare_attack(skill)  # 做攻击之前，加载skill相关
        _res = self.__damage(attacker=self, defender=enemy, skill=skill, unit_num=1)
        enemy.Hp_damage(_res) # 敌人掉血攻击
        return back_format_data(_res, skill, attack_point, effect_ids)
    
    def __atk_enemy(self, enemy, skill, attack_point, state): # 攻击敌人
        result = {"damage":None, "back_attck":None}
        effect_ids = enemy.before_be_attacked(skill) # 被攻击者添加被动skill
        unit_num = self.__get_unit_num(skill=skill, state=state)
        _res = self.__damage(attacker=self, defender=enemy, skill=skill, unit_num=unit_num) # 需要damage 判断是否由于被动技能，是攻击无效
        # 添加被动技能的effect
        for each_id in effect_ids:
            _res[0]["effects"].append(Hero.effect_format_data(enemy, each_id))
        miss_effect_id, is_miss = enemy.is_miss_hit(skill)
        if is_miss: # 被动技能使攻击失效 # TODO 彬哥 
            _res[0]["effects"].append(Hero.effect_format_data(enemy, miss_effect_id))
            for _ in _res:
                _["damage"] = 0
            result["damage"] = copy.deepcopy(_res)
            print(f"~~~~ {enemy.HeroID} 的被动技能使攻击无效～", _res)
            return result
        result["damage"] = copy.deepcopy(_res)
        enemy.Hp_damage(_res) # 敌人掉血攻击
        if enemy.is_death:
            enemy.leve_game(state)
            return result
        else: # 没有被打死，可以发动反击
            for each_back_skill in enemy.get_back_skills(self, skill): # 发动反击
                print("use back skill:", each_back_skill.SkillId)
                if enemy.is_in_backskill_range(each_back_skill, self, state):
                    result["back_attck"] = enemy.back_attack(enemy=self, skill=each_back_skill, attack_point=self.position)
                    print("end back....")
                else:
                    print("not in backskill range ")
        enemy.after_be_attacked(skill) # 被攻击者添加被动skill
        return result
    
    def __atk_attachment(self, enemy, skill, attack_point, state): # 攻击附着物
        map_obj = state.get("maps")
        return map_obj.attack_attachment(wage_object=self, skill=skill, attachment=enemy, stats=state)

    def func_attack(self, enemys=[], skill=None, attack_point=[], state={}): #技能攻击
        """
            @enemys       被攻击敌人对象列表
            @skill        使用的技能对象
            @attack_point 技能释放点位
            @map_obj map_obj
        """
        # TODO 调用攻击伤害函数
        # self 自己属性的改表
        # 敌人属性的改变
        # 地块的改变
        result = {}
        self.prepare_attack(skill)  # 做攻击之前，加载skill相关
        for each in enemys:
            if self.is_death: # 死亡了
                self.leve_game(state)
                break
            
            if isinstance(each, Attachment):
                result[each] = self.__atk_attachment(each, skill, attack_point, state)
            else:
                print("攻击敌人")
                result[each] = self.__atk_enemy(each, skill, attack_point, state)

        self.after_atk_skill(enemys=enemys, skill=skill, attack_point=attack_point, state=state)
        return result
    
    def friend_treatment(self, friends=[], skill=None, attack_point=[], state=[]): # 对队友释放治疗技能
        """
            @friends      治疗的对象列表
            @skill        使用的技能对象
            @state        
        """
        # 敌人属性的改变
        # 地块的改变
        result = {}
        for each in friends:
            _res = heal(caster=self, target=each, skill=skill)
            for _ in _res: # 向上取整
                _["heal"] = round_up_2_integer(_["heal"])
                _["pre_heal"] = round_up_2_integer(_["pre_heal"])
            print(_res)
            result[each] = copy.deepcopy(_res)
            # TODO
            each.Hp_add(_res)
        self.after_medical_skill(friends, skill, state)
        return result
    
    def trigger_buff(self, buff_dic): # 有些技能需要主动出发执行，比如 BUFF_ADD_HP
        result = buff_dic.get("buff").make_effective(self)
        buff_dic["damage"] = [result,]
        return buff_dic

    def open_box(self, box_object, state):
        map_obj = state.get("maps")
        map_obj.open_box(box_object)
        return self