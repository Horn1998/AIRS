from Common.Database_Option.MongoDB.init_Mongo import *
from Common.Text_Processing import TXTFile_Process as fp
from Config.ModuleConfig.TextProcessingEngine import DataBasePath
import jieba.posseg as psg
import jieba
import datetime
import os
#初始化mongodb数据库
def mongodb_Init(Data_BasePath, database = 'test'):
    try:
        db = connect_MongoDB(database)
        indexnames = os.listdir(Data_BasePath)
        for name in indexnames:
            init_Table(db, name)
        return db
    except Exception as ex:
            print('创建数据库失败' , ex)



#将文件数据导入mongodb
def mongodb_Import(Data_BasePath, database = 'test'):
    '''
    导入数据
    :param Data_BasePath: 数据所在根目录
    :param database: 数据库名字
    :return:
    '''
    print(datetime.datetime.now())
    db = mongodb_Init(Data_BasePath, database)
    indexnames = os.listdir(Data_BasePath)
    try:
        for name in indexnames:
            save_dict = []
            table = db[name]
            ChildPath = Data_BasePath + '\\' + name
            txt_files = fp.TXT_Process(ChildPath)
            for file in txt_files:
                content = fp.readFile(file)
                result = (str(content)).replace("\r\n", "").strip()  # 删除多余空行与空格
                cutResult = jieba.cut(result)  # 默认方式分词，分词结果用空格隔开
                save_dict.append({'file_name': ChildPath, 'content': result, 'type': name, 'keywords': ' '.join(cutResult)})
            table.insert_many(save_dict)
    except Exception as ex:
        print(ex, '插入数据失败')
    finally:
        print(datetime.datetime.now())



#倒排索引表创建
#创建文档的倒排索引
def keywords_Init(Data_BasePath, DataBase = 'test'):
    '''

       :param Data_BasePath:
       :param index_name:
       :return:
       '''
    indexnames = os.listdir(Data_BasePath)  # 获取根目录下的子文件夹（不同类型)
    print(datetime.datetime.now())          # 计算耗时
    print("开始创建关键词表")
    db = connect_MongoDB(DataBase)
    collectionN = init_Table(db, 'InverseN_Index')#名词倒排索引
    collectionV = init_Table(db, 'InverseV_Index')#动词倒排索引
    collectionL = init_Table(db, 'InverseL_Index')#形容词倒排索引
    for name in indexnames:
        ChildPath = Data_BasePath + '\\' + name  # 获得当前索引类别对应的文件夹
        txt_files = fp.TXT_Process(ChildPath)  # 获取当前子目录下的txt文件列表
        for file in txt_files:
            content = fp.readFile(file)  # io阻塞
            result = (str(content)).replace("\r\n", "").strip()  # 删除多余空行与空格
            cutResult = set(psg.cut(result))  # cutResult: generator对象 可用迭代器获取值
            for item in cutResult:
                # item = {word:分词， flag：词性}
                # 获取名词分词
                if item.flag.endswith('v') or item.flag.endswith('vn'):
                    # db.[collectionName].update({查询器},{修改器})
                    # upsert = True :如果当前查询条件不存在，则创建该查询条件
                    collectionV.update({"keyword": item.word, "type": name}, {"$push": {'filename': file}, },
                                      upsert=True)
                elif item.flag.endswith('n') or item.flag[:-1].endswith('n'):
                    collectionN.update({"keyword": item.word, "type": name}, {"$push": {'filename': file}, },
                                       upsert=True)
                elif item.flag.endswith('l'):
                    collectionL.update({"keyword": item.word, "type": name}, {"$push": {'filename': file}, },
                                       upsert=True)
    print(datetime.datetime.now())



#停用词导入
def stopwords_Init(file_name, DataBase = 'test'):
    try:
        print(datetime.datetime.now())
        content = fp.readFileStop(file_name)
        result = (str(content)).replace("\r\n", "").strip()
        db = connect_MongoDB(DataBase)
        collection = init_Table(db, 'stopword')
        cutResult = set(psg.cut(result))
        insert_dict = []
        for item in cutResult:
            insert_dict.append({'word':item.word, 'type':item.flag})
        collection.insert_many(insert_dict)
        print("插入完毕，共插入{}条数据".format(len(insert_dict)))
        print(datetime.datetime.now())
    except Exception as ex:
        print(ex," 初始化停用表失败")
        if 'stopword' in db.list_collection_names():
            drop_Table(db, 'stopword')




#停用词添加
def stopwords_Add(file_name, DataBase = 'test'):
    try:
        print(datetime.datetime.now())
        content = fp.readFileStop(file_name)
        result = (str(content)).replace("\r\n", "").strip()
        db = connect_MongoDB(DataBase)
        collection = init_Table(db, 'stopword')
        cutResult = set(psg.cut(result))
        for item in cutResult:
            inset_dict = {'word': item.word, 'type': item.flag}
            collection.update(inset_dict, {'$set':inset_dict}, True)    #防止有重复的数据被插入
        print("插入完毕")
        print(datetime.datetime.now())
    except Exception as ex:
        print(ex, " 初始化停用表失败")
        if 'stopword' in db.list_collection_names():
            drop_Table(db, 'stopword')


# if __name__ == '__main__':
#     #keywords_Init(DataBasePath['DataBasePath'], 'test')
#     stopwords_Add(DataBasePath['stopwordpath'], 'test')

