from Modules.TextProcessEngine import get_Module
from UUData.EngineInit.TextProcessEngine import TextEngineInit
from Common.Database_Option.MongoDB.init_Mongo import connect_MongoDB, init_Table, get_message
from Common.logger.logger import get_log
'''
说明：
        子引擎返回值为最终推荐结果和模型序列号
        模型序列号：
                    文本处理推荐引擎      0
                    
'''
def get_MongoPara(database):
    db = connect_MongoDB(database)
    table = db.user_config
    return table


def get_Engine(dict):
    # 获取引擎参数
    paras = dict['para']
    print("获取引擎参数")
    # 获取操作表
    table = get_MongoPara(paras['database'])
    result = get_message(table, {'app_id': paras['user_id']})
    if result['engine'] == 'TextProcessingEngine':   #运行文本处理引擎
       try:
            TextEngineInit(paras)
            return get_Module(result['tag'], paras)
       except Exception as e:
           get_log().error(e)



if __name__ == '__main__':
    get_Engine({
    'engineType':'TextProcessingEngine',#文本处理推荐引擎(引擎类型， 引擎号)  ->   文本处理引擎 0号模型
    'ModuleName':'TF_IDF_Module',
    'tag' : 0,  #文本处理引擎 0号模型
    'para':{'database': 'test','user_id':'779161602'},
})