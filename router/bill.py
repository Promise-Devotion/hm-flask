from functools import reduce

from flask import Flask, request, Blueprint

billlist = Blueprint('bill-list', __name__)
billtask = Blueprint('bill-task', __name__)


@billlist.route('/bill-list', methods=['GET'])
def bill_list():
    if request.method == 'GET':
        return [{'id': '123', 'name': 'task1'}]
    else:
        return []


@billtask.route('/bill-task', methods=['GET', 'POST', 'DELETE'])
def bill_task():
    if request.method == 'POST':
        return '新增一条数据'
    elif request.method == 'DELETE':
        taskid = request.args["id"]
        return f'删除{taskid}'
    else:
        taskid: str = request.args["id"]
        return f'查询数据{taskid}'
