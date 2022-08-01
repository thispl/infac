# Copyright (c) 2021, teampro and contributors
# For license information, please see license.txt

from types import FrameType
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
from frappe import _


class PermissionRequest(Document):

	def on_submit(self):
		att = frappe.db.exists('Attendance',{'attendance_date':self.permission_date,'employee':self.employee_id})
		if att:
			frappe.db.set_value('Attendance',att,'permission_request',self.name)
			frappe.db.set_value('Attendance',att,'status','Present')
		#Title of the Function Employee Late Deduct
		late_punch = frappe.db.get_value('Attendance',{'attendance_date':self.permission_date,'employee':self.employee_id},['in_time'])
		in_time = datetime.strptime(str(late_punch),'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
		permission_to_time = datetime.strptime(str(self.to_time),'%H:%M:%S').strftime('%H:%M:%S')
		if in_time < permission_to_time:
			frappe.db.set_value('Attendance',att,'late_hours','00:00')
			frappe.db.set_value('Attendance',att,'late_hrs','')
			frappe.db.set_value('Attendance',att,'late_deduct','00:00')
		else:	
			late_deduct = frappe.db.get_value('Attendance',{'attendance_date':self.permission_date,'employee':self.employee_id},['late_hours'])
			if late_deduct:
				late_hr = datetime.strptime(str(late_deduct),'%H:%M:%S')
				perm_hour = datetime.strptime(str(self.hours),'%H:%M:%S')
				total_late = late_hr - perm_hour
				frappe.db.set_value('Attendance',att,'late_hours',total_late)
				if total_late :
					late_deduct_hour = total_late.seconds//3600
					late_deduct_minute = ((total_late.seconds//60)%60)
					deducted_minute = late_deduct_minute
					deducted_hour = late_deduct_hour
					if late_deduct_minute >= 1 and late_deduct_minute <= 5:
						deducted_minute = 5
					elif late_deduct_minute >= 6  and late_deduct_minute <=10:
						deducted_minute = 10
					elif late_deduct_minute >= 11 and late_deduct_minute <= 15:
						deducted_minute = 15
					elif late_deduct_minute >= 16 and late_deduct_minute <= 20:
						deducted_minute = 20
					elif late_deduct_minute >= 21 and late_deduct_minute <= 25:
						deducted_minute = 25
					elif late_deduct_minute >= 26 and late_deduct_minute <= 30:
						deducted_minute = 30
					elif late_deduct_minute >= 31 and late_deduct_minute <= 35:
						deducted_minute = 35
					elif late_deduct_minute >= 36 and late_deduct_minute <= 40:
						deducted_minute = 40
					elif late_deduct_minute >= 41 and late_deduct_minute <= 45:
						deducted_minute = 45
					elif late_deduct_minute >= 46 and late_deduct_minute <= 50:
						deducted_minute = 50 
					elif late_deduct_minute >= 51 and late_deduct_minute <= 55:
						deducted_minute = 55    
					elif late_deduct_minute >= 56 and late_deduct_minute <= 60:
						deducted_hour = late_deduct_hour +1
						deducted_minute = 00
					late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute)+':00'
					time = datetime.strptime(str(late_deducted_time),'%H:%M:%S')
					tm = time.strftime('%H:%M')
					frappe.db.set_value('Attendance',att,'late_deduct',tm)

		



	def validate(self):
		per_req = frappe.db.exists('Permission Request',{'permission_date':self.permission_date,'employee_id':self.employee_id,'name':('!=',self.name)})
		if per_req:
			frappe.throw('Permission Date Already Applied')	

#This is the Permission Validation of 2 Hours Each Employee
# @frappe.whitelist()
# def to_time(from_time):
# 	time = datetime.strptime(from_time,'%H:%M:%S')
# 	to_time = timedelta(hours=2)+ time
# 	return str(to_time.time())

#This is the time difference between from and to time
@frappe.whitelist()
def get_time_difference(permission_date,from_time,to_time):
	permission_date = datetime.strptime(permission_date,'%Y-%m-%d')
	from_time = datetime.strptime(from_time,'%H:%M:%S').time()
	to_time = datetime.strptime(to_time,'%H:%M:%S').time()
	from_time = datetime.combine(permission_date, from_time)
	to_time = datetime.combine(permission_date, to_time)
	total_hours = to_time - from_time
	ftr = [3600,60,1]
	hr = sum([a*b for a,b in zip(ftr, map(int,str(total_hours).split(':')))])
	perm_hr = round(hr/3600,1)
	return total_hours, perm_hr
 
# This is the late deduct identify 
# @frappe.whitelist()
# def check_late(self):

	
	
