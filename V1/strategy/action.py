# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/25 15:25
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

    def heal(self, hero, enemies, maps):
        hero_hp = hero["Hp"]
        hero_base_hp = hero["HpBase"]
        hero_skills = hero["skills"]
        hero_position = hero["position"]
        hero_max_step = hero["RoundAction"]

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
        hero_position = tuple(hero["position"])
        hero_max_step = hero["RoundAction"]
        hero_normal_attack_range = 2

        if SkillFunc().has_attack_skill_available(hero_skills):
            res, move_queue, attack, attack_enemies = SelfFunc().can_skill_attack_multiple_enemies(
                hero_position, hero_skills, enemies, maps, hero_max_step
            )

            if res:
                # print(f"移动步骤：{move_queue}, 技能攻击：{attack}")
                # move_step = [{"action_type": "MOVE", "steps": m} for m in move_queue]
                move_step = self.move_step_handler([hero_position] + move_queue)

                atk_position = tuple(tuple(_["position"]) for _ in attack_enemies)
                attack_enemies = [_.get("MonsterId") for _ in attack_enemies if _.get("MonsterId")] + [_.get("HeroID")
                                                                                                       for _ in
                                                                                                       attack_enemies if
                                                                                                       _.get("HeroID")]
                move_step.append(
                    {"action_type": f"SKILL_{attack}", "atk_range": atk_position, "atk_position": hero_position,
                     "attack_enemies": attack_enemies})
                return True, move_step
            else:
                res, move_queue, attack, attack_enemies = SelfFunc().can_normal_attack_multiple_enemies(
                    hero_position, hero_normal_attack_range, enemies, maps, hero_max_step
                )
                if res:
                    # print(f"移动步骤：{move_queue}, 普通攻击：{attack}")
                    # move_step = [{"action_type": "MOVE", "steps": m} for m in move_queue]

                    move_step = self.move_step_handler([hero_position] + move_queue)

                    atk_position = tuple(tuple(_["position"]) for _ in attack_enemies)
                    attack_enemies = [_.get("MonsterId") for _ in attack_enemies if _.get("MonsterId")] + [
                        _.get("HeroID") for _ in attack_enemies if _.get("HeroID")]
                    move_step.append(
                        {"action_type": "SKILL_NORMAL", "atk_range": atk_position, "atk_position": hero_position,
                         "attack_enemies": attack_enemies})
                    return True, move_step
                    # return True, [{"action_type": "move", "steps": move_queue}, {"action_type": "normal_attack", "steps": attack, "attack_enemies": attack_enemies}]

        return False, {}

    def move(self, hero, enemies, maps):
        hero_skills = hero["skills"]
        hero_dog_base = hero["DogBase"]
        hero_position = hero["position"]
        hero_max_step = hero["RoundAction"]
        boss_position = enemies[0]["position"]  # TODO 假设BOSS
        hero_normal_attack_range = 2
        enemies_within_range = DistanceFunc().is_within_attack_range(hero_dog_base, hero_position, enemies)

        if enemies_within_range:
            # res, move_queue, attack, attack_enemies = SelfFunc().can_normal_attack_multiple_enemies(
            #     hero_position, hero_normal_attack_range, enemies, maps, hero_max_step
            # )
            move_queue = DistanceFunc().manhattan_path(hero_position, enemies[0]["position"], hero_max_step)
            print("警戒范围内有敌方单位: ", move_queue)


        else:
            # res, move_queue, attack, attack_enemies = SelfFunc().can_normal_attack_multiple_enemies(
            #     hero_position, hero_normal_attack_range, boss, maps, hero_max_step
            # )
            move_queue = DistanceFunc().manhattan_path(hero_position, boss_position, hero_max_step)
            print(f"警戒范围无敌方单位， 向boss地点{boss_position}移动:", move_queue)

        # move_step = [{"action_type": "MOVE", "steps": m} for m in move_queue]
        move_step = self.move_step_handler([hero_position] + move_queue)

        return True, move_step

    def wait(self):
        print("当前回合行动：WAIT")
        return [{"action_type": "WAIT"}]

    def select_action(self, hero, enemies, maps):
        tf, steps = self.attack(hero, enemies, maps)
        if tf:
            return steps
        else:
            tf, steps = self.move(hero, enemies, maps)
            if tf:
                return steps
            else:
                return True, self.wait()

    def monster_action(self):
        print("敌人在原地发呆！")

    def choose_action(self, step, hero, monster):
        res = {"action_type": step["action_type"]}
        if step["action_type"] == "heal" and step["steps"]:
            print("执行虎哥[加血]函数")

        if step["action_type"] in ["LEFT", "RIGHT", "TOP", "BOTTOM"]:
            # hero = [h for h in hero if h.protagonist == 1][0]
            hero.move_position(*step["move_position"])

        if "SKILL_" in step["action_type"]:
            if step["action_type"] == "SKILL_NORMAL":
                attack_enemies_ids = step["attack_enemies"]
                # hero = [h for h in hero if h.protagonist == 1][0]
                skill = hero.skills[0]
                try:
                    attack_enemies = [e for e in monster if e.MonsterId in attack_enemies_ids]
                except Exception as e:
                    attack_enemies = [e for e in monster if e.HeroID in attack_enemies_ids]
                hero.func_attack(attack_enemies, skill)
                print(f"使用普通攻击 攻击敌人{attack_enemies_ids}")
                res["atk_range"] = step["atk_range"]
                res["atk_position"] = step["atk_position"]
            else:
                attack_enemies_ids = step["attack_enemies"]
                # hero = [h for h in hero if h.protagonist == 1][0]
                skill = [s for s in hero.skills if s.SkillId == int(step["action_type"].replace("SKILL_", ""))][0]
                try:
                    attack_enemies = [e for e in monster if e.MonsterId in attack_enemies_ids]
                except Exception as e:
                    attack_enemies = [e for e in monster if e.HeroID in attack_enemies_ids]
                print(f"使用技能[{skill}] 攻击敌人{attack_enemies_ids}")
                hero.func_attack(attack_enemies, skill)
                res["atk_range"] = step["atk_range"]
                res["atk_position"] = step["atk_position"]
        return res



    def run_action(self, steps, hero, monster):
        # print(f"本次行动步骤：{steps}")
        return self.choose_action(steps, hero, monster)

    def choose_action_v2(self):
        pass

    def select_action_v2(self, hero, enemies, maps):
        pass


if __name__ == '__main__':
    from V1.strategy.handler.constant import HERO, ENEMY_A, ENEMY_B, MAPS

    hero = HERO
    maps = MAPS
    enemies = [ENEMY_A, ENEMY_B]

