def get_manhattan_range(x, y, max_distance):
    points = []
    for dx in range(-max_distance, max_distance + 1):
        for dy in range(-max_distance, max_distance + 1):
            if abs(dx) + abs(dy) <= max_distance:
                points.append((x + dx, y + dy))
    return points


def get_skill_attack_range(skill, x, y, direction):
    if skill == "A":
        if direction == "up":
            return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y - 2), (x, y - 3)]
        elif direction == "down":
            return [(x, y + 1), (x - 1, y), (x + 1, y), (x, y + 2), (x, y + 3)]
        elif direction == "left":
            return [(x - 1, y), (x, y - 1), (x, y + 1), (x - 2, y), (x - 3, y)]
        elif direction == "right":
            return [(x + 1, y), (x, y - 1), (x, y + 1), (x + 2, y), (x + 3, y)]
    elif skill == "B":
        attack_range = set(get_manhattan_range(x, y, 3)) - set(get_manhattan_range(x, y, 2))
        return list(attack_range)
    else:
        return []


def find_enemies_in_range(hero_pos, direction, enemies, skill, skill_range):
    # 获取技能释放范围内的所有点
    manhattan_range = get_manhattan_range(hero_pos[0], hero_pos[1], skill_range)

    results = []
    # 在这些点上应用攻击范围
    for point in manhattan_range:
        attack_range = get_skill_attack_range(skill, point[0], point[1], direction)
        enemies_in_range = [enemy for enemy in enemies if (enemy['x'], enemy['y']) in attack_range]
        results.append([hero_pos, point, enemies_in_range])

    return results


def get_all_possible_attacks(start_pos, move_range, direction, enemies, skill, skill_range):
    # 获取英雄可移动的范围
    move_positions = get_manhattan_range(start_pos[0], start_pos[1], move_range)

    all_attacks = []
    for move_pos in move_positions:
        # 获取从每个移动位置出发的所有攻击可能
        attacks = find_enemies_in_range(move_pos, direction, enemies, skill, skill_range)
        all_attacks.extend(attacks)

    return all_attacks


# 示例数据
hero_position = (5, 5)
direction = "up"
enemies = [{'x': 4, 'y': 4}, {'x': 6, 'y': 4}, {'x': 5, 'y': 3}, {'x': 5, 'y': 7}]
move_range = 2

# 技能A
# skill_A = "A"
# skill_A_range = 2
# possible_attacks_A = get_all_possible_attacks(hero_position, move_range, direction, enemies, skill_A, skill_A_range)
#
# print("Skill A Possible Attacks:")
# for attack in possible_attacks_A:
#     print(f"Hero moved to: {attack[0]}, Skill released at: {attack[1]}, Enemies attacked: {attack[2]}")

# 技能B
skill_B = "B"
skill_B_range = 1
possible_attacks_B = get_all_possible_attacks(hero_position, move_range, direction, enemies, skill_B, skill_B_range)

print("\nSkill B Possible Attacks:")
for attack in possible_attacks_B:
    print(f"Hero moved to: {attack[0]}, Skill released at: {attack[1]}, Enemies attacked: {attack[2]}")
