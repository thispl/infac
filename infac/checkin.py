# import mysql.connector
# from frappeclient import FrappeClient
# import requests,json
# from datetime import date
# from datetime import time


# mydb = mysql.connector.connect(
# host="localhost",
# user="root",
# passwd="Pa55w0rd@",
# database="easytimepro"
# )

# mycursor = mydb.cursor(dictionary=True)
# client = FrappeClient("http://172.16.1.47", "Administrator", "1234@Mpl")
# query = "SELECT id,emp_code as biometric_pin,punch_time as log_time,terminal_alias as log_type,date(punch_time) as log_date,checkin_marked FROM `iclock_transaction` where emp_code is not null and checkin_marked = '0' "
# mycursor.execute(query)
# devicelog = mycursor.fetchall()
# if devicelog:
#     if client:
#         for d in devicelog:
#             if d["biometric_pin"]:
#                 employee = client.get_value("Employee","name",{"biometric_pin": d["biometric_pin"]})
#                 if employee:
#                     time = str(d["log_time"])
#                     check = client.get_value("Employee Checkin",{"biometric_pin": d["biometric_pin"],"time":time})
#                     if not check:
#                         doc = {"doctype":"Employee Checkin"}
#                         doc["log_date"] = str(d["log_date"])
#                         doc["biometric_pin"] = str(d["biometric_pin"])
#                         doc["employee"] = employee['name']
#                         doc["time"] = str(d["log_time"])
#                         if d["log_type"] in ('P1 IN','P2 IN','SPIC'):
#                             doc['log_type'] = 'IN'
#                         elif d["log_type"] in ('P1 OUT','P2 OUT'):
#                             doc['log_type'] = 'OUT'
#                         doc['device_area'] = str(d["log_type"])
#                         client.insert(doc)
#                         update_query = "update `iclock_transaction` set checkin_marked='1' where id = %s" % str(d["id"])
#                         mycursor.execute(update_query)
#                         mydb.commit()
#                     else:
#                         update_query = "update `iclock_transaction` set checkin_marked='1' where id = %s" % str(d["id"])
#                         mycursor.execute(update_query)
#                         mydb.commit()
