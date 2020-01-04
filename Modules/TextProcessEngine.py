from Common.logger.logger import get_log
'''
文本推荐引擎
说明：
'''
from Result_Processing.DocumentRP.BayesAlgorithm import TF_IDF_Module

module_dict = {
        0: TF_IDF_Module,
        1: ""
    }


def get_Module(tag, paras):
    try:
        module = module_dict[tag]
        return module(database = paras['database'], user_id = paras['user_id'])
    except Exception as ex:
        get_log().error(ex)



# #种类预测模块接口
# class ITypePredict:
#     def TypePredict(self):
#         raise Exception('子类必须实现种类预测接口')
#
#
# #信息资源管理模块接口
# class IBaseMessage:
#     def BaseMessage(self):
#         raise Exception('子类必须实现信息资源提取模块接口')


    