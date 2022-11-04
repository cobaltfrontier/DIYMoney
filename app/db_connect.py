import pymysql

def connect():
    connection = pymysql.connect(host='database-1.cj6y4kwxksyv.us-east-1.rds.amazonaws.com',
                                 port=3306,
                                 database='sys',
                                 user='admin',
                                 password='Excalibur789!',
                                 cursorclass=pymysql.cursors.DictCursor)
    print("Connected")
    return connection