import json
import os
from elasticsearch import Elasticsearch
import datetime

#连接elasticsearch
def connect_Elasticsearch():
    BasePath = os.path.dirname(os.path.abspath(__file__))
    with open(BasePath + r'\\package.json', 'r') as file:
        json_config = json.load(file)
        _es = Elasticsearch([{'host': json_config['elasticsearch']['host'],'port': json_config['elasticsearch']['port']}])
        if _es.ping():
            print('connect success')
        else:
            print('connect fail')
        return _es


def create_index(es_object, index_name = 'test'):
    '''
    :param es_object:
    :param index_name:每一个索引对应一个用户，索引名字用用户id
    :return:
    '''
    created = False
    settings = {
        "settings":{
            "numbser_of_shards":5,    #一个分片
            "number_of_replicas":1    #0个备份
        },
        "mappings":{
            "Document":{
                "dynamic":"strict",   #含义不明确
                "properties":{
                    "content":{
                        "type":"text"
                    },
                    "file_name":{
                        "type":"text"
                    },
                    "Date":{
                        "type":"date"
                    }
                }
            }
        }
    }
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index = index_name, ignore = 400, body = settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


# 使日期序列化
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)



#记录索引
def store_record(elastic_object, index_name, type_name, record):
    try:
        record = json.dumps(record,cls = DateEncoder)
        outcome = elastic_object.index(index = index_name, doc_type = type_name, body = record)
    except  Exception as ex:
        print('Error in indexing data')
        print(str(ex))





#查询样例
def ES_search(es_object, index_name = 'test'):
    if es_object:
        search_object = {
            'query':
                {
                    'match':
                        {'file_name':'123'}
                }
        }
        query = es_object.search(index = index_name, body = search_object)
        print(query['hits']['hits'][0]['_source'])
        #{'content': '123', 'file_name': '123', 'date': '2019-11-22 00:47:17'}



