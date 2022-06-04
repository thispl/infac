# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

import re
from sqlite3 import Row
from warnings import filters
import frappe
# from __future__ import unicode_literals
from frappe import msgprint, _
from frappe.utils import cstr, add_days, date_diff, getdate, format_date


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns +=[
		_('Employee ID') +':Data/:150',_('Employee Name') +':Data/:150',_('Employee Category') +':Data:150',_('DOJ') +':Data:100',_('Att Date') +':Data/:150',
		_('Shift Assigned') +':Dat/:150',_('Shift Attended') +':Data/:150'
	]
	return columns

def get_data(filters):
	data = []
	# row = ['','','','']
	# data.append(row)
	# return data
	dates = get_dates(filters.from_date,filters.to_date)
	for date in dates:
		# attendance = frappe.db.get_all('Attendance',{'attendance_date':date,},['employee','employee_name','employee_category','shift','in_time','out_time'])
		# for att in attendance:
		# 	frappe.errprint(att)
		# 	shift_assign = frappe.db.get_value('Shift Assignment',{'start_date':date,'employee':att.employee},'shift_type')
		# 	if shift_assign:
		# 		if att.shift != shift_assign:
		# 			row = [att.employee,att.employee_name,att.employee_category,date,att.in_time,att.out_time,shift_assign,att.shift]
		# 			data.append(row)

		employees = get_employees(filters)
		for emp in employees:
			attendance = frappe.db.get_value('Attendance',{'status':('not equals',),'attendance_date':date,'employee':emp.name,},['shift'])
			# attendance = frappe.db.sql(""" sel """)
			shift_assign = frappe.db.get_value('Shift Assignment',{'start_date':date,'employee':emp.name},'shift_type')
			# for att in attendance:
			if shift_assign:
				if attendance != shift_assign:
					row = [emp.name,emp.employee_name,emp.employee_category,emp.date_of_joining,date,shift_assign,attendance]
					data.append(row)
	return data


def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates	

def get_employees(filters):
		conditions = ''
		if filters.employee:
			conditions += "and employee = '%s' " % (filters.employee)
		if filters.employee_category:
			conditions += "and employee_category = '%s' " % (filters.employee_category)

		employees = frappe.db.sql("""select name, employee_name,employee_category,date_of_joining from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
		return employees	      	

	

	# employees = get_employees(filters)
	# 	for day in get_dates(filters.from_date,filters.to_date):
	# 		attendance = frappe.db.get_all('Attendance',{'attendance_date':day},['shift','employee'])
	# 		# attendance = frappe.db.sql(""" sel """)
	# 		for att in attendance:
	# 			shift_assign = frappe.db.get_value('Shift Assignment',{'start_date':day,'employee':att.employee},'shift_type')
	# 			# for att in attendance:
	# 			if shift_assign:
	# 				if att.shift != shift_assign:
	# 					emp = frappe.get_doc('Employee',att.employee)
	# 					row = [emp.name,emp.employee_name,emp.employee_category,emp.date_of_joining,day,shift_assign,att.shift]
	# 					data.append(row)
	# return data