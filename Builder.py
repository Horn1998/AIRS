from Core import Engine


class Builder:
    #初始化建造配置文件
    def __init__(self, opts):
        self.opts = opts

    def build(self, modules):
        return Engine(opts = self.opts, inject=modules)



def EngineBuilder(config):
    return Builder(config)

