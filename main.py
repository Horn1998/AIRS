from Builder import EngineBuilder
import json
from concurrent import futures
'''
此处为要注入的模块
'''
json_path = r'Config\TextProcessingEngine.json'
config = json.load(json_path)
#转换成字符串,可以按照操作字典的方法取值
str_config = json.loads(config)


modules = [(
    'TextProcessingEngine', 0,  []              #文本处理推荐引擎(引擎名， 引擎号， 引擎用到的模型)
)]

#使用协程与期物实现并发
if __name__ == '__main__':
    workers = len(modules)
    with futures.ProcessPoolExecutor(workers)  as executor:
        actual_worker = executor._max_workers
        to_do = []
        for work in modules:
            engine = EngineBuilder(config = config).build(work).run()
            future = executor.submit(engine)
            to_do.append(future)

    for future in futures.as_completed(to_do):
        res = future.result()
        #res = {"name":引擎名字, "answer":引擎运算结果"}
        print('modules' + res['name'] + 'works done')
        #下方为返回运算结果经过处理后交给微信小程序
        pass