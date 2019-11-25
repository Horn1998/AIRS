#用户特征向量提取模块
from Common.Text_Processing.TXTFile_Process import readBunch, writeBunch
from sklearn.feature_extraction.text import  TfidfTransformer #TF_IDF向量转换类
from sklearn.feature_extraction.text import TfidfVectorizer   #TF_IDF向量生成类
import Common.Text_Processing.File_Process as fp
from sklearn.datasets.base import Bunch
import pickle  #序列化
import jieba
import time
import os
#获取文件分词
def segText(inputPath, resultPath):
    fatherLists = os.listdir(inputPath)                     # 主目录
    for eachDir in fatherLists:                             # 遍历主目录中各个文件夹
        eachPath = inputPath + "/" + eachDir + "/"                # 保存主目录中每个文件夹目录，便于遍历二级文件
        each_resultPath = resultPath +'/'+ eachDir +"/"       # 分词结果文件存入的目录
        if not os.path.exists(each_resultPath):
            os.makedirs(each_resultPath)
        childLists = os.listdir(eachPath)                   # 获取每个文件夹中的各个文件
        for eachFile in childLists:                         # 遍历每个文件夹中的子文件
            eachPathFile = eachPath + eachFile               # 获得每个文件路径
            content = fp.readFile(eachPathFile)              # 调用上面函数读取内容
            result = (str(content)).replace("\r\n", "").strip()  # 删除多余空行与空格

            cutResult = jieba.cut(result)                       # 默认方式分词，分词结果用空格隔开
            fp.saveFile(each_resultPath + eachFile, " ".join(cutResult))  # 调用上面函数保存文件



#将对象序列化后保存
def bunchSave(inputFile, outputFile):
    print('run bunchSave' , time.time())
    start = time.time()
    catelist = os.listdir(inputFile)

    bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
    bunch.target_name.extend(catelist)  # 将类别保存到Bunch对象中

    for eachDir in catelist:
        eachPath = inputFile + "/" + eachDir + "/"
        fileList = os.listdir(eachPath)
        for eachFile in fileList:  # 二级目录中的每个子文件
            fullName = eachPath + eachFile  # 二级目录子文件全路径
            bunch.label.append(eachDir)  # 当前分类标签
            bunch.filenames.append(fullName)  # 保存当前文件的路径
            bunch.contents.append(fp.readFile(fullName).strip())  # 保存文件词向量
    with open(outputFile, 'wb') as file_obj:  # 持久化必须用二进制访问模式打开
        pickle.dump(bunch, file_obj)  #文件可以不建立，但是文件夹必须建立
        #pickle.dump(obj, file, [,protocol])函数的功能：将obj对象序列化存入已经打开的file中。
        #obj：想要序列化的obj对象。
        #file:文件名称。
        #protocol：序列化使用的协议。如果该项省略，则默认为0。如果为负值或HIGHEST_PROTOCOL，则使用最高的协议版本
    print('finish bunch save + ', time.time(),  ', use time :' + str(start - time.time()))



#得到停用词
# def getStopWord(inputFile):
#     stopWordList = fp.readFileStop(inputFile).splitlines()
#     return stopWordList







def getTestSpace(testSetPath, trainSpacePath, stopWordList, testSpacePath):
    bunch = readBunch(testSetPath)
    # 构建测试集TF-IDF向量空间
    testSpace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[],
                      vocabulary={})
    # 导入训练集的词袋  改进：从elasticsearch中获取词袋
    trainbunch = readBunch(trainSpacePath)
    # 使用TfidfVectorizer初始化向量空间模型  使用训练集词袋向量
    #参数：
    #       max_df:当构建词汇表时，严格忽略高于给出阈值的文档频率的词条，语料指定的停用词，如果是浮点值， 该参数代表文档的比例，
    #       sublinear_tf:应用线性放缩TF，例如使用1 + log(tf)覆盖tf
    vectorizer = TfidfVectorizer( stop_words=stopWordList, sublinear_tf=True, max_df=0.5,
                                 vocabulary=trainbunch.vocabulary)
    #经过测试后发现一个字的话不会被删除掉，但是tfidf本身应该可以帮忙过滤掉单个的词（默认情况下，但是可以设置不过滤 token = r'(?)/b/w+/b'
    #经实验发现本文本是否使用停用词影响不大
    transformer = TfidfTransformer()
    testSpace.tdm = vectorizer.fit_transform(bunch.contents)
    testSpace.vocabulary = trainbunch.vocabulary
    # 持久化
    writeBunch(testSpacePath, testSpace)









