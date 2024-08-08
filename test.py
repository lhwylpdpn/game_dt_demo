




def xiangzi_info():
    xiangzi_1= {"tiji":40*30*30,"zhongliang":20}
    xiangzi_2= {"tiji":40*30*30,"zhongliang":7}
    xiangzi_3= {"tiji":40*30*30,"zhongliang":11}
    xiangzi_4= {"tiji":40*30*30,"zhongliang":20}
    xiangzi_5= {"tiji":40*30*30,"zhongliang":17}
    xiangzi_6= {"tiji":40*30*30,"zhongliang":20}
    xiangzi_7= {"tiji":40*30*30,"zhongliang":20}
    xiangzi_8= {"tiji":40*30*30,"zhongliang":10}
    xiangzi_9= {"tiji":30*40*55,"zhongliang":7}
    xiangzi_10= {"tiji":60*50*75,"zhongliang":25}
    xiangzi_11= {"tiji":60*50*75,"zhongliang":30}
    xiangzi_12= {"tiji":60*50*75,"zhongliang":30}
    xiangzi_13= {"tiji":60*50*75,"zhongliang":45}
    xiangzi_14= {"tiji":30*20*40,"zhongliang":5}
    return [xiangzi_1,xiangzi_2,xiangzi_3,xiangzi_4,xiangzi_5,xiangzi_6,xiangzi_7,xiangzi_8,xiangzi_9,xiangzi_10,xiangzi_11,xiangzi_12,xiangzi_13,xiangzi_14]
def zhongliang(tiji,zhongliang):
    tiji_zhongliang=tiji/6000
    return max(tiji_zhongliang,zhongliang)


def debang(zhongliang):
    single=150/120
    return zhongliang*single

def huolala(zhongliang):
    single=150/120
    return zhongliang*single

if __name__ == '__main__':
    xiangzi=xiangzi_info()
    tiji=0
    zhonglaing=0
    for x in xiangzi:
        tiji=x["tiji"]+tiji
        zhonglaing=x["zhongliang"]+zhonglaing
    print(tiji,zhonglaing)
    print(debang(zhongliang(tiji,zhonglaing)))
    print(120*170*100)