from Config.ModuleConfig.TextProcessingEngine import Path
from UUData.DBImport import Documents_Mongo as dmip
from UUData.DBExport import Document_Mongo as dmep
from UUData.DBImport import Documents_ES as de
from Common.Text_Processing.TXTFile_Process import writeBunch
from Common.logger.logger import get_log
def TextEngineInit(args):
    dbname = args['database']
    try:
        pathdict = Path(dbname).get_PathDict()
        # #mongo导入操作
        dmip.mongodb_Import(pathdict['DataBasePath'], dbname)
        dmip.stopwords_Init(pathdict['stopwords'],   dbname)
        # dmip.keywords_Init(pathdict['DataBasePath'],  dbname)

        # #mongo序列化操作
        bunchObj = dmep.bunchSave(dbname)
        writeBunch(pathdict['trainset'], bunchObj)


        #es导入操作
        de.documents_Init(pathdict['DataBasePath'], dbname)
    except Exception as ex:
        get_log().error(ex)



if __name__ == '__main__':
    TextEngineInit({'database':'test'})