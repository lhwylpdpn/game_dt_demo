# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:41
import heapq
from strategy.handler.func import BasicFunc
from strategy.handler.skill_attack_range import SkillRange


class DistanceFunc(object):
    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def is_within_enemy_range(hero_position, enemies):
        # 能攻击到英雄的敌人数量
        count = []
        for enemy in enemies:
            e_position = enemy["position"]
            e_atk_range = enemy["normal_attack_range"]

            if abs(e_position[0] - hero_position[0]) + abs(e_position[1] - hero_position[1]) <= e_atk_range:
                count.append(enemy)
        return count

    @staticmethod
    def find_closest_enemy(hero_position, enemies):
        # 获取距离最近的敌人
        closest_enemy = None
        min_distance = float('inf')

        for enemy in enemies:
            distance = BasicFunc().manhattan_distance(hero_position, enemy["position"])
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy

        return closest_enemy

    @staticmethod
    def is_within_range(range, hero_position, enemies):
        # 在范围内的敌人列表
        count = []
        for enemy in enemies:
            if enemy["Hp"] > 0:
                enemy_position = enemy["position"]
                if BasicFunc().manhattan_distance(hero_position, enemy_position) <= range:
                    count.append(enemy)
        return count

    @staticmethod
    def find_shortest_path(start, end, jump_height, maps):
        """ 查找点与点之间的最近路径 """
        start_pos = maps[(start[0], start[1])]
        end_pos = maps[(end[0], end[1])]

        open_set = []
        heapq.heappush(open_set, (0, start_pos['position']))

        came_from = {}
        g_score = {start_pos['position']: 0}
        f_score = {start_pos['position']: DistanceFunc.heuristic(start_pos['position'], end)}

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
            current = maps[(x, y)]
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_coord = (x + dx, y + dy)
                if next_coord in maps:
                    next_pos = maps[next_coord]
                    tentative_g_score = g_score[current_position] + 1
                    if BasicFunc().is_reach(current, next_pos, jump_height):
                    # if is_reachable(current, next_pos, jump_height):
                        if next_pos['position'] not in g_score or tentative_g_score < g_score[next_pos['position']]:
                            came_from[next_pos['position']] = current_position
                            g_score[next_pos['position']] = tentative_g_score
                            f_score[next_pos['position']] = tentative_g_score + DistanceFunc.heuristic(next_pos['position'], end)
                            heapq.heappush(open_set, (f_score[next_pos['position']], next_pos['position']))
        return []

    @staticmethod
    def manhattan_path(start, end, steps, maps, jump_height):
        x1, y1, z1 = start
        x2, y2, z2 = end

        path = [start]
        x, y, z = x1, y1, z1

        while x != x2 and y != y2 and steps > 0:
            if x < x2:
                x += 1
            elif x > x2:
                x -= 1
            elif y < y2:
                y += 1
            elif y > y2:
                y -= 1

            if (x, y) in maps:
                _point = maps[(x, y)]
                if _point.get("used") == 1:
                    continue
                print('--------->', start, _point["position"], jump_height)

                is_reach = BasicFunc().is_reach(start, _point, jump_height)
                # is_reach = BasicFunc().is_reach(start, _point, jump_height)
                if is_reach:
                    # if tuple(_point["position"]) != end:
                    path.append(tuple(_point["position"]))
                    steps -= 1

        return path

    @staticmethod
    def get_furthest_position(hero_position, enemy_positions, max_distance, maps, jump_height):
        # 获取可到达的 距离敌人最远的位置
        positions_within_range = SkillRange.get_manhattan_path(*hero_position, max_distance, maps, jump_height)
        max_distance_sum = -1
        best_position = None

        for position, routes in positions_within_range.items():
            distance_sum = sum(BasicFunc().manhattan_distance(position, enemy) for enemy in enemy_positions)
            if distance_sum > max_distance_sum:
                max_distance_sum = distance_sum
                best_position = routes

        return best_position


if __name__ == '__main__':
    hero_position = (1, 1, 1)
    enemy_positions = (5, 7, 5)
    f = DistanceFunc()
    print(f.manhattan_path())