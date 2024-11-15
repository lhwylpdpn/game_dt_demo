# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/8/30 18:32
import heapq
import sys
from itertools import product
from collections import OrderedDict

from utils.strategy_utils.basic_data import Data


class DictLRUCache:
    def __init__(self, max_size_mb):
        self.cache = OrderedDict()  # 使用有序字典来保持插入顺序
        self.max_size = max_size_mb * 1024 * 1024  # 最大缓存大小（字节）
        self.current_size = 0  # 当前缓存使用的大小

    def _make_hashable(self, item):
        """将不可哈希的字典转换为 frozenset，并递归处理元组或列表"""
        if isinstance(item, dict):
            return frozenset((k, self._make_hashable(v)) for k, v in item.items())
        elif isinstance(item, (tuple, list)):
            return tuple(self._make_hashable(i) for i in item)
        return item

    def __call__(self, func):
        def wrapper(*args):
            # 将所有传入参数转换为可哈希形式
            hashable_args = tuple(self._make_hashable(arg) for arg in args)

            if hashable_args in self.cache:
                # 移动最近访问的项到最后
                self.cache.move_to_end(hashable_args)
                return self.cache[hashable_args]

            result = func(*args)
            result_size = sys.getsizeof(result)

            if result_size + self.current_size > self.max_size:
                self._evict_cache(result_size)

            # 更新缓存
            self.cache[hashable_args] = result
            self.current_size += result_size
            return result

        return wrapper

    def _evict_cache(self, needed_size):
        while self.current_size + needed_size > self.max_size and self.cache:
            # 删除最早插入的缓存项
            evicted_key, evicted_value = self.cache.popitem(last=False)
            self.current_size -= sys.getsizeof(evicted_value)


def get_maps_point(xz, map):
    y = map[xz]["y"]
    return xz[0], y, xz[1]


def is_atk_distance(point1, point2, distance):
    # 攻击是否受到高低差影响
    if abs(point1[1] - point2[1]) <= int(distance):
        return True
    return False


def is_reach(start, end, jump_height, block_type=None):
    # 是否可到达
    if not block_type:
        block_type = [0, 2, 3]

    if abs(start["position"][1] - end["position"][1]) <= int(jump_height):
        if end["Block"] in block_type:
            return True
    return False


def get_damage_skills(role):
    # 获取主动的可用的攻击技能
    s = []
    available_skills = role.get("AvailableSkills", [])
    for skill in role["skills"]:
        if skill["SkillId"] in available_skills:
            if skill["SkillClass"] == 1 and skill["SkillCalc"] == 1 and 1 in skill["SkillGoals"]:
                if "ATK_DISTANCE" in skill["effects"]:
                    if skill["DefaultSkills"] == 1:  # 普攻
                        s.append(skill)
                    else:
                        if int(skill["use_count"]) > 1 or skill["use_count"] == -1:
                            s.append(skill)
    return s


def get_heal_skills(role):
    # 获取主动的可用的治疗技能
    s = []
    available_skills = role.get("AvailableSkills", [])
    for skill in role["skills"]:
        if skill["SkillId"] in available_skills:
            if skill["SkillClass"] == 1 and skill["SkillCalc"] == 5:
                if 4 in skill["SkillGoals"]:
                    if "ATK_DISTANCE" in skill["effects"]:
                        if int(skill["use_count"]) > 1 or skill["use_count"] == -1:
                            s.append(skill)
                if 3 in skill["SkillGoals"]:
                    if int(skill["use_count"]) > 1 or skill["use_count"] == -1:
                        s.append(skill)
    return s



def manhattan_distance(point1, point2):
    # 曼哈顿距离计算 （ 只计算xz
    point1, point2 = tuple(point1), tuple(point2)
    return abs(point1[0] - point2[0]) + abs(point1[2] - point2[2])

def square_distance_points(point, distances):
    # 获取某个点位  正方形范围内的所有点位
    x, z = point
    points = set()  # 使用集合避免重复点
    for distance in distances:
        distance = int(distance)
        for dx in range(-distance, distance + 1):
            for dz in range(-distance, distance + 1):
                points.add((x + dx, z + dz))

    return list(points)


