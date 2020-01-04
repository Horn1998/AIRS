import logging
import os
import logging.handlers


#创建logger对象
lg = logging.getLogger("Error")
def get_log():

    """
    初始化存放日志的位置
    """
    lg = logging.getLogger("Error")
    log_path = os.getcwd() + r"\logs"
    try:
        if not os.path.exists(log_path):
            os.makedirs(log_path)
    except:
        print("创建日志目录失败")
        exit(1)
    if len(lg.handlers) == 0: #避免重复
        #2.创建handler(负责输出，输出到屏幕streamhandler输出道文件filehandler)
        filename = os.path.join(log_path,'error.log')
        fh = logging.FileHandler(filename, mode="a", encoding="utf-8")
        sh = logging.StreamHandler()
        #创建formmatter:
        formatter = logging.Formatter(fmt = '%(asctime)s - %(levelname)s - Model:%(filename)s - Fun:%(funcName)s - Message:%(message)s - Line:%(lineno)d')
        lg.addHandler(fh)
        lg.addHandler(sh)
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        #设置日志级别（日志级别两层关卡必须都通过，日志才能正常记录
        lg.setLevel(40)
        fh.setLevel(40)
        sh.setLevel(40)
        return lg


class Logger:

    def __init__(self, loggername = 'log'):
        self.logger = logging.getLogger(loggername)
        log_path = os.getcwd() + r"\logs"
        try:
            if not os.path.exists(log_path):
                os.makedirs(log_path)
        except:
            print("创建日志目录失败")
            exit(1)
        if len(lg.handlers) == 0:  # 避免重复
            filename = os.path.join(log_path, loggername + '.log')
            fh = logging.FileHandler(filename, mode="a", encoding="utf-8")
            sh = logging.StreamHandler()
            # 创建formmatter:
            formatter = logging.Formatter(
                fmt='%(asctime)s - Model:%(filename)s - Fun:%(funcName)s - Message:%(message)s - Line:%(lineno)d')
            self.logger.addHandler(fh)
            self.logger.addHandler(sh)
            fh.setFormatter(formatter)
            sh.setFormatter(formatter)
            # 设置日志级别（日志级别两层关卡必须都通过，日志才能正常记录
            self.logger.setLevel(40)
            fh.setLevel(40)
            sh.setLevel(40)


    def get_log(self):
        return self.logger
