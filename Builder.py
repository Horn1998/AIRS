from Core import Engine

#相当于一个引擎工厂
class Builder:
    #初始化建造配置文件
    def __init__(self, opts):
        self.opts = opts

    def build(self):
        return Engine(inject = self.opts)





