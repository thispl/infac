# Copyright (c) 2024, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days,date_diff
from datetime import date, datetime, timedelta

class LiveAttendance(Document):
	pass

@frappe.whitelist()
def get_data_system():
	nowtime = datetime.now()
	max_out1 = datetime.strptime('05:15', '%H:%M').time()
	max_out2 = datetime.strptime('08:45', '%H:%M').time()
	max_out3 = datetime.strptime('14:45', '%H:%M').time()
	max_out4 = datetime.strptime('17:15', '%H:%M').time()
	
	time = nowtime.strftime("%H:%M:%S")
	date_1 = nowtime.date()
	
	data = "<div style='text-align: center;'>"
	data += "<table class='table table-bordered=1' style='width: 50%; margin: auto;'>"
	data += "<tr style='font-size:10px;padding:2px'><td colspan = 3 style='border: 2px solid black;background-color:#AEB6BF;padding:1px'><b><center>Live Attendance - %s %s</center></b></td></tr>" % (time, date_1)
	data += "<tr style='font-size:10px;padding:2px'><td style='border: 2px solid black;background-color:#AEB6BF;padding:1px'><b><center>Category</center></b></td><td style='border: 2px solid black;background-color:#AEB6BF;padding:1px'><b><center>Shift</center></b></td><td style='border: 2px solid black;background-color:#AEB6BF;padding:1px'><b><center>Count</center></b></td></tr>"
	category = frappe.db.sql("""SELECT * FROM `tabEmployee Category` ORDER BY name""", as_dict=True)
	total = 0
	for c in category:
		if frappe.db.exists("Employee",{'status':"Active",'employee_category':c.name}):
			if nowtime.time() > max_out1:
				date1 = nowtime.date()
				if nowtime.time() < max_out2:
					count = frappe.db.sql("""SELECT COUNT(*) AS count FROM `tabAttendance` 
						WHERE attendance_date = %s 
						AND employee_category = %s
						AND shift = "A"
						AND in_time IS NOT NULL
						AND out_time IS NULL
					""", (date1,c.name), as_dict=True)
					if count:
						count_value = count[0]['count']
						total += count_value
					else:
						count_value = 0
						total += count_value
					data += "<tr style='font-size:10px;padding:2px'><td style='border: 2px solid black;padding:1px'><b>%s</b></td><td style='border: 2px solid black;padding:1px'><b><center>A</center></b></td><td style='border: 2px solid black;padding:1px'><b><center>%s</center></b></td></tr>" % (c.name,count_value)
				elif nowtime.time() > max_out2 and nowtime.time() < max_out3:
					count1 = frappe.db.sql("""SELECT COUNT(*) AS count FROM `tabAttendance` 
						WHERE attendance_date = %s 
						AND employee_category = %s
						AND shift = "A"
						AND in_time IS NOT NULL
						AND out_time IS NULL
					""", (date1,c.name), as_dict=True)
					count2 = frappe.db.sql("""SELECT COUNT(*) AS count FROM `tabAttendance` 
						WHERE attendance_date = %s 
						AND employee_category = %s
						AND shift = "G"
						AND in_time IS NOT NULL
						AND out_time IS NULL
					""", (date1,c.name), as_dict=True)
					if count1:
						count_value1 = count1[0]['count']
						total += count_value1
					else:
						count_value1 = 0
						total += count_value1
					if count2:
						count_value2 = count2[0]['count']
						total += count_value2
					else:
						count_value2 = 0
						total += count_value2

					data += "<tr style='font-size:10px;padding:2px'><td rowspan = 2 style='border: 2px solid black;padding:1px'><b>%s</b></td><td style='border: 2px solid black;padding:1px'><b><center>A</center></b></td><td style='border: 2px solid black;padding:1px'><b><center>%s</center></b></td></tr>" % (c.name,count_value1)
					data += "<tr style='font-size:10px;padding:2px'><td style='border: 2px solid black;padding:1px'><b><center>G</center></b></td><td style='border: 2px solid black;padding:1px'><b><center>%s</center></b></td></tr>"%(count_value2)
				elif nowtime.time() > max_out3 and nowtime.time() < max_out4:
					count1 = frappe.db.sql("""SELECT COUNT(*) AS count FROM `tabAttendance` 
						WHERE attendance_date = %s 
						AND employee_category = %s
						AND shift = "B"
						AND in_time IS NOT NULL
						AND out_time IS NULL
					""", (date1,c.name), as_dict=True)
					count2 = frappe.db.sql("""SELECT COUNT(*) AS count FROM `tabAttendance` 
						WHERE attendance_date = %s 
						AND employee_category = %s
						AND shift = "G"
						AND in_time IS NOT NULL
						AND out_time IS NULL
					""", (date1,c.name), as_dict=True)
					if count1:
						count_value1 = count1[0]['count']
						total += count_value1
					else:
						count_value1 = 0
						total += count_value1
					if count2:
						count_value2 = count2[0]['count']
						total += count_value2
					else:
						count_value2 = 0
						total += count_value2
					data += "<tr style='font-size:10px;padding:2px'><td rowspan = 2 style='border: 2px solid black;padding:1px'><b>%s</b></td><td style='border: 2px solid black;padding:1px'><b><center>B</center></b></td><td style='border: 2px solid black;padding:1px'><b><center>%s</center></b></td></tr>" % (c.name,count_value1)
					data += "<tr style='font-size:10px;padding:2px'><td style='border: 2px solid black;padding:1px'><b><center>G</center></b></td><td style='border: 2px solid black;padding:1px'><b><center>%s</center></b></td></tr>"%(count_value2)
				elif nowtime.time() > max_out4:
					count = frappe.db.sql("""SELECT COUNT(*) AS count FROM `tabAttendance` 
						WHERE attendance_date = %s 
						AND employee_category = %s
						AND shift = "B"
						AND in_time IS NOT NULL
						AND out_time IS NULL
					""", (date1,c.name), as_dict=True)
					if count:
						count_value = count[0]['count']
						total += count_value
					else:
						count_value = 0
						total += count_value
					data += "<tr style='font-size:10px;padding:2px'><td style='border: 2px solid black;padding:1px'><b>%s</b></td><td style='border: 2px solid black;padding:1px'><b><center>B</center></b></td><td style='border: 2px solid black;padding:1px'><b><center>%s</center></b></td></tr>" % (c.name,count_value)
			else:
				date1 = (nowtime - timedelta(days=1)).date()
				count = frappe.db.sql("""SELECT COUNT(*) AS count FROM `tabAttendance` 
					WHERE attendance_date = %s 
					AND employee_category = %s
					AND shift = "C"
					AND in_time IS NOT NULL
					AND out_time IS NULL
				""", (date1,c.name), as_dict=True)
				if count:
					count_value = count[0]['count']
					total += count_value
				else:
					count_value = 0
					total += count_value
				data += "<tr style='font-size:10px;padding:2px'><td style='border: 2px solid black;padding:1px'><b>%s</b></td><td style='border: 2px solid black;padding:1px'><b><center>C</center></b></td><td style='border: 2px solid black;padding:1px'><b><center>%s</center></b></td></tr>" % (c.name,count_value)
	data += "<tr style='font-size:10px;padding:2px'><td colspan = 2 style='border: 2px solid black;padding:1px'><b>Total</b></td><td style='border: 2px solid black;padding:1px'><b><center>%s</center></b></td></tr>" % (total)
	data += "</table>"
	return data
