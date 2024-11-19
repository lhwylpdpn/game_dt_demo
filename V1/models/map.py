# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-07-18
"""

import pandas as pd
import copy
import numpy as np
import itertools
from .land import Land
from .attachment import Attachment, AttachmentHelper
from utils.damage import damage
from utils.attachment_damage import damage_calc
from utils.tools import round_up_2_integer


class Map(): # 地图
    """
    """
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
        self.map = np.zeros((self._x, self._y, self._z), dtype=np.object)
        self.__attachments = []          # 当前地图上附着物
        self.__removed_attchments = []   # 当前地图被移除的附着物
        self.__hidden_attachment = []    # 隐藏的attachment 比如 “火药桶碎片” 
        self.__h_m_objects = []          # 当前地图里面的英雄 or monster

    @property
    def x(self):
        return self._x - 1
    
    @property
    def y(self):
        return self._y - 1
    
    @property
    def z(self):
        return self._z - 1
    
    def view_from_y(self):
        return np.max(self.map, axis=1)
    
    def correct_map_bonus(self, x, z): # x, z 中检查地图的边界
        x = x if self.x > x else self.x
        x = 0 if x < 0 else  x
        z = z if self.z > z  else  self.z
        z = 0 if z < 0 else z
        return x, z

    def get_y_from_xz(self, x, z):  # 从y俯视图中，根据 x,z 来确定 地块
        if x >=0 and x <= self.x and z >= 0 and z <= self.z:
            position = np.max(self.map[x, :, z], axis=0)
            if isinstance(position, Land):
                return position.y
            else:
                return None
        else:
            raise Exception(f"{x}, {z} is wrong")

    def land_can_pass(self, x, y, z): # 判断地图是否可以通过
        try:
            land = self.map[x,y,z]
            if isinstance(land, Land):
                if land.Block is None:
                    return False
                return land.is_can_pass()
            return False
        except Exception:
            return False
    
    def get_land(self, x, y, z):  # 获取地图上的地块
        try:
            land = self.map[x,y,z]
            if isinstance(land, Land):
                return land
            return None
        except Exception:
            return None

    def view_from_y_dict(self):
        data = {}
        a = pd.DataFrame(self.view_from_y())
        for each_coloum in np.array(a.values.tolist()).tolist():
            for each in each_coloum:
                if isinstance(each, Land):
                    x,y,z = each.position
                    land = self.map[x,y,z]
                    data[(x,y,z)] = land.dict()
        return data

    def dict(self, for_view=False):
        data = []
        for each_postion in self.list_land_postion():
            x,y,z = each_postion
            land = self.map[x,y,z]
            if isinstance(land, Land):
                land_data = land.dict()
                data.append(land_data)
        return data
    
    def get_return_box(self, land): # 是否返回宝箱
        # 是否返回距离该地块符合宝箱返回距离的宝箱
        result_box = []
        for _at in self.__attachment:
            if _at.is_box(): # 是宝箱
                if abs(land.x - _at.x) + abs(land.z - _at.z) <= _at.box_open_distance(): # 在宝箱开启距离范围内
                    result_box.append(_at)
        return result_box
    
    def set_land_no_pass(self, x,y,z, block): # 训练使用，实际情况用不到这个
        land = self.map[x,y,z]
        if isinstance(land, Land):
            land.set_Block_train(block)
        return self

    def exit(self, h_m_object): # 离开地块
        x,y,z = h_m_object.position
        land = self.map[x,y,z]
        if isinstance(land, Land):
            if land.stand_object:
                if land.stand_object.HeroID == h_m_object.HeroID:
                    land.set_stand_object(None)
                else:
                    raise Exception("地块 {x}, {y}, {z} 不是该对象站立")
        return self
    
    def enter(self, x, y, z, h_m_object, init_position=False): # 进入地块 
        land = self.map[x,y,z]
        if isinstance(land, Land):
            if not land.stand_object:
                land.set_stand_object(h_m_object)
                if init_position:
                    self.__h_m_objects.append(h_m_object)
                # TODO 地块伤害
                h_m_object.Hp_damage(land.land_damage())
            else:
                raise Exception("land {x}, {y}, {z} 被占用")
        return self
    
    def load_land(self,x,y,z, land): # 加载地块
        self.map[x,y,z] = land
        return self
    
    def load_attachment(self, attachment): #加载附着物
        x,y,z = attachment.position
        land = self.map[x,y,z]
        # 地块空间存在， 并且上面有地块，可以加附着物
        if isinstance(land, Land):
            if land.is_exist_attachment_at_same_layer(attachment): # 判断和 附着物同层上是否有其他附着物
                old_attachment = land.get_attachment_at_same_layer(attachment)
                self.unload_attachment(old_attachment) # 卸载旧附着物
            # 地块加载新的附着物
            if land.add_attachment(attachment):
                self.__attachments.append(attachment)
            if attachment.is_fire():
                if not self.__hidden_attachment:
                    example_attachment = copy.deepcopy(attachment)
                    self.__hidden_attachment.append(example_attachment)
        return self
    
    def unload_attachment(self, attachment): #卸载附着物
        x,y,z = attachment.position
        land = self.map[x,y,z]
        land.del_attachment(attachment)
        self.__attachments.remove(attachment)
        self.__removed_attchments.append(attachment) 
        return self
    
    @staticmethod
    def find_map_size(origin_map_data):
        postion_list = []
        for each in origin_map_data:
            postion_list.append(each.get('position'))
        df = pd.DataFrame(postion_list)
        x, y, z = list(df.max())
        print("map size:", x+1, z+1, y+1)
        return x+1, y+1, z+1 
    
    def list_land_postion(self):
        a = pd.DataFrame(np.nonzero(self.map))
        return np.array(a.T.values.tolist()).tolist()
    
    def __square(self, o_point, distance): # 正方形形状，
        """
        o_point    原始点
        distance   距离
        """
        x_points = range(o_point.x - distance, o_point.x + distance + 1)
        z_points = range(o_point.z - distance, o_point.z + distance + 1)
        points = list(itertools.product(x_points, z_points)) # 笛卡尔积
        return points
    
    def __rhombus(self, o_point, distance) : # 菱形
        """
        o_point    原始点
        distance   曼哈顿距离
        """
        points = []
        for each in self.__square(o_point, distance):
            if abs(each[0] - o_point.x) + abs(each[1] - o_point.z) <= distance:
                points.append(each)
        return points

    def calc_shape_point(self, effect, o_point): # 根据effect里面的形状key，参数，原点，计算出范围点
        inner, out = int(effect.param[0]), int(effect.param[1])
        result_p_l , points = [], []
        
        if effect.key in ["HIT_SQUARE", "CREATE_PLOT_SQUARE"]: # 生效范围(正方形)	以原点延伸{0|0}格, HIT_SQUARE: 打击范围。 CREATE_PLOT_SQUARE ：产生碎片范围
            points = list(set(self.__square(o_point, out)) - set(self.__square(o_point, inner)))  # 外圈减去内圈
        
        if effect.key == "HIT_RANGE": # 生效范围(菱形)	以原点延伸{0|0}格
            points = list(set(self.__rhombus(o_point, out)) - set(self.__rhombus(o_point, inner))) # 外圈减去内圈
        
        for each_point in points:
            x, z = self.correct_map_bonus(*each_point)
            y = self.get_y_from_xz(x, z)
            if y:
                result_p_l.append(tuple([x,y,z]))
        
        return result_p_l

    def h_m_focus(self, h_m_object):            # 英雄被选中的时候，需要在地图上也有foucus操作， 用于计数
        for each in self.__attachments:
            each.focus_object(h_m_object)
        x,y,z = h_m_object.position
        land = self.map[x,y,z]
        h_m_object.Hp_damage(land.land_damage()) # 每次被选中时候，地块伤害
        return self
    
    def h_m_unfocus(self, h_m_object): # 英雄取消被选中的时候，需要在地图上也有unfoucus操作， 用于计数,消除
        for each in self.__attachments:
            each.unfocus_object(self.__h_m_objects)
            if not each.is_alive():
                self.unload_attachment(each)
        return self
    
    def open_box(self, box_attachment):
        if box_attachment.is_box():
            box_attachment.open()
            # TODO 
        return self
    
    def bomb_killed(self, wage_object, attachment, stats):
        # TODO 打击的范围
        new_death_att = []
        atk_points = self.calc_shape_point(attachment.get_bomb_attack_effect(), attachment)
        att_frage_effect = attachment.get_bomb_fragment_effect()
        frag_points= self.calc_shape_point(att_frage_effect,  attachment)
        
        # TODO 对周围的英雄，monster，附着物产生影响
        print("爆炸对周围的英雄，monster，附着物产生影响:")
        damage = {"damage":attachment.back_damage()}
        for each_point_atk in atk_points:
            land = self.get_land(*each_point_atk)
            new_d = land.be_attacked(attachment, [damage], stats=stats) # 爆炸的冲击
            if new_d:
                new_death_att.extend(new_d)
        
        # TODO 产生爆炸碎片
        print("爆炸产生碎片:")
        for each_frag_point in frag_points:
            land = self.get_land(*each_frag_point)
            new_frage_att = AttachmentHelper.create_attachment(self.__hidden_attachment, int(att_frage_effect.param[2]))
            new_frage_att.set_position(land.position)
            print(f"碎片地块:{land.position} {new_frage_att.sn}")
            # 碎片 产生debuff
            self.load_attachment(new_frage_att)
            # 碎片伤害 (碎片只对地块上站立的hero和monster产生影响) damage 是 0 
            new_d = land.be_attacked(new_frage_att, [{"damage":new_frage_att.get_damage()}], stats=stats)
            if new_d:
                new_death_att.extend(new_d)
        
        return list(set(new_death_att))
    
    def judge_attachment_status(self, wage_object, skill, attachment, stats): # 判断打附属物后，附属物的状态
        new_death = []       
        if attachment.is_death:           # 被打消失了 
            self.unload_attachment(attachment)  # 去掉
            if attachment.is_bomb():            # 火药桶逻辑
                new_death = self.bomb_killed(wage_object, attachment, stats)
        return new_death
    
    def format_result(self, attachment, damage_res, is_include_chain_field=True):
        
        result = {"damage": damage_res,
                  "new_frag": {}, 
                  "atk_o_point": [], 
                  "atk_range":[],
                  "chain_atk_result":[],
                  "back_attck": None
                  }
        
        if attachment.is_death and attachment.is_bomb():
            # 碎片
            result["new_frag"] = {"sn": int(attachment.get_bomb_fragment_effect().param[2]),
                                  "points":self.calc_shape_point(attachment.get_bomb_fragment_effect(), attachment)}
            result["atk_o_point"] = attachment.position
            result["atk_range"] = self.calc_shape_point(attachment.get_bomb_attack_effect(), attachment)
    
        if not is_include_chain_field:
            result.pop("chain_atk_result")
    
        return result
        
    def attack_attachment(self, wage_object, skill, attachment, stats):  # 攻击附着物
        """
        攻击附着物
        wage_object   发动攻击的对象
        skill         使用的技能
        attachment    被攻击的对象
        stats         stats
        """
        damage_res = damage_calc(attacker=wage_object, defender=attachment, skill=skill)
        for _ in damage_res: # 向上取整
            _["damage"] = round_up_2_integer(_["damage"])
            _["pre_damage"] = round_up_2_integer(_["pre_damage"])

        attachment.be_attacked(wage_object, skill, damage_res)
        
        result = self.format_result(attachment, damage_res)
        
        new_att_list = self.judge_attachment_status(wage_object, skill, attachment, stats)
        
        attachment_list = []
        if new_att_list:
            attachment_list = list(zip((wage_object)*len(new_att_list), new_att_list))
        
        while attachment_list: # 循环去找被打击的对象
            _wage_object, each_attachment = attachment_list.pop(0)
            new_att_list = self.judge_attachment_status(_wage_object, skill, each_attachment, stats)
            if new_att_list:
                attachment_list.extend(
                    list(zip((_wage_object)*len(new_att_list), new_att_list))
                    )
            damage = {"damage": _wage_object.back_damage()}
            result["chain_atk_result"].append({ each_attachment : self.format_result(each_attachment, damage, is_include_chain_field=False) })
        print("---->>attack_attachment:[result]", result)
        return result
                
                    
if __name__ == "__main__":
   print(Map(4,4,4).view_from_y())