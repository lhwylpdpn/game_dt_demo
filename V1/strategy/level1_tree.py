import random
import matplotlib.pyplot as plt

import matplotlib.font_manager as fm


class Node:
    def __init__(self, name, action=None,selection=None, probability=1.0):
        self.name = name
        self.action = action

        self.probability = probability
        self.selection=selection if selection is not None else []
        self.true_child=None
        self.false_child=None
    def add_true_child(self, child_node):
        self.true_child = child_node
    def add_false_child(self, child_node):
        self.false_child = child_node

    def evaluate(self):
        # 是行动节点直接行动
        if self.action:
            self.action()
            return
        #非行动节点判断概率，如果需要随机，就随机选择一个子节点
        if random.random() < 1-self.probability:
            #随机选择一个子节点
            child = random.choice([self.true_child, self.false_child])
            child.evaluate()
        else:

            if self.true_child.selection:
                if all([s() for s in self.true_child.selection]):
                    self.true_child.evaluate()
                    return
            else:
                self.false_child.evaluate()



def plot_tree(node, x=0, y=0, layer=1):
    if node is None:
        return
    font_path = '../utils/fireflysung.ttf'  # 根据你的系统调整路径
    font_prop = fm.FontProperties(fname=font_path)
    #selection_text = "\n".join([str(cond) for cond in node.selection])
    node_text = f"{node.name}"

    plt.text(x, y, node_text, ha='center', va='center', fontproperties=font_prop,bbox=dict(facecolor='white', edgecolor='black'))

    # 计算子节点位置
    children = []
    if node.true_child:
        children.append(node.true_child)
    if node.false_child:
        children.append(node.false_child)
    offset = 1 / (2 ** layer)
    for i, child in enumerate(children):
        child_x = x + (i - (len(children) - 1) / 2) * offset
        child_y = y - 1
        plt.plot([x, child_x], [y, child_y], color='black')  # 连接线
        plot_tree(child, child_x, child_y, layer + 1)



def move_to_attack():
    print("move_to_attack!")
    #引用find_targets_within_atk_range
def move_to_enemie():
    print("move_to_enemie!")
    #引用 fmove_to_enemy
#返回周围敌人的数量
def nearby_enemy_count(N):
    #随机返回true或者false
    print("Counting enemies!",N)
    return random.random() < 0.5

def is_within_range(N):
    print("is_within_range!",N)
    return random.random() < 0.5

def move_to_allies():
    #move_to_combat_teammate()
    print("move_to_allies!")
def move_to_boss():
    print("move_to_boss!")
    #move_to_boss()

def is_fight_allies():
    print("is_fight_allies!")

#返回自身血量是否少于上限
def is_health_below_threshold(N):
    print("Getting health!",N)
    return True




def lambda_is_health_below_threshold(N):
    return lambda : is_health_below_threshold(N)

def lambda_nearby_enemy_count(N):
    return lambda : nearby_enemy_count(N) #自己是不是在几个敌人范围内

def lambda_is_within_range(N):
    return lambda : is_within_range(N) #自己的警戒周围是不是有几个敌人

def lambda_is_fight_allies():
    return lambda : is_fight_allies()


def lambda_is_not_fight_allies():
    return lambda :not is_fight_allies()

def lambda_have_targets_within_atk_range():
    #print("have_targets_within_atk_range!")
    return lambda : random.random() < 0.5



def lambda_have_not_targets_within_atk_range():
    #print("have_not_targets_within_atk_range!")
    return lambda :  random.random() < 0.5



def action_eascape():#todo
    print("eascape!")
    #eascape()



# 创建决策树
root = Node("判断是否满足逃跑条件", action=None, selection=[lambda_is_health_below_threshold(40),lambda_nearby_enemy_count(1)],probability=1)
action_escape_node = Node("逃跑", action=action_eascape)
is_have_enemie_within_range_node = Node("判断警戒范围内是否有敌人", action=None, selection=[lambda_is_within_range(0)],probability=1)
is_have_targets_within_atk_range_node=Node("判断是否有敌人在攻击范围内",action=None,selection=[lambda_have_targets_within_atk_range()],probability=1)
is_have_allies_within_range_node=Node("判断是否有友军在战斗",action=None,selection=[lambda_is_fight_allies()],probability=1)
move_to_enemies_node=Node("移动到敌人附近",action=move_to_enemie,probability=1)
move_to_allies_node=Node("移动到友军附近",action=move_to_allies,probability=1)
move_to_boss_node=Node("移动到boss附近",action=move_to_boss,probability=1)
move_and_attack_node=Node("移动到敌人附近并攻击",action=move_to_attack,probability=1)
root.add_true_child(action_escape_node)
root.add_false_child(is_have_enemie_within_range_node)
is_have_enemie_within_range_node.add_true_child(is_have_targets_within_atk_range_node)
is_have_enemie_within_range_node.add_false_child(is_have_allies_within_range_node)
is_have_targets_within_atk_range_node.add_true_child(move_and_attack_node)
is_have_targets_within_atk_range_node.add_false_child(move_to_enemies_node)
is_have_allies_within_range_node.add_true_child(move_to_allies_node)
is_have_allies_within_range_node.add_false_child(move_to_boss_node)

# # 评估决策树
root.evaluate()

# # 绘制决策树
plt.figure(figsize=(10, 10))
plot_tree(root)
plt.axis('off')
plt.show()

