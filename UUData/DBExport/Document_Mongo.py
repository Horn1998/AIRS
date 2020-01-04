from Common.Database_Option.MongoDB.init_Mongo import *
from Common.Text_Processing.TXTFile_Process import readFile
from Common.logger.logger import get_log, Logger

from sklearn.datasets.base import Bunch
from Config.ModuleConfig.TextProcessingEngine import Path
import pandas as pd
import pickle
import os


#将数据库信息转为bunch对象
def bunchSave(database = 'test'):
    try:
        Logger().get_log().error('将数据库信息转换为bunch对象')
        dbname = database
        pathdict = Path(dbname).get_PathDict()
        print('run bunchSave')
        catelist = os.listdir(pathdict['DataBasePath'])
        bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
        bunch.target_name.extend(catelist)  # 将类别保存到Bunch对象中
        db = connect_MongoDB(database)
        for table in catelist:
            # init_Table(db, table)
            collection = db[table]
            for item in collection.find():
                bunch.label.append(item['type'])
                bunch.filenames.append(item['file_name'])
                bunch.contents.append(item['content'].strip())
    except Exception as ex:
         get_log().error(ex)
    return bunch

#将txt文件转换为dat文件
def bunchSaveFile(inputFile, outputFile):
    try:
        Logger().get_log().error('将文件信息转换为bunch对象')
        catelist = os.listdir(inputFile)
        bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
        bunch.target_name.extend(catelist)  # 将类别保存到Bunch对象中
        for eachDir in catelist:
            print(eachDir, inputFile)
            eachPath = inputFile + r"\\" + eachDir + r"\\"
            fileList = os.listdir(eachPath)
            for eachFile in fileList:  # 二级目录中的每个子文件
                fullName = eachPath + eachFile  # 二级目录子文件全路径
                bunch.label.append(eachDir)  # 当前分类标签
                bunch.filenames.append(fullName)  # 保存当前文件的路径
                bunch.contents.append(readFile(fullName).strip())  # 保存文件词向量
        with open(outputFile, 'wb') as file_obj:  # 持久化必须用二进制访问模式打开
            pickle.dump(bunch, file_obj)
            # pickle.dump(obj, file, [,protocol])函数的功能：将obj对象序列化存入已经打开的file中。
            # obj：想要序列化的obj对象。
            # file:文件名称。
            # protocol：序列化使用的协议。如果该项省略，则默认为0。如果为负值或HIGHEST_PROTOCOL，则使用最高的协议版
    except Exception as ex:
        get_log().error(ex)







