from flask import jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
import pymysql
import routes.ConnectDB as ConnectDB


room_status_detail = Blueprint('room_status_detail', __name__)





@room_status_detail.route('/show/room_status/detail/<room_id>') # ex) room_id = 101  (101 호)
@cross_origin()
def getRoomdetail(room_id):
	cur = ConnectDB.connect_db().cursor()
	result = []

	#find room status and request
	cur.execute("Select reservation_status,type_id,request from room where room_id =" + str(room_id))
	rows = cur.fetchone()
	if rows == None:
		status = None
		room_type = None
		resquest = None
		abort(404)
	else:
		status = rows[0]
		room_type = rows[1]
		request = rows[2]
		if status == 0:
			cur.execute(f"Select type_id, size, price from type where type_id = '{room_type}'")
			no_res_row = cur.fetchone()
			return jsonify({"room_detail_type": no_res_row[0],
							"room_detail_size": no_res_row[1],
							"room_detail_price": no_res_row[2],
				})

	#find reservation_id, customer_id, adults number and children number
	cur.execute("Select reservation_id, customer_id,adults,children from reservation where room_id = " + str(room_id))
	rows = cur.fetchone()

	if rows == None:
		reservation = None
		customer = None
		adults = None
		children = None
	else:
		reservation = rows[0]
		customer = rows[1]
		adults = rows[2]
		children = rows[3]
	
	

	#find duration
	if reservation == None:
		duration = None
	else:
		cur.execute("Select valid_date from reservation_detail where reservation_id = " + str(reservation) + " order by valid_date asc")
		rows = cur.fetchall()

		if len(rows)==1:
			duration = str(rows[0][0])
		else:
			durationfirst = rows[0][0]
			durationlast = rows[len(rows)-1][0]
			duration = str(durationfirst) + " ~ " + str(durationlast)


	#find phone, name and full_address
	if customer == None:
		phone = None
		name = None
		zone_no = None
		build_manage_no = None
		address_detail = None
	else:
		cur.execute("Select phone_num, name, zone_no, build_manage_no, address_detail from customer where customer_id = " + str(customer))
		rows = cur.fetchone()

		phone = rows[0]
		name = rows[1]
		zone_no = rows[2]
		build_manage_no = rows[3]
		address_detail = rows[4]
		



	#find full_address

	if zone_no == None or build_manage_no == None:
		full_address = None
	else:
		cur.execute(f"Select CTPRVN,SIGNGU,RN from ZIPDB where zone_no = '{zone_no}' and  BULD_MANAGE_NO= '{build_manage_no}'")
		rows = cur.fetchone()
		full_address = rows[0] + " " + rows[1] + " " + rows[2] + " " +str(address_detail)

	#find car id

	if customer == None:
		park_id = None
		car_id = None
	else:
		cur.execute("Select park_id from customer where customer_id = " + str(customer))
		rows = cur.fetchone()
		park_id = rows[0]
		cur.execute("Select car_id from parking where park_id = " + str(park_id))
		rows = cur.fetchone()
		car_id = rows[0]


	#find room_type to make room_detail
	if room_type == None:
		size = None
		price = None
		room_detail = None
	else:
		cur.execute("select * from type where type_id = %s", room_type)
		rows = cur.fetchone()

		room_type_id = rows[0]
		size = rows[1]
		price = rows[2]


	return jsonify({"status": status, "duration" :duration, "car_id": car_id, "full_address":full_address,
					"phone" : phone, "name": name, "adults": adults, "children": children,
					"room_detail_size": size, "room_detail_type": room_type_id, "room_detail_price": price, "request": request})