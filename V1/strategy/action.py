# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:25
import time
from strategy.game_utils import GameUtils
from strategy.handler.attack import Attack
from strategy.handler.move import Move
from utils.strategy_utils.basic_utils import square_distance_points
from utils.strategy_utils.range import Range

ATTACHMENT_SELECT = 1  # 可以被攻击的附着物类型

class Action(object):
    def calc_damage(self, damage_data):
        d = []
        for each in damage_data:
            damage = [_["damage"] for _ in damage_data[each]["damage"]]
            pre_damage = [_["pre_damage"] for _ in damage_data[each]["damage"]]
            st = [_["st"] for _ in damage_data[each]["damage"]]
            crit = [_["crit"] for _ in damage_data[each]["damage"]]

            d.extend([["ATK", [each.__class__.__name__.lower(), each.HeroID], damage, pre_damage, st, crit]])
        return d

    def calc_effect(self, effect_data):
        d = []
        for each in effect_data:
            for e in effect_data[each]["damage"]:
                if e["effects"]:
                    eff = [_["effect_id"] for _ in e["effects"]]
                    d.extend([[[each.__class__.__name__.lower(), each.HeroID], eff, []]])
        return d

    def calc_back_damage(self, damage_data):
        d = []
        for each in damage_data["damage"]:
            damage = each["damage"]
            pre_damage = each["pre_damage"]
            st = each["st"]
            crit = each["crit"]

            d.extend([["ATKBACK", [damage_data["effects"][0]["role"], damage_data["effects"][0]["role_id"]], [damage], [pre_damage], st, crit]])
        return d

    def calc_heal(self, heal_data):
        d = []
        for each in heal_data:
            heal = [_["heal"] for _ in heal_data[each]]
            pre_damage = [_["pre_heal"] for _ in heal_data[each]]
            # st = [_["st"] for _ in heal_data[each]]

            d.extend([["HEAL", [each.__class__.__name__.lower(), each.HeroID], heal, pre_damage]])
        return d

    def atk_back(self, back_data):
        if back_data:
            pass

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
            box_action = []
            move_position = step["move_position"]
            hero.move_position(*move_position, state)
            res["move_position"] = move_position
            if state.get("attachment") and hero.is_hero():  # 只有英雄能开宝箱
                for att in state["attachment"]:
                    if att.is_box():
                        box_open_points = square_distance_points((att.x, att.z), att.box_open_distance())
                        if (move_position[0], move_position[2]) in box_open_points:
                            hero.open_box(att, state) # 预置开宝箱的动作
                            box_action.append({"action_type": "OPEN_BOX"})
            if box_action:
                return [res] + box_action

        if step["action_type"] == "MOVE_START":
            res["move_start"] = Range(hero, state).role_move_start()
            res["sequence"] = step["sequence"]
            return res

        if "EFFECT_" in step["action_type"]:
            buff_res = hero.trigger_buff(step)
            res["damage"] = buff_res["damage"]
            return res

        if "SKILL_" in step["action_type"]:
            skill = [s for s in hero.skills if s.SkillId == int(step["action_type"].replace("SKILL_", ""))][0]

            if step["type"] == "ATK":
                back_res = []
                attachment_in_atk = [a for a in state["attachment"] if a.Selected == ATTACHMENT_SELECT and tuple(a.position) in step["release_range"]]

                if attachment_in_atk:
                    print("本次攻击到的附着物:", attachment_in_atk)

                attack_enemies = [e for e in state["monster"] if tuple(e.position) in step["skill_range"] and e.Hp > 0]
                # atk_res = hero.func_attack(attack_enemies + attachment_in_atk, skill, step["skill_pos"], state)  TODO
                atk_res = hero.func_attack(attack_enemies, skill, step["skill_pos"], state)
                for _ in atk_res:
                    if atk_res[_].get("back_attck"):
                        atk_back = atk_res[_]["back_attck"]
                        atk_back["id"] = atk_back["id"]
                        atk_back["class"] = atk_back["class"]
                        atk_back["damage"] = self.calc_back_damage(atk_back)
                        back_res.append(atk_back)

                res["atk_range"] = step["skill_range"]
                res["atk_position"] = step["skill_pos"]
                res["release_range"] = step["release_range"]
                res["damage"] = self.calc_damage(atk_res)
                res["effects"] = self.calc_effect(atk_res)
                if back_res: # 返回攻击+反击
                    return [res] + back_res


            if step["type"] == "HEAL":
                target_ids = [_["HeroID"] for _ in step["target"]]
                target = [e for e in state["monster"] + state["hero"] if e.HeroID in target_ids]
                heal_res = hero.friend_treatment(target, skill, step["skill_pos"], state)

                res["atk_range"] = step["skill_range"]
                res["atk_position"] = step["skill_pos"]
                res["release_range"] = step["release_range"]
                res["damage"] = self.calc_heal(heal_res)

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
    data = {"0x13506ff40": {'damage': [{'damage': 0, 'miss': 0, 'pre_damage': -54, 'st': 'Equal', 'effects': [{'role': 'hero', 'role_id': 5002, 'effect_id': 67}, {'role': 'hero', 'role_id': 5002, 'effect_id': 65}], 'crit': 'Default'}, {'damage': 0, 'miss': 0, 'pre_damage': -54, 'st': 'Equal', 'effects': [], 'crit': 'Default'}], 'back_attck': {'action_type': 'SKILL_82', 'atk_range': [[11, 3, 13]], 'atk_position': [[11, 3, 13]], 'release_range': [[11, 3, 13]], 'damage': [{'damage': 0, 'miss': 0, 'pre_damage': 77, 'st': 'Equal', 'effects': [{'role': 'hero', 'role_id': 5002, 'effect_id': 84}], 'crit': 'Default'}], 'effects': [68, 63, 84, 57]}}}


    print(Action().calc_back_damage(data["0x13506ff40"]["back_attck"]))