def h_manhattan_distance(point1, point2, gap, h_effect):
    # 受高度差影响的曼哈顿距离
    base_distance = manhattan_distance(point1, point2)
    adjusted_distance = base_distance

    # 计算高度差异对距离的额外影响
    if gap and h_effect:
        gap, h_effect = int(gap), int(h_effect)
        height_difference = point1[1] - point2[1]

        if abs(height_difference) >= gap:
            extra_effects = (abs(height_difference) // gap) * h_effect
            adjusted_distance += extra_effects

    return adjusted_distance


# @DictLRUCache(max_size_mb=128)
def get_manhattan_path(x, y, z, max_distance, jump_height=None, map=None):
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
                if p not in map:
                    continue

                if map[p].get("Block") in (1, 2, 3):
                    continue
                point = get_maps_point(p, map)

                if jump_height is not None:
                    if abs(current_y - point[1]) > jump_height:
                        continue
                if (point[0], point[1], point[2]) not in visited:
                    points.append(point)
                    new_path = path + [point]
                    paths[point] = new_path
                    queue.append((point, new_path))
    return paths


# @DictLRUCache(max_size_mb=128)
def find_shortest_path(start, end, jump_height, block_type=None, map=None):
    # 查找点与点之间的可通行的最近路径， 返回路径list
    start, end = tuple(start), tuple(end)
    start_pos = map[(start[0], start[2])]
    # end_pos = maps[(end[0], end[2])]
    paths = []

    open_set = []
    heapq.heappush(open_set, (0, start_pos['position']))

    came_from = {}
    g_score = {start_pos['position']: 0}
    f_score = {start_pos['position']: manhattan_distance(start_pos['position'], end)}

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
        current = map[(x, z)]
        for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_coord = (x + dx, z + dz)
            if next_coord in map:
                next_pos = map[next_coord]
                _block_cost = Data.block_score(next_pos)
                tentative_g_score = g_score[current_position] + _block_cost
                if is_reach(current, next_pos, jump_height, block_type):
                    if next_pos['position'] not in g_score or tentative_g_score < g_score[next_pos['position']]:
                        came_from[next_pos['position']] = current_position
                        g_score[next_pos['position']] = tentative_g_score
                        f_score[next_pos['position']] = tentative_g_score + manhattan_distance(
                            next_pos['position'], end)
                        heapq.heappush(open_set, (f_score[next_pos['position']], next_pos['position']))
    if paths:
        return min(paths, key=lambda x: x[1])[0]
    return []

def range_cross(point, o, i, gap, effect, map):
    o = int(o) + 1
    i = int(i) + 1
    atk_range = []
    positions = []
    x, y, z = point
    for r in [i, o]:
        # 水平方向
        for p in [(x + r, z), (x - r, z), (x, z + r), (x, z - r)]:
            if p in map:
                positions.append(map[p]["position"])
    return positions


# @DictLRUCache(max_size_mb=128)
def range_mht_hollow_circle(point, o, i, gap, effect, map):
    # 获取空心菱形范围  o: 外圆范围 i: 内圆范围
    o = int(o) + 1
    i = int(i) + 1
    atk_limit = range(i, o)
    atk_range = []

    for m in map:
        m_pos = map[m]["position"]
        if h_manhattan_distance(point, m_pos, gap, effect) in atk_limit:
            atk_range.append(m_pos)
    if i == 1:
        atk_range.append(point)
    return atk_range


# @DictLRUCache(max_size_mb=128)
def skill_release_range(position, skill, map, role):
    # 获取某个技能施放范围（射程
    points = []
    gap, effect = 0, 0
    if "ATK_DISTANCE" not in skill["effects"]:
        return [position]

    if "ADD_ATK_DISTANCE" in skill["effects"]:
        gap, effect = skill["effects"]["ADD_ATK_DISTANCE"]["param"][0], skill["effects"]["ADD_ATK_DISTANCE"]["param"][1]

    if "ATK_DISTANCE" in skill["effects"]:
        range = skill["effects"]["ATK_DISTANCE"]["param"]
        points = range_mht_hollow_circle(position, int(range[1]), int(range[0]), gap, effect, map)

    if "ATK_DISTANCE_CROSS" in skill["effects"]:
        range = skill["effects"]["ATK_DISTANCE_CROSS"]["param"]
        points = range_cross(position, int(range[1]), int(range[0]), gap, effect, map)

    return points


# @DictLRUCache(max_size_mb=128)
def hit_line_range(move_point, point, param, map):
    # 线性技能的攻击范围
    x, y, z = point
    x1, y1, z1 = move_point
    attack_range = []  # 包含该点位自身
    param = [abs(int(_)) for _ in param]
    param_a, param_b = param[0], param[1]

    # 如果x相等，计算左右范围
    if x == x1:
        for i in range(-param_a, param_b + 1):
            # attack_range.append((x, z + i))
            xz = (x + i, z)
            if xz in map:
                attack_range.append(Data.get_maps_point(xz, map))

    # 如果z相等，计算上下范围
    elif z == z1:
        for i in range(-param_a, param_b + 1):
            xz = (x, z + i)
            if xz in map:
                attack_range.append(Data.get_maps_point(xz, map))

    return attack_range


# @DictLRUCache(max_size_mb=128)
def skill_effect_range(move_point, point, skill, map):
    # 获取在point点位施放技能的生效范围
    atk_range = []
    point = tuple(point)

    hit_line = skill["effects"].get("HIT_LINE", {}).get("param")
    hit_range = skill["effects"].get("HIT_RANGE", {}).get("param")
    check_atk_distance = skill["effects"].get("IS_ATK_DISTANCE", {}).get("param", [0])[0]

    if hit_line:
        atk_range += hit_line_range(tuple(move_point), point, hit_line, map)  # TODO
    if hit_range:
        if "ADD_ATK_DISTANCE" in skill["effects"]:
            gap, effect = skill["effects"]["ADD_ATK_DISTANCE"]["param"][0], \
                skill["effects"]["ADD_ATK_DISTANCE"]["param"][1]
        else:
            gap, effect = 0, 0
        atk_range += range_mht_hollow_circle(point, hit_range[1], hit_range[0], gap, effect, map)
    if not atk_range and not hit_range:  # 单体攻击
        atk_range = [point]

    if check_atk_distance:  # 判断高低差影响
        atk_range = [_ for _ in atk_range if is_atk_distance(point, _, check_atk_distance)]
    return atk_range


def get_attack_range(role, position, map):
    # 获取攻击者, 在传入的点位上, 所有可释放范围内所有技能的攻击范围并集
    attack_range = []
    skills = get_damage_skills(role)
    for skill in skills:
        release_range = skill_release_range(position, skill, map, role=role)
        for point in release_range:
            attack_range += skill_effect_range( Data.value("position", role), point, skill, map)
    return set(tuple(attack_range))
