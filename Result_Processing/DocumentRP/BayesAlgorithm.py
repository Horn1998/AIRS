from sklearn.feature_extraction.text import TfidfTransformer                # TF-IDF向量转换类
from sklearn.feature_extraction.text import TfidfVectorizer                 # TF_IDF向量生成类
from sklearn.datasets.base import Bunch
from sklearn.naive_bayes import MultinomialNB       #多项式贝叶斯算法

from Common.Text_Processing.TXTFile_Process import readBunch, writeBunch
from Common.Database_Option.MongoDB.init_Mongo import connect_MongoDB
from Common.logger.logger import get_log, Logger

from DataAnalysis.Feature_Extraction.User_Portrait.DocumentsAnalysis.TF_IDF import segText
from Config.ModuleConfig.TextProcessingEngine import Path
from UUData.DBExport.Document_Mongo import bunchSave, bunchSaveFile
import pandas as pd

class TF_IDF_Module:
    def __init__(self, **kwargs):
        try:
            Logger().get_log().error("TF_IDF模型初始化结束")
            self.database = kwargs['database']
            self.stopwords = self.get_StopWords()
            self.path_dict = Path(self.database).get_PathDict()
        except Exception as e:
            get_log().error(e)





    # 获取停用词列表
    def get_StopWords(self):
        Logger().get_log().error("停用词表获取成功")
        db = connect_MongoDB(self.database)
        stopword = db['stopword']
        data = pd.DataFrame(list(stopword.find()))
        return data['word'].values.tolist()



    # 求得TF-IDF向量
    def getTFIDFMat(self):
        try:
            Logger().get_log().error("获取TF-IDF向量,得到tfidfspace.dat")
            bunch = readBunch(self.path_dict["trainset"])
            tfidfspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[],
                               vocabulary={})
            # 初始化向量空间
            vectorizer = TfidfVectorizer(stop_words=self.stopwords, sublinear_tf=True, max_df=0.5)
            # transformer = TfidfTransformer()  # 该类会统计每个词语的TF-IDF权值
            # 文本转化为词频矩阵，单独保存字典文件
            tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
            tfidfspace.vocabulary = vectorizer.vocabulary_  # 获取词汇
            writeBunch(self.path_dict["tfidfspace"], tfidfspace)
        except Exception as ex:
            get_log().error(ex)



    #获取测试集分词结果
    def getTestDat(self):
        try:
            Logger().get_log().error("获取测试集分词结果")
            #获取分词结果
            segText(self.path_dict["TestBasePath"], self.path_dict["outputpath"] )
            #获取testspace.bat
            bunchSaveFile(self.path_dict["TestBasePath"], self.path_dict["testbunch"])
        except Exception as ex:
            get_log().error(ex)



    # 求得预测结果集
    def getTestSpace(self):
        try:
            Logger().get_log().error("获取预测结果集")
            bunch = readBunch(self.path_dict['testbunch'])
            # 构建测试集TF-IDF向量空间
            testSpace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[],
                              vocabulary={})
            # 导入训练集的词袋  改进：从elasticsearch中获取词袋
            trainbunch = readBunch(self.path_dict['tfidfspace'])
            # 使用TfidfVectorizer初始化向量空间模型  使用训练集词袋向量
            vectorizer = TfidfVectorizer(stop_words=self.stopwords, sublinear_tf=True, max_df=0.5,
                                         vocabulary=trainbunch.vocabulary)
            transformer = TfidfTransformer()
            testSpace.tdm = vectorizer.fit_transform(bunch.contents)
            testSpace.vocabulary = trainbunch.vocabulary
            # 持久化
            writeBunch(self.path_dict['predictspace'], testSpace)
        except Exception as ex:
            get_log().error(ex)



    # 通过贝叶斯进行种类预测
    def bayesAlgorithm(self):
        try:
            Logger().get_log().error("贝叶斯种类预测")
            trainSet = readBunch(self.path_dict['tfidfspace'])
            testSet = readBunch(self.path_dict['predictspace'])
            clf = MultinomialNB(alpha=0.001).fit(trainSet.tdm, trainSet.label)  # 不同样例对应不同的标签
            # alpha:0.001 alpha 越小，迭代次数越多，精度越高
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
        except Exception as ex:
            get_log().error(ex)



    #启动引擎
    def run(self):
        Logger().get_log().error('run 执行')
        # 获取tfidfspace.dat
        self.getTFIDFMat()
        # 获取test_set.dat
        self.getTestDat()
        #获取tfidfspace.dat
        self.getTFIDFMat()
        # 获取testspace.dat
        self.getTestSpace()
        #获取预测结果
        self.bayesAlgorithm()


if __name__ == '__main__':
    tf_idf = TF_IDF_Module(database='test')
    tf_idf.run()