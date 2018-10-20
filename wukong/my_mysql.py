import mysql.connector as myConn
import traceback

config = {
    'host': 'xxx',
    'user': 'xxx',
    'password': 'xxx',
    'port': 3306,
    'database': 'xxx',
    'charset': 'utf8'
}

def createTable(tb_name, *args):
    '''
    :param tb_name: 需要创建的表格名
    :param autoUpNum: 主键在columns中的索引
    :param args: 表格字段名和字段类型，args中包含两个list，第一个为字段名list，第二个为字段类型list，两个list长度需要一致
    :return:无
    '''
    try:
        conn = myConn.connect(**config)
        cursor = conn.cursor()

        columns = args[0]
        colsType = args[1]
        len1 = columns.__len__()
        len2 = colsType.__len__()
        if len1 == len2:
            crtTbSql = 'create table if not exists ' + tb_name + '('
            for i in range(len1):
                if i == len1 - 1:
                        crtTbSql = crtTbSql + columns[i] + ' ' + colsType[i]
                else:
                        crtTbSql = crtTbSql + columns[i] + ' ' + colsType[i] + ','
            crtTbSql = crtTbSql + ')'

        # crtTbSql = 'create table if not exists tb_toutiao(num int PRIMARY KEY,title VARCHAR(50),url VARCHAR(50),source VARCHAR(10),commentNum VARCHAR(5),NewsDate DATE)'
        cursor.execute(crtTbSql)
        print("mysql表格创建完成---------")
        conn.commit()
    except myConn.Error as e:
        print("connect fails! {}".format(e))
        print(traceback.format_exc())
    finally:
        cursor.close()
        conn.close()

# 一条记录一条记录提交，数据库存储相当慢
def insertSingleToutiao(tb_name, valuesTuple):
    try:
        conn = myConn.connect(**config)
        cursor = conn.cursor()
        # 这个地方 必须全为 %s，因为sql 语句 必须是 字符串，如果写 %d，报错：Not all parameters were used in the SQL statement
        insertSql = 'replace into ' + tb_name + ' (NewsID,title,url,source,commentNum,NewsDate) values (%s,%s,%s,%s,%s,%s)'
        cursor.execute(insertSql, valuesTuple)
        effectRow = cursor.rowcount
        print("mysql插入完成，受影响行数：{}".format(effectRow))
        # 删除重复，保留新记录
        dltReptSql = 'delete from a using ' + tb_name + ' as a,' + tb_name + ' as b where a.num < b.num and a.NewsID = b.NewsID'
        cursor.execute(dltReptSql)
        effectRow = cursor.rowcount
        print("mysql删除重复记录完成，受影响行数：{}".format(effectRow))
        conn.commit()
    except myConn.Error as e:
        print("connect fails! {}".format(e))
        print(traceback.format_exc())
    finally:
        cursor.close()
        conn.close()

# 多次插入、删除，一次性提交，速度比较快
def insertBatchToutiao(tb_name,valuesList):
    listLen = len(valuesList)
    insertSql = 'replace into ' + tb_name + ' (NewsID,title,url,source,commentNum,NewsDate) values (%s,%s,%s,%s,%s,%s)'
    dltReptSql = 'delete from a using ' + tb_name + ' as a,' + tb_name + ' as b where a.num < b.num and a.NewsID = b.NewsID'
    effectRow = 0
    try:
        conn = myConn.connect(**config)
        cursor = conn.cursor()
        if listLen >= 1:
            for li in valuesList:
                valuesTuple = li
                cursor.execute(insertSql, valuesTuple)
                effectRow = effectRow + 1
            print("mysql插入完成，受影响行数：{}".format(effectRow))
            cursor.execute(dltReptSql)
            effectRow = cursor.rowcount
            print("mysql删除重复记录完成，受影响行数：{}".format(effectRow))
    except myConn.Error as e:
        print("connect fails! {}".format(e))
        print(traceback.format_exc())
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def insertSingleWukong(tb_name, valuesTuple):
    try:
        conn = myConn.connect(**config)
        cursor = conn.cursor()
        # 这个地方 必须全为 %s，因为sql 语句 必须是 字符串，如果写 %d，报错：Not all parameters were used in the SQL statement
        insertSql = 'replace into ' + tb_name + ' (NewsID,url,keyword,title,replyNum,collectNum,likeNum,commentNum) values (%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(insertSql, valuesTuple)
        effectRow = cursor.rowcount
        print("mysql插入完成，受影响行数：{}".format(effectRow))
        # 删除重复，保留新记录
        dltReptSql = 'delete from a using ' + tb_name + ' as a,' + tb_name + ' as b where a.num < b.num and a.NewsID = b.NewsID'
        cursor.execute(dltReptSql)
        effectRow = cursor.rowcount
        print("mysql删除重复记录完成，受影响行数：{}".format(effectRow))
        conn.commit()
    except myConn.Error as e:
        print("connect fails! {}".format(e))
        print(traceback.format_exc())
    finally:
        cursor.close()
        conn.close()

