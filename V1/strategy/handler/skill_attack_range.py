# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/30 16:42

from functools import lru_cache
from itertools import product

from strategy.game_utils import GameUtils


class SkillRange:
    @staticmethod
    def is_atk_distance(point1, point2, distance):
        if abs(point1[1] - point2[1]) <= int(distance):
            return True
        return False

    @staticmethod
    def get_manhattan_path(x, y, z, max_distance, maps, jump_height=None):
        #  获取曼哈顿范围路径
        points = []
        max_distance = int(max_distance)
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

            for dx, dz in product(range(-1, 2), repeat=2):
                if abs(dx) + abs(dz) <= 1 and (dx != 0 or dz != 0):
                    p = (current_x + dx, current_z + dz)
                    if p not in maps:
                        continue

                    if maps[p].get("Block") in (0, 2):
                        continue
                    point = GameUtils.get_maps_point(p, maps)

                    if jump_height is not None:
                        if abs(current_y - point[1]) > jump_height:
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
        if "ADD_ATK_DISTANCE" in skill["effects"]:
            gap, effect = skill["effects"]["ADD_ATK_DISTANCE"]["param"][0], skill["effects"]["ADD_ATK_DISTANCE"]["param"][1]
        else:
            gap, effect = 0, 0
        points = GameUtils.range_mht_hollow_circle(position, int(range[1]), int(range[0]), gap, effect, maps)
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
        is_atk_distance = skill["effects"].get("IS_ATK_DISTANCE", {}).get("param", [0])[0]

        if hit_line:
            atk_range += GameUtils.hit_line_range(position, maps, hit_line, is_atk_distance) # TODO
        if hit_range:
            if "ADD_ATK_DISTANCE" in skill["effects"]:
                gap, effect = skill["effects"]["ADD_ATK_DISTANCE"]["param"][0], skill["effects"]["ADD_ATK_DISTANCE"]["param"][1]
            else:
                gap, effect = 0, 0
            atk_range += GameUtils.range_mht_hollow_circle(position, hit_range[1], hit_range[0], gap, effect, maps)
        if not atk_range and not hit_range:  # 单体攻击
            atk_range = [position]

        if is_atk_distance:  # 判断高低差影响
            atk_range = [_ for _ in atk_range if SkillRange.is_atk_distance(position, _, is_atk_distance)]
        return atk_range

    def get_attack_range(self, attacker, maps):
        # 获取攻击者 目前点位所有可释放范围内所有技能的攻击范围并集
        attack_range = []
        skills = GameUtils.get_damage_skills(attacker)
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
            enemies_in_range = [enemy for enemy in enemies if tuple(enemy["position"]) in attack_range and int(enemy["Hp"]) > 0]
            if tuple(point) in [tuple(e["position"]) for e in enemies]:
                if len(enemies_in_range) > 0:  # 技能范围内>0的敌人才返回
                    results.append(
                        {
                            "hero_pos": hero_pos,
                            "skill_pos": point,
                            "atk_range": attack_range,
                            "release_range": release_range,
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
        hero_y = hero_position[1]

        for position in base_positions:
            x, y, z = position
            height_diff = abs(hero_y - y)
            range_adjustment = height_diff // 2

            if height_diff >= 2:
                for i in range(1, range_adjustment + 1):
                    if x > hero_position[0]:  # 右
                        xz = (x + i, z)
                        if xz in maps: adjusted_positions.add(tuple(maps[xz]["position"]))
                    if x < hero_position[0]:  # 左
                        xz = (x - i, z)
                        if xz in maps: adjusted_positions.add(tuple(maps[xz]["position"]))
                    if z > hero_position[2]:  # 上
                        xz = (x, z + i)
                        if xz in maps: adjusted_positions.add(tuple(maps[xz]["position"]))
                    if z < hero_position[2]:  # 下
                        xz = (x, z - i)
                        if xz in maps: adjusted_positions.add(tuple(maps[xz]["position"]))

        return list(adjusted_positions)


if __name__ == '__main__':
    f = SkillRange()
