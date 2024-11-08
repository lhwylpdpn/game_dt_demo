
def damage_calc(attacker, defender, skill):

    # ####-------------------------------------------------------------------
    # ####这里负责取值，不负责计算
    # 英雄的属性

    attacker_PhysicalAtk = attacker.Atk
    defender_hp = defender.DestroyEffect
    damage = attacker_PhysicalAtk  # 现在没有防御

    return [{'damage': damage, 'miss': 0, "pre_damage": damage, "st": "Advantage", "effects": [], "crit": "Default"}]