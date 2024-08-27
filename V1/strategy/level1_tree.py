import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from utils.strategy_utils.range import Range

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
            print(f"决策树选择执行动作: {self.name}",self.action())
            return self.action()
        #非行动节点判断概率，如果需要随机，就随机选择一个子节点
        if random.random() < 1-self.probability:
            #随机选择一个子节点
            child = random.choice([self.true_child, self.false_child])
            return child.evaluate()
        else:

            if self.true_child.selection:
                if all([s() for s in self.true_child.selection]):
                    return self.true_child.evaluate()
                else:
                    return self.false_child.evaluate()


            else:
                return self.false_child.evaluate()



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




def move_to_attack(obj):
    return lambda: obj.find_attack_target()
def move_to_enemie(obj):
    return lambda: obj.move_to_enemy()
def move_to_allies(obj):
    return lambda: obj.move_to_combat_teammate()
def move_to_boss(obj):
    return lambda: obj.move_to_boss()

def wait(obj):
    return lambda: obj.wait()


def action_eascape(obj):
    return lambda : obj.get_furthest_position()



###=------- 所有判断函数
def lambda_is_health_below_threshold(obj,N):
    return lambda : obj.is_health_below_threshold(N)
def lambda_nearby_enemy_count(obj,N):
    return lambda : obj.nearby_enemy_count(N) #自己是不是在几个敌人范围内
def lambda_is_within_range(obj,N):

    return lambda : obj.is_within_range(N) #自己的警戒周围是不是有几个敌人
def lambda_is_fight_allies(obj):
    return lambda : obj.is_combat_teammate()
def lambda_have_targets_within_atk_range(obj):
    return lambda : True if len(obj.find_targets_within_atk_range())>0 else False
def lambda_is_have_boss(obj):
    return lambda : obj.is_boss()


def make_decision(hero,state):
    root= create_decision_tree(hero,state)

    return root.evaluate()

def show_plot_tree():
    from buildpatrol import BuildPatrol
    state = BuildPatrol("../data.json").load_data()
    hero=state['hero'][0]
    root=create_decision_tree(hero,state)
    plt.figure(figsize=(10, 10))
    plot_tree(root)
    plt.axis('off')
    plt.show()
def create_decision_tree(hero,state):


    range_obj=Range(hero,state)
    # 创建决策树

    #所有判断节点
    root = Node("判断是否满足逃跑条件", action=None, selection=[lambda_is_health_below_threshold(range_obj,0.4),lambda_nearby_enemy_count(range_obj,1)],probability=1)
    is_have_enemie_within_range_node = Node("判断警戒范围内是否有敌人", action=None, selection=[lambda_is_within_range(range_obj,0)],probability=1)
    is_have_targets_within_atk_range_node=Node("判断是否有敌人在攻击范围内",action=None,selection=[lambda_have_targets_within_atk_range(range_obj)],probability=1)
    is_have_allies_within_range_node=Node("判断是否有友军在战斗",action=None,selection=[lambda_is_fight_allies(range_obj)],probability=1)
    is_have_boss_node=Node("判断是否有boss",action=None,selection=[lambda_is_have_boss(range_obj)],probability=1)

    #所有叶子节点
    action_escape_node = Node("逃跑", action=action_eascape(range_obj))
    move_to_enemies_node=Node("移动到敌人附近",action=move_to_enemie(range_obj),probability=1)
    move_to_allies_node=Node("移动到友军附近",action=move_to_allies(range_obj),probability=1)
    move_to_boss_node=Node("移动到boss",action=move_to_boss(range_obj),probability=1)
    move_and_attack_node=Node("移动到敌人附近并攻击",action=move_to_attack(range_obj),probability=1)
    move_to_wait_node=Node("等待",action=wait(range_obj),probability=1)


    #构建关系
    root.add_true_child(action_escape_node)
    root.add_false_child(is_have_enemie_within_range_node)
    is_have_enemie_within_range_node.add_true_child(is_have_targets_within_atk_range_node)
    is_have_enemie_within_range_node.add_false_child(is_have_allies_within_range_node)
    is_have_targets_within_atk_range_node.add_true_child(move_and_attack_node)
    is_have_targets_within_atk_range_node.add_false_child(move_to_enemies_node)
    is_have_allies_within_range_node.add_true_child(move_to_allies_node)
    is_have_allies_within_range_node.add_false_child(is_have_boss_node)
    is_have_boss_node.add_true_child(move_to_boss_node)
    is_have_boss_node.add_false_child(move_to_wait_node)

    return root

if __name__ == '__main__':

    show_plot_tree()

