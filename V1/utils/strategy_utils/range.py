# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/21 16:06
import heapq
from copy import deepcopy
from itertools import product

from buildpatrol import BuildPatrol
from log.log import log_manager
from strategy.handler.weight import Weight
from test_hero_data import origin_hero_data
from test_map_data import origin_map_data
from test_monster_data import origin_monster_data
from utils.strategy_utils.basic_data import Data


class Range(Data):
    def __init__(self, role=None, state=None):
        if role:
            self.role = role
            if not isinstance(self.role, dict):
                self.role = role.dict()

        if state:
            if "map" in state:
                if not isinstance(state["map"], dict):
                    self.map = state["map"]
                    self.map = Data.convert_maps_xz(self.map.view_from_y_dict())
                else:
                    self.map = state["map"]

            if "hero" in state:
                self.teammates = []
                for _ in state["hero"]:
                    if not isinstance(_, dict):
                        _ = _.dict()
                    if Data.value("HeroID", _) != Data.value("HeroID", self.role):
                        self.teammates.append(_)

            if "monster" in state:
                self.enemies = []
                for _ in state["monster"]:
                    if not isinstance(_, dict):
                        _ = _.dict()
                    if Data.value("Hp", _) > 0:
                        self.enemies.append(_)

    def is_health_below_threshold(self, num):
        # 血量是否小于num比例

        hp = Data.value("Hp", self.role)
        hp_base = Data.value("HpBase", self.role)
        return float(hp) / float(hp_base) <= float(num)

    def is_reach(self, start, end, jump_height, block_type=None):
        # 是否可到达
        if not block_type:
            block_type = [1, 2, 3]
        # block_type = [1, 2, 3]

        if abs(start["position"][1] - end["position"][1]) <= int(jump_height):
            if end["Block"] in block_type:
                return True
        return False

    def get_block_step(self, steps, block_status, maps):
        move_steps = []
        for k, s in enumerate(steps):
            xz = Data.get_xz(s)
            if k > 0:
                if maps[xz]["Block"] not in block_status:
                    break
            move_steps.append(s)
        return move_steps

    def get_damage_skills(self):
        # 获取主动的可用的攻击技能
        s = []
        available_skills = self.role.get("AvailableSkills", [])
        for skill in self.role["skills"]:
            if skill["SkillId"] in available_skills:
                if skill["ActiveSkills"] == 1:
                    if "ATK_DISTANCE" in skill["effects"]:
                        if skill["DefaultSkills"] == 1:  # 普攻
                            s.append(skill)
                        else:
                            if int(skill["use_count"]) > 1:
                                s.append(skill)
        return s

    def manhattan_distance(self, point1, point2):
        # 曼哈顿距离计算 （ 只计算xz
        point1, point2 = tuple(point1), tuple(point2)
        return abs(point1[0] - point2[0]) + abs(point1[2] - point2[2])

    def get_manhattan_range(self, x, y, z, max_distance, jump_height=None):
        # 获取曼哈顿范围内的所有点位
        points = []
        for dx, dz in product(range(-max_distance, max_distance + 1), repeat=2):
            if abs(dx) + abs(dz) <= max_distance:
                p = (x + dx, z + dz)

                if p not in self.map:
                    continue
                point = self.get_maps_point(p, self.map)
                if jump_height:
                    if abs(y - point[1]) > jump_height:
                        continue

                points.append(point)
        return points

    # def manhattan_range_xz(self, center, distance):
    #     # 获取center点distance曼哈顿范围内所有点位
    #     x0, y0, z0 = center
    #     points = []
    #
    #     for dx in range(-distance, distance + 1):
    #         dz = distance - abs(dx)
    #         p = (x0 + dx, z0 + dz)
    #
    #         if p in self.map:
    #             points.append(Data.get_maps_point(p, self.map))
    #
    #     return points

    def h_manhattan_distance(self, point1, point2, gap, h_effect):
        # 受高度差影响的曼哈顿距离
        base_distance = self.manhattan_distance(point1, point2)
        adjusted_distance = base_distance

        # 计算高度差异对距离的额外影响
        if gap and h_effect:
            gap, h_effect = int(gap), int(h_effect)
            height_difference = point1[1] - point2[1]

            if abs(height_difference) >= gap:
                extra_effects = (abs(height_difference) // gap) * h_effect
                adjusted_distance += extra_effects

        return adjusted_distance

    def get_manhattan_path(self, x, y, z, max_distance, jump_height=None):
        # 获取曼哈顿范围路径
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
                    if p not in self.map:
                        continue

                    if self.map[p].get("Block") in (0, 2):
                        continue
                    point = self.get_maps_point(p, self.map)

                    if jump_height is not None:
                        if abs(current_y - point[1]) > jump_height:
                            continue
                    if (point[0], point[1], point[2]) not in visited:
                        points.append(point)
                        new_path = path + [point]
                        paths[point] = new_path
                        queue.append((point, new_path))
        return paths

    def is_role_in_enemies_warning_range(self, role, enemies):
        # 是否在敌人警戒范围内
        role_position = Data.value("DogBase", role)

        for e in enemies:
            _position = Data.value("position", e)
            _doge_base = Data.value("DogBase", e)
            if role_position in self.get_manhattan_range(*_position, _doge_base):
                return True
        return False

    def get_furthest_position(self):
        # 获取可到达的 距离敌人最远的位置
        role_position = Data.value("position", self.role)
        round_action = Data.value("RoundAction", self.role)
        jump_height = Data.value("JumpHeight", self.role)

        positions_within_range = self.get_manhattan_path(*role_position, round_action, jump_height)
        max_distance_sum = -1
        best_position = None

        for position, routes in positions_within_range.items():
            distance_sum = sum(self.manhattan_distance(position, Data.value("position", enemy)) for enemy in self.enemies)
            if distance_sum > max_distance_sum:
                max_distance_sum = distance_sum
                best_position = routes

        return best_position

    def is_in_combat(self, role, enemies):
        # 角色是否处于战斗状态
        if self.enemies_in_warning_range_count() or self.is_role_in_enemies_warning_range(role, enemies):
            return True
        return False

    def has_combat_ready_teammate(self, role, teammates, enemies):
        # 获取在战斗状态的队友的位置
        distance = None
        teammate_position = None
        role_position = Data.value("position", role)

        for t in teammates:
            if Data.value("team_id", role) == Data.value("team_id", t):  # 小队编号一致
                if self.is_in_combat(t, enemies):
                    _teammate_position = Data.value("position", t)
                    _distance = self.manhattan_distance(role_position, _teammate_position)

                    if distance and teammate_position:
                        if distance > _distance:
                            distance, teammate_position = _distance, _teammate_position
                    else:
                        distance, teammate_position = _distance, _teammate_position
        return teammate_position

    def range_mht_hollow_circle(self, point, o, i, gap, effect):
        # 获取空心菱形范围  o: 外圆范围 i: 内圆范围

        o = int(o) + 1
        i = int(i) + 1
        atk_limit = range(i, o)
        atk_range = []

        for m in self.map:
            m_pos = self.map[m]["position"]
            if self.h_manhattan_distance(point, m_pos, gap, effect) in atk_limit:
                atk_range.append(m_pos)
        return atk_range

    def hit_line_range(self, point, param):
        # 线性技能的攻击范围
        x, y, z = point
        x1, y1, z1 = Data.value("position", self.role)
        attack_range = []  # 包含该点位自身
        param = [abs(int(_)) for _ in param]
        param_a, param_b = param[0], param[1]

        # 如果x相等，计算左右范围
        if x == x1:
            for i in range(-param_a, param_b + 1):
                # attack_range.append((x, z + i))
                xz = (x, z + i)
                if xz in self.map:
                    attack_range.append(Data.get_maps_point(xz, self.map))

        # 如果y相等，计算上下范围
        elif z == z1:
            for i in range(-param_a, param_b + 1):
                xz = (x + i, z)
                if xz in self.map:
                    attack_range.append(Data.get_maps_point(xz, self.map))

        return attack_range

    def is_atk_distance(self, point1, point2, distance):
        # 攻击是否受到高低差影响
        if abs(point1[1] - point2[1]) <= int(distance):
            return True
        return False

    def is_within_range(self, num):
        # 是否在num个敌人的范围内
        doge_base = Data.value("DogBase", self.role)
        role_position = Data.value("position", self.role)
        count = 0
        for enemy in self.enemies:
            enemy_position = Data.value("position", enemy)
            if self.manhattan_distance(role_position, enemy_position) <= doge_base:
                count += 1
        return num <= count

    def find_shortest_path(self, start, end, jump_height, block_type=None):
        # 查找点与点之间的可通行的最近路径， 返回路径list
        start, end = tuple(start), tuple(end)
        start_pos = self.map[(start[0], start[2])]
        # end_pos = maps[(end[0], end[2])]
        paths = []

        open_set = []
        heapq.heappush(open_set, (0, start_pos['position']))

        came_from = {}
        g_score = {start_pos['position']: 0}
        f_score = {start_pos['position']: self.manhattan_distance(start_pos['position'], end)}

        while open_set:
            _, current_position = heapq.heappop(open_set)

            if current_position == end:
                path = []
                while current_position in came_from:
                    path.append(current_position)
                    current_position = came_from[current_position]
                path.append(start)
                path.reverse()

                # 将路径及其对应的 g_score 存储
                paths.append((path, g_score[end]))

            x, y, z = current_position
            current = self.map[(x, z)]
            for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_coord = (x + dx, z + dz)
                if next_coord in self.map:
                    next_pos = self.map[next_coord]
                    _block_cost = Data.block_score(next_pos)
                    tentative_g_score = g_score[current_position] + _block_cost
                    if self.is_reach(current, next_pos, jump_height, block_type):
                        if next_pos['position'] not in g_score or tentative_g_score < g_score[next_pos['position']]:
                            came_from[next_pos['position']] = current_position
                            g_score[next_pos['position']] = tentative_g_score
                            f_score[next_pos['position']] = tentative_g_score + self.manhattan_distance(
                                next_pos['position'], end)
                            heapq.heappush(open_set, (f_score[next_pos['position']], next_pos['position']))
        if paths:
            return min(paths, key=lambda x: x[1])[0]
        return []

    def find_closest_attack_position(self, hero, enemy_position):
        # 获取对于攻击者来说能攻击到敌人最近的位置，并得到前往这个位置的在round_action行动内的前进列表
        enemy_position = tuple(enemy_position)
        hero_position = Data.value("position", hero)
        jump_height = Data.value("JumpHeight", hero)
        round_action = Data.value("RoundAction", hero)
        attack_pos_dict = {}

        for xz in self.map:
            point = tuple(self.map[xz]["position"])
            _hero = deepcopy(hero)
            _hero["position"] = point

            stk_range = self.get_attack_range(point)
            if enemy_position in stk_range:
                move_steps = self.find_shortest_path(hero_position, point, jump_height, [1, 2, 3])[: round_action + 1]
                if move_steps:
                    attack_pos_dict[point] = move_steps

        if attack_pos_dict:
            closest_pos = min(attack_pos_dict.keys(), key=lambda k: self.manhattan_distance(k, hero_position))
            steps = attack_pos_dict[closest_pos]
            return closest_pos, steps
        else:
            return None, None

    def find_closest_enemy(self):
        # 获取距离最近的敌人
        closest_enemy = None
        min_distance = float('inf')
        role_position = Data.value("position", self.role)

        for enemy in self.enemies:
            enemy_position = Data.value("position", enemy)
            distance = self.manhattan_distance(role_position, enemy_position)
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def skill_effect_range(self, point, skill):
        # 获取在point点位施放技能的生效范围
        atk_range = []
        point = tuple(point)

        hit_line = skill["effects"].get("HIT_LINE", {}).get("param")
        hit_range = skill["effects"].get("HIT_RANGE", {}).get("param")
        is_atk_distance = skill["effects"].get("IS_ATK_DISTANCE", {}).get("param", [0])[0]

        if hit_line:
            atk_range += self.hit_line_range(point, hit_line)  # TODO
        if hit_range:
            if "ADD_ATK_DISTANCE" in skill["effects"]:
                gap, effect = skill["effects"]["ADD_ATK_DISTANCE"]["param"][0], \
                skill["effects"]["ADD_ATK_DISTANCE"]["param"][1]
            else:
                gap, effect = 0, 0
            atk_range += self.range_mht_hollow_circle(point, hit_range[1], hit_range[0], gap, effect)
        if not atk_range and not hit_range:  # 单体攻击
            atk_range = [point]

        if is_atk_distance:  # 判断高低差影响
            atk_range = [_ for _ in atk_range if self.is_atk_distance(point, _, is_atk_distance)]
        return atk_range

    def skill_release_range(self, position, skill):
        # 获取某个技能施放范围（射程
        # position = Data.value("position", self.role)
        range = skill["effects"]["ATK_DISTANCE"]["param"]
        if "ADD_ATK_DISTANCE" in skill["effects"]:
            gap, effect = skill["effects"]["ADD_ATK_DISTANCE"]["param"][0], \
            skill["effects"]["ADD_ATK_DISTANCE"]["param"][1]
        else:
            gap, effect = 0, 0
        points = self.range_mht_hollow_circle(position, int(range[1]), int(range[0]), gap, effect)
        return points

    def enemies_in_warning_range(self, role):
        # 获取角色的警戒范围
        role_position = Data.value("position", role)
        doge_base = Data.value("DogBase", role)

        warning_range = self.get_manhattan_range(*role_position, doge_base)
        return warning_range

    def get_attack_range(self, position):
        # 获取攻击者 目前点位所有可释放范围内所有技能的攻击范围并集
        attack_range = []
        skills = self.get_damage_skills()
        for skill in skills:
            release_range = self.skill_release_range(position, skill)
            for point in release_range:
                attack_range += self.skill_effect_range(point, skill)
        return set(tuple(attack_range))

    def nearby_enemy_count(self, num):
        # 获取附近的敌人数量( 是否在num个敌人的警戒范围内
        _count = 0
        role_position = Data.value("position", self.role)

        for enemy in self.enemies:
            enemy_atk_range = self.enemies_in_warning_range(enemy)
            if role_position in enemy_atk_range:
                _count += 1
        return num >= _count

    def enemies_in_warning_range_count(self,):
        # 警戒范围内的敌人数量
        doge_base = Data.value("DogBase", self.role)
        role_position = Data.value("position", self.role)
        enemies_position = [Data.value("position", _) for _ in self.enemies]
        warning_range = self.get_manhattan_range(*role_position, doge_base)
        return len(Data.intersection(enemies_position, warning_range))

    def find_enemies_in_range(self, move_pos, skill, paths):
        # 获取技能释放范围内的所有点
        release_range = self.skill_release_range(move_pos, skill)
        results = []
        for point in release_range:
            attack_range = self.skill_effect_range(point, skill)
            enemies_in_range = [enemy for enemy in self.enemies if Data.value("position", enemy) in attack_range]
            if tuple(point) in [Data.value("position", e) for e in self.enemies]:
                if len(enemies_in_range) > 0:  # 技能范围内>0的敌人才返回
                    results.append(
                        {
                            "hero_pos": move_pos,
                            "skill_pos": point,
                            "atk_range": attack_range,
                            "release_range": release_range,
                            "enemies_in_range": enemies_in_range,
                            "route": paths,
                            "skill": skill
                        }
                    )
        return results

    def get_all_possible_attacks(self, move_pos, skill, paths):
        """
        获取英雄在某个位置可以施放技能并且打到的敌人
        :param move_pos: 英雄可以移动到的位置
        """
        all_attacks = []
        attacks = self.find_enemies_in_range(move_pos, skill, paths)
        all_attacks.extend(attacks)
        return all_attacks

    def find_targets_within_atk_range(self):
        # 获取在攻击范围内的目标选项
        pick_list = []
        skills = self.get_damage_skills()
        doge_base = Data.value("DogBase", self.role)
        max_step = Data.value("RoundAction", self.role)
        position = Data.value("position", self.role)
        jump_height = Data.value("JumpHeight", self.role)

        print(f"[ATK]警戒范围内存在敌人, 攻击者{self.role['HeroID']}{position},警戒范围{doge_base}, 本回合可移动{max_step}, 跳跃高度:{jump_height},  本次可用技能:{len(skills)}")
        move_positions = self.get_manhattan_path(*position, max_step, jump_height)  # 英雄可移动到的点位
        for move, paths in move_positions.items():
            for skill in skills:
                pick_list += self.get_all_possible_attacks(move, skill, paths)

        if pick_list:
            state = {"map": self.map,
                     "hero": self.teammates + [self.role],
                     "monster": self.enemies}
            tmp = log_manager.add_log(log_data=str({"role": self.role, "state": state}) )
            print(f"log tmp: {tmp}")
        return pick_list

    def find_attack_target(self):
        # 确定攻击目标
        pick = {}
        pick_list = self.find_targets_within_atk_range()
        for each in pick_list:
            _weight = Weight().clac_skill_weight(each)
            if not pick:
                pick = {"weight": _weight, "data": each}
                continue
            if pick["weight"] < _weight:
                pick = {"weight": _weight, "data": each}
        print(f"[ATK]攻击者在{pick['data']['hero_pos']}位置对{pick['data']['skill_pos']}位置施放技能[{pick['data']['skill']['SkillId']}], 需要移动{pick['data']['route']}")
        return pick["data"]

    def move_to_enemy(self):
        # 向最近的敌人移动
        doge_base = Data.value("DogBase", self.role)
        round_action = Data.value("RoundAction", self.role)
        position = Data.value("position", self.role)
        jump_height = Data.value("JumpHeight", self.role)

        self.role["skills"] = self.get_damage_skills()
        if self.is_within_range(0):
            closest_enemy_position = self.find_closest_enemy()
            print(f"[MOVE]警戒范围{doge_base}内存在敌人{closest_enemy_position['position']}")
            atk_position, move_steps = self.find_closest_attack_position(self.role, closest_enemy_position["position"])
            if atk_position:
                move_steps = self.get_block_step(move_steps, (1,), self.map)
                if len(move_steps) > 1:
                    print(f"[MOVE]{self.role['HeroID']}:{position}跳跃高度:{jump_height},警戒范围:{doge_base},本回合可移动{round_action},向敌人{closest_enemy_position['position']}移动, 移动目标: {atk_position},攻击位置:{atk_position}, 本次移动{move_steps}")
                    return move_steps
        return []

    def is_combat_teammate(self):
        # 是否存在战斗状态的队友
        teammate_position = self.has_combat_ready_teammate(self.role, self.teammates, self.enemies)
        if teammate_position: return True
        return False

    def move_to_combat_teammate(self):
        # 向战斗状态的队友移动
        round_action = Data.value("RoundAction", self.role)
        position = Data.value("position", self.role)
        jump_height = Data.value("JumpHeight", self.role)

        teammate_position = self.has_combat_ready_teammate(self.role, self.teammates, self.enemies)
        if teammate_position:
            print(f"[MOVE]存在战斗状态的队友: {teammate_position}")
            steps = self.find_shortest_path(position, teammate_position, jump_height, [1, 2, 3])[: round_action + 1]
            move_steps = self.get_block_step(steps, (1,), self.map)
            if len(move_steps) > 1:
                return move_steps
        return []

    def is_boss(self):
        # 是否存在boss
        closest_enemy_position = [e for e in self.enemies if e.get("Quality") == 2]
        if closest_enemy_position:return True
        return False

    def move_to_boss(self):
        doge_base = Data.value("DogBase", self.role)
        round_action = Data.value("RoundAction", self.role)
        position = Data.value("position", self.role)
        jump_height = Data.value("JumpHeight", self.role)

        self.role["skills"] = self.get_damage_skills()
        print(f"[MOVE]警戒范围{doge_base}内没有敌人, 检查BOSS位置")
        closest_enemy_position = [e for e in self.enemies if e.get("Quality") == 2]
        if closest_enemy_position:
            closest_enemy_position = closest_enemy_position[0]
            atk_position, move_steps = self.find_closest_attack_position(self.role, closest_enemy_position["position"])
            print(f"[MOVE]BOSS位置为{closest_enemy_position['position']}")
            if atk_position:
                print(f"[MOVE]{self.role['HeroID']}:{position}跳跃高度:{jump_height},警戒范围:{doge_base},本回合可移动{round_action},向敌人{closest_enemy_position['position']}移动, 移动目标: {atk_position},攻击位置:{atk_position}, 本次移动{move_steps}")
                move_steps = self.get_block_step(move_steps, (1,), self.map)
                if len(move_steps) > 1:
                    return move_steps

        return []

    def wait(self):
        # 本轮行动WAIT
        return [{"action_type": "WAIT"}]


if __name__ == '__main__':
    map = BuildPatrol.build_map(origin_map_data)
    heros = BuildPatrol.build_heros(origin_hero_data)  # heros
    monster = BuildPatrol.build_monster(origin_monster_data)  # monster
    state = {"map": map,
             "hero": heros,
             "monster": monster
             }
    # print(state)

    f = Range(heros[1], state)
    print(f.find_targets_within_atk_range())