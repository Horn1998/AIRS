import pickle
import os
def readFile(path):
    with open(path, 'r',errors='ignore') as file:  # 文档中编码有些问题，所有用errors过滤错误
        content = file.read()
        return content

def readFileStop(path):

    with open(path, 'r',   encoding='utf-8', errors='ignore') as file:  # 文档中编码有些问题，所有用errors过滤错误
        content = file.read()
        return content



def saveFile(path, result):
    with open(path, 'w', errors='ignore') as file:
        file.write(result)


#将文件中的序列化Bunch对象读出
def readBunch(path):
    with open(path, 'rb') as file:
        bunch = pickle.load(file)
        # pickle.load(file)
        # 函数的功能：将file中的对象序列化读出。
    return bunch



#将对象转化为字节流保存
def writeBunch(path, bunchFile):
    with open(path, 'wb') as file:
        pickle.dump(bunchFile, file)



def TXT_Process(Data_BasePase) -> list:
    '''
    :param Data_BasePase: 总文件夹路径
    :return: TXT文件路径列表
    '''
    txt_File = []
    def get_Path(Path:str):
        if Path.endswith('txt'):
            txt_File.append(Path)
            return
        fatherLists = os.listdir(Path)
        while fatherLists:
            LastFile = fatherLists.pop()
            Path += '\\' + LastFile
            get_Path(Path)
            Path = Path[:-len(LastFile) - 1]
    get_Path(Data_BasePase)
    return txt_File

#将Bunch对象序列化后写入bunchFile
def writeBunch(path, bunchFile):
    with open(path, 'wb') as file:
        pickle.dump(bunchFile, file)