# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:25
from strategy.game_utils import GameUtils
from strategy.handler.attack import Attack
from strategy.handler.move import Move


class Action(object):

    def move_step_handler(self, move_queue):
        res = []
        move = GameUtils.generate_pairs(move_queue)
        for m in move:
            f = GameUtils.determine_direction(*m)
            m_dict = {
                "action_type": f,
                "move_position": m[1]
            }
            res.append(m_dict)
        return res

    def monster_action(self):
        print("敌人在原地发呆！")

    def choose_action(self, step, hero, state):
        res = {"action_type": step["action_type"]}
        if step["action_type"] in ["LEFT", "RIGHT", "TOP", "BOTTOM"]:
            hero.move_position(*step["move_position"], state)

        if "SKILL_" in step["action_type"]:
            attack_enemies_ids = [_["HeroID"] for _ in step["attack_enemies"]]
            skill = [s for s in hero.skills if s.SkillId == int(step["action_type"].replace("SKILL_", ""))][0]
            attack_enemies = [e for e in state["monster"] if e.HeroID in attack_enemies_ids]
            hero.func_attack(attack_enemies, skill, step["atk_position"], state)
            res["atk_range"] = step["atk_range"]
            res["atk_position"] = step["atk_position"]
            res["release_range"] = step["release_range"]
        if step["action_type"] == "WAIT":
            return step
        return res

    def attack(self, hero, atk_pick):
        action_step = []
        hero_position = hero["position"]

        if atk_pick["hero_pos"] != hero_position:
            action_step += self.move_step_handler(atk_pick["route"])
        action_step.append(
            {"action_type": f"SKILL_{atk_pick['skill']['SkillId']}", "atk_range": atk_pick["atk_range"],
             "atk_position": atk_pick["skill_pos"], "attack_enemies": atk_pick["enemies_in_range"], "release_range": atk_pick["release_range"]})
        # print('action_step: ----->', action_step)
        return action_step

    def move(self, hero, enemies, maps):
        move_steps = Move().choose_move_steps(hero, enemies, maps)
        action_step = self.move_step_handler(move_steps)
        return action_step

    def run_action(self, steps, hero, state):
        # print(f"本次行动步骤：{steps}")
        return self.choose_action(steps, hero, state)

    def get_action_steps(self, hero, enemies, maps):
        print('-----------------------------------------')
        print(f"攻击者位置{hero['position']}, 跳跃高度为{hero['JumpHeight']}, 敌人们的位置为: {[_['position'] for _ in enemies]}")
        # 判断是否逃跑
        if Move().is_escape(hero, enemies, maps):
            move_steps = Move().escape(hero, enemies, maps)
            return self.move_step_handler(move_steps)

        # 判断能否攻击
        atk_pick = Attack().find_targets_within_atk_range(hero, enemies, maps)
        if atk_pick:
            pick_data = Attack().select_atk(atk_pick)
            return self.attack(hero, pick_data)

        # 选择移动
        move_steps = Move().choose_move_steps(hero, enemies, maps)
        steps = self.move_step_handler(move_steps)
        if steps:
            return steps
        else:
            return [{"action_type": "WAIT"}]


if __name__ == '__main__':
    from strategy.handler.constant import HERO, ENEMY_A, ENEMY_B, MAPS

    hero = HERO
    maps = MAPS
    enemies = [ENEMY_A, ENEMY_B]

