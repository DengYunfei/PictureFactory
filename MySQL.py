import datetime

import pymysql


def MySQL(sql):
    host = 'feifei.iask.in'
    port = 3306
    user = 'root'
    passwd = 'feiyang411'
    dbName = 'Picture_Factory'
    print('sql=', sql)
    # 创建数据链接
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=dbName)
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute(sql)

    cursor.connection.commit()
    result = cursor.fetchall()
    return result
    cursor.close()
    conn.close()


if __name__ == '__main__':
    # # print(type(time.localtime(time.time())))
    # dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print(dt)
    for a in MySQL('select * from products'):
        print(a)
