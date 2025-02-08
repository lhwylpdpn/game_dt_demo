import pickle
import time
import random
class Test():
    
    def __init__(self):
        self.result = []
        self.total_tiks = 100
        self.tick=0
        self.end_tick=random.randint(0,100)
    
    def run(self): 
        for i in range(0, self.total_tiks):

            self.tick+=1
            print('我是第',i,'次循环')
            if i>self.end_tick:
                return
            time.sleep(0.1)
        print('我是第',self.tick,'tick')
        return

def save_context(obj):
    file = "test.data"
    with open(file, "wb") as file_obj: 
        pickle.dump(obj, file_obj)

def load_contect():
    file = "test.data"
    with open(file, "rb") as file_obj:
        new_state = pickle.load(file_obj)
        return new_state


# def main():
#     test_object = Test()           # 第一次
#     #test_object = load_contect()  # 第二次运行时候， 加载场景
#     test_object.run() 
#     print(test_object.result)
#     save_context(test_object)


def main():
    test_object = Test()           # 第一次
    test_object.run()
    save_context(test_object)

def main_load():
    test_object = Test()           # 第一次
    test_object = load_contect()  # 第二次运行时候， 加载场景
    test_object.run()

if __name__ == "__main__":
    main_load()


