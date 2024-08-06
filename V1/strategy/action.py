# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:25
from V1.strategy.handler.attack import Attack
from V1.strategy.handler.move import Move
from V1.strategy.handler.self_func import SelfFunc
from V1.strategy.handler.skill_func import SkillFunc
from V1.strategy.handler.distance_func import DistanceFunc


class Action(object):

    def move_step_handler(self, move_queue):
        res = []
        move = SelfFunc().generate_pairs(move_queue)
        for m in move:
            f = SelfFunc().determine_direction(*m)
            m_dict = {
                "action_type": f,
                "move_position": m[1]
            }
            res.append(m_dict)
        return res

    def monster_action(self):
        print("敌人在原地发呆！")

    def choose_action(self, step, hero, monster):
        res = {"action_type": step["action_type"]}
        if step["action_type"] in ["LEFT", "RIGHT", "TOP", "BOTTOM"]:
            hero.move_position(*step["move_position"])

        if "SKILL_" in step["action_type"]:
            attack_enemies_ids = [_["HeroID"] for _ in step["attack_enemies"]]
            skill = [s for s in hero.skills if s.SkillId == int(step["action_type"].replace("SKILL_", ""))][0]
            attack_enemies = [e for e in monster if e.HeroID in attack_enemies_ids]
            hero.func_attack(attack_enemies, skill)
            res["atk_range"] = step["atk_range"]
            res["atk_position"] = step["atk_position"]
        return res

    def attack(self, hero, atk_pick):
        action_step = []
        hero_position = hero["position"]

        if atk_pick["hero_pos"] != hero_position:
            action_step += self.move_step_handler(atk_pick["route"])
        action_step.append(
            {"action_type": f"SKILL_{atk_pick['skill']['SkillId']}", "atk_range": atk_pick["atk_range"],
             "atk_position": atk_pick["skill_pos"], "attack_enemies": atk_pick["enemies_in_range"]})
        # print('action_step: ----->', action_step)
        return action_step

    def move(self, hero, enemies, maps):
        move_steps = Move().choose_move_steps(hero, enemies, maps)
        action_step = self.move_step_handler(move_steps)
        return action_step

    def run_action(self, steps, hero, monster):
        # print(f"本次行动步骤：{steps}")
        return self.choose_action(steps, hero, monster)

    def get_action_steps(self, hero, enemies, maps):
        # 判断是否逃跑
        if Move().is_escape(hero, enemies, maps):
            print("逃跑！")
            move_steps = Move().escape(hero, enemies, maps)
            return self.move_step_handler(move_steps)

        # 判断能否攻击
        atk_pick = Attack().find_targets_within_atk_range(hero, enemies, maps)
        if atk_pick:
            print("攻击！")
            pick_data = Attack().select_atk(atk_pick)
            return self.attack(hero, pick_data)

        # 选择移动
        move_steps = Move().choose_move_steps(hero, enemies, maps)
        # print('--?', move_steps)
        return self.move_step_handler(move_steps)


if __name__ == '__main__':
    from V1.strategy.handler.constant import HERO, ENEMY_A, ENEMY_B, MAPS

    hero = HERO
    maps = MAPS
    enemies = [ENEMY_A, ENEMY_B]

