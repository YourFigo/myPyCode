import os
from datetime import datetime,timedelta
import pandas as pd

#创建文件夹
def mkdir(path):
    path = path.strip()
    path = path.rstrip("/")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("  路径创建成功--------")
        return True
    else:
        print( "  路径已存在---------")
        return False

#返回nowTime
def getNowTime(delta = 0,type='_'):
    nowTime = (datetime.now() + timedelta(days= delta)).strftime('%Y_%m_%d_%H_%M_%S')
    if type == '-':
        nowTime = (datetime.now() + timedelta(days=delta)).strftime('%Y-%m-%d-%H-%M-%S')
    return nowTime

#返回数据保存路径
def getDirPath(nowTime,type = "data"):
    if type == "log":
        path = 'D:/360security/logs/' + nowTime[0:10] + '/'
    elif type == "data":
        path = 'D:/360security/data/' + nowTime[0:10] + '/'
    return path

#返回文件名
def getExcelName(nowTime,webName):
    excelName = "DailyReport_" + webName + ".xls"
    # excelName = "DailyReport_" + webName + "_" + nowTime[11:] + ".xlsx"
    return excelName

# 其他格式转为 xls,AdName,match_Str 二者要成对出现，用于指定广告网站和要保留行的日期
def turnToXls_ByPandas(file1, file2, AdName = None, match_Str = None):
    '''
    :param file1: 待转换的文件名
    :param file2: 转换后的文件名
    :param AdName: 广告厂家名，不同情况不同处理
    :param match_Str: Adview中需要删除其他日期，这个是 当天日期的字符串形式，用于排除其他日期
    :param match_Str_before: Adview中如果昨天没有数据，前一天的字符串形式，用于排除其他日期
    :return:
    '''
    # 关于encoding 试过 utf-8 ascii 等都不行
    if AdName == "openx":
        # 主要编码格式，使用不当会出现 UnicodeDecodeError
        csv = pd.read_excel(file1,encoding='gb18030')
    else:
        csv = pd.read_csv(file1,encoding='gb18030')
    if AdName == "Adview":
        csv = pd.DataFrame(csv, columns=["Date", "App name", "SDK-KEY", "Ad Type", "Impressions", "Clicks", "CTR",
                                         "Number of plays(video)", "eCPM($)", "CPC($)", "Gross Revenue($)"])
        # 在第一列寻找当天的的数据，将其他日期的删除
        dateCol = csv.Date
        rowNum = dateCol.size
        yesterNum = 0
        for i in range(1, rowNum):
            if dateCol[i] == match_Str:
                yesterNum = yesterNum + 1
        if yesterNum >= 1:
            for i in range(1,rowNum):
                if dateCol[i] != match_Str:
                    csv.drop([i], inplace=True)

    csv.to_excel(file2, sheet_name=AdName)

# 扫描指定路径下，指定文件名前缀的所有文件,返回文件名list
def scan_File(path,prefix):
    FileList = []

    for root, sub_dirs, files in os.walk(path):
        if root == path:
            for file in files:
                # 判断字符串是否以 prefix 开头
                if file.startswith(prefix):
                    FileList.append(file)
    return FileList

# 扫描指定路径下，指定文件名前缀的所有文件,并删除
def remove_File(path,prefix):

    for root, sub_dirs, files in os.walk(path):
        if root == path:
            for file in files:
                # 判断字符串是否以 prefix 开头
                if file.startswith(prefix):
                    os.remove(path + file)