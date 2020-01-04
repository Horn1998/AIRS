from Mapper import Mapper, Module
from Modules.Child_Engine import get_Engine
import asyncio
#Core函数拥有了Module中的属性，但是Core子类不能重载Module中的方法
class Core(metaclass=Module):
    """
    推荐引擎核心，相关模块注入该核心内
    """
    def __init__(self, modules):
        self.modules = modules
        for name in modules.keys():
            setattr(self, name, modules[name])


class Engine:
    """
    推荐引擎
    """
    def __init__(self, inject:dict):
        print('start engine')
        #给核心注入相应的模块
        # self.core  = Mapper.register(Core, get_Engine(inject))        #建立引擎核心与模块之间的映射关系,目前不清楚这个干什么用的
        self.engine = get_Engine(inject)                              #获取引擎



    def run(self):
        """
        启动引擎
        :return: {"name":引擎名字,res:"计算结果"}
        """
        print('engine is running')
        self.engine.run()






    def shutDown(self):
        """
        关闭引擎
        :return:
        """
        print('engine is shutdown')