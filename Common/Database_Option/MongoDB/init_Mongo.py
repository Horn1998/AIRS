from Config.DBConfig.Mongodb import mongo_config
import pymongo
from Common.logger.logger import get_log
myclient = pymongo.MongoClient("mongodb://"+mongo_config['host'] + ':' + mongo_config['port'])


#创建数据库
def init_MongoDB(name = 'test'):
    try:
        dbnames = myclient.list_database_names()
        print(dbnames)
        if name in dbnames:
            print('数据库已经存在')
        #空数据库不能创建 除非添加数据
        mongo_db = myclient[name]
        return mongo_db
    except Exception as e:
        get_log().error(e)



#连接mongodb
def connect_MongoDB(name):
    try:
        return myclient[name]
    except Exception as e:
        get_log().error(e)



#创建数据表
def init_Table(DB, table_name):
    try:
        collist = DB.list_collection_names()
        if table_name in collist:
            print('数据表已经存在,无需重复创建')
        return DB[table_name]
    except Exception as e:
        get_log().error(e)



#删除数据表
def drop_Table(DB, table_name):
    try:
        collist = DB.list_collection_names()
        if table_name in collist:
            DB[table_name].drop()
            print("删除{}表成功".format(table_name))
        else:
            print("删除{}表失败".format(table_name))
    except Exception as e:
        get_log().error(e)




#查询数据
def get_message(collection, dict):
    try:
        result = collection.find_one(dict)
        return result
    except Exception as e:
        get_log().error(e)

if __name__ == '__main__':
    drop_Table(connect_MongoDB('test'),'体育')
    drop_Table(connect_MongoDB('test'),'女性')
    drop_Table(connect_MongoDB('test'),'文学出版')
    drop_Table(connect_MongoDB('test'),'校园')
    drop_Table(connect_MongoDB('test'),'stopword')
