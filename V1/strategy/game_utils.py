# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/16 14:01
import heapq
from itertools import product



class GameUtils(object):
    @staticmethod
    # 获取地图点位
    def get_maps_point(xz, maps):
        y = maps[xz]["y"]
        return xz[0], y, xz[1]

    @staticmethod
    # 获取地图点位
    def get_xz(point):
        return point[0], point[2]

    @staticmethod
    def manhattan_distance(point1, point2):
        # 曼哈顿距离计算
        point1, point2 = tuple(point1), tuple(point2)
        return abs(point1[0] - point2[0]) + abs(point1[2] - point2[2])

    @staticmethod
    def manhattan_range_xz(center, distance, maps):
        # 获取center点distance曼哈顿范围内所有点位
        x0, y0, z0 = center
        points = []

        for dx in range(-distance, distance + 1):
            dz = distance - abs(dx)
            p = (x0 + dx, z0 + dz)

            if p in maps:
                points.append(GameUtils.get_maps_point(p, maps))

        return points

    @staticmethod
    def get_manhattan_range(x, y, z, max_distance, maps, jump_height=None):
        # 获取曼哈顿范围
        points = []
        for dx, dz in product(range(-max_distance, max_distance + 1), repeat=2):
            if abs(dx) + abs(dz) <= max_distance:
                p = (x + dx, z + dz)

                if p not in maps:
                    continue
                point = GameUtils.get_maps_point(p, maps)
                if jump_height:
                    if abs(y - point[1]) > jump_height:
                        continue

                points.append(point)
        return points

    @staticmethod
    def has_intersection(list1, list2):
        # 对比两个列表是否并集
        return bool(set(list1) & set(list2))

    @staticmethod
    def h_manhattan_distance(point1, point2, gap, h_effect):
        # 受高度差影响的曼哈顿距离
        base_distance = GameUtils.manhattan_distance(point1, point2)
        adjusted_distance = base_distance

        # 计算高度差异对距离的额外影响
        if gap and h_effect:
            gap, h_effect = int(gap), int(h_effect)
            height_difference = point1[1] - point2[1]

            if abs(height_difference) >= gap:
                extra_effects = (abs(height_difference) // gap) * h_effect
                adjusted_distance += extra_effects

        return adjusted_distance

    @staticmethod
    def is_reach(start, end, jump_height, block_type=None):
        # 是否可到达
        if not block_type:
            block_type = [1, 2]

        if abs(start["position"][1] - end["position"][1]) <= int(jump_height):
            if end["Block"] in block_type:
                return True
        return False

    @staticmethod
    def is_reach_point(start, end, jump_height, block_type=None):
        # 是否可到达
        if not block_type:
            block_type = [1, 2]

        if abs(start[1] - end[1]) <= int(jump_height):
            if end["Block"] in block_type:
                return True
        return False

    @staticmethod
    def get_damage_skills(hero):
        # 获取主动的可用的攻击技能
        s = []
        available_skills = hero.get("AvailableSkills", [])
        for skill in hero["skills"]:
            if skill["SkillId"] in available_skills:
                if skill["ActiveSkills"] == 1:
                    if "ATK_DISTANCE" in skill["effects"]:
                        if skill["DefaultSkills"] == 1:  # 普攻
                            s.append(skill)
                        else:
                            if int(skill["use_count"]) > 1:
                                s.append(skill)
        return s

    @staticmethod
    def determine_direction(pos1, pos2):
        # 判断移动方向
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2

        if x2 == x1 + 1 and z2 == z1:
            return "RIGHT"
        elif x2 == x1 - 1 and z2 == z1:
            return "LEFT"
        elif z2 == z1 + 1 and x2 == x1:
            return "TOP"
        elif z2 == z1 - 1 and x2 == x1:
            return "BOTTOM"
        else:
            raise Exception(f"invalid move, {pos1} > {pos2}")

    @staticmethod
    def generate_pairs(lst):
        # 返回相邻数组  [1, 2, 3] > [[1, 2], [2, 3]]
        return [(lst[i], lst[i + 1]) for i in range(len(lst) - 1)]

    @staticmethod
    def find_shortest_path(start, end, jump_height, maps, block_type=None):
        # 查找点与点之间的可通行的最近路径
        start, end = tuple(start), tuple(end)
        start_pos = maps[(start[0], start[2])]
        # end_pos = maps[(end[0], end[2])]

        open_set = []
        heapq.heappush(open_set, (0, start_pos['position']))

        came_from = {}
        g_score = {start_pos['position']: 0}
        f_score = {start_pos['position']: GameUtils.manhattan_distance(start_pos['position'], end)}

        while open_set:
            _, current_position = heapq.heappop(open_set)

            if current_position == end:
                path = []
                while current_position in came_from:
                    path.append(current_position)
                    current_position = came_from[current_position]
                path.append(start)
                path.reverse()
                return path

            x, y, z = current_position
            current = maps[(x, z)]
            for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_coord = (x + dx, z + dz)
                if next_coord in maps:
                    next_pos = maps[next_coord]
                    tentative_g_score = g_score[current_position] + 1
                    if GameUtils.is_reach(current, next_pos, jump_height, block_type):
                        if next_pos['position'] not in g_score or tentative_g_score < g_score[next_pos['position']]:
                            came_from[next_pos['position']] = current_position
                            g_score[next_pos['position']] = tentative_g_score
                            f_score[next_pos['position']] = tentative_g_score + GameUtils.manhattan_distance(
                                next_pos['position'], end)
                            heapq.heappush(open_set, (f_score[next_pos['position']], next_pos['position']))
        return []

    @staticmethod
    def range_mht_hollow_circle(point, o, i, gap, effect, maps):
        """
        获取空心菱形范围
        :param o: 外圆范围
        :param i: 内圆范围
        """
        o = int(o) + 1
        i = int(i) + 1
        atk_limit = range(i, o)
        atk_range = []

        for m in maps:
            m_pos = maps[m]["position"]
            if GameUtils.h_manhattan_distance(point, m_pos, gap, effect) in atk_limit:
                atk_range.append(m_pos)
        return atk_range

    @staticmethod
    def hit_line_range(point, maps, param, is_atk_distance=0):
        # 线性技能的攻击范围
        x, y, z = point
        attack_range = [point]  # 包含该点位自身
        param = [int(_) for _ in param]

        # 左上的距离
        for i in range(1, param[0] + 1):
            if (x - i, z) in maps:
                attack_range.append(GameUtils.get_maps_point((x - i, z), maps))
            if (x, z - i) in maps:
                attack_range.append(GameUtils.get_maps_point((x, z - i), maps))

        # 右下的距离
        for i in range(1, param[1] + 1):
            if (x + i, z) in maps:
                attack_range.append(GameUtils.get_maps_point((x + i, z), maps))
            if (x, z + i) in maps:
                attack_range.append(GameUtils.get_maps_point((x, z + i), maps))

        return attack_range

    @staticmethod
    def is_enemies_in_warning_range(role, enemies, maps):
        # 警戒范围内是否有敌人
        role_position = role["position"]
        doge_base = int(role["DogBase"])
        enemies_position = [tuple(_["position"]) for _ in enemies]
        warning_range = GameUtils.get_manhattan_range(*role_position, doge_base, maps)
        return GameUtils.has_intersection(enemies_position, warning_range)

    @staticmethod
    def is_role_in_enemies_warning_range(role, enemies, maps):
        # 是否在敌人警戒范围内
        role_position = tuple(role["position"])

        for e in enemies:
            e_position = tuple(e["position"])
            doge_base = int(e["DogBase"])
            if role_position in GameUtils.manhattan_range_xz(e_position, doge_base, maps):
                return True
        return False

    @staticmethod
    def is_in_combat(role, enemies, maps):
        # 角色是否处于战斗状态
        if GameUtils.is_enemies_in_warning_range(role, enemies, maps) or GameUtils.is_role_in_enemies_warning_range(role, enemies, maps):
            return True
        return False



