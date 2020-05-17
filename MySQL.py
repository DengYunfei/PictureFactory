
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
    for a in MySQL('select `client`.`client_name` AS `client_name`,`products`.`product_size` AS `product_size`,`products`.`product_style` AS `product_style`,`products`.`product_type` AS `product_type`,`products`.`date_created` AS `date_created`,`products`.`pic_count` AS `pic_count` from (`products` join `client` on((`products`.`client_id` = `client`.`client_id`)))'):

        format_date = str(a.get('date_created').year) + "-" + str(a.get('date_created').month) + "-" + str(a.get('date_created').day)
        print(format_date)

