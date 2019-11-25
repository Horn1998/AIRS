from Common.Database_Option.MongoDB.init_Mongo import *
from sklearn.datasets.base import Bunch
from Config.ModuleConfig.TextProcessingEngine import DataBasePath
import pandas as pd
import os

#将数据库信息转为bunch对象
def bunchSave(database = 'test'):
    print('run bunchSave')
    catelist = os.listdir(DataBasePath['DataBasePath'])
    bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
    bunch.target_name.extend(catelist)  # 将类别保存到Bunch对象中
    db = connect_MongoDB(database)
    for table in catelist:
        init_Table(db, table)
        collection = db[table]
        for item in collection.find():
            bunch.label.append(item[table])
            bunch.filenames.append(item['file_name'])
            bunch.contents.append(item['content'].strip())
    return bunch





#
if __name__ == '__main__':
    bunchSave()
