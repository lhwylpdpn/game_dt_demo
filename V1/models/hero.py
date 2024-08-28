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
# from utils.transposition import trans_postion
from utils.tools import random_choices
from .map import Map, Land
from .buff import Buff
from .teamflag import TeamFlag

class Hero():
    
    def __init__(self, **kwargs):
        # 初始数据留存为后续重新初始化做准备
        # 行动力增加自增的函数
        # 移动 - 连带地块对hero属性营销
        # 攻击地块，敌人 - 连带地块
        #
        # skill攻击 - 地块，敌人
        # buff 

        # 基本属性
        self.__HeroID = int(kwargs.get("HeroID", None))
        self.__protagonist = kwargs.get("protagonist", 0)          # 是否是主角
        self.__AvailableSkills = kwargs.get("AvailableSkills", []) # 可用的技能     #
        self.__RoundAction = kwargs.get("RoundAction", None)       # 行动步数
        self.__JumpHeight = kwargs.get("JumpHeight", [])           # 跳跃的高度 
        self.__skills =  kwargs.get("skills", [])                  # 技能
        self.__DogBase = kwargs.get("DogBase", None)               # 警戒-初始
        self.__BaseClassID = kwargs.get("BaseClassID", None)           # 职业
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
        # self.__position = list(trans_postion(*kwargs.get("position")))       #  坐标
        self.__position = kwargs.get("position")                               #  坐标
        self.__avali_move_p_list = kwargs.get("avali_move_p_list", [])         #  可移动范围
        self.__shoot_p_list = kwargs.get("shoot_p_list", [])                   #  可攻击范围
        self.__atk_effect_p_list = kwargs.get("atk_effect_p_list", [])         #  攻击效果范围

        #### buff
        self.__buff = []                                                       # 带的buff

        self.fields =  ["HeroID", "protagonist", "AvailableSkills", "RoundAction", "JumpHeight", "skills",
            "DogBase", "BaseClassID",  "Hp", "HpBase", "Atk",  "Def", "MagicalAtk",
            "MagicalDef",  "Agile",  "Velocity", "Quality", "team",
            "Luck", "position", 
            "avali_move_p_list", "shoot_p_list", "atk_effect_p_list"
            ]
        ### unit_hero
        self.__unit_skill_buff = []                                             # 连携攻击增加的buf(每行动一次，重新组织一次此数据)
        self.__Block = 2                                                        # 地块站立的属性 hero 为2， monster 为 3

    def hero_or_monster(self):
        "HERO or MONSER"
        return self.__class__.__name__.upper()
    
    def get_fields(self):
        return self.fields
    
    def join_game(self, state, init_position=True): # 进入战局
        self.move_position(*self.position, state, init_position)
        return self

    def leve_game(self, state): # 退出战局
        map_obj = state.get('maps')
        map_obj.set_land_pass(*self.position)
        self.team.leve_game(self)
        print(f"{self.HeroID} is Killed, leve game.")
        return self

    def dict(self, fields=[], for_view=False):
        if not fields:
            fields = copy.deepcopy(self.fields)
        data = {}
        if "skills" in fields:
            data["skills"] = []
            fields.remove("skills")
            for each in self.__skills:
                data["skills"].append(each.dict(for_view=for_view))
        data.update({field: self.__getattribute__(field) for field in fields})
        if "team" in fields:
            if self.team:
                data["team"] = self.team.dict()
            else:
                data["team"] = []
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
    def team(self): # 
        return self.__team
    
    def set_team(self, v):
        self.__team = v
        return self
    
    @property
    def Quality(self):
        return self.__Quality

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
    def JumpHeight(self):
        return self.__JumpHeight
    
    def set_JumpHeight(self, JumpHeight):
        self.__JumpHeight = JumpHeight
        return self
    
    @property
    def skills(self):
        return self.__skills
    
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
    
    @property
    def Hp(self):
        return self.__Hp
    
    def set_Hp(self, Hp):
        self.__Hp = Hp
        return self
    
    @property
    def AtkBase(self):
        return self.__AtkBase

    @property
    def Atk(self):
        return self.__Atk
    
    def set_Atk(self, Atk):
        self.__Atk = Atk
        return self
    
    @property
    def DefBase(self):
        return self.__DefBase

    @property
    def Def(self):
        return self.__Def
    
    def set_Def(self, Def):
        self.__Def = Def
        return self

    @property
    def MagicalAtkBase(self):
        return self.__MagicalAtkBase

    @property
    def MagicalAtk(self):
        return self.__MagicalAtk
    
    def set_MagicalAtk(self, v):
        self.__MagicalAtk = v
        return self
    
    @property
    def MagicalDefBase(self):
        return self.__MagicalDefBase
    
    @property
    def MagicalDef(self):
        return self.__MagicalDef
    
    def set_MagicalDef(self, MagicalDef):
        self.__MagicalDef = MagicalDef
        return self
    
    @property
    def AgileBase(self):
        return self.__AgileBase

    @property
    def Agile(self):
        return self.__Agile
    
    def set_Agile(self, Agile):
        self.__Agile = Agile
        return self
    
    @property
    def VelocityBase(self):
        return self.__VelocityBase

    @property
    def Velocity(self):
        return self.__Velocity
    
    def set_Velocity(self, Velocity):
        self.__Velocity = Velocity
        return self

    @property
    def BaseClassID(self):
        return self.__BaseClassID
    
    def set_BaseClassID(self, v):
        self.__BaseClassID = BaseClassID
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
                        land = map_object.get_land_from_xz(p_x, p_z)
                        drange.append(tuple([p_x, land.y, p_z]))
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
    
    @property
    def BUFF_HIT_RATE(self): # 增加{0}的命中率
        value = None
        for each in self.__buff:
            if each.buff_key == "BUFF_HIT_RATE":
                if value is not None:
                    value += int(each.buff_value)
                else:
                    value = int(each.buff_value)
        return value

    @property
    def BUFF_MISS_HIT(self): # {0}%机率使攻击无效，并持续{0}行动回合
        value = None
        for each in self.__buff:
            if each.__buff_key == "BUFF_MISS_HIT":
                if value is not None:
                    value += int(each.buff_value)
                else:
                    value = int(each.buff_value)
        return value

    @property
    def BUFF_MAX_ATK_DISTANCE(self): # 攻击范围最大值增加{0}格，并持续{0}行动回合
        value = None
        for each in self.__buff:
            if each.__buff_key == "BUFF_MAX_ATK_DISTANCE":
                if value is not None:
                    value += int(each.buff_value)
                else:
                    value = int(each.buff_value)
        return value

    def add_buff(self, buff_key, param): # 增加普通buff
        buff = Buff.create_buff(self, buff_key, param)
        buff.make_effective(self) # buff生效
        self.__buff.append(buff)
        return self

    def check_buff(self): # 回合结束后，检查buff的加成
        for each in self.__buff:
            if not each.is_avaliable:
                each.make_invalid(self)
                self.__buff.remove(each)
        return self
    
    def add_unit_buff(self, buff_key, param): # 增加连携buff
        buff = Buff.create_buff(self, buff_key, param)
        buff.make_effective(self)
        self.__unit_skill_buff.append(buff)
        return self
    
    def remove_unit_buff(self, state): # 去除连携buff
        friends = state['hero'] if self in state['hero'] else state['monster'] # 找到己方的所有人
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
        if not self.is_alive():
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
        map_obj.set_land_pass(*self.position)             # 出发地块设置为可通过
        map_obj.set_land_no_pass(x,y,z, self.Block)       # 抵达地块设置为不可通过
        self.set_x(x).set_y(y).set_z(z)       # 设置新位置
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
    
    def get_inactive_Skills(self): # 获取主动 1 or 被动技能 0
        skill = []
        for _ in self.__skills:
            if not _.is_active_skill():
                skill.append(_)
        return skill
    
    def get_back_skills(self, enemy, attach_skill): # 获取反击技能
        skill = []
        for _ in self.get_inactive_Skills():
            if "ATK_BACK" in _.avaliable_effects() and ("IS_HIT" in _.avaliable_effects() or "IS_DEFAULT_HIT" in _.avaliable_effects()):
                # 是默认技能， 默认技能攻击时候触发
                if int(attach_skill.DefaultSkills) == 1 and "IS_DEFAULT_HIT" in _.avaliable_effects():
                    skill.append(_)
                # 不是默认技能，其他技能攻击时候触发
                if int(attach_skill.DefaultSkills) == 0 and "IS_DEFAULT_HIT"  not in _.avaliable_effects():
                    skill.append(_)
            if "DEBUFF_ROUND_ACTION_BACK" in _.avaliable_effects() and "IS_HIT" in _.avaliable_effects():
                effect = _.get_effect_by_key("DEBUFF_ROUND_ACTION_BACK")
                if random_choices({True:int(effect.param[0])/100.0, False:1 - int(effect.param[0])/100.0}): # 几率判断
                    enemy.add_buff(buff_key="DEBUFF_ROUND_ACTION_BACK", param=effect.param[1:])
        return skill

    def load_init_unActiveSkill(self): # load  buff
        # 初始的时候，增加非主动，非被动触发的技能, 不是被普通攻击 , 不是连携
        for each_skill in self.get_inactive_Skills():
            if each_skill.is_buff(): 
                for each in each_skill.effects:
                    self.add_buff(buff_key=each.key, param=each.param)
        return self

    def get_unit_skill(self): # 获取连携攻击
        unit_skills = []
        for each_skill in self.get_inactive_Skills():
            if each_skill.is_unit_skill(): 
               unit_skills.append(each_skill)
        return unit_skills
                
    def load_unit_buff(self, state): # 加载连携攻击
        # 我身边的位置 几格之内有队友
        """
        @ value 几格
        @ state 场景 {"hero":{}, "monster":{}, "maps": map}
        """
        friends = state['hero'] if self in state['hero'] else state['monster'] # 找到己方的所有人
        for each in friends:
            unit_skill = each.get_unit_skill() # 获取连携攻击
            for each_skill in unit_skill:
                # 确定连携的范围
                buff_range = each_skill.get_effect_by_key("ADD_BUFF_RANGE")
                if buff_range is None: buff_range = 0
                else: buff_range = buff_range.param[1]
                near_friends = self.__search_near_friends(buff_range, friends)
                if len(near_friends) >1: # 多于一个人才可以连携 (自己一个人不算哈)
                    for friend in near_friends:
                        for e_skill in each_skill.effects:
                            friend.add_unit_buff(buff_key=e_skill.key, param=e_skill.param)
        return                
                    
    def __search_near_friends(self, range, friends):
        near_friends = []
        for each in friends:
            if abs(self.x - each.x) + abs(self.z - each.z) <= int(range): # 在范围内
                near_friends.append(each)
        return near_friends                 
        
    def prepare_attack(self, skill): # 被攻击之前，加载主动技能 (作为 施动者 )
        skill.make_effective(self)
        return self

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

    def skill_move_to_position(self, target, value, state): # 自己走向 target 点 
        map_obj = state.get("maps")
        move_value = int(value[0])
        print(f"{self.HeroID} 计划从{self.position} 走向 {target.position} 方向 {move_value} 步")
        position_ok = None
        move_x, move_y, move_z = None, None, None
        total_step = move_value
        direction = self.judge_direction(target)
        if direction == "OTHER":
            print("不在十字位置，不移动")
            return self
        while move_value:
            move_x, move_y, move_z = self.position
            if direction == "UP":
                move_z = move_z + move_value # 我的z减小
            elif direction == "DOWN":
                move_z = move_z - move_value
            elif direction == "RIGHT":
                move_x = move_x + move_value
            elif direction == "LEFT":
                move_x = move_x - move_value
            else:
                pass
            move_x, move_z  = map_obj.correct_map_bonus(move_x, move_z)
            move_y = map_obj.get_land_from_xz(move_x, move_z).y
            if self.is_position_ok(move_x, move_y, move_z, state):
                total_step = move_value if position_ok is None else total_step
                position_ok = [move_x, move_y, move_z] if position_ok is None else position_ok
            else:
                position_ok = None
            print(f" >>移动 {move_value}步数 , 落点[{move_x, move_y, move_z}]", self.is_position_ok(move_x, move_y, move_z, state))
            move_value = move_value - 1
        if position_ok and tuple([move_x, move_y, move_z]) != tuple(self.position):
            print(f"{self.HeroID} 实际从{self.position} 走向 {target.position} 方向 {total_step} 步, 到达 {position_ok} 点")
            self.move_position(*position_ok, state)
        else:
            print(f"{self.HeroID} 实际从{self.position} 走向 {target.position} 方向 0 步")
        return self
    
    def move_back(self, enemy, move_value, state): # 敌人的攻击使我后退x格
        map_obj = state.get('maps')
        move_value = int(move_value[0])
        print(f"{self.HeroID} 计划从{self.position}后退 {move_value} 步, 此时敌人位置{enemy.position}")
        position_ok = None
        move_x, move_y, move_z = None, None, None
        total_step = move_value
        direction = self.judge_direction(enemy)
        if direction == "OTHER":
            print("不在十字位置，不移动")
            return self
        while move_value:
            move_x, move_y, move_z = self.position
            if direction == "UP":
                move_z = move_z - move_value 
            elif direction == "DOWN":
                move_z = move_z + move_value
            elif direction == "RIGHT": # 敌人在右侧, 我向左侧走
                move_x = move_x - move_value
            elif direction == "LEFT":  # 敌人在左侧, 我向右侧走
                move_x = move_x + move_value
            else:
                pass
            move_x, move_z  = map_obj.correct_map_bonus(move_x, move_z)
            move_y = map_obj.get_land_from_xz(move_x, move_z).y
            if self.is_position_ok(move_x, move_y, move_z, state):
                total_step = move_value if position_ok is None else total_step
                position_ok = [move_x, move_y, move_z] if position_ok is None else position_ok
            else:
                position_ok = None
            print(f" >>移动 {move_value}步数 , 落点[{move_x, move_y, move_z}]", self.is_position_ok(move_x, move_y, move_z, state))
            move_value = move_value - 1
        if position_ok and tuple([move_x, move_y, move_z]) != tuple(self.position):
            print(f"{self.HeroID} 实际从 {self.position} 后退 {total_step} 步,后退 {position_ok} 点")
            self.move_position(*position_ok, state)
        else:
            print(f"{self.HeroID} 实际从{self.position} 后退 0 步")
        return self
    
    def use_skill(self, enemys=[], skill=None, attack_point=[], state=None): # 使用技能后
        if not skill.use_skill(self).is_avaliable(): # 使用次数减少 后 判断技能是否还是可用的
            self.__AvailableSkills.remove(skill.skillId)
        enemy = None
        for each_e in enemys: # 只有技能落点的敌人移动
            if tuple(each_e.position) == tuple(attack_point):
                enemy = each_e
                continue
        if enemy is None:
            return self
        map_obj = state.get("maps")
        # 判断自己是否向敌人移动 #TODO
        if "MOVE_SELF2TARGET" in skill.avaliable_effects():
            print("use: MOVE_SELF2TARGET 自己向敌人移动")
            move_value = skill.get_effect_by_key("MOVE_SELF2TARGET").param # 移动距离
            self.skill_move_to_position(target=enemy, value=move_value, state=state)
        # 判断敌人是否向自己移动 
        if "MOVE_TARGET2SELF" in skill.avaliable_effects():
            print("use: MOVE_TARGET2SELF 敌人向自己移动")
            move_value = skill.get_effect_by_key("MOVE_TARGET2SELF").param # 移动距离
            enemy.skill_move_to_position(target=self, value=move_value, state=state)
        # 击退几格
        if "REPEL_TARGET" in skill.avaliable_effects():
            print("use: REPEL_TARGET 被击退几格")
            move_value = skill.get_effect_by_key("REPEL_TARGET").param # 移动距离
            enemy.move_back(self, move_value, state)
        return self

    def before_be_attacked(self, skill):           # 被攻击之前，加载被动技能(作为被攻击对象)
        for each_skill in self.get_inactive_Skills():
            if "IS_HIT" in each_skill.avaliable_effects() : # 被动触发的技能
                if "IS_DEFAULT_HIT" in each_skill.avaliable_effects(): # 被默认技能攻击
                    if int(skill.DefaultSkills) == 1: # 技能是默认技能
                        each_skill.make_effective(self)
                else: # 不是被默认攻击时候出发
                    if int(skill.DefaultSkills) == 0: # 技能不是默认技能
                        each_skill.make_effective(self)
        return self
    
    def reduce_buff_round_action(self): # 每次行动后，减少buff中的round_action
        for each in self.__buff:
            each.reduce_round_action()
        return self

    def dont_move(self): # 移动不移动
        self.check_buff()                                       # 减少buff
        for each_skill in self.get_inactive_Skills():
            if "IS_HIT" not in each_skill.avaliable_effects():  # 非被动触发的技能
                if "IS_WAIT" in each_skill.avaliable_effects(): # 不移动
                    each_skill.make_effective(self)
        self.reduce_buff_round_action()
        return self
    
    # 被动技能使攻击失效
    def is_miss_hit(self):
        for each_skill in self.get_inactive_Skills():
            if "IS_DEFAULT_HIT" in each_skill.avaliable_effects() and\
               "BUFF_MISS_HIT" in each_skill.avaliable_effects():
               effect = each_skill.get_effect_by_key("BUFF_MISS_HIT")
               return random_choices({True:int(effect.param[0])/100.0, False:1 - int(effect.param[0])/100.0})
        return False
    
    def is_in_hitline_range(self, range_line_value,  enemy, state): # 
        """
        range_line_value 以我为原点,朝向敌人线性延伸{0｜0}
        enemy 目标敌人，即方向
        """
        map_obj = state.get("maps")
        if self.judge_direction(enemy) in ("UP", "DOWN", "LEFT", "RIGHT"):
            if abs(self.x - enemy.x) + abs(self.z - enemy.z) <= int(range_line_value): # 在范围内
                return True
        return False
 
    def is_in_hit_range(self, gap, radis, enemy, state):
        map_obj = state.get("maps")
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
            map_obj = state.get("maps")
            effect = back_skill.get_effect_by_key("ATK_DISTANCE")
            atk_distance = effect.param[1]
            l_in_range,r_in_range = False, False
            # 高度影响攻击范围, 高低差每{0}格，最大攻击范围加{0}格, 暂时不处理
            # if "ADD_ATK_DISTANCE" in back_skill.avaliable_effects():
            #     pass
            if "HIT_LINE" in back_skill.avaliable_effects():
                _eff = back_skill.get_effect_by_key("HIT_LINE")
                range_line_value =  _eff.param[1] + 1
                l_in_range = self.is_in_hitline_range(range_line_value,  enemy, state)
            if "HIT_RANGE" in back_skill.avaliable_effects(): # 高度影响范围
                _eff = back_skill.get_effect_by_key("HIT_LINE")
                gap, radis = _eff.param[0], _eff.param[1] 
                r_in_range = self.is_in_hit_range(gap, radis, enemy, state)
            if not l_in_range and not r_in_range: # 没有在范围内
                return False
            else:
                if "IS_ATK_DISTANCE" in back_skill.avaliable_effects(): # 攻击范围限制高度，高低差{0}内生效
                    _eff = back_skill.get_effect_by_key("IS_ATK_DISTANCE")
                    if abs(enemy.y - self.y) <= _eff.param[0]:
                        return True
                    else:
                        return False
                else: # 没有高度影响范围
                    return True
        return True

    def func_attack(self, enemys=[], skill=None, attack_point=[], state={}, is_back_atk=False): #技能攻击
        """
            @enemys       被攻击敌人对象列表
            @skill        使用的技能对象
            @attack_point 技能释放点位
            @map_obj map_obj
            is_back_atk 是不是反击
        """
        # TODO 调用攻击伤害函数
        # self 自己属性的改表
        # 敌人属性的改变
        # 地块的改变
        result = {}
        self.check_buff()           # 减少buff
        self.prepare_attack(skill)  # 做攻击之前，加载skill相关
        for each in enemys:
            if self.is_death: # 死亡了
                self.leve_game(state)
                return
            if not is_back_atk:
                if each.is_miss_hit():
                    print(f"** {each.HeroID} 的被动技能使攻击无效～")
                    continue
            each.before_be_attacked(skill) # 被攻击者添加被动skill
            result = damage(attacker=self, defender=each, skill=skill)
            result[each] = copy.deepcopy(result)
            _t_hp = each.Hp - result.get("damage")
            print("(^ ^)反击(^ ^)" if is_back_atk else "攻击")
            print(each.HeroID ,"Hp <before>: ", each.Hp)
            print(each.HeroID ,"Hp <damaeg>: ", result)
            each.set_Hp(float("%.2f"%_t_hp) if _t_hp >= 0 else 0) # 血量
            print(each.HeroID ,"Hp <after>: ", each.Hp)
            if each.is_death:
                each.leve_game(state)
                continue
            if not is_back_atk and each.is_alive: # 不是反击攻击， 并且没有被打死，可以发动反击
                for each_back_skill in each.get_back_skills(self, skill): # 发动反击
                    if self.is_in_backskill_range(each_back_skill, self, state):
                        each.func_attack(enemys=[self], skill=each_back_skill, 
                                         attack_point=self.position, state=state, is_back_atk=True)
        self.use_skill(enemys=enemys, skill=skill, attack_point=attack_point, state=state)
        self.reduce_buff_round_action() # 减少buff的round action
        return result