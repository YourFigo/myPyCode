import pymysql
import mysql.connector

config = {
    'host': '127.0.0.1',
    'user': 'user',
    'password': 'password',
    'port': 3306,
    'database': 'database',
    'charset': 'utf8'
}

def crePltfmTb():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        crtTbSql = 'create table if not exists platformAccount (name varchar(20) primary key,username varchar(30),password varchar(20))'
        cursor.execute(crtTbSql)

        insertSql = 'replace into platformAccount (name,username,password) values (%s, %s,%s)'
        cursor.execute(insertSql, ('Adview', 'xxx', 'xxx'))
        cursor.execute(insertSql, ('AOL', 'xxx', 'xxx'))
        cursor.execute(insertSql, ('cm', 'xxx', 'xxx'))
        cursor.execute(insertSql, ('Mobfox', 'xxx', 'xxx'))
        cursor.execute(insertSql, ('Mopub', 'xxx', 'xxx'))
        cursor.execute(insertSql, ('NewCM', 'xxx', 'xxx'))
        cursor.execute(insertSql, ('OpenX', 'xxx', 'xxx'))
        cursor.execute(insertSql, ('Pubnative', 'xxx', 'xxx'))
        cursor.execute(insertSql, ('Smaato', 'xxx', 'xxx'))
        cursor.execute(insertSql, ('Solo', 'xxx', 'xxx'))
        cursor.execute(insertSql, ('Tappx', 'xxx', 'xxx'))

        print("mysql表格创建完成---------")
        conn.commit()
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
    finally:
        cursor.close()
        conn.close()

def selectFromTb(item):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        selectOneSql = 'select * from platformAccount where name = %s'
        selectAllSql = 'select * from platformAccount'
        cursor.execute(selectOneSql,(item,))
        values = cursor.fetchall()
        # print(values[0][1],values[0][2])
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))
    finally:
        cursor.close()
        conn.close()
        return values[0][1],values[0][2]

if __name__ == '__main__':
    username,password = selectFromTb('Adview')
    print(username)
    print(password)