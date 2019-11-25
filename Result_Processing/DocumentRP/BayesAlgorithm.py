from sklearn.feature_extraction.text import TfidfTransformer                # TF-IDF向量转换类
from sklearn.feature_extraction.text import TfidfVectorizer                 # TF_IDF向量生成类
from sklearn.datasets.base import Bunch
from sklearn.naive_bayes import MultinomialNB       #多项式贝叶斯算法
from Common.Text_Processing.TXTFile_Process import readBunch, writeBunch
from Common.Database_Option.MongoDB.init_Mongo import connect_MongoDB
from Config.ModuleConfig.TextProcessingEngine import init_Path
from UUData.DBExport.Document_Mongo import bunchSave

import numpy as np
import pandas as pd
#获取停用词列表
def get_StopWords(database = 'test'):
    db = connect_MongoDB(database)
    stopword = db['stopword']
    data = pd.DataFrame(list(stopword.find()))
    return data['word'].values.tolist()



# 求得TF-IDF向量
def getTFIDFMat(database, pathdict, stopwordList):
    bunch = readBunch(pathdict[database]["outputfile"])
    tfidfspace = Bunch(target_name=bunch.target_name,label=bunch.label, filenames=bunch.filenames, tdm=[],
                       vocabulary={})
    # 初始化向量空间
    vectorizer = TfidfVectorizer(stop_words=stopwordList, sublinear_tf=True, max_df=0.5)
    # transformer = TfidfTransformer()  # 该类会统计每个词语的TF-IDF权值
    # 文本转化为词频矩阵，单独保存字典文件
    tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
    tfidfspace.vocabulary = vectorizer.vocabulary_   #获取词汇
    writeBunch(pathdict[database]["tfidfspace"], tfidfspace)



#求得预测结果集
def getTestSpace(database, path_dict, stopWordList):
    bunch = readBunch(path_dict[database]['testbunch'])
    # 构建测试集TF-IDF向量空间
    testSpace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[],
                      vocabulary={})
    # 导入训练集的词袋  改进：从elasticsearch中获取词袋
    trainbunch = readBunch(path_dict[database]['tfidfspace'])
    # 使用TfidfVectorizer初始化向量空间模型  使用训练集词袋向量
    vectorizer = TfidfVectorizer(stop_words=stopWordList, sublinear_tf=True, max_df=0.5,
                                 vocabulary=trainbunch.vocabulary)
    transformer = TfidfTransformer()
    testSpace.tdm = vectorizer.fit_transform(bunch.contents)
    testSpace.vocabulary = trainbunch.vocabulary
    # 持久化
    writeBunch(path_dict[database]['predictspace'], testSpace)



#通过贝叶斯进行种类预测
def bayesAlgorithm(database, path_dict):
    trainSet = bunchSave(path_dict[database]['tfidfspace'])
    testSet = readBunch(path_dict[database]['predictspace'])
    clf = MultinomialNB(alpha=0.001).fit(trainSet.tdm, trainSet.label)  #不同样例对应不同的标签
    #alpha:0.001 alpha 越小，迭代次数越多，精度越高
    # print(shape(trainSet.tdm))  #输出单词矩阵的类型 (样例数，特征数）
    # print(shape(testSet.tdm))
    predicted = clf.predict(testSet.tdm)
    total = len(predicted)
    rate = 0
    for flabel, fileName, expct_cate in zip(testSet.label, testSet.filenames, predicted):
        if flabel != expct_cate:
            rate += 1
            print(fileName, ":实际类别：", flabel, "-->预测类别：", expct_cate)
    print("erroe rate:", float(rate) * 100 / float(total), "%")




def TF_IDF_Module(database):
    Path_Dict = init_Path(database)
    stopwords = get_StopWords(database)
    getTFIDFMat(database, Path_Dict, stopwords)
    getTestSpace(database, Path_Dict, stopwords)
    bayesAlgorithm(database, Path_Dict)


