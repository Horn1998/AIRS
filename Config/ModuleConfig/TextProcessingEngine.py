import os
BaseDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DataBasePath = BaseDir + "\\测试样例\\机器学习之文本分类"
database_name =""  #引擎初始化时设置
Path_Dict = {}
#创建当前文本处理模型的基本路径字典
def init_Path(database_name):
      #创建文件夹
    try:
      Path_Dict[database_name] = {
          "DataBasePath":   DataBasePath + "\\" + database_name + "\\data",
          "inputpath":      DataBasePath + "\\" + database_name + "\\data",
          "outputpath":     DataBasePath + "\\" + database_name + "\\segResult",
          "outputfile":     DataBasePath + "\\" + database_name + "\\trainset.dat",
          "tfidfspace":     DataBasePath + "\\" + database_name + "\\tfidfspace.dat",
          "testbunch":      DataBasePath + "\\" + database_name + "\\test_set.dat",
          "predictspace":   DataBasePath + "\\" + database_name + "\\predict.dat"
      }
    except Exception as ex:
        print('创建失败， 错误信息:', ex)
    return Path_Dict

