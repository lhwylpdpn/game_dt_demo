# -*- coding: utf-8 -*-
# @Author  : Bin
# @Time    : 2024/7/22 10:59
from V1.strategy.action import Action


class Hero(object):
    def __init__(self, hero):
        self.id = hero["id"]
        self.name = hero["name"]
        self.hp = hero["hp"]
        self.normal_attack_damage = hero["normal_attack_damage"]
        self.normal_attack_range = hero["normal_attack_range"]
        self.position = hero["position"]
        self.aggro = hero["aggro"]
        self.skill_A = Skill(hero["skill_A"])
        self.skill_B = Skill(hero["skill_B"])
        self.skills = [self.skill_A, self.skill_B]


class Skill:
    def __init__(self, skill):
        self.name = skill["name"]
        self.range = skill["range"]
        self.damage = skill["damage"]
        self.max_uses = skill["max_uses"]
        self.attack_type = skill["attack_type"]
        self.remaining_use = skill["max_uses"]

    def can_use(self, distance):
        if self.remaining_use > 0 and distance <= self.range:
            return True
        return False


class Enemy:
    def __init__(self, enemy_data):
        self.enemy_id = enemy_data["id"]
        self.name = enemy_data["name"]
        self.hp = enemy_data["hp"]
        self.position = enemy_data["position"]
        self.left = None
        self.right = None


class Game(object):
    def __init__(self):
        pass

    def action(self, step):
        Action().run_action(step)

    def get_current_alive_hero(self, heroes):
        heroes_data = heroes.now_data()

    def start(self, heroes, enemies, maps):
        pass


if __name__ == '__main__':
    f = Game()
