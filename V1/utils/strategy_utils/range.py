# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/21 16:06
import time
from collections import deque
from copy import deepcopy
from itertools import product

from log.log import log_manager
from strategy.handler.weight import Weight
from utils.strategy_utils.action_weight import ActionWeight

from utils.strategy_utils.basic_data import Data
from utils.strategy_utils.basic_utils import get_attack_range, find_shortest_path, skill_effect_range, \
    skill_release_range, get_manhattan_path, manhattan_distance, get_damage_skills, is_reach, get_heal_skills


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
                        if Data.value("Hp", _) > 0:
                            self.teammates.append(_)

            if "monster" in state:
                self.enemies = []
                for _ in state["monster"]:
                    if not isinstance(_, dict):
                        _ = _.dict()
                    if Data.value("Hp", _) > 0:
                        _["warning_range"] = self.enemies_in_warning_range(_)
                        self.enemies.append(_)

    def generate_pairs(self, lst):
        # 返回相邻数组  [1, 2, 3] > [[1, 2], [2, 3]]
        return [(lst[i], lst[i + 1]) for i in range(len(lst) - 1)]

    def determine_direction(self, pos1, pos2):
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

    def move_step_handler(self, move_queue):
        res = []
        move = self.generate_pairs(move_queue)
        for m in move:
            f = self.determine_direction(*m)
            m_dict = {
                "action_type": f,
                "move_position": m[1]
            }
            res.append(m_dict)
        return res

    def is_health_below_threshold(self, num):
        # 血量是否小于num比例

        hp = Data.value("Hp", self.role)
        hp_base = Data.value("HpBase", self.role)
        return float(hp) / float(hp_base) <= float(num)

    def get_block_step(self, steps, block_status, maps):
        move_steps = []
        for k, s in enumerate(steps):
            xz = Data.get_xz(s)
            if k > 0:
                if maps[xz]["Block"] not in block_status:
                    break
            move_steps.append(s)
        return move_steps

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

        positions_within_range = get_manhattan_path(*role_position, round_action, jump_height, self.map)
        max_distance_sum = -1
        best_position = None

        for position, routes in positions_within_range.items():
            distance_sum = sum(manhattan_distance(position, Data.value("position", enemy)) for enemy in self.enemies)
            if distance_sum > max_distance_sum:
                max_distance_sum = distance_sum
                best_position = routes

        return self.move_step_handler(best_position)

    def is_in_combat(self, role, enemies):
        # 角色是否处于战斗状态
        if self.enemies_in_warning_range_count(role, enemies) or self.is_role_in_enemies_warning_range(role, enemies):
            return True
        return False

    def has_combat_ready_teammate(self, role, teammates, enemies):
        # 获取在战斗状态的队友的位置
        distance = None
        teammate_position = None
        role_position = Data.value("position", role)
        # print(f"ROLE : {Data.value('HeroID', self.role)}, team_id: {Data.value('team_id', self.role)}, {Data.value('position', self.role)}")
        for t in teammates:
            # print(f"队友: {Data.value('HeroID', t)}, team_id: {Data.value('team_id', t)},{Data.value('position', t)}")
            if Data.value("team_id", role) == Data.value("team_id", t):  # 小队编号一致
                if self.is_in_combat(t, enemies):
                    _teammate_position = Data.value("position", t)
                    _distance = manhattan_distance(role_position, _teammate_position)

                    if distance and teammate_position:
                        if distance > _distance:
                            distance, teammate_position = _distance, _teammate_position
                    else:
                        distance, teammate_position = _distance, _teammate_position
        # if not teammate_position:
        #     state = {"map": self.map,
        #                  "hero": self.teammates + [self.role],
        #                  "monster": self.enemies}
        #     tmp = log_manager.add_log(log_data=str({"role": self.role, "state": state}) )
        #     print(f"无战斗状态的队友log tmp: {tmp}")

        return teammate_position

    def is_atk_distance(self, point1, point2, distance):
        # 攻击是否受到高低差影响
        if abs(point1[1] - point2[1]) <= int(distance):
            return True
        return False

    def is_within_range(self, num):
        # 自己的警戒范围内是否有num个敌人
        doge_base = Data.value("DogBase", self.role)
        role_position = Data.value("position", self.role)
        count = 0
        for enemy in self.enemies:
            enemy_position = Data.value("position", enemy)
            if manhattan_distance(role_position, enemy_position) <= doge_base:
                count += 1
        print(f"警戒范围内是否有>={num}个敌方单位: {num <= count}  ,count:{count}")
        return num <= count

    def find_closest_attack_position(self, hero, enemy_position):
        # 获取对于攻击者来说能攻击到敌人最近的位置，并得到前往这个位置的在round_action行动内的前进列表
        enemy_position = tuple(enemy_position)
        hero_position = Data.value("position", hero)
        jump_height = Data.value("JumpHeight", hero)
        round_action = Data.value("RoundAction", hero)
        attack_pos_dict = {}

        # move_steps = find_shortest_path(hero_position, enemy_position, jump_height, [1, 2, 3], self.map)[: round_action + 1]
        # return move_steps

        queue = deque([hero_position])
        visited = set()  # 用来存储已经访问过的点
        visited.add(hero_position)
        # #
        while queue:
            x, y, z = queue.popleft()
            point = tuple(self.map[(x, z)]["position"])
            _hero = deepcopy(hero)
            _hero["position"] = point

            stk_range = get_attack_range(self.role, point, self.map)
            if enemy_position in stk_range:
                move_steps = find_shortest_path(hero_position, point, jump_height, [1, 2, 3], self.map)[
                             : round_action + 1]
                if move_steps:
                    return move_steps

            for dx, dz in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, nz = x + dx, z + dz
                if (nx, nz) in self.map:
                    _p = tuple(self.map[(nx, nz)]["position"])
                    if _p not in visited:
                        queue.append(_p)
                        visited.add(_p)
        return []

        # for xz in self.map:
        #     point = tuple(self.map[xz]["position"])
        #     _hero = deepcopy(hero)
        #     _hero["position"] = point
        #
        #     stk_range = get_attack_range(self.role, point, self.map)
        #     if enemy_position in stk_range:
        #         move_steps = find_shortest_path(hero_position, point, jump_height, [1, 2, 3], self.map)[
        #                      : round_action + 1]
        #         if move_steps:
        #             attack_pos_dict[point] = move_steps
        #
        # if attack_pos_dict:
        #     closest_pos = min(attack_pos_dict.keys(), key=lambda k: manhattan_distance(k, hero_position))
        #     steps = attack_pos_dict[closest_pos]
        #     return steps
        # else:
        #     return []
    def find_closest_enemy(self):
        # 获取距离最近的敌人
        closest_enemy = None
        min_distance = float('inf')
        role_position = Data.value("position", self.role)

        for enemy in self.enemies:
            enemy_position = Data.value("position", enemy)
            distance = manhattan_distance(role_position, enemy_position)
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def enemies_in_warning_range(self, role):
        # 获取角色的警戒范围
        role_position = Data.value("position", role)
        doge_base = Data.value("DogBase", role)

        warning_range = self.get_manhattan_range(*role_position, doge_base)
        return warning_range

    def nearby_enemy_count(self, num):
        # 获取附近的敌人数量( 是否在num个敌人的警戒范围内
        _count = 0
        role_position = Data.value("position", self.role)

        for enemy in self.enemies:
            enemy_atk_range = self.enemies_in_warning_range(enemy)
            if role_position in enemy_atk_range:
                _count += 1
        return num >= _count

    def enemies_in_warning_range_count(self, role, enemies):
        # 警戒范围内的敌人数量
        doge_base = Data.value("DogBase", role)
        role_position = Data.value("position", role)
        enemies_position = [Data.value("position", _) for _ in enemies]
        warning_range = self.get_manhattan_range(*role_position, doge_base)
        return len(Data.intersection(enemies_position, warning_range))

    def find_enemies_in_range(self, move_pos, skill, paths):
        # 获取技能释放范围内的所有点
        release_range = skill_release_range(move_pos, skill, self.map)
        results = []
        for point in release_range:
            attack_range = skill_effect_range(self.role, point, skill, self.map)
            enemies_in_range = [enemy for enemy in self.enemies if Data.value("position", enemy) in attack_range]
            # if tuple(point) in [Data.value("position", e) for e in enemies_in_range]:
            if len(enemies_in_range) > 0:  # 技能范围内>0的敌人才返回
                results.append(
                    {
                        "hero_pos": move_pos,
                        "skill_pos": point,
                        "skill_range": attack_range,
                        "release_range": release_range,
                        "target": enemies_in_range,
                        "route": paths,
                        "skill": skill,
                        "type": "ATK"
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

    def get_all_possible_heal(self, move_pos, skill, paths):
        """
        获取英雄在某个位置可以施放技能并且治疗到队友
        :param move_pos: 英雄可以移动到的位置
        """
        release_range = skill_release_range(move_pos, skill, self.map)
        results = []
        for point in release_range:
            skill_range = skill_effect_range(self.role, point, skill, self.map)
            t_in_range = [t for t in self.teammates + [self.role] if Data.value("position", t) in skill_range]  # 治疗对象为队友+自己
            if tuple(point) in [Data.value("position", e) for e in t_in_range]:
                if len(t_in_range) > 0:  # 技能范围内>0的目标才返回
                    results.append(
                        {
                            "hero_pos": move_pos,
                            "skill_pos": point,
                            "skill_range": skill_range,
                            "release_range": release_range,
                            "target": t_in_range,
                            "route": paths,
                            "skill": skill,
                            "type": "HEAL"
                        }
                    )
        return results

    def find_targets_within_atk_range(self):
        # 获取在攻击范围内的目标选项
        pick_list = []
        skills = get_damage_skills(self.role)
        doge_base = Data.value("DogBase", self.role)
        max_step = Data.value("RoundAction", self.role)
        position = Data.value("position", self.role)
        jump_height = Data.value("JumpHeight", self.role)

        print(
            f"[ATK]警戒范围内存在敌人, 攻击者{self.role['HeroID']}{position},警戒范围{doge_base}, 本回合可移动{max_step}, 跳跃高度:{jump_height},  本次可用技能:{len(skills)}")
        move_positions = get_manhattan_path(*position, max_step, jump_height, self.map)  # 英雄可移动到的点位
        for move, paths in move_positions.items():
            for skill in skills:
                pick_list += self.get_all_possible_attacks(move, skill, paths)

        # if pick_list:
        # state = {"map": self.map,
        #          "hero": self.teammates + [self.role],
        #          "monster": self.enemies}
        # tmp = log_manager.add_log(log_data=str({"role": self.role, "state": state}) )
        # print(f"log tmp: {tmp}")
        print(f"[ATK]攻击可选择数量为: {len(pick_list)}")
        return pick_list

    def find_targets_within_heal_range(self):
        # 获取在可治疗的释放范围内的目标选项
        pick_list = []
        skills = get_heal_skills(self.role)
        max_step = Data.value("RoundAction", self.role)
        position = Data.value("position", self.role)
        jump_height = Data.value("JumpHeight", self.role)
        move_positions = get_manhattan_path(*position, max_step, jump_height, self.map)  # 英雄可移动到的点位

        for move, paths in move_positions.items():
            for skill in skills:
                pick_list += self.get_all_possible_heal(move, skill, paths)

        print(f"[HEAl]治疗可选择数量为: {len(pick_list)}")
        return pick_list

    def find_heal_target(self):
        pick_list = self.find_targets_within_heal_range()
        if pick_list:
            pick = ActionWeight(
                self.role,
                self.teammates,
                self.enemies,
                self.map
            ).select_assist_strategy(pick_list)
        else:
            return []

        pick_data = pick["data"]
        print(f"[HEAL]本次治疗选择", pick_data)
        action_step = []
        if pick_data["hero_pos"] != Data.value("position", self.role):
            action_step += self.move_step_handler(pick_data["route"])
        action_step.append(
            {"action_type": f"SKILL_{pick_data['skill']['SkillId']}", "skill_range": pick_data["skill_range"],
             "skill_pos": pick_data["skill_pos"], "target": pick_data["target"], "release_range": pick_data["release_range"], "type": "HEAL"})
        return action_step

    def find_attack_target(self):
        # 确定攻击目标
        t = time.time()
        pick = {}
        pick_list = self.find_targets_within_atk_range()
        if pick_list:
            pick = ActionWeight(
                self.role,
                self.teammates,
                self.enemies,
                self.map
            ).select_attack_strategy(pick_list)
        else:
            return []

        # for each in pick_list:
        #     _weight = Weight().clac_skill_weight(each)
        #     if not pick:
        #         pick = {"weight": _weight, "data": each}
        #         continue
        #     if pick["weight"] < _weight:
        #         pick = {"weight": _weight, "data": each}
        print(f"[ATK]本次行动为攻击,攻击者在{pick['data']['hero_pos']}位置对{pick['data']['skill_pos']}位置施放技能[{pick['data']['skill']['SkillId']}], 需要移动{pick['data']['route']}")
        pick_data = pick["data"]
        action_step = []
        if pick_data["hero_pos"] != Data.value("position", self.role):
            action_step += self.move_step_handler(pick_data["route"])
        action_step.append(
            {"action_type": f"SKILL_{pick_data['skill']['SkillId']}", "skill_range": pick_data["skill_range"],
             "skill_pos": pick_data["skill_pos"], "target": pick_data["target"],
             "release_range": pick_data["release_range"], "type": pick_data["type"]})

        return action_step

    def move_to_enemy(self):
        # 向最近的敌人移动
        doge_base = Data.value("DogBase", self.role)
        round_action = Data.value("RoundAction", self.role)
        position = Data.value("position", self.role)
        jump_height = Data.value("JumpHeight", self.role)

        self.role["skills"] = get_damage_skills(self.role)
        if self.is_within_range(0):
            closest_enemy_position = self.find_closest_enemy()
            print(f"[MOVE]警戒范围{doge_base}内存在敌人{closest_enemy_position['position']}")
            move_steps = self.find_closest_attack_position(self.role, closest_enemy_position["position"])
            if move_steps:
                move_steps = self.get_block_step(move_steps, (1,), self.map)
                if len(move_steps) > 1:
                    # state = {"map": self.map,
                    #          "hero": self.teammates + [self.role],
                    #          "monster": self.enemies}
                    # tmp = log_manager.add_log(log_data=str({"role": self.role, "state": state}))
                    # print(f"log tmp: {tmp}")
                    print(
                        f"[MOVE]{self.role['HeroID']}:{position}跳跃高度:{jump_height},警戒范围:{doge_base},本回合可移动{round_action},向敌人{closest_enemy_position['position']}移动, 本次移动{move_steps}")
                    return self.move_step_handler(move_steps)
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

            steps = find_shortest_path(position, teammate_position, jump_height, [1, 2, 3], self.map)[
                    : round_action + 1]
            move_steps = self.get_block_step(steps, (1,), self.map)
            if len(move_steps) > 1:
                return self.move_step_handler(move_steps)
        return []

    def is_boss(self):
        # 是否存在boss
        closest_enemy_position = [e for e in self.enemies if e.get("Quality") == 2]
        if closest_enemy_position: return True
        return False

    def move_to_boss(self):
        doge_base = Data.value("DogBase", self.role)
        round_action = Data.value("RoundAction", self.role)
        position = Data.value("position", self.role)
        jump_height = Data.value("JumpHeight", self.role)

        self.role["skills"] = get_damage_skills(self.role)
        print(f"[MOVE]警戒范围{doge_base}内没有敌人, 检查BOSS位置")
        closest_enemy_position = [e for e in self.enemies if e.get("Quality") == 2]
        if closest_enemy_position:
            closest_enemy_position = closest_enemy_position[0]
            move_steps = self.find_closest_attack_position(self.role, closest_enemy_position["position"])
            print(f"[MOVE]BOSS位置为{closest_enemy_position['position']}", move_steps)
            if move_steps:
                print(
                    f"[MOVE]{self.role['HeroID']}:{position}跳跃高度:{jump_height},警戒范围:{doge_base},本回合可移动{round_action},向敌人{closest_enemy_position['position']}移动,本次移动{move_steps}")
                move_steps = self.get_block_step(move_steps, (1,), self.map)
                if len(move_steps) > 1:
                    return self.move_step_handler(move_steps)

        return []

    def wait(self):
        # 本轮行动WAIT
        state = {"map": self.map,
                 "hero": self.teammates + [self.role],
                 "monster": self.enemies}
        tmp = log_manager.add_log(log_data=str({"role": self.role, "state": state}))
        print(f"wait: log tmp: {tmp}")
        return [{"action_type": "WAIT"}]

    def is_heal(self, k1, k2, k3):
        skills = get_heal_skills(self.role)
        # state = {"map": self.map,
        #              "hero": self.teammates + [self.role],
        #              "monster": self.enemies}
        # tmp = log_manager.add_log(log_data=str({"role": self.role, "state": state}) )
        # print(f"HEAL log tmp: {tmp}")
        print(f'[HEAL]可用治疗技能数量: {len(skills)}')

        if skills:
            doge_base = Data.value("DogBase", self.role)
            role_position = Data.value("position", self.role)
            for t in self.teammates + [self.role]:
                t_position = Data.value("position", t)
                if manhattan_distance(role_position, t_position) <= doge_base:
                    if self.is_in_combat(t, self.enemies):
                        if Data.value("ClassType3", t) == 1:
                            if float(Data.value("Hp", t) / Data.value("HpBase", t)) < k1:
                                print(f"[HEAL]存在可治疗角色, 有战斗中前卫防守型角色血量低于{k1 * 100}%: {Data.value('HeroID', t)}")
                                return True

                        if float(Data.value("Hp", t) / Data.value("HpBase", t)) < k2:
                            print(f"[HEAL]存在可治疗角色, 任何战斗中角色血量低于{k2 * 100}%: {Data.value('HeroID', t)}")
                            return True
                    else:
                        if float(Data.value("Hp", t) / Data.value("HpBase", t)) < k3:
                            print(f"[HEAL]存在可治疗角色, 任何非战斗中角色血量低于{k3 * 100}%: {Data.value('HeroID', t)}")
                            return True
        print("[HEAL]无可治疗角色")
        return False

    def simple_strategy(self):
        # 返回当前可行动的步骤
        steps = {
            "MOVE": [],  # 可移动
            "ATK": [],  # 可攻击
            "HEAL": []  # 可治疗
        }

        atk = []
        heal = []

        skills = get_damage_skills(self.role)
        heal_skills = get_heal_skills(self.role)
        hero_position = Data.value("position", self.role)
        jump_height = Data.value("JumpHeight", self.role)
        print(f"role position: {hero_position}")

        # 可移动选择
        for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_coord = (hero_position[0] + dx, hero_position[2] + dz)
            if next_coord in self.map:
                next_pos = self.map[next_coord]
                _block_cost = Data.block_score(next_pos)
                if is_reach(self.role, next_pos, jump_height, [1]):
                    print(f"可移动步骤：{hero_position} > {next_pos['position']}")
                    steps["MOVE"].append(self.move_step_handler([hero_position, next_pos["position"]]))

        # 可攻击选择
        for skill in skills:
            atk += self.get_all_possible_attacks(hero_position, skill, [])

        for _ in atk:
            steps["ATK"].append({"action_type": f"SKILL_{_['skill']['SkillId']}", "skill_range": _["skill_range"],
                                 "skill_pos": _["skill_pos"], "target": _["target"], "release_range": _["release_range"], "type": _["type"]})

        # 可治疗选择
        for skill in heal_skills:
            heal += self.get_all_possible_heal(hero_position, skill, [])

        for _ in heal:
            steps["HEAL"].append({"action_type": f"SKILL_{_['skill']['SkillId']}", "skill_range": _["skill_range"],
                                 "skill_pos": _["skill_pos"], "target": _["target"], "release_range": _["release_range"], "type": _["type"]})

        return steps




if __name__ == '__main__':
    tmp = "2024-09-06 10:44:11"
    # print(log_manager.get_log(tmp))

    tmp_data = eval(log_manager.get_log(tmp))
    print(tmp_data.keys())

    state = tmp_data["state"]
    role = tmp_data["role"]

    r = Range(role, state)
    r.simple_strategy()
