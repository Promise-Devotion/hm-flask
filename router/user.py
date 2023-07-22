import json
import pprint
import time

from flask import request
from flask import Blueprint
from flask import jsonify
from common.md5_operate import get_md5

from config import SQLManager
# from flask_restful import Resource, Api
from db import update_data
from redis_common.redis_client import redis_db

userapi = Blueprint('user', __name__)


@userapi.route('/user', methods=['POST', 'GET', 'PUT', 'DELETE'])
def user():
    if request.method == 'GET':
        sql = ''
        person_id = request.args.get('id')
        if person_id:
            sql = f"SELECT first_name AS firstname, last_name AS lastname, email AS email, nick_name AS nickname, user_id AS userid, sex AS sex FROM t_user WHERE user_id={person_id}"
        else:
            sql = "SELECT first_name AS firstname, last_name AS lastname, email AS email, nick_name AS nickname, user_id AS userid, sex AS sex FROM t_user"
        db = SQLManager()
        datas = db.get_list(sql)
        db.close()
        if len(datas) > 1:
            response = jsonify({'code': 200, 'data': datas, "message": "查询成功!"})
        else:
            response = jsonify({'code': 200, 'data': datas[0], "message": "查询成功!"})
        # response = jsonify(datas)
        return response
    elif request.method == 'POST':
        get_data = request.form.to_dict()
        request_form = get_data
        print(get_data)

        person_id = request_form['id']
        last_name = request_form['lastname']
        first_name = request_form['firstname']
        sex = request_form['sex']
        email = request_form['email']
        password = request_form['password']
        nick_name = request_form['nickname']
        sql = f"""
        INSERT INTO t_user (user_id, last_name, first_name, nick_name, sex, email, user_password)
        VALUES ({person_id}, '{last_name}', '{first_name}', '{nick_name}', {sex}, '{email}', '{password}')
        """
        db = SQLManager()
        datas = db.create(sql)
        db.close()
        response = jsonify({"code": 200, "data": datas, "message": "操作成功"})
        return response
    elif request.method == 'PUT':
        return 'PUT'
    elif request.method == 'DELETE':
        person_id = request.args.get('id')
        sql = f"DELETE FROM t_user WHERE user_id={person_id}"
        datas = update_data(sql)
        return datas
    else:
        return 'error'


@userapi.route("/login", methods=["post"])
def user_login():
    """登录用户"""
    email = request.values.get("email", "").strip()
    password = request.values.get("password", "").strip()
    if email and password:  # 注意if条件中空串 "" 也是空, 按False处理
        sql1 = "SELECT email FROM t_user WHERE email = '{}'".format(email)
        db = SQLManager()
        res1 = db.get_list(sql1)
        print("查询到用户名 ==>> {}".format(res1))
        if not res1:
            db.close()
            return jsonify({"code": 1003, "msg": "用户不存在！！！"})
        md5_password = get_md5(email, password)  # 把传入的明文密码通过MD5加密变为密文
        sql2 = "SELECT * FROM t_user WHERE email = '{}' and user_password = '{}'".format(email, password)
        res2 = db.get_list(sql2)
        db.close()
        print("获取 {} 用户信息 == >> {}".format(email, res2))
        if res2:
            time_stamp = int(time.time())  # 获取当前时间戳
            # token = "{}{}".format(username, timeStamp)
            # username = res2[0].username
            token = get_md5(email, str(time_stamp))  # MD5加密后得到token
            redis_db.handle_redis_token(email, token)  # 把token放到redis中存储
            data = {  # 构造一个字段，将 id/username/token/login_time 返回
                "id": res2[0]["user_id"],
                "email": email,
                # "username": username,
                "token": token,
                "login_time": time.strftime("%Y/%m/%d %H:%M:%S")
            }
            return jsonify({"code": 200, "login_info": data, "message": "恭喜，登录成功！"})
        return jsonify({"code": 1002, "message": "用户邮箱或密码错误！！！"})
    else:
        return jsonify({"code": 1001, "message": "用户邮箱或密码不能为空！！！"})
