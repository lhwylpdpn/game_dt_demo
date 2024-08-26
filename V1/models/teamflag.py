# -*- coding:utf-8 -*-
"""
author : HU
date: 2024-08-01

"""
import json
import copy
import math
import traceback
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as axes3d
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class TeamFlag():

    def __init__(self, team_id):
        self.__team_id = team_id
        self.__team_name = None
        self.__team_member = []
    
    def dict(self):
        return {
            "team_id": self.team_id,
            "team_member": [each.HeroID for each in self.team_member]
        }

    @property
    def team_id(self):
        return self.__team_id

    def set_team_id(self, v):
        self.__team_id = v
        return self

    @property
    def team_name(self):
        return self.__team_name

    def set_team_name(self, value):
        self.__team_name = value
        return self
    
    @property
    def team_member(self):
        return self.__team_member
    
    def join_team(self, hero_or_monster): # 加入队伍
        hero_or_monster.set_team(self)
        self.__team_member.append(hero_or_monster)
        return self
     
    def get_should_combine_team(hero_or_monster, state): # 位置变化后，检查是否需要合并队伍
        enter_other_team_dog_range = []  # 进入其他队伍的警戒范围
        for each_team in TeamFlag.get_teams(hero_or_monster, state):
            if each_team == hero_or_monster.team:
                continue
            if tuple(hero_or_monster.position) in each_team.get_dog_range(state):
                if each_team != hero_or_monster.team:
                    enter_other_team_dog_range.append(each_team)
        return enter_other_team_dog_range
        
    @staticmethod
    def recombine_team(team_1,  team_2): # 两个队伍 重组队伍
        """
        """
        for each in team_2.team_member:
            team_2.leve_game(each)
            team_1.join_team(each)
        print("[TEAM] >>--<< ", team_2.team_id, "合并进入", team_1.team_id)
        return
    
    def leve_game(self, hero_or_monster): # 离开队伍
        self.__team_member.remove(hero_or_monster)
        hero_or_monster.set_team(None)
        return self
    
    def break_up_team(self): # 解散队伍
        for each in self.__team_member:
            self.leve_game(each)
        return self
    
    def get_dog_range(self, state): # 整队伍的警戒范围
        drange = []
        for each in self.__team_member:
            for each_d_p in each.get_dog_range(state):
                if each_d_p not in drange:
                    drange.append(each_d_p)
        return drange
    
    @staticmethod
    def get_teams(hm_object, state): # 找到当前对象一方的所有队伍
        teams = []
        friends = state['hero'] if hm_object in state['hero'] else state['monster'] # 找到己方的所有人
        for each in friends:
            if each.team not in teams:
                if each.is_alive:
                    teams.append(each.team)
        return teams
    
    @staticmethod
    def choose_team(hm_object, state, teams):
        return teams[0]
    
    @staticmethod
    def search_besk_k(x):
        k_socre = []
        if 2 == math.ceil(len(x)/2)+1:
            return 2
        for k in range(2, math.ceil(len(x)/2)+1): # 分队伍的数量
            km = KMeans(n_clusters=k)
            km.fit(x)
            score = silhouette_score(x, km.labels_)
            k_socre.append({'k':k, "score":score})
        best_k_data = sorted(k_socre, key=lambda x:x["score"], reverse=True)[0]
        return best_k_data["k"]

    @staticmethod
    def search_teammate(h_m_objects): # 寻找队友 k-means
        """
        """
        x =[_.position for _ in h_m_objects]
        km = KMeans(n_clusters=TeamFlag.search_besk_k(x))
        km.fit(x)
        predict = km.predict(x)
        team_flag_dict = {}
        for label, h_or_m in zip(predict, h_m_objects):
            h_m = h_or_m.hero_or_monster() # HERO MONSTER
            label = f"{h_m}_{label}"
            if label not in team_flag_dict.keys():
                team_flag_dict[label] = TeamFlag(label)
            team_flag_dict[label].join_team(h_or_m)
        # return
        # # 可视化
        # plt.scatter([_[0] for _ in x], [_[2] for _ in x], c=predict)
        # plt.show()

        # plt.figure('3D Scatter')
        # ax3d = plt.gca(projection='3d')
        # ax3d.set_xlabel('X', fontsize=14)
        # ax3d.set_ylabel('Z', fontsize=14)
        # ax3d.set_zlabel('Y', fontsize=14)
        # ax3d.scatter([_[0] for _ in x],  [_[2] for _ in x],  [_[1] for _ in x], c=predict)
        # plt.show()
