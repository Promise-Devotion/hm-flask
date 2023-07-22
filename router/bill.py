from functools import reduce

from flask import Flask
from flask import request
from flask import Blueprint
from flask import jsonify
from pre_request import Rule
from config import SQLManager


billlist = Blueprint('bill-list', __name__)
billtask = Blueprint('bill-task', __name__)


@billlist.route('/bill-list', methods=['GET'])
def bill_list():
    if request.method == 'GET':
        user_id = request.args.get('id')
        sql = f'''
        SELECT user_id AS userid, bill_id AS billid, create_time AS createtime, 
        update_time AS updatetime, bill_name AS billname, bill_amount AS billamount, 
        bill_remark AS billremark, bill_type AS billtype, bill_status AS billstatus 
        FROM t_bill 
        WHERE user_id = {user_id}
        '''
        db = SQLManager()
        datas = db.get_list(sql)
        db.close()
        response = jsonify({'code': 200, 'data': datas, "message": "查询成功!"})
        print(response)
        return response


rule = {
    "billname": Rule(type=str, required=True, gte=3, lte=20, dest="billname"),
    "billamount": Rule(type=int, required=True, gte=0, lte=999999),
    "billtype": Rule(type=int, required=True, gte=2, default="0")
}


@billtask.route('/bill-task', methods=['GET', 'POST', 'DELETE'])
def bill_task():
    if request.method == 'POST':

        request_data = request.json
        print(request_data.get('createtime'))
        sql = f'''
        INSERT INTO t_bill (user_id, bill_id, create_time,update_time, bill_status, bill_amount,bill_name, bill_remark, bill_type)
        VALUES ({repr(request_data.get('userid'))}, {repr(request_data.get('billid'))}, {repr(request_data.get('createtime'))}, {repr(request_data.get('updatetime'))}, {request_data.get('billstatus')}, {request_data.get('billamount')}, {repr(request_data.get('billname'))}, {repr(request_data.get('billremark'))}, {request_data.get('billtype')});'''
        db = SQLManager()
        datas = db.create(sql)
        db.close()
        response = jsonify({"code": 200, "data": datas, "message": "操作成功"})
        return response
    elif request.method == 'DELETE':
        bill_id = request.args["id"]
        print(bill_id)
        sql = f'''
        DELETE FROM t_bill WHERE bill_id = {bill_id}
        '''
        db = SQLManager()

        datas = db.moddify(sql)
        db.close()
        response = jsonify({'code': 200, 'data': datas})
        return response
    else:
        bill_id: str = request.args.get("id")
        sql = f"""
        SELECT * FROM t_bill WHERE bill_id = {bill_id}
        """
        db = SQLManager()
        datas = db.get_one(sql)
        db.close()
        response = jsonify({'code': 200, 'data': datas, 'message': '操作成功'})
        return response
