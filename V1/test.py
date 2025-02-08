import pickle
import time

class Test():
    
    def __init__(self):
        self.result = []
        self.total_tiks = 10000
        self.end_tik = 0

    def run(self): 
        time1 = time.time()
        for i in range(self.end_tik, self.total_tiks):
            self.result.append(i) # TODO do something
            self.end_tik = i
            if time.time() - time1 > 5: # 触发停止条件
                break
            time.sleep(1)
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


def main():
    test_object = Test()           # 第一次
    #test_object = load_contect()  # 第二次运行时候， 加载场景
    test_object.run() 
    print(test_object.result)
    save_context(test_object)



if __name__ == "__main__":
    main()
