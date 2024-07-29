# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:25
from V1.strategy.handler.self_func import SelfFunc
from V1.strategy.handler.skill_func import SkillFunc
from V1.strategy.handler.distance_func import DistanceFunc


class Action(object):
    def heal(self, hero, enemies, maps):
        hero_hp = hero["Hp"]
        hero_base_hp = hero["HpBase"]
        hero_skills = hero["skills"]
        hero_position = hero["position"]
        hero_max_step = hero["max_step"]

        if len(DistanceFunc().is_within_enemy_range(hero_position, enemies)) > 1:
            if SelfFunc().is_health_sub_half(hero_hp, hero_base_hp):
                if SkillFunc().can_heal_skill(hero_skills):

                    SelfFunc.execute_heal()
                    print("加血 ！")
                    return True, {"action_type": "heal", "steps": []}
                else:
                    move_seq = SelfFunc.escape(hero_position, enemies, maps, hero_max_step)
                    print(f"逃跑 ！{move_seq}")
                    return True, {"action_type": "move", "steps": move_seq}
        return False, {}

    def attack(self, hero, enemies, maps):
        hero_skills = hero["skills"]
        hero_position = hero["position"]
        hero_max_step = hero["max_step"]
        hero_normal_attack_range = hero["normal_attack_range"]

        if SkillFunc().has_attack_skill_available(hero_skills):
            res, move_queue, attack = SelfFunc().can_skill_attack_multiple_enemies(
                hero_position, hero_skills, enemies, maps, hero_max_step
            )

            if res:
                print(f"移动步骤：{move_queue}, 技能攻击：{attack}")
                return True, [{"action_type": "move", "steps": move_queue}, {"action_type": "skill_attack", "steps": attack}]
            else:
                res, move_queue, attack = SelfFunc().can_normal_attack_multiple_enemies(
                    hero_position, hero_normal_attack_range, enemies, maps, hero_max_step
                )
                if res:
                    print(f"移动步骤：{move_queue}, 普通攻击：{attack}")
                    return True, [{"action_type": "move", "steps": move_queue}, {"action_type": "normal_attack", "steps": attack}]

        return False, {}

    def move(self, hero, enemies, maps):
        hero_skills = hero["skills"]
        hero_dog_base = hero["dogBase"]
        hero_position = hero["position"]
        hero_max_step = hero["max_step"]
        boss = [enemies[0]]   # TODO 假设BOSS
        hero_normal_attack_range = hero["normal_attack_range"]

        if DistanceFunc().is_within_attack_range(hero_dog_base, hero_position, enemies):
            res, move_queue, attack = SelfFunc().can_normal_attack_multiple_enemies(
                hero_position, hero_normal_attack_range, enemies, maps, hero_max_step
            )
            print("警戒范围内有敌方单位: ", move_queue)
            return True, [{"action_type": "move", "steps": move_queue}]

        else:
            res, move_queue, attack = SelfFunc().can_normal_attack_multiple_enemies(
                hero_position, hero_normal_attack_range, boss, maps, hero_max_step
            )
            print("警戒范围无有敌方单位， 向boss地点移动:", move_queue)
            return True, [{"action_type": "move", "steps": move_queue}]

    def hero_action(self, hero, enemies, maps):
        tf, steps = self.heal(hero, enemies, maps)
        if tf:
            return steps
        else:
            tf, steps = self.attack(hero, enemies, maps)
            if tf:
                return steps
            else:
                tf, steps = self.move(hero, enemies, maps)
                if tf:
                    return steps
                else:
                    raise Exception("ERROR!")

    def monster_action(self):
        print("敌人在原地发呆！")

    def choose_action(self, step):
        if step["action_type"] == "heal" and step["steps"]:
            print("执行虎哥[加血]函数")
        if step["action_type"] == "move" and step["steps"]:
            print("执行虎哥[移动]函数")
        if step["action_type"] == "normal_attack" and step["steps"]:
            print("执行虎哥[普通攻击]函数")
        if step["action_type"] == "skill_attack" and step["steps"]:
            print("执行虎哥[技能攻击]函数")

    def run_action(self, steps):
        if isinstance(steps, dict):
            self.choose_action(steps)
        if isinstance(steps, list):
            for step in steps:
                self.choose_action(step)


if __name__ == '__main__':
    from V1.strategy.handler.constant import HERO, ENEMY_A, ENEMY_B, MAPS

    hero = HERO
    maps = MAPS
    enemies = [ENEMY_A, ENEMY_B]

    f = Action()
    s = f.hero_action(hero, enemies, maps)
    print('-->', s)
    f.run_action(s)