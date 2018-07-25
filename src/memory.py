import pickle
import os.path


class Memory:
    """
    一个简单的内存类用于封装项目操纵的数据对象
    volatile是未保存的内存变量
    """
    volatile = {}

    def __init__(self):
        self.load_state()   # 创建时启动载入函数

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save_state() # 退出时启用保存函数

    def load_state(self):
        if os.path.exists('dump.rdb'): # 如果存在rdb快照
            state = pickle.load(open('dump.rdb', 'rb')) # 载入快照
            # 分别读取分序列化后相应的值
            self.volatile = state['volatile']

            # print("dump.rdb loaded into volatile memory") # 测试用

    # 执行save命令：同步保存操作，将当前redis实例的所有数据快照以rdb的形式保存到硬盘。
    def save_state(self):
        pickle.dump({'volatile': self.volatile}, open('dump.rdb', 'wb'))
        print("dump.rdb saved to disk")


memory = Memory()

