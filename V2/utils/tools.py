import dictdiffer
import time
import pandas as pd
import random
import math
import uuid
import os

class performance:
    def __init__(self):
        self.start_time = time.time()
        self.result = {}
        self.tag_time={}
        self.event_count={}
        self.tick=0
    def event_start(self, event_name):
        self.tag_time[event_name]=time.time()
    def event_end(self, event_name):
        use_time=time.time()-self.tag_time[event_name]
        self.result[event_name]=use_time if self.result.get(event_name) is None else self.result[event_name]+use_time
        self.event_count[event_name]=self.event_count[event_name]+1 if self.event_count.get(event_name) is not None else 1
        self.tag_time[event_name]=None

    def end(self):
        self.result['total_time']=time.time()-self.start_time
        self.event_count['total_time']=1


    def static(self):
        #计算各类事件的平均时间转成df
        df=pd.DataFrame(self.result.items(),columns=['event','time'])
        #合并每个事件的次数
        df['count']=df['event'].apply(lambda x:self.event_count[x])
        df['avg_time']=round(df['time']/df['count'],2)
        df['time']=round(df['time'],2)


        df=df.sort_values(by=['time'],ascending=False)

        new_row = pd.Series(['tick',self.tick,'',''] , index=df.columns)
        df = df.append(new_row, ignore_index=True)
        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.width', 1000)
        print(df.to_string(index=False))
        #df.to_csv(os.path.dirname(os.path.abspath(__file__))+'/../log/time_static.csv', index=False)


def Deepdiff_modify(before,after):
    #
    # print('Deepdiff_modify_before给强爷----',"before['hero'][5002]['AvailableSkills']",before['hero'][5002]['AvailableSkills'])
    #
    # print('手动变化',"['hero'][5002]['test']={'k':[200, 201, 202, 203, 204, 205, 3],'K2':[33,33]}")
    # after['hero'][5002]['test'] = {'k': [200, 201, 202, 203, 204, 205, 3], 'K2': [33, 33]}
    # print('Deepdiff_modify_after给强爷',"before['hero'][5002]['AvailableSkills']",after['hero'][5002]['AvailableSkills'])

    #res=list(dictdiffer.diff(before, after))
    # print('before',before['hero']['heroID'][5003])
    # print('after',after['hero']['heroID'][5003])
    # print('Deepdiff_modify_before',res)
    # return_res={}
    # for i in res:
    #     if i[0]=='change':
    #         path=i[1]
    #         res={}
    #         tmp={}
    #         value_tmp=after
    #         for _ in path:
    #             value_tmp=value_tmp[_]
    #         res = {path[-1]: value_tmp}
    #         path=path[::-1][1:]
    #         for _ in path:
    #             tmp={}
    #             tmp[_]=res.copy()
    #             res=tmp
    #
    #     if i[0]=='add':
    #         path=i[1]
    #         res={}
    #         tmp={}
    #         value_tmp=after
    #         for _ in path:
    #             value_tmp=value_tmp[_]
    #         res = {path[-1]: value_tmp}
    #         path=path[::-1][1:]
    #         for _ in path:
    #             tmp={}
    #             tmp[_]=res.copy()
    #             res=tmp
    #
    #     if i[0]=='remove':
    #         path=i[1]
    #         res={'remove':i[2]}
    #         tmp={}
    #         path=path[::-1]
    #         for _ in path:
    #
    #             tmp={}
    #             tmp[_]=res.copy()
    #             res=tmp
    #
    #
    #     merge_dicts(return_res,res)
    #print('Deepdiff_modify_after',return_res)
    #return_res=res

    return list(dictdiffer.diff(before, after))


def merge_dicts(dict_a, dict_b):
    for key in dict_b:
        if key in dict_a:
            # 如果值都是字典，则递归合并
            if isinstance(dict_a[key], dict) and isinstance(dict_b[key], dict):
                merge_dicts(dict_a[key], dict_b[key])
            else:
                # 否则，直接赋值
                dict_a[key] = dict_b[key]
        else:
            # 如果在 A 中不存在，直接添加
            dict_a[key] = dict_b[key]


def random_choices(dict_):
    if type(dict_)!=dict:
        raise ValueError('input must be dict')
    choice_res=[k for k in dict_.keys()]
    choice_p=[float(v) for v in dict_.values()]
    if sum(choice_p)!=1:
        raise ValueError('sum of choice_p must be 1')
    if len(choice_res)!=len(choice_p):
        raise ValueError('len of choice_res must be equal to len of choice_p')
    if len(choice_res)==0:
        raise ValueError('len of choice_res must be greater than 0')

    res=random.choices(choice_res,choice_p)[0]
    return res


def round_up_2_integer(src_num):
    # 向上取整 
    return math.ceil(float(src_num))


import collections
from pympler import asizeof


def print_object_details(obj, seen=None, prefix=''):
    """打印对象及其属性、方法的内存占用"""
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        print(f"{prefix}（已访问）: {asizeof.asizeof(obj)} bytes")
        return

    seen.add(obj_id)

    # 打印对象本身的大小
    size = asizeof.asizeof(obj)
    print(f"{prefix}{type(obj).__name__}: {size} bytes")

    # # 打印对象的属性
    # if hasattr(obj, '__dict__'):
    #     for attr, value in obj.__dict__.items():
    #         attr_size = asizeof.asizeof(value)
    #         print(f"{prefix}  {attr}: {attr_size} bytes")
    #         print_object_details(value, seen, prefix + '    ')

    # 打印对象的方法
    # methods = [method for method in dir(obj) if callable(getattr(obj, method)) and not method.startswith("__")]
    # for method in methods:
    #     method_size = asizeof.asizeof(getattr(obj, method))
    #     print(f"{prefix}  {method}: {method_size} bytes")
    #
    # # 处理列表类型的属性，打印每个元素的大小
    # if isinstance(obj, list):
    #     for index, item in enumerate(obj):
    #         item_size = asizeof.asizeof(item)
    #         print(f"{prefix}[{index}]: {item_size} bytes")
    #         print_object_details(item, seen, prefix + '  ')

def uniqueID_32():
    uuid_obj = uuid.uuid4()
    uuid_int = uuid_obj.int
    int32 = uuid_int & ((1 << 31) - 1)
    return int32

def uniqueID_64():
    uuid_obj = uuid.uuid4()
    uuid_int = uuid_obj.int
    int64 = uuid_int & ((1 << 31) - 1)
    return int64

if __name__ == '__main__':
    dict_= {0: 0.6, 1: 0.4}
    res=0
    for i in range(100):
        res+=random_choices(dict_)
    print(res)