def insertBatchWukong(tb_name,valuesList):
    listLen = len(valuesList)
    insertSql = 'replace into ' + tb_name + ' (NewsID,url,keyword,title,replyNum,collectNum,likeNum,commentNum) values (%s,%s,%s,%s,%s,%s,%s,%s)'
    dltReptSql = 'delete from a using ' + tb_name + ' as a,' + tb_name + ' as b where a.num < b.num and a.NewsID = b.NewsID'
    effectRow = 0
    try:
        conn = myConn.connect(**config)
        cursor = conn.cursor()
        if listLen >= 1:
            for li in valuesList:
                valuesTuple = li
                cursor.execute(insertSql, valuesTuple)
                effectRow = effectRow + 1
            print("mysql插入完成，受影响行数：{}".format(effectRow))
            cursor.execute(dltReptSql)
            effectRow = cursor.rowcount
            print("mysql删除重复记录完成，受影响行数：{}".format(effectRow))
    except myConn.Error as e:
        print("connect fails! {}".format(e))
        print(traceback.format_exc())
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def selectTable(sql):
    try:
        conn = myConn.connect(**config)
        cursor = conn.cursor()
        selectSql = sql
        cursor.execute(selectSql)
        values = cursor.fetchall()
        return values
    except myConn.Error as e:
        print("connect fails! {}".format(e))
        print(traceback.format_exc())
    finally:
        cursor.close()
        conn.close()

def run_Create_toutiao():
    tb_name = 'tb_toutiao'
    autoUpNum = 0
    priKeyNum = 1
    columns = ['num', 'NewsID', 'title', 'url', 'source', 'commentNum', 'NewsDate']
    colsType = ['INT AUTO_INCREMENT PRIMARY KEY', 'VARCHAR(20)', 'VARCHAR(100)', 'VARCHAR(50)', 'VARCHAR(20)',
                'INT', 'DATE']
    args = [columns, colsType]
    createTable(tb_name, *args)

def run_Create_wukong():
    tb_name = 'tb_wukong'
    autoUpNum = 0
    priKeyNum = 1
    columns = ['num', 'NewsID', 'url','keyword', 'title', 'replyNum', 'collectNum','likeNum','commentNum']
    colsType = ['INT AUTO_INCREMENT PRIMARY KEY', 'VARCHAR(20)', 'VARCHAR(50)', 'VARCHAR(10)', 'VARCHAR(100)','INT','INT','INT','INT']
    args = [columns, colsType]
    createTable(tb_name, *args)

# 判断一个数字是否为小数
def is_float(str):
    if str.count('.') == 1: #小数有且仅有一个小数点
        left = str.split('.')[0]  #小数点左边（整数位，可为正或负）
        right = str.split('.')[1]  #小数点右边（小数位，一定为正）
        lright = '' #取整数位的绝对值（排除掉负号）
        if str.count('-') == 1 and str[0] == '-': #如果整数位为负，则第一个元素一定是负号
            lright = left.split('-')[1]
        elif str.count('-') == 0:
            lright = left
        else:
            # print('%s 不是小数'%str)
            return False
        if right.isdigit() and lright.isdigit(): #判断整数位的绝对值和小数位是否全部为数字
            # print('%s 是小数'%str)
            return True
        else:
            # print('%s 不是小数'%str)
            return False
    else:
        # print('%s 不是小数'%str)
        return False

def run_Select():
    tb_name = 'tb_toutiao'
    sqlAll = 'SELECT * FROM tb_toutiao'
    sqlCount = 'SELECT COUNT(*) FROM tb_toutiao'
    sqlComment = 'SELECT commentNum FROM tb_toutiao'
    NewsNum = selectTable(sqlCount)
    values = selectTable(sqlAll)
    comment = selectTable(sqlComment)
    for li in comment:
        if is_float(li[0]):
            print(li)

    print("查询结束，共 {} 条记录".format(NewsNum[0][0]))


if __name__ == '__main__':
    run_Create_toutiao()
    # run_Select()
    # run_Select()