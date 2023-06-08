from functools import reduce

from flask import Flask, request, Blueprint

billlist = Blueprint('billlist', __name__)
billtask = Blueprint('billtask', __name__)


@billlist.route('/billlist', methods=['GET'])
def bill_list():
    if request.method == 'GET':
        return billlist
    else:
        return []


@billtask.route('/billtask', methods=['GET', 'POST', 'DELETE'])
def bill_task():
    if request.method == 'POST':
        return '新增一条数据'
    elif request.method == 'DELETE':
        id = request.args["id"]
        return f'删除{id}'
    else:
        id = request.args["id"]
        return f'查询数据{id}'
