from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from routes.employ import employ_print
from routes.room_status import room_status_print
from routes.room_status_detail import room_status_detail
from routes.parking import parking
import pymysql
import sys


app = Flask(__name__)
cors = CORS(app)
app.config['JSON_AS_ASCII'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

# ------------------------------------------------------
app.register_blueprint(employ_print)
app.register_blueprint(room_status_print)
app.register_blueprint(room_status_detail)
app.register_blueprint(parking)
# ------------------------------------------------------

@app.route('/')
@cross_origin()
def hello():
    return "Hello"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug = True)