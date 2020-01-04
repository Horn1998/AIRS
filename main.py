from Common.Database_Option.MongoDB.init_Mongo import *
from Common.Database_Option.Elasticsearch.Init_ES import *
from Config.ModuleConfig.TextProcessingEngine import Path
from Common.logger.logger import *
from django.http import HttpResponse
from django.shortcuts import render
from Builder import Builder
from concurrent import futures
import json
import os
'''
此处为要注入的模块
'''
#test样例
modules = [{
    'para':{'database': 'test','user_id':'779161602'},
}]


#文本分类初始化
def text_classify_init(request):
    args = request.POST
    module = {'para':{'database': request.POST['database'], 'user_id':request.POST['user_id']}}
    print(module)
    engine = Builder(module).build()
    engine.run()
    return HttpResponse(module['para']['user_id'] + "用户执行完毕")


#用户初始化数据恢复
def text_classify_reverse(request):
    try:
        args = request.POST
        module = {'para': {'database': request.POST['database'], 'user_id': request.POST['user_id']}}
        DB = connect_MongoDB(request.POST["database"])
        drop_Table(DB,'体育')
        drop_Table(DB,'女性')
        drop_Table(DB,'文学出版')
        drop_Table(DB,'校园')
        drop_Table(DB,'InverseL_Index')
        drop_Table(DB,'InverseN_Index')
        drop_Table(DB,'InverseV_Index')
        drop_Table(DB,'stopword')
        es = connect_Elasticsearch()
        es.indices.delete(index=request.POST['database'], ignore=[400, 404])
        path_dict = Path(request.POST['database']).get_PathDict()
        if os.path.exists(path_dict['tfidfspace']):
            os.remove(path_dict['tfidfspace'])
        if os.path.exists(path_dict['predictspace']):
            os.remove(path_dict['predictspace'])
        if os.path.exists(path_dict['trainset']):
            os.remove(path_dict['trainset'])
        if os.path.exists(path_dict['testbunch']):
            os.remove(path_dict['testbunch'])
        if os.path.exists(path_dict['outputpath']):
            os.removedirs(path_dict['outputpath'])
        return HttpResponse(module['para']['user_id'] + "用户数据恢复完毕")
    except Exception as ex:
        get_log().error(ex)
        return HttpResponse('error')




#使用协程与期物实现并发
if __name__ == '__main__':
    workers = len(modules)
    with futures.ProcessPoolExecutor(workers) as executor:
        actual_worker = executor._max_workers
        to_do = []
        for work in modules:
            engine = Builder(config = work).build().run()
            future = executor.submit(engine)
            to_do.append(future)

    for future in futures.as_completed(to_do):
        res = future.result()
        #res = {"name":引擎名字, "answer":引擎运算结果"}
        print('modules' + res['name'] + 'works done')
        #下方为返回运算结果经过处理后交给微信小程序
        pass