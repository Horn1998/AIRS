from Mapper import Mapper, Module
from Modules.Child_Engine import run_engine
import asyncio

class Core(metaclass=Module):
    """
    推荐引擎核心，相关模块注入该核心内
    """
    def __init__(self, modules):
        self.modules = modules
        for name in modules.keys():
            setattr(self, name, modules[name])


class Engine(object):
    """
    推荐引擎
    """
    def __init__(self, opts = None, inject = dict):
        print('start engine')
        #给核心注入相应的模块
        Mapper.register(Core, dict)        #建立引擎核心与模块之间的映射关系
        #存在疑问
        self.engine = dict         #保存引擎的名字

    @asyncio.coroutine
    def run(self):
        """
        启动引擎
        :return: {"name":引擎名字,res:"计算结果"}
        """
        print('engine is running')
        res = yield from run_engine(self.engine[1], self.engine[2])





    def shutDown(self):
        """
        关闭引擎
        :return:
        """
        print('engine is shutdown')