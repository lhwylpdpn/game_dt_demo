import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from utils.strategy_utils.range import Range
from strategy.strategy_context import strategy_params as sp
import time
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

    def evaluate(self,performance=None):
        # 是行动节点直接行动

        if self.action:
            if performance is not None:
                performance.event_start(self.name)
            res=self.action()
            if performance is not None:
                performance.event_end(self.name)
            return res
        #非行动节点判断概率，如果需要随机，就随机选择一个子节点
        if random.random() < 1-self.probability:
            #随机选择一个子节点
            child = random.choice([self.true_child, self.false_child])
            return child.evaluate(performance=performance)
        else:

            if self.selection:
                #逐个打印判断条件的结果
                for s in self.selection:
                    print(f"判断条件: {s} 结果: {s()}")

                res=[]

                for s in self.selection:
                    if performance is not None:
                        performance.event_start("selection_"+str(s))
                    res.append(s())
                    if performance is not None:
                        performance.event_end("selection_"+str(s))

                if all(res):
                    print('选择了left node:',self.true_child.name)
                    return self.true_child.evaluate(performance=performance)
                else:
                    print('选择了right node:',self.false_child.name)
                    return self.false_child.evaluate(performance=performance)


            else:
                print('无判断条件，直接选择right node:',self.false_child.name)
                return self.false_child.evaluate(performance=performance)



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



def lambda_use_single_skill():
    #返回随机TorF
    return lambda :random.random() > 0.5

def lambda_include_base_class_id(base_class_id):
    #返回随机TorF
    return lambda :random.random() > 0.5
#不包含某个职业
def lambda_exclude_base_class_id(base_class_id):
    #返回随机TorF
    return lambda :random.random() > 0.5

def lambda_is_min_hp():
    #返回随机TorF
    return lambda :random.random() > 0.5

def lambda_is_special_skill(skill_id):
    #返回随机TorF
    return lambda :random.random() > 0.5

def lambda_all_targets():
    #返回随机TorF
    return lambda :random.random() > 0.5

#可以攻击到多个目标
def lambda_have_targets_within_atk_range(n):
    return lambda :random.random() > 0.5


def lambda_is_max_def():
    return lambda :random.random() > 0.5


#向某个点释放某个技能:
def attack_to_point(skill_id,point):
    return lambda :random.random() > 0.5

def make_decision(hero,state,performance=None):
    root= create_decision_tree(hero,state)
    a=time.time()
    if performance is not None:
        performance.event_start('evaluate')
    res=root.evaluate(performance=performance)
    if performance is not None:
        performance.event_end('evaluate')
    print('决策树耗时:',time.time()-a)
    return res

def show_plot_tree():
    from buildpatrol import BuildPatrol
    state = BuildPatrol("../data.json").load_data()
    hero=state['hero'][0].dict()
    root=create_decision_tree(hero,state)
    plt.figure(figsize=(20, 10))
    plot_tree(root)
    plt.axis('off')
    plt.show()
def create_decision_tree(hero,state):
    BaseClassID=hero.get("BaseClassID")
    sp_obj=sp()


    sp_obj=sp()
    eascape_hp=sp_obj.get_strategy_params(BaseClassID)[1]['escape']['is_health_below_threshold']['weight']
    range_obj=Range(hero,state)
    # 创建决策树

    #所有判断节点
    root = Node("1_判断_单体技能_支援_血最少", action=None, selection=[lambda_use_single_skill,lambda_include_base_class_id(1),lambda_is_min_hp()],probability=1)
    p_2 = Node("2_判断_劈砍_全部单位_攻击目标", action=None, selection=[lambda_is_special_skill(1),lambda_all_targets,lambda_have_targets_within_atk_range(1)],probability=1)
    p_3=Node("3_使用突刺_不含后卫_防御最高",action=None,selection=[lambda_is_special_skill(1),lambda_exclude_base_class_id(1),lambda_is_max_def],probability=1)


    p_1_action_select_node=Node("条件1动作是否能完成", action=None, selection=[attack_to_point(1,2)],probability=1)
    p_2_action_select_node=Node("条件2动作是否能完成", action=None, selection=[attack_to_point(1,2)],probability=1)
    p_3_action_select_node=Node("条件3动作是否能完成", action=None, selection=[attack_to_point(1,2)],probability=1)
    #所有叶子节点
    p1_action_node= Node("条件1_用某个技能攻击某个点", action=attack_to_point(1,2))
    p2_action_node= Node("条件2_用某个技能攻击某个点", action=attack_to_point(1,2))
    p3_action_node= Node("条件3_用某个技能攻击某个点", action=attack_to_point(1,2))

    wait_node=Node("等待",action=None)

    #构建关系
    root.add_true_child(p_1_action_select_node)
    p_1_action_select_node.add_true_child(p1_action_node)
    p_1_action_select_node.add_false_child(p_2)
    p_2.add_true_child(p_2_action_select_node)
    p_2_action_select_node.add_true_child(p2_action_node)
    p_2_action_select_node.add_false_child(p_3)
    p_3.add_true_child(p_3_action_select_node)
    p_3_action_select_node.add_true_child(p3_action_node)
    p_3_action_select_node.add_false_child(wait_node)



    return root

if __name__ == '__main__':

    show_plot_tree()
