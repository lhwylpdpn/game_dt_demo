import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from utils.strategy_utils.range import Range
from strategy.strategy_context import strategy_params as sp
import time
from log.log import log_manager
from V1.strategy.strategy_context import simple_strategy_params
from V1.strategy.handler.simple_strategy import SimpleStrategy
class Node:
    def __init__(self, name, action=None,selection=None, probability=1.0):
        self.name = name
        self.action = action
        self.probability = probability
        self.selection=selection if selection is not None else []
        self.true_child=None
        self.false_child=None
        self.evaluate_result=None
    def add_true_child(self, child_node):
        self.true_child = child_node
    def add_false_child(self, child_node):
        self.false_child = child_node

    def evaluate(self,performance=None):
        # 是行动节点直接行动
        if self.evaluate_result is not None:
            return self.evaluate_result,self
        if self.action:
            if performance is not None:
                performance.event_start(self.name)
            res=self.action()
            log_manager.add_log({'stepname': '偏好_evaluate执行动作', 'action': self.name, 'result_len': len(res)})
            if performance is not None:
                performance.event_end(self.name)
            self.evaluate_result=res
            return res,self
        #非行动节点判断概率，如果需要随机，就随机选择一个子节点
        if random.random() < 1-self.probability:
            #随机选择一个子节点
            child = random.choice([self.true_child, self.false_child])
            return child.evaluate(performance=performance)
        else:

            if self.selection:
                res=[]

                for s in self.selection:
                    if performance is not None:
                        performance.event_start("selection_"+str(s))
                    res.append(s())
                    log_manager.add_log({'stepname': '偏好_evaluate执行判断', 'selection': str(self.name)+'_'+str(s), 'result_len': str(res[-1])})
                    if performance is not None:
                        performance.event_end("selection_"+str(s))

                if all(res):
                    #log_manager.add_log({'stepname': '决策树-通用决策的选择,选择了T子节点', 'action': self.true_child.name})
                    return self.true_child.evaluate(performance=performance)
                else:
                    #log_manager.add_log({'stepname': '决策树-通用决策的选择,选择了F子节点', 'action': self.false_child.name})
                    return self.false_child.evaluate(performance=performance)

            else:
                #log_manager.add_log({'stepname': '决策树-通用决策的选择,选择了F子节点,因为没有条件', 'action': self.false_child.name})
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



def lambda_select_fun(obj,strategy,type):
    return lambda: obj.choice(strategy,type)

def wait():
    return []




def make_decision(hero,state,performance=None):
    root= create_decision_tree(hero,state)
    a=time.time()
    if performance is not None:
        performance.event_start('evaluate')
    res=root.evaluate(performance=performance)
    if performance is not None:
        performance.event_end('evaluate')
    print('偏好_决策树耗时:',time.time()-a)
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
    HeroID=int(hero.get("HeroID"))
    sp_obj=sp()
    eascape_hp=sp_obj.get_strategy_params(BaseClassID)[1]['escape']['is_health_below_threshold']['weight']
    range_obj=Range(hero,state)
    simple_obj=simple_strategy_params()
    param_list=simple_obj.get_strategy_params(HeroID)
    wait_node = Node("等待", action=wait)
    if len(param_list)==0:#没有任何偏好设置
        return wait_node
    # 创建决策树
    #所有判断节点
    node_dict={}
    node_action_dict={}
    SimpleStrategy_obj=SimpleStrategy(hero,state)


    for i in range(len(param_list)):
        node_dict['p_'+str(i)]=Node("p_"+str(i)+"_select",action=None,selection=[lambda_select_fun(SimpleStrategy_obj,param_list[i],'enemy')],probability=1)
        node_action_dict['p_action_'+str(i)]=Node("p_"+str(i)+"_action",action=lambda_select_fun(SimpleStrategy_obj,param_list[i],'enemy'))
        node_dict['p_' + str(i)].add_true_child(node_action_dict['p_action_'+str(i)])
    for i in range(len(param_list)):
        if i==len(param_list)-1:
            node_dict['p_' + str(i)].add_false_child(wait_node)
        else:
            node_dict['p_' + str(i)].add_false_child(node_dict['p_' + str(i+1)])



    return node_dict['p_0']


if __name__ == '__main__':
    show_plot_tree()
