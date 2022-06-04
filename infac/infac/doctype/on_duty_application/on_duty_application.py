# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from unicodedata import name
import frappe
import frappe
from frappe.model.document import Document
import frappe,os,base64
import requests
import datetime
import json,calendar
from datetime import datetime,timedelta,date,time
import datetime as dt
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from frappe.desk.notifications import delete_notification_count_for
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today
from frappe import _, set_value


class OnDutyApplication(Document):

	def on_submit(self):
		att = frappe.db.exists('Attendance',{'attendance_date':self.od_date,'employee':self.employee})
		# frappe.errprint(att)
		if att:
			frappe.db.set_value('Attendance',att,'status','Present')
			frappe.db.set_value('Attendance',att,'on_duty_marked',self.name)
			# att_mark = frappe.db.get_value('Attendance',{'employee':self.employee,'attendance_date':self.od_date,'docstatus':1},['status'])
			# frappe.errprint(att_mark)
			# if att_mark:
			# 	frappe.db.set_value('Attendnace',att,'on_duty_marked',self.name)
		# elif att:
		# 	frappe.db.set_value('Attendance',att,'status','Present')
		# 	frappe.db.set_value('Attendance',att,'on_duty_marked',self.name)
		else:
			attendance = frappe.new_doc('Attendance')
			attendance.employee = self.employee	
			attendance.attendance_date = self.od_date
			attendance.status = "Present"
			attendance.on_duty_marked = self.name
			attendance.save(ignore_permissions = True)
			frappe.db.commit()
		
@frappe.whitelist()
def get_time_difference(od_date,in_time,out_time):
	od_date = datetime.strptime(od_date,'%Y-%m-%d')
	in_time = datetime.strptime(in_time,'%H:%M:%S').time()
	out_time = datetime.strptime(out_time,'%H:%M:%S').time()
	in_time = datetime.combine(od_date, in_time)
	out_time = datetime.combine(od_date, out_time)
	hours = out_time - in_time
	# frappe.errprint(total_hours)
	ftr = [3600,60,1]
	hr = sum([a*b for a,b in zip(ftr, map(int,str(hours).split(':')))])
	od_hr = round(hr/3600,1)
	return hours, od_hr
			
			
			

			
		