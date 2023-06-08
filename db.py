import pymysql
import pprint


# 创建连接

def get_conn():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='sophie123456',
        database='huamao',
        charset='utf8'
    )


def query_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


def update_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        conn.commit()
        return '删除成功'
    finally:
        conn.close()


if __name__ == "__main__":
    sql = "SELECT * FROM Persons"
    datas = query_data(sql)
    pprint.pprint(datas)
