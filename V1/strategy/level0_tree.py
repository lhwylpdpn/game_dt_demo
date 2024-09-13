import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from utils.strategy_utils.range import Range
from strategy.strategy_context import strategy_params as sp
import time
from log.log import log_manager
class Node:
    def __init__(self, name, action=None,selection=None, probability=1.0):
        self.name = name
        self.action = action
        self.probability = probability
        self.selection=selection if selection is not None else []
        self.true_child=None
        self.false_child=None
        self.selection_result=None
    def add_true_child(self, child_node):
        self.true_child = child_node
    def add_false_child(self, child_node):
        self.false_child = child_node

    def evaluate(self,performance=None, params=None):
        # 是行动节点直接行动

        if self.action:
            if performance is not None:
                performance.event_start(self.name)
            if self.selection_result:
                res=self.action(self.selection_result)
            else:
                res=self.action()
                log_manager.add_log(
            log_manager.add_log({'stepname': '决策树-个人偏好最终选择的行动', 'action': self.name, 'result': res}))
            if performance is not None:
                performance.event_end(self.name)
            return res
        #非行动节点判断概率，如果需要随机，就随机选择一个子节点
        if random.random() < 1-self.probability:
            #随机选择一个子节点
            child = random.choice([self.true_child, self.false_child])
            return child.evaluate(performance=performance)
        else:
            #有判断节点走判断节点，无判断节点直接走右节点
            if self.selection:
                res=[]

                for s in self.selection:
                    if performance is not None:
                        performance.event_start("selection_"+str(s))
                    res.append(s())
                    if performance is not None:
                        performance.event_end("selection_"+str(s))
                params_=[]
                #判断是不是返回都都是空列表
                for r in res:
                    #如果不是列表，转换成列表
                    if not isinstance(r,list):
                        r=[r]
                    if len(r)>0:
                        params_.extend(r)
                #T 走左节点，F走右节点
                if len(params_)>0:

                    log_manager.add_log({'stepname': '决策树-个人偏好选择的行动，选择了T子节点，因为[aramas]不为空', 'action': self.true_child.name, 'result': params_})
                    self.true_child.selection_result=params_
                    return self.true_child.evaluate(performance=performance)
                else:
                    log_manager.add_log({'stepname': '决策树-个人偏好选择的行动，选择了F子节点，因为[aramas]为空', 'action': self.false_child.name, 'result': params_})
                    self.false_child.selection_result=params_
                    return self.false_child.evaluate(performance=performance)


            else:
                log_manager.add_log({'stepname': '决策树-个人偏好选择的行动，选择了F子节点，因为没有判断条件', 'action': self.false_child.name})
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



def lambda_select_fun(params_list):
    return lambda: []

def wait():
    return False



#向某个点释放某个技能:
def action_fun(params):
    print(f"执行函数: {params}")
    return 333333
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

    res = root.evaluate()
    print('action node 结果',res)

    plt.figure(figsize=(20, 10))
    plot_tree(root)
    plt.axis('off')
    plt.show()
def create_decision_tree(hero,state):
    BaseClassID=hero.get("BaseClassID")
    sp_obj=sp()
    eascape_hp=sp_obj.get_strategy_params(BaseClassID)[1]['escape']['is_health_below_threshold']['weight']
    range_obj=Range(hero,state)
    # 创建决策树

    #所有判断节点
    root = Node("1_判断_单体技能_支援_血最少", action=None, selection=[lambda_select_fun([1,3,4])],probability=1)
    p_2  = Node("2_判断_劈砍_全部单位_攻击目标", action=None, selection=[lambda_select_fun([2,9,5])],probability=1)
    p_3  = Node("3_使用突刺_不含后卫_防御最高",action=None,selection=[lambda_select_fun([3,6,7])],probability=1)

    p1_action_node= Node("行动1_用某个技能攻击某个点", action=action_fun)
    p2_action_node= Node("行动2_用某个技能攻击某个点", action=action_fun)
    p3_action_node= Node("行动3_用某个技能攻击某个点", action=action_fun)

    wait_node=Node("等待",action=wait)

    #构建关系
    root.add_true_child(p1_action_node)
    root.add_false_child(p_2)
    p_2.add_true_child(p2_action_node)
    p_2.add_false_child(p_3)
    p_3.add_true_child(p3_action_node)
    p_3.add_false_child(wait_node)




    return root


if __name__ == '__main__':
    show_plot_tree()
