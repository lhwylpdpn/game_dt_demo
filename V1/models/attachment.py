# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-10-25
"""
import copy
import random
from .effect import Effect
from collections import Counter

ATTACHMENT_COMPARE = {
    31: "炸药桶",
    35: "炸药桶碎片",
    32: "宝箱",
    34: "拒马"
}


class AttachmentHelper():
    
    @staticmethod
    def create_attachment(example_attments, dst_att_sn):
        for each in example_attments:
            if each.sn == dst_att_sn:
                new_att =  copy.deepcopy(each)
                new_att.set_id(int(random.random() * 100000000))
                return new_att
        return None


class Attachment():
    
    def __init__(self, **kwargs):
        self.__id = kwargs.get("id", None)
        self.__sn = kwargs.get("sn", None)                                    # sn
        self.__position = kwargs.get("position", [])
        self.__effects = kwargs.get("effects", [])
        self.__Layer = kwargs.get("Layer", None)
        self.__Block = kwargs.get("Block", 0)          
        self.__Ap = kwargs.get("Ap", 0)
        self.__Selected = kwargs.get("Selected", 0)                         # 是否可以被攻击
        self.__DestroyEffect = kwargs.get("DestroyEffect", 0)               # 物品的HP
        self.__ExcludePlot = kwargs.get("ExcludePlot", [])
        self.__is_need_timer = True if self.__sn == 35 else False            # 是否需要 计数
        self.__focus_object = []                                            # 计数器，先放置每次 focus 的(英雄) ID

    def dict(self):
        fields = ["id", "sn", "position", "effects", "Layer", "Block", "Ap", "Selected", "DestroyEffect", "ExcludePlot"]
        data = {}
        if "effects" in fields:
            data["effects"] = {}
            fields.remove("effects")
            for each in self.__effects:
                data["effects"][each.key] = each.dict()
        data.update({field:self.__getattribute__(field) for field in fields})
        return data

    def is_box(self): # 判断是不是 宝箱
        return self.sn == 32
    
    def is_fire(self): # 判断是不是 火 火药桶碎片
        return self.sn == 35
    
    def is_bomb(self): # 判断是不是 炸药桶
        return self.sn == 31
    
    def is_horse(self): # 判断是不是 拒马
        return self.sn == 34 

    def is_alive(self): # 判断是否还存在
        return self.DestroyEffect > 0
    
    @property
    def is_death(self): # 判断是否死了
        return not self.is_alive()
    
    def is_can_selected(self): # 判断自己是否可以被选中
        return self.Selected == 1
    
    def box_open_distance(self): # 获取宝箱的开启距离
        if self.is_box():
            return self.get_effect_by_key("OPEN_DISTANCE").param
        else:
            return None
    
    def avaliable_effects(self): # 当前attachment有哪些效果
        return [each.key for each in self.__effects]
        
    @property
    def sn(self): # 
        return self.__sn
    
    def set_sn(self, sn_new):
        self.__sn = sn_new
        return self 
    
    @property
    def id(self): # 
        return self.__id
    
    def set_id(self, id_new):
        self.__id = id_new
        return self
    
    @property
    def position(self): # 
        return self.__position
    
    def set_position(self, position_new):
        self.__position = position_new
        return self 
    
    @property
    def x(self):
        return self.__position[0]
    
    @property
    def y(self):
        return self.__position[1]
    
    @property
    def z(self):
        return self.__position[2]
    
    @property
    def effects(self): # 
        return self.__effects
    
    def set_effects(self, effects_new):
        self.__effects = effects_new
        return self 
    
    def add_effect(self, new_effect):
        self.__effects.append(new_effect)
        # 技能按照优先级排序
        self.__effects = sorted(self.__effects, key=lambda x:x.Priority, reverse=True) 
        return self
    
    def del_effect(self, effect):
        self.__effects.remove(effect)
        return self
    
    @property
    def Layer(self): # 
        return self.__Layer
    
    def set_Layer(self, Layer_new):
        self.__Layer = Layer_new
        return self
    
    @property
    def Block(self): # 
        return self.__Block
    
    def set_Block(self, Block_new):
        self.__Block = Block_new
        return self
        
    @property
    def Ap(self): # 
        return self.__Ap
    
    def set_Ap(self, Ap_new):
        self.__Ap = Ap_new
        return self
    
    @property
    def Selected(self): # 
        return self.__Selected
    
    def set_Selected(self, Selected_new):
        self.__Selected = Selected_new
        return self
    
    @property
    def DestroyEffect(self): # 
        return self.__DestroyEffect
    
    def set_DestroyEffect(self, DestroyEffect_new):
        self.__DestroyEffect = DestroyEffect_new
        return self 
        
    @property
    def ExcludePlot(self): # 
        return self.__ExcludePlot
    
    def set_ExcludePlot(self, ExcludePlot_new):
        self.__ExcludePlot= ExcludePlot_new
        return self 
    
    def is_need_timer(self):                     # 收否需要存活计数
        return self.__is_need_timer
    
    # 获取存活了多少 roundaction, 最慢的那个hero or monster被选中的次数
    def __del_get_lived_round(self, h_m_objects):   # 暂时废弃
        if self.is_need_timer():
            if self.__focus_object:
                counter = Counter(self.__focus_object)
                __round = []
                for each_h_m in h_m_objects:
                    if each_h_m.is_alive():
                        __round.append(counter.get(each_h_m, 0))
                return min(__round)
        return None

    # 获取存活了多少 roundaction， 总体被选中的次数/所有活着的
    def get_lived_round(self, h_m_objects):      
        if self.is_need_timer():
            if self.__focus_object:
                live_obj = []
                for each_h_m in h_m_objects:
                    if each_h_m.is_alive:
                        live_obj.append(each_h_m)
                live_round = len(self.__focus_object)  / len(live_obj)
                return live_round
        return None

    def get_fire_round_action(self):
        """
        炸药桶碎片 火 应该存活的时间
        """
        if self.is_fire():
            return int(self.get_effect_by_key("DEBUFF_PLOT_FIRE").param[1])
        return None
    
    def get_damage(self): # 普通伤害 (都不产生伤害， hero 和 monster 挂上 debuff)
        """
        伤害 
        """
        # if self.is_fire(): # 火的伤害
        #     return int(self.get_effect_by_key("DEBUFF_PLOT_FIRE").param[0])
        return 0
       
    def focus_object(self, m_h_obj):
        if self.is_need_timer():
            self.__focus_object.append(m_h_obj.HeroID)
        return self

    def unfocus_object(self, h_m_objects):
        if self.is_need_timer():
            if self.get_lived_round(h_m_objects) >= self.get_fire_round_action(): # 存活的时间超过了
                self.set_DestroyEffect(0) # 设置Hp为0 
        return self

    def get_effect_by_key(self, key):
        for each in self.__effects:
            if each.key == key:
                return each
        print(f"Warn: {key} not exit in skill {self.SkillId}, so return None")
        return None
    
    def open(self): # 开宝箱
        if self.is_box():
            print("Open Box !!!!!")
        return self
    
    def before_attacked(self, wage_object, skill, **kwargs): # 被攻击前的准备（预留）
        return self
    
    def after_attacked(self, wage_object, skill, **kwargs):  # 被攻击之后的反应 （预留）
        return self
    
    def be_attacked(self, wage_object, skill, damage_res): # 被攻击
        """
        wage_object 发动攻击对象
        skill       使用的技能
        damage_res  造成的伤害
        """
        #if self.is_horse() or self.is_bomb(): # 拒马和火药桶
        if self.is_can_selected(): # 可以被选中，就可以被伤害
            print(f"Attachment be aattacked. {self.sn}")
            self.before_attacked(wage_object, skill)
            print(f"Attachment be aattacked. Before Hp:{self.DestroyEffect}")
            damage = sum([_.get("damage") for _ in damage_res])
            print(f"Attachment be aattacked. damage:{damage}") 
            _t_hp = self.DestroyEffect - damage
            self.set_DestroyEffect(float("%.2f"%_t_hp) if _t_hp >= 0 else 0) # 血量
            print(f"Attachment be aattacked. Dst Hp:{self.DestroyEffect}")
            self.after_attacked(wage_object, skill)
        else:
            print("不可以被选择，不可以被攻击。")
        return self

    def get_bomb_attack_effect(self): # 返回打击的 effect
        if self.is_bomb():
            return self.get_effect_by_key("HIT_SQUARE")
        return None
    
    def get_bomb_fragment_effect(self): # 爆炸碎片效果
        if self.is_bomb():
            return self.get_effect_by_key("CREATE_PLOT_SQUARE")
        return None
    
    def back_damage(self): # 附着物被打时候，产生的被动伤害
        if self.is_bomb() and (not self.is_alive()) : # 火药桶被打爆时候伤害
            return int(self.get_effect_by_key("ATK_BOMB").param[0])
        # 其他附着物的伤害为 0 
        return 0
    
    def move_position(self, x,y,z): # 附件安排新位置
        # TODO
        return self
    
    def buff_data_for_hmobject(self):  # 由于被加载进地块，对地块上的hero or monster 产生 buff
        if self.is_fire(): # 火时候，产生一个debuff
            effect = self.get_effect_by_key("DEBUFF_PLOT_FIRE")
            buff_data = {
                "buff_id" : effect.id,  
                "buff_key" : effect.key, 
                "param" : effect.param, 
                "buff_percent" : None, 
                "BuffType": effect.BuffType
                }
            return buff_data
        else:
            return None
