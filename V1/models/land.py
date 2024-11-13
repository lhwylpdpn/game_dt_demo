# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-18
"""

from .effect import Effect
from .attachment import Attachment
from .buff import Buff


HEIGHT = 1     # 1 y轴， 2 Z轴
CAN_PASS = 0


class Land(): # 地块
    
    def __init__(self, **kwargs):
        self.__position = kwargs.get("position", None)                        # 坐标
        self.__sn = kwargs.get("sn", None)                                    # sn
        self.__PlotDescription = kwargs.get("PlotDescription", None)          # 地块描述
        self.__Ap = kwargs.get("Ap", None)                                    # 通过地块的消耗
        self.__Block = kwargs.get("Block", CAN_PASS)                          # 收否可以通过 0可以，其他不可以
        self.__Block_Base = kwargs.get("Block", CAN_PASS)                     # 收否可以通过 0可以，其他不可以
        self.__DestroyEffectsId = kwargs.get("DestroyEffectsId", [])          # 破坏地块效果
        self.__DestroyState = kwargs.get("DestroyState", [])                  # 地块状态
        self.__Selected = kwargs.get("Selected", 0)                           # 是否可以被攻击
        self.__DestroyEffect = kwargs.get("DestroyEffect", 0)                 # 物品的HP
        self.__ExcludePlot = kwargs.get("ExcludePlot", [])                    # 不能在地块上出现的附着物
        self.__effects = kwargs.get("effects", [])
        self.__layer2 = kwargs.get("layer2", None)                            # 地块上的附着物
        self.__layer3 = kwargs.get("layer3", None)                            # 地块上的附着物
        self.__layer4 = kwargs.get("layer4", None)                            # 地块上的附着物
        self.__stand_object = None                                            # 地块上站立的对象
        
        
    def dict(self, fields=[]):
        fields = ["position", "sn", "PlotDescription", "Ap", "Block", "DestroyEffectsId", "DestroyState", "DestroyEffect", "effects", "attachments"]
        data = {}
        if "attachments" in fields:
            data["attachments"] = []
            fields.remove("attachments")
            for each in self.__getattribute__("attachments"):
                if each.is_alive():
                    data["attachments"].append(each.dict())
        data = {field: self.__getattribute__(field) for field in fields}
        return data
    
    def __gt__(self, other):
        if isinstance(other, Land):
            other = other.position[HEIGHT]
        if self.position[HEIGHT] > other:
            return True
        return False
    
    def __lt__(self, other):
        if isinstance(other, Land):
            other = other.position[HEIGHT]
        if self.position[HEIGHT] < other:
            return True
        return False
    
    def __le__(self, other):
        if isinstance(other, Land):
            other = other.position[HEIGHT]
        if self.position[HEIGHT] <= other:
            return True
        return False
    
    def __ge__(self, other):
        if isinstance(other, Land):
            other = other.position[HEIGHT]
        if self.position[HEIGHT] >= other:
            return True
        return False
    
    def __eq__(self, other):
        if isinstance(other, Land):
            other = other.position[HEIGHT]
        if self.position[HEIGHT] == other:
            return True
        return False
        
    @property
    def position(self): # 
        return self.__position
    
    def set_position(self, position):
        self.__position = position
        return self 
    
    @property
    def sn(self): # 
        return self.__sn
    
    def set_sn(self, sn_new):
        self.__sn = sn_new
        return self 
    
    @property
    def PlotDescription(self): # 
        return self.__PlotDescription
    
    def set_PlotDescription(self, v):
        self.__PlotDescription = v
        return self
    
    @property
    def Ap(self): # 
        return self.__Ap
    
    def set_Ap(self, v):
        self.__Ap = v
        return self 
    
    @property
    def Block(self): # 
        self.set_Block()
        return self.__Block
    
    @property
    def Block_Base(self): # 
        return self.__Block_Base

    def set_Block_train(self, v):
        self.__Block = v
        return
    
    def set_Block(self):
        if self.__stand_object: # 站立了英雄ormonster
            self.__Block = self.__stand_object.Block
        else:
            block = self.Block_Base + sum([_.Block for _ in self.attachments])
            self.__Block = 1 if block >=1 else CAN_PASS
        return self 
    
    def is_can_pass(self):
        return self.Block == CAN_PASS
    
    @property
    def DestroyEffectsId(self): # 
        return self.__DestroyEffectsId
    
    def set_DestroyEffectsId(self, v):
        self.__DestroyEffectsId = v
        return self
    
    @property
    def DestroyState(self): # 
        return self.__DestroyState
    
    def set_DestroyState(self, v):
        self.__DestroyState = v
        return self
    
    @property
    def DestroyEffect(self): # 
        return self.__DestroyEffect
    
    def set_DestroyEffect(self, v):
        self.__DestroyEffect = v
        return self
    
    @property
    def stand_object(self): # 
        return self.__stand_object
    
    def set_stand_object(self, v):
        self.__stand_object = v
        self.set_Block()
        if self.__stand_object:
            for _ in self.attachments:
                self.add_buff_for_stand_object(_)       
        return self
    
    @property
    def effects(self): # 
        return self.__effects
    
    def set_effects(self, v):
        self.__effects = v
        return self

    def all_ExcludePlot(self): # 所有的排斥
        all_exclude = []
        for _ in self.attachments:
            all_exclude.extend(_.ExcludePlot)
        all_exclude.extend(self.ExcludePlot)
        return all_exclude

    @property
    def layer2(self): # 
        return self.__layer2
    
    def set_layer2(self, v):
        if isinstance(v, Attachment):
            if v.sn not in self.all_ExcludePlot():
                if isinstance(self.__layer2, Attachment): # 替换旧的
                    self.__layer2.set_DestroyEffect = 0
                self.__layer2 = v
            else:
                print(f"地块层不允许加入该附属物")
                return False
        else:
            self.__layer2 = None
        self.set_Block()
        return self
    
    @property
    def layer3(self): # 
        return self.__layer3
    
    def set_layer3(self, v):
        if isinstance(v, Attachment):
            if v.sn not in self.all_ExcludePlot():
                if isinstance(self.__layer3, Attachment): # 替换旧的
                    self.__layer3.set_DestroyEffect = 0
                self.__layer3 = v
            else:  
                print(f"不可以在当前层加入该附属物")
                return False
        else:
            self.__layer3 = None
        self.set_Block()
        return self
    
    @property
    def layer4(self): # 
        return self.__layer4
    
    def set_layer4(self, v):
        if isinstance(v, Attachment):
            if v.sn not in self.all_ExcludePlot():
                if isinstance(self.__layer3, Attachment): # 替换旧的
                    self.__layer3.set_DestroyEffect = 0
                self.__layer4 = v
            else:  
                print(f"不可以在当前层加入该附属物")
                return False
        else:
            self.__layer3 = None
        self.set_Block()
        return self
    
    @property
    def attachments(self): # 地块2，3，4 层的附着物
        attach = []
        for _ in [self.__layer2, self.__layer3, self.__layer4]:
            if isinstance(_, Attachment):
                attach.append(_)
        return attach
    
    def is_exist_attachment_at_same_layer(self, attachment):
        """ 本地块在 attachment 这层上面是不是存在其他的attachment
        """
        if attachment.Layer == 2:
            return isinstance(self.layer2, Attachment)
        if attachment.Layer == 3:
            return isinstance(self.layer3, Attachment)
        if attachment.Layer == 4:
            return isinstance(self.layer4, Attachment)
    
    def get_attachment_at_same_layer(self, attachment):
        """ 本地块在 attachment 这层上面是不是存在其他的attachment
        """
        if attachment.Layer == 2:
            return self.layer2
        if attachment.Layer == 3:
            return self.layer3
        if attachment.Layer == 4:
            return self.layer4 

    def add_attachment(self, attachment): # 记载附着物
        if attachment.Layer == 2:
            self.set_layer2(attachment)
        elif attachment.Layer == 3:
            self.set_layer3(attachment)
        else:
            #attachment.Layer == 4:
            self.set_layer4(attachment)
    
        self.add_buff_for_stand_object(attachment)

        return self
    
    def del_attachment(self, attachment): # 卸载附着物
        if attachment.Layer == 2:
            return self.set_layer2(None)
        elif attachment.Layer == 3:
            return self.set_layer3(None)
        else:
            #attachment.Layer == 4:
            return self.set_layer4(None)
    
    def add_buff_for_stand_object(self, attachment):
        # 判断是否对站立的
        buff_data = attachment.buff_data_for_hmobject()
        if buff_data and self.stand_object:
            print("对地块上的人增加buff", attachment, self.stand_object)
            print([_.buff_key for _ in self.stand_object.buff], self.stand_object.Hp)
            self.stand_object.add_buff(**buff_data)
            print([_.buff_key for _ in self.stand_object.buff], self.stand_object.Hp)
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
        if self.Selected == 1: # 不能被选择，就不可以被攻击（修改血量）
            self.__DestroyEffect = DestroyEffect_new
        return self 
        
    @property
    def ExcludePlot(self): # 
        return self.__ExcludePlot
    
    def set_ExcludePlot(self, ExcludePlot_new):
        self.__ExcludePlot= ExcludePlot_new
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
    
    def land_damage(self): # 地块伤害
        """
        进入地块的伤害(当前地块的伤害只有火伤害)
        """
        damage = sum([each.get_damage() for each in self.attachments])
        return [{"damage":damage, "pre_damag":damage}]
    
    def be_attacked(self, wage_object, damage_res, stats, skill=None): # 地块被攻击
        """
        wage_object   发动攻击的对象
        damage_res       造成的伤害
        stats         stats
        skill = None  如果发动攻击的对象为hero or monster, 需要把技能带过来 
        当前是地块的第四层 & 地块上的英雄 or monster 受到攻击
        """

        new_death_attachment = [] # 只返回附属物的死亡

        for each in self.attachments:
            if wage_object != each:
                each.be_attacked(wage_object=wage_object, skill=skill, damage_res=damage_res)
                if each.is_death:
                    new_death_attachment.append(each)
                
        if self.stand_object:
            self.stand_object.Hp_damage(damage_res)
            if self.stand_object.is_death:
                self.stand_object.leave_game(stats) # 离开游戏
                self.set_stand_object(None)
        
        return new_death_attachment