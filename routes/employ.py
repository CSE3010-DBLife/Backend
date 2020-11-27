from flask import request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
import routes.ConnectDB as ConnectDB


employ_print = Blueprint('employ_print', __name__)


@employ_print.route('/show/employ')
def get_all_employ():
    conn = ConnectDB.connect_db()
    cur = conn.cursor()
    result = list()
    cur.execute("Select employ_id,employ_name,employ_status from employ")
    data = cur.fetchall()
    for x in data:
        employee = dict()
        employee['employ_id'] = x[0]
        employee['employ_name'] = x[1]
        employee['employ_status'] = x[2]
        result.append(employee)
    return jsonify(result)


@employ_print.route('/show/employ/<employ_id>')
def get_employ(employ_id):
    conn = ConnectDB.connect_db()
    cur = conn.cursor()
    result = dict()
    cur.execute(f"Select employ_id, room_id, employ_status, employ_name,\
            role, phone_num from employ where employ_id = {employ_id}")
    data = cur.fetchall()
    result['employ_id'] = data[0][0]
    result['room_id'] = data[0][1]
    result['employ_status'] = data[0][2]
    result['employ_name'] = data[0][3]
    result['role'] = data[0][4]
    result['phone_num'] = data[0][5]

    return jsonify(result)


def get_id():
    conn = ConnectDB.connect_db()
    cur = conn.cursor()
    cur.execute("Select employ_id from employ order by employ_id asc")
    data = cur.fetchall()
    newid = 0
    for i in range(0, len(data)):
        if data[i][0] != i+1:
            newid = i+1
            break
    if newid == 0:
        newid = len(data)+1
    print(newid)
    return newid


@employ_print.route('/add/employ', methods=['POST'])
@cross_origin()
def add_employ():
    conn = ConnectDB.connect_db()
    cur = conn.cursor()
    data = request.get_json()
    employ_id = get_id()
    room_id = 101
    employ_pw = data['employ_pw']
    employ_name = data['employ_name']
    role = data['role']
    salary = data['salary']
    phone_code = data['phone_code']
    phone_num = data['phone_num']
    address_detail = data['address_detail']
    zone_no = data['zone_no']
    build_manage_no = data['build_manage_no']
    employ_status = 0
    park_id = 0

    check = cur.execute(f"insert into employ values ({employ_id},{room_id},\
        '{employ_pw}','{employ_name}','{role}',{salary},\
        '{phone_code}','{phone_num}','{address_detail}','{zone_no}',\
        '{build_manage_no}','{employ_status}',{park_id})")

    conn.commit()
    if check:
        return jsonify(result=200)
    return jsonify(result=401)


@employ_print.route('/update/employ/status/<employ_id>', methods=['POST'])
@cross_origin()
def update_employstatus(employ_id):
    conn = ConnectDB.connect_db()
    cur = conn.cursor()
    
    data = request.get_json()
    employ_status = data['employ_status']
    check = cur.execute(f"update employ set employ_status = '{employ_status}'\
    where employ_id = {employ_id}")

    conn.commit()

    if check:
        return jsonify(result=200)
    return jsonify(result=401)


# 원래 주차된 곳을 NULL로 만들고 새로 주차된 곳 업데이트
@employ_print.route('/update/employ/park_id/<employ_id>', methods=['POST'])
@cross_origin()
def update_employcar(employ_id):
    conn = ConnectDB.connect_db()
    data = request.get_json()
    park_id = data['park_id']
    car_id = data['car_id']
    
    cur = conn.cursor()
    cur.execute(f"select park_id from employ where employ_id = {employ_id}")
    car_num = cur.fetchall()[0][0]
    
    cur = conn.cursor()
    check1 = cur.execute(f"update employ set park_id = {park_id}\
    where employ_id = {employ_id}")

    cur = conn.cursor()
    check2 = cur.execute(f"update parking set car_id = '{car_id}' \
    where park_id = {park_id}")
    
    
    if(car_num != 0):
        cur.execute(f"update parking set car_id = NULL\
        where park_id = {car_num}")
        
    conn.commit()

    if check1 and check2:
        return jsonify(result=200)
    return jsonify(result=401)


@employ_print.route('/delete/employ/<employ_id>', methods=['POST'])
@cross_origin()
def delete_employ(employ_id):
    conn = ConnectDB.connect_db()
    
    cur = conn.cursor()
    cur.execute(f"select park_id from employ where employ_id = {employ_id}")
    car_num = cur.fetchall()[0][0]
    
    if(car_num != 0):
        cur.execute(f"update parking set car_id = NULL\
        where park_id = {car_num}")
    
    cur = conn.cursor()
    check = cur.execute(f"delete from employ where employ_id = {employ_id}")
    conn.commit()
    
    if check:
        return jsonify(result=200)
    return jsonify(result=401)


