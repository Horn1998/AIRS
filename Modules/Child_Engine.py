from Modules.TextProcessEngine import  *
'''
说明：
        子引擎返回值为最终推荐结果和模型序列号
        模型序列号：
                    文本处理推荐引擎      0
                    
'''
def run_engine(tag, modules):
    if tag == 0:   #运行文本处理引擎
        Engine = TextProcessEngine(modules)
        pass