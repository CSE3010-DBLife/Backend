from flask import Flask, request, jsonify, Blueprint,abort
from flask_cors import CORS, cross_origin
import pymysql
import sys
import routes.ConnectDB as ConnectDB

parking = Blueprint('parking', __name__)

@parking.route('/parking')
def parking_status():

    cur = ConnectDB.connect_db().cursor()
    cur.execute("Select count(car_id) from parking ")
    summary = cur.fetchone()
    result = list()
    status = dict()
    status['parking status'] = summary[0]
    result.append(status)

    return jsonify(result)


@parking.route('/parking/<car_id>/')
def car_num_inquiry(car_id):
    conn = ConnectDB.connect_db()
    cur = conn.cursor()
    
    cur.execute(f"Select park_id from parking where car_id = '{car_id}'")
    park_data = cur.fetchone()
    park_id = park_data[0]
    
    cur = conn.cursor()
    cur.execute("Select * from customer where park_id = " + str(park_id))
    cus_data = cur.fetchone()
    if(cus_data == None):
        cur = conn.cursor()
        cur.execute("Select employ_name,employ_id,role from employ where park_id = "+str(park_id))
        employ_data = cur.fetchone()
        if(employ_data == None):
            abort(404) 
        employ_name = employ_data[0]
        employ_id = employ_data[1]
        employ_role = employ_data[2]

        result = list()
        dic = dict()

        dic['employ_name'] = employ_name
        dic['car_id'] = car_id
        dic['employ_id'] = employ_id
        dic['employ_role'] = employ_role
        result.append(dic)
        return jsonify(result)
    else:
        cur = conn.cursor()
        cur.execute("Select customer_id,name from customer where park_id = "+str(park_id))
        cus_data = cur.fetchone()
        cus_id = cus_data[0]
        cus_name = cus_data[1]

        cur = conn.cursor()
        cur.execute("Select reservation_id,room_id from reservation "
                    "where customer_id = " + str(cus_id))
        reserve_data = cur.fetchone()
        reserve_id = reserve_data[0]
        room_id = reserve_data[1]

        cur = conn.cursor()
        cur.execute("Select valid_date from reservation_detail"
                    " where reservation_id = "+str(reserve_id))
        reserve_date = cur.fetchall()
        check_in_date = reserve_date[0]
        check_out_date = reserve_date[-1]

        result = list()
        dic = dict()

        dic['cus_name'] = cus_name
        dic['car_id'] = car_id
        dic['room_id'] = room_id
        dic['check_in_date'] = check_in_date
        dic['check_out_date'] = check_out_date
        result.append(dic)
        return jsonify(result)
                    
                    