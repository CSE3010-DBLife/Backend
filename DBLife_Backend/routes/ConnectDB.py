import pymysql
import sys

def connect_db():
    try:
        conn = pymysql.connect(
        user = "root",
        password = "dblife3010good119!",
        host = "foolminecraft.iptime.org",
        port = 6605,
        database = "Bhotel"
        )
        return conn
    
    except pymysql.Error as e:
        print(f"Error connecting to MariaDB Platform: {e} ")
        sys.exit(1)