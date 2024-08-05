# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/30 16:42
import time
from functools import lru_cache

from V1.strategy.handler.constant_2 import HERO, ENEMY_A, ENEMY_B
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
    @lru_cache(maxsize=None)
    def hit_line_range(point, maps, param):
        x, y, z = point
        attack_range = [point]  # 包含该点位自身

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
        hit_line = skill["effects"].get("HIT_LINE", {}).get("param")
        hit_range = skill["effects"].get("HIT_RANGE", {}).get("param")
        if hit_line:
            atk_range += SkillRange().hit_line_range(position, maps, hit_line)
        if hit_range:
            atk_range += SkillRange().range_mht_hollow_circle(*position, hit_range[1], hit_range[0], maps)
        return atk_range

    @staticmethod
    def find_enemies_in_range(hero_pos, enemies, skill, maps, paths):
        # 获取技能释放范围内的所有点
        release_range = SkillRange.skill_release_range(hero_pos, skill, maps)
        results = []
        for point in release_range:
            attack_range = SkillRange.skill_effect_range(point, skill, maps)
            enemies_in_range = [enemy for enemy in enemies if enemy["position"] in attack_range]
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


if __name__ == '__main__':
    maps = {(0, 1): {'z': 5}, (0, 2): {'z': 5}, (0, 3): {'z': 5}, (0, 4): {'z': 5}, (0, 5): {'z': 5}, (0, 6): {'z': 5}, (0, 7): {'z': 5}, (0, 8): {'z': 5}, (0, 9): {'z': 5}, (0, 10): {'z': 5}, (0, 11): {'z': 5}, (0, 12): {'z': 5}, (0, 13): {'z': 5}, (1, 1): {'z': 5}, (1, 2): {'z': 5}, (1, 3): {'z': 5}, (1, 4): {'z': 5}, (1, 5): {'z': 5}, (1, 6): {'z': 5}, (1, 7): {'z': 5}, (1, 8): {'z': 5}, (1, 9): {'z': 5}, (1, 10): {'z': 5}, (1, 11): {'z': 5}, (1, 12): {'z': 5}, (1, 13): {'z': 5}, (2, 1): {'z': 5}, (2, 2): {'z': 5}, (2, 3): {'z': 5}, (2, 4): {'z': 5}, (2, 5): {'z': 5}, (2, 6): {'z': 5}, (2, 7): {'z': 5}, (2, 8): {'z': 5}, (2, 9): {'z': 5}, (2, 10): {'z': 5}, (2, 11): {'z': 5}, (2, 12): {'z': 5}, (2, 13): {'z': 5}, (3, 1): {'z': 5}, (3, 2): {'z': 5}, (3, 3): {'z': 5}, (3, 4): {'z': 5}, (3, 5): {'z': 5}, (3, 6): {'z': 5}, (3, 7): {'z': 5}, (3, 8): {'z': 5}, (3, 9): {'z': 5}, (3, 10): {'z': 5}, (3, 11): {'z': 5}, (3, 12): {'z': 5}, (3, 13): {'z': 5}, (4, 1): {'z': 5}, (4, 2): {'z': 5}, (4, 3): {'z': 5}, (4, 4): {'z': 5}, (4, 5): {'z': 5}, (4, 6): {'z': 5}, (4, 7): {'z': 5}, (4, 8): {'z': 5}, (4, 9): {'z': 5}, (4, 10): {'z': 5}, (4, 11): {'z': 5}, (4, 12): {'z': 5}, (4, 13): {'z': 5}, (5, 1): {'z': 5}, (5, 2): {'z': 5}, (5, 3): {'z': 5}, (5, 4): {'z': 5}, (5, 5): {'z': 5}, (5, 6): {'z': 5}, (5, 7): {'z': 5}, (5, 8): {'z': 5}, (5, 9): {'z': 5}, (5, 10): {'z': 5}, (5, 11): {'z': 6}, (5, 12): {'z': 5}, (5, 13): {'z': 5}, (6, 1): {'z': 5}, (6, 2): {'z': 5}, (6, 3): {'z': 5}, (6, 4): {'z': 5}, (6, 5): {'z': 5}, (6, 6): {'z': 5}, (6, 7): {'z': 5}, (6, 8): {'z': 5}, (6, 9): {'z': 5}, (6, 10): {'z': 5}, (6, 11): {'z': 5}, (6, 12): {'z': 5}, (6, 13): {'z': 5}, (7, 1): {'z': 5}, (7, 2): {'z': 5}, (7, 3): {'z': 5}, (7, 4): {'z': 5}, (7, 5): {'z': 5}, (7, 6): {'z': 5}, (7, 7): {'z': 7}, (7, 8): {'z': 7}, (7, 9): {'z': 5}, (7, 10): {'z': 5}, (7, 11): {'z': 5}, (7, 12): {'z': 5}, (7, 13): {'z': 5}, (8, 1): {'z': 5}, (8, 2): {'z': 5}, (8, 3): {'z': 5}, (8, 4): {'z': 5}, (8, 5): {'z': 5}, (8, 6): {'z': 5}, (8, 7): {'z': 5}, (8, 8): {'z': 5}, (8, 9): {'z': 5}, (8, 10): {'z': 5}, (8, 11): {'z': 5}, (8, 12): {'z': 5}, (8, 13): {'z': 5}, (9, 1): {'z': 5}, (9, 2): {'z': 5}, (9, 3): {'z': 5}, (9, 4): {'z': 5}, (9, 5): {'z': 5}, (9, 6): {'z': 5}, (9, 7): {'z': 5}, (9, 8): {'z': 5}, (9, 9): {'z': 5}, (9, 10): {'z': 5}, (9, 11): {'z': 5}, (9, 12): {'z': 5}, (9, 13): {'z': 5}, (10, 1): {'z': 5}, (10, 2): {'z': 5}, (10, 3): {'z': 5}, (10, 4): {'z': 5}, (10, 5): {'z': 5}, (10, 6): {'z': 5}, (10, 7): {'z': 5}, (10, 8): {'z': 5}, (10, 9): {'z': 5}, (10, 10): {'z': 5}, (10, 11): {'z': 5}, (10, 12): {'z': 5}, (10, 13): {'z': 5}}
    f = SkillRange()
    print(f.range_mht_hollow_circle(*(3, 6, 5), 1, 1, maps))


