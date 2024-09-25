# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:25
import time

from models.buff import Buff
from strategy.game_utils import GameUtils
from strategy.handler.attack import Attack
from strategy.handler.move import Move
from utils.strategy_utils.range import Range


class Action(object):
    def calc_damage(self, damage_data):
        d = []
        for each in damage_data:
            damage = [_["damage"] for _ in damage_data[each]]
            pre_damage = [_["pre_damage"] for _ in damage_data[each]]
            st = [_["st"] for _ in damage_data[each]]

            d.extend([[[each.__class__.__name__.lower(), each.HeroID], damage, pre_damage, st]])
        return d

    def calc_effect(self, effect_data):
        d = []
        for each in effect_data:
            for e in effect_data[each]:
                if e["effects"]:
                    eff = [_["effect_id"] for _ in e["effects"]]
                    d.extend([[[each.__class__.__name__.lower(), each.HeroID], eff, []]])
        return d

    def calc_heal(self, heal_data):
        d = []
        for each in heal_data:
            heal = [_["heal"] for _ in heal_data[each]]
            pre_damage = [_["pre_heal"] for _ in heal_data[each]]
            # st = [_["st"] for _ in heal_data[each]]

            d.extend([[[each.__class__.__name__.lower(), each.HeroID], heal, pre_damage]])
        return d

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
            res["move_position"] = step["move_position"]

        if step["action_type"] == "MOVE_START":
            res["move_start"] = Range(hero, state).role_move_start()
            return res

        if "EFFECT_" in step["action_type"]:
            hero.trigger_buff(step)

        if "SKILL_" in step["action_type"]:
            skill = [s for s in hero.skills if s.SkillId == int(step["action_type"].replace("SKILL_", ""))][0]

            if step["type"] == "ATK":
                attack_enemies_ids = [_["HeroID"] for _ in step["target"]]
                attack_enemies = [e for e in state["monster"] if e.HeroID in attack_enemies_ids]
                atk_res = hero.func_attack(attack_enemies, skill, step["skill_pos"], state)

                res["atk_range"] = step["skill_range"]
                res["atk_position"] = step["skill_pos"]
                res["release_range"] = step["release_range"]
                res["damage"] = self.calc_damage(atk_res)
                res["effects"] = self.calc_effect(atk_res)

            if step["type"] == "HEAL":
                target_ids = [_["HeroID"] for _ in step["target"]]
                target = [e for e in state["monster"] + state["hero"] if e.HeroID in target_ids]
                heal_res = hero.friend_treatment(target, skill, step["skill_pos"], state)

                res["heal_range"] = step["skill_range"]
                res["heal_position"] = step["skill_pos"]
                res["release_range"] = step["release_range"]
                res["heal"] = self.calc_heal(heal_res)

        if step["action_type"] == "WAIT":  # TODO
            hero.dont_move()
            return step
        return res

    def attack(self, hero, atk_pick):
        action_step = []
        hero_position = hero["position"]

        if atk_pick["hero_pos"] != hero_position:
            action_step += self.move_step_handler(atk_pick["route"])
        action_step.append(
            {"action_type": f"SKILL_{atk_pick['skill']['SkillId']}", "atk_range": atk_pick["skill_range"],
             "atk_position": atk_pick["skill_pos"], "attack_enemies": atk_pick["target"], "release_range": atk_pick["release_range"]})
        return action_step

    # def move(self, hero, enemies, maps):
    #     move_steps = Move().choose_move_steps(hero, enemies, maps)
    #     action_step = self.move_step_handler(move_steps)
    #     return action_step

    def run_action(self, steps, hero, state):
        # print(f"本次行动步骤：{steps}")
        return self.choose_action(steps, hero, state)

    def get_action_steps(self, role, state):
        print('-----------------------------------------')
        # print(f"攻击者位置{hero['position']}, 跳跃高度为{hero['JumpHeight']}, 敌人们的位置为: {[_['position'] for _ in enemies]}")
        # 判断是否逃跑
        if Move().is_escape(role, state):
            move_steps = Move().escape(role, state)
            return self.move_step_handler(move_steps)

        # 判断能否攻击
        atk_pick = Attack().find_targets_within_atk_range(role, state)
        if atk_pick:
            pick_data = Attack().select_atk(atk_pick)
            return self.attack(role, pick_data)

        # 判断选择移动
        move_steps = Move().choose_move_steps(role, state)
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

