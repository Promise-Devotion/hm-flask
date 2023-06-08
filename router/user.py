import json
import pprint

from flask import request, Blueprint, jsonify
# from flask_restful import Resource, Api
from db import query_data, update_data


userapi = Blueprint('user', __name__)


@userapi.route('/user', methods=['POST', 'GET', 'PUT', 'DELETE'])
def user():
    if request.method == 'GET':
        sql = ''
        person_id = request.args.get('id')
        if person_id:
            sql = f"SELECT * FROM Persons WHERE PersonID={person_id}"
        else:
            sql = "SELECT * FROM Persons"
        datas = query_data(sql)
        if len(datas) > 1:
            response = jsonify({'code': 200, 'data': datas})
        else:
            response = jsonify({'code': 200, 'data': datas[0]})
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
        INSERT INTO Persons (PersonID, LastName, FirstName, NickName, Sex, Email, PASSWORD)
        VALUES ({person_id}, '{last_name}', '{first_name}', '{nick_name}', {sex}, '{email}', '{password}')"""
        datas = update_data(sql)
        return datas
    elif request.method == 'PUT':
        return 'PUT'
    elif request.method == 'DELETE':
        person_id = request.args.get('id')
        sql = f"DELETE FROM Persons WHERE PersonID={person_id}"
        datas = update_data(sql)
        return datas
    else:
        return 'error'

