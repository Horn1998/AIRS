import os
import pandas as pd
from Common.Database_Option.MongoDB.init_Mongo import connect_MongoDB
from Common.logger.logger import get_log

BaseDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DataBasePath = BaseDir + "\\测试样例"
Path_Dict, database_name = {}, ""  #引擎初始化时设置
#创建路径类
class Path:
    def __init__(self, database):
        self.database = database
        self.path_dict = self.init_Path()


    #创建当前文本处理模型的基本路径字典
    def init_Path(self):
      #创建文件夹
        try:
          Path_Dict[self.database] = {
              "DataBasePath":   DataBasePath + "\\" + self.database + "\\data",
              "TestBasePath":   DataBasePath + "\\" + self.database + "\\test",
              "inputpath":      DataBasePath + "\\" + self.database + "\\data",
              "outputpath":     DataBasePath + "\\" + self.database + "\\segResult",
              "trainset":       DataBasePath + "\\" + self.database + "\\trainset.dat",
              "tfidfspace":     DataBasePath + "\\" + self.database + "\\tfidfspace.dat",
              "testbunch":      DataBasePath + "\\" + self.database + "\\test_set.dat",
              "predictspace":   DataBasePath + "\\" + self.database + "\\predict.dat",
              "stopwords":      DataBasePath + "\\" + self.database + "\\stopword.txt"
          }
        except Exception as ex:
            get_log().error(ex)
        return Path_Dict[self.database]


    #获取路径字典
    def get_PathDict(self):
        return self.path_dict
