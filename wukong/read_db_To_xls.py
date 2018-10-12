# Copyright 2018 Figo Individual. All Rights Reserved.
import sqlite3 as db
import xlwt
# 从SQLite文件中读取数据
def readFronSqllite(db_path,exectCmd):
    conn = db.connect(db_path)  # 该 API 打开一个到 SQLite 数据库文件 database 的链接，如果数据库成功打开，则返回一个连接对象
    cursor=conn.cursor()        # 该例程创建一个 cursor，将在 Python 数据库编程中用到。
    conn.row_factory=db.Row     # 可访问列信息
    cursor.execute(exectCmd)    #该例程执行一个 SQL 语句
    rows=cursor.fetchall()      #该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。
    return rows
    #print(rows[0][2]) # 选择某一列数据

if __name__=="__main__":
    rows = readFronSqllite('C:/Users/Administrator/Desktop/db_wukong.db',"select * from tb_wukong")
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet1 = workbook.add_sheet("悟空问答")
    readLines = rows.__len__()
    lineIndex = 0
    while lineIndex < readLines:
        row = rows[lineIndex]
        cols = row.__len__()
        col = 0
        while col < cols:
            if col == 6:
                worksheet1.write(lineIndex, col, row[col] + "赞")
            elif col == 7:
                worksheet1.write(lineIndex, col, row[col] + "评论")
            else:
                worksheet1.write(lineIndex, col, row[col])
            col += 1
        lineIndex += 1
    workbook.save("C:/Users/Administrator/Desktop/XLS_wukong.xls")