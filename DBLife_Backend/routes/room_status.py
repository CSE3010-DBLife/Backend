from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS, cross_origin
import pymysql
import sys
from datetime import datetime
import routes.ConnectDB as ConnectDB

room_status_print = Blueprint('index', __name__)

@room_status_print.route('/show/room_status')
def show_room_status():
    cur = ConnectDB.connect_db().cursor()
    cur.execute("select * from room")
    rows = cur.fetchall()
    room_status = list()

    # 0: 예약 가능
    # 1: 예약됨
    # 2: 외출 중
    # 3: 사용 중
    for row in rows:
        tmp = dict()
        tmp["room_id"] = row[0]
        tmp["room_status"] = row[1]
        room_status.append(tmp)

    cur.close()

    return jsonify(room_status)

@room_status_print.route("/show/reservation_status/<checkin_date>/<checkout_date>", methods=['POST'])
def show_reservation_status(checkin_date, checkout_date):
    cur = ConnectDB.connect_db().cursor()
    cur.execute("select * from reservation")
    rows = cur.fetchall()
    ss = list()
    result = list()

    for row in rows:
        cur.execute(f"select * from reservation_detail where reservation_id = {int(row[0])}")
        dates = cur.fetchall()
        if dates[0][2] == datetime.strptime(checkin_date, "%Y-%m-%d").date() and dates[0][2] == datetime.strptime(checkin_date, "%Y-%m-%d").date():
            ss.append(row[1])

    for s in ss:
        cur.execute(f"select * from room where room_id = {s}")
        rows = cur.fetchall()
        for row in rows:
            tmp = dict()
            tmp["room_id"] = row[0]
            tmp["room_status"] = row[1]
        result.append(tmp)

    cur.close()

    return jsonify(result)

if __name__ == "__main__":
	app.run(host="127.0.0.1", port=80)