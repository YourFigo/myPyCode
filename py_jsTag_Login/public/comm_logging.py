import time
import logging
from public import common


class MyLogging:
    # 初始化日志
    def __init__(self):
        # 创建日志文件夹
        nowTime = common.getNowTime()
        self.nowDate = common.getNowTime()
        self.logPath = common.getDirPath(nowTime, "log")
        common.mkdir(self.logPath)
        # 设置日志文件的文件名
        self.logName = 'jsTag_' + time.strftime('%Y%m%d_%H_%M_%S_%M', time.localtime(time.time())) + '.log'
        self.logFile = self.logPath + self.logName

        # 初始化日志
        # 1、设置formatter，日志的输出格式
        self.logFormat = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        self.formatter = logging.Formatter(self.logFormat)
        # 2、设置Handler，用于写入日志的控制。先创建Handler，然后设置Handler级别
        # 级别：CRITICAL > ERROR > WARNING > INFO > DEBUG，默认级别为 WARNING
        self.handler = logging.FileHandler(self.logFile,mode='a')
        self.handler.setLevel(logging.DEBUG)
        self.handler.setFormatter(self.formatter)
        # 3、创建及配置logger
        self.logger = logging.getLogger()
        self.logger.addHandler(self.handler)
    # 写日志
    def write_logger(self,content):
        self.logger.error(content)

# 初始化 myLogger 对象，供多个子程序使用
myLogger = MyLogging()