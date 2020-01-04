from Config.ModuleConfig.TextProcessingEngine import DataBasePath
from Common.Database_Option.Elasticsearch.Init_ES import *
from Common.Text_Processing import TXTFile_Process as fp
from elasticsearch import helpers
import datetime
import jieba
import os
Data_BasePath = DataBasePath

# 文件批量导入type
def bulk_import(es, index_name='test', data_list=[]):
    index = index_name
    actions = []
    for data in data_list:
        action = {
            "_index": index,
            "_type": type,
            "_id": None,
            "_source":data
        }

        actions.append(action)
    if len(actions) > 0:
        try:
            helpers.bulk(es, actions, request_timeout=100)
        except Exception as ex:
            error_message = ex.args[0]
            if 'document(s) failed to index' in error_message:
                raise ImportError(error_message)
    end_time = datetime.datetime.now()
    print(end_time, '本次共写入了{}条数据'.format(len(actions)))



#将所有文档存储到elasticsearch
def documents_Init(DataBasePath, index_name = 'test'):
    '''
    在index_name数据库下创建表并添加数据
    :param Data_BasePath: 数据文件夹根目录
    :param index_name:    数据库名称
    :return:
    '''
    print('将所有文档存储到elasticsearch')
    es = connect_Elasticsearch()
    indexnames = os.listdir(DataBasePath)
    print(datetime.datetime.now())
    save_dict = []
    for name in indexnames:
        ChildPath = DataBasePath + '\\' + name                 #获得当前索引类别对应的文件夹
        txt_files = fp.TXT_Process(ChildPath)                    #获取当前子目录下的txt文件列表
        for file in txt_files:
            content = fp.readFile(file)                             #io阻塞
            result = (str(content)).replace("\r\n", "").strip()     # 删除多余空行与空格
            cutResult = jieba.cut(result)                             # 默认方式分词，分词结果用空格隔开
            save_dict.append( {'file_name':ChildPath, 'content':result, 'type':name, 'keywords':' '.join(cutResult)})
    try:
        create_index(connect_Elasticsearch(), index_name)
        bulk_import(es, index_name, save_dict)    #将数据批量导入elasticsearch
    except Exception as ex:
        # es.indices.delete(index_name)
        print(ex, ' ,' + index_name + ' has been deleted')
    else:
        print('索引数据初始化完成')









