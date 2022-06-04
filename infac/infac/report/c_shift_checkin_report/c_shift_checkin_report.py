# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

from webbrowser import get
import frappe
from frappe import _, msgprint
from numpy import column_stack

def execute(filters=None):
	columns = get_columns()
	data = []
	attendance = get_attendance(filters)
	for att in attendance:
		data.append(att)
	return columns, data

def get_columns():
	columns = [
		_('Employee') +':Data:150',_('Employee Name') +':Data:150',_('Employee Category') +':Data:150',_('Attendance Date') +':Data:150',
		_('Check-in Time') +':Data:150',_('Check -Out Time') +':Data:150'
	]
	return columns

def get_attendance(filters):
	data = []
	if filters.employee:
		frappe.db.get_all('Attendance',{'employee':filters.employee,'shift':'C','attendance_date':('between',(filters.from_date,filters.to_date))},['*'])

	elif filters.employee_category:
		frappe.db.get_all('Attendance',{'employee':filters.employee,'shift':'C','employee_category':filters.employee_category,'attendance_date':('between',(filters.from_date,filters.to_date))},['*'])	
	else:
		frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date)),'shift':'C'},['*'])

	attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date)),'shift':'C'},['*'])

	for att in attendance:
		if att:
			row = [att.employee,att.employee_name,att.employee_category,att.attendance_date.strftime('%d-%m-%Y'),att.in_time.strftime('%H:%M:%S'),att.out_time]
			data.append(row)
	return data		


