# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/30 16:42
import time
from functools import lru_cache

from functools import lru_cache
from itertools import product

SKILL_TYPE = {
    "1": {"out_range": 2, "in_range": 1, "cross_range": None},
    "2": {"out_range": None, "in_range": None, "cross_range": 5}
}


class SkillRange:
    @staticmethod
    # @lru_cache(maxsize=None)
    def get_maps_point(xy, maps):
        z = maps[xy]["z"]
        return xy[0], xy[1], z

    @staticmethod
    def get_manhattan_path(x, y, z, max_distance, maps, jump_height=None):
        #  获取曼哈顿范围路径
        points = []
        paths = {(x, y, z): [(x, y, z)]}
        initial_point = (x, y, z)

        queue = [(initial_point, [initial_point])]  # 使用队列记录点和路径
        visited = set()

        while queue:
            (current_x, current_y, current_z), path = queue.pop(0)
            if len(path) > max_distance:  # 确保路径不超过 max_distance
                continue
            if (current_x, current_y, current_z) in visited:
                continue
            visited.add((current_x, current_y, current_z))

            for dx, dy in product(range(-1, 2), repeat=2):
                if abs(dx) + abs(dy) <= 1 and (dx != 0 or dy != 0):
                    p = (current_x + dx, current_y + dy)
                    if p not in maps:
                        continue
                    if maps[p].get("used") == 1:
                        continue
                    point = SkillRange.get_maps_point(p, maps)
                    if jump_height is not None:
                        if abs(current_z - point[2]) > jump_height:
                            continue
                    if (point[0], point[1], point[2]) not in visited:
                        points.append(point)
                        new_path = path + [point]
                        paths[point] = new_path
                        queue.append((point, new_path))

        return paths

    @staticmethod
    # @lru_cache(maxsize=None)
    def get_manhattan_range(x, y, z, max_distance, maps, jump_height=None):
        # 获取曼哈顿范围
        points = []
        for dx, dy in product(range(-max_distance, max_distance + 1), repeat=2):
            if abs(dx) + abs(dy) <= max_distance:
                p = (x + dx, y + dy)

                if p not in maps:
                    continue
                point = SkillRange().get_maps_point(p, maps)
                if jump_height:
                    if abs(z - point[2]) > jump_height:
                        continue

                points.append(point)
        return points

    @staticmethod
    def hit_line_range(point, maps, param):
        x, y, z = point
        attack_range = [point]  # 包含该点位自身
        param = [int(_) for _ in param]

        # 左上的距离
        for i in range(1, param[0] + 1):
            if (x - i, y) in maps:
                attack_range.append(SkillRange().get_maps_point((x - i, y), maps))
            if (x, y - i) in maps:
                attack_range.append(SkillRange().get_maps_point((x, y - i), maps))

        # 右下的距离
        for i in range(1, param[1] + 1):
            if (x + i, y) in maps:
                attack_range.append(SkillRange().get_maps_point((x + i, y), maps))
            if (x, y + i) in maps:
                attack_range.append(SkillRange().get_maps_point((x, y + i), maps))

        return attack_range

    @staticmethod
    def range_mht_hollow_circle(x, y, z, o, i, maps):
        """
        获取曼哈顿 空心圆范围
        :param x: x坐标
        :param y: y左右
        :param o: 外圆范围
        :param i: 内圆范围
        """
        o = int(o)
        i = int(i)-1
        outer_range = set(SkillRange.get_manhattan_range(x, y, z, o, maps))
        inner_range = set(SkillRange.get_manhattan_range(x, y, z, i, maps))
        return list(outer_range - inner_range)

    @staticmethod
    @lru_cache(maxsize=None)
    def range_cross(x, y, z, range_size=5):
        attack_range = {(x, y, z)}  # center position
        for i in range(1, range_size // 2 + 1):
            attack_range.update([(x, y - i, z), (x, y + i, z), (x - i, y, z), (x + i, y, z)])  # up, down, left, right
        return attack_range

    @staticmethod
    def skill_release_range(position, skill, maps):
        """
        获取技能可施放的范围
        :param position: 英雄位置
        :param skill: 技能
        :param maps: 地图
        """
        range = skill["effects"]["ATK_DISTANCE"]["param"]
        points = SkillRange.range_mht_hollow_circle(*position, int(range[1]), int(range[0]), maps)
        points = SkillRange.adjust_shooting_range(points, position, maps)
        return points

    @staticmethod
    def skill_effect_range(position, skill, maps):
        """
        获取技能生效的范围
        :param position: 英雄位置
        :param skill: 技能
        :param maps: 地图
        """
        atk_range = []
        position = tuple(position)

        hit_line = skill["effects"].get("HIT_LINE", {}).get("param")
        hit_range = skill["effects"].get("HIT_RANGE", {}).get("param")
        # print(hit_line)
        if hit_line:
            atk_range += SkillRange().hit_line_range(position, maps, hit_line)
        if hit_range:
            atk_range += SkillRange().range_mht_hollow_circle(*position, hit_range[1], hit_range[0], maps)
        if not atk_range and not hit_range:  # 单体攻击
            atk_range = [position]
        return atk_range

    def get_attack_range(self, attacker, maps):
        # 获取攻击者 目前点位所有可释放范围内所有技能的攻击范围并集
        attack_range = []
        skills = attacker["skills"]
        attacker_position = tuple(attacker["position"])
        for skill in skills:
            release_range = SkillRange.skill_release_range(attacker_position, skill, maps)
            for point in release_range:
                attack_range += SkillRange.skill_effect_range(point, skill, maps)
        return set(tuple(attack_range))

    @staticmethod
    def find_enemies_in_range(hero_pos, enemies, skill, maps, paths):
        # 获取技能释放范围内的所有点
        release_range = SkillRange.skill_release_range(hero_pos, skill, maps)
        results = []
        for point in release_range:
            attack_range = SkillRange.skill_effect_range(point, skill, maps)
            enemies_in_range = [enemy for enemy in enemies if tuple(enemy["position"]) in attack_range]
            if len(enemies_in_range) > 0:  # 技能范围内>0的敌人才返回
                results.append(
                    {
                        "hero_pos": hero_pos,
                        "skill_pos": point,
                        "atk_range": attack_range,
                        "enemies_in_range": enemies_in_range,
                        "route": paths,
                        "skill": skill
                    }
            )
        return results

    @staticmethod
    def get_all_possible_attacks(move_pos, enemies, skill, maps, paths):
        """
        获取英雄在某个位置可以施放技能并且打到的敌人
        :param move_pos: 英雄可以移动到的位置
        """
        all_attacks = []
        attacks = SkillRange.find_enemies_in_range(move_pos, enemies, skill, maps, paths)
        all_attacks.extend(attacks)
        return all_attacks

    @staticmethod
    def adjust_shooting_range(base_positions, hero_position, maps):
        # 根据高低差计算实际射程的影响
        adjusted_positions = set(base_positions)
        hero_z = hero_position[2]

        for position in base_positions:
            x, y, z = position
            height_diff = abs(hero_z - z)
            range_adjustment = height_diff // 2

            if height_diff >= 2:
                for i in range(1, range_adjustment + 1):
                    if x > hero_position[0]:  # 右
                        xy = (x + i, y)
                        if xy in maps: adjusted_positions.add(tuple(maps[xy]["position"]))
                    if x < hero_position[0]:  # 左
                        xy = (x - i, y)
                        if xy in maps: adjusted_positions.add(tuple(maps[xy]["position"]))
                    if y > hero_position[1]:  # 上
                        xy = (x, y + i)
                        if xy in maps: adjusted_positions.add(tuple(maps[xy]["position"]))
                    if y < hero_position[1]:  # 下
                        xy = (x, y - i)
                        if xy in maps: adjusted_positions.add(tuple(maps[xy]["position"]))

        return list(adjusted_positions)


if __name__ == '__main__':
    f = SkillRange()


