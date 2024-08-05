import dictdiffer
import time
import pandas as pd



class performance:
    def __init__(self):
        self.start_time = time.time()
        self.result = {}
        self.tag_time={}
        self.event_count={}
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
        df['avg_time']=df['time']/df['count']
        print(df)

def Deepdiff_modify(before,after):
    #
    # print('Deepdiff_modify_before给强爷----',"before['hero'][5002]['AvailableSkills']",before['hero'][5002]['AvailableSkills'])
    #
    # print('手动变化',"['hero'][5002]['test']={'k':[200, 201, 202, 203, 204, 205, 3],'K2':[33,33]}")
    # after['hero'][5002]['test'] = {'k': [200, 201, 202, 203, 204, 205, 3], 'K2': [33, 33]}
    # print('Deepdiff_modify_after给强爷',"before['hero'][5002]['AvailableSkills']",after['hero'][5002]['AvailableSkills'])

    res=list(dictdiffer.diff(before, after))
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
    return_res=res

    return return_res


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

