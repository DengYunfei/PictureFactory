import datetime

import pymysql


def MySQL(sql):
    host = 'feifei.iask.in'
    port = 3306
    user = 'root'
    passwd = 'feiyang411'
    dbName = 'Picture_Factory'

    # 创建数据链接
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=dbName)
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    cursor.execute(sql)

    result = cursor.fetchall()

    return result
    cursor.close()
    conn.close()


if __name__ == '__main__':
    # print(type(time.localtime(time.time())))
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(dt)
    MySQL(
        "INSERT INTO client ( studio_id,client_name,product_count,date_created)VALUES(%d,'%s',%d,str_to_date('%s','%%Y-%%m-%%d %%H:%%i:%%s'))" % (
            1, 'asd', 10, dt))
    print(MySQL('select * from client order by client_id desc limit 1'))
