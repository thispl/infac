# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

# import frappe
# from frappe import _, msgprint
# from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form

# def execute(filters=None):
# 	columns = get_columns(filters)
# 	data = get_data(filters)
# 	return columns, data

# def get_columns(filters):
# 	columns = [
# 		_('Attendance ID') +":Link/Attendance:150",
# 		_('Attendance Date') +':Data:150',
# 		_('Employee ID') +':Data:100',
# 		_('Employee Name') +':Data:200',
# 		_('Employee Category') +':Data:200',
# 		_('In Time')+':Data:200',
# 		_('Out Time')+':Data"200',
# 		_('Assign Shift') +':Data:150',
# 		_('Attended Shift') +':Data:150'
# 	]
# 	return columns

# def get_data(filters):
# 	data = []
# 	if filters.employee:
# 		attendance = frappe.db.sql("""select * from `tabAttendance` where attendance_date between '%s' and '%s'  and matched_status != "Matched" and employee = '%s' order by attendance_date ASC """%(filters.from_date,filters.to_date,filters.employee),as_dict = True)
# 	else:
# 		attendance = frappe.db.sql("""select * from `tabAttendance` where attendance_date between '%s' and '%s'  and matched_status != "Matched" order by attendance_date ASC """%(filters.from_date,filters.to_date),as_dict = True)
# 	for att in attendance:
# 		if att.in_time or att.out_time :
# 			row = [
# 				att.name,
# 				format_date(att.attendance_date),
# 				att.employee,
# 				att.employee_name,
# 				att.employee_category,
# 				att.in_time or '',
# 				att.out_time  or '',
# 				att.shift_type,
# 				att.actual_shift
# 			]
# 			data.append(row)
# 	return data	


# def get_employees(filters):
# 	conditions = ''
# 	if filters.employee:
# 		conditions += "and employee = '%s' " % filters.employee
# 	employees = frappe.db.sql("""select * from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
# 	left_employees = frappe.db.sql("""select * from `tabEmployee` where status = 'Left' and relieving_date >= '%s' %s """ %(filters.from_date,conditions),as_dict=True)
# 	employees.extend(left_employees)
# 	return employees



import frappe
from frappe import _, msgprint
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date, get_url_to_form

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		_('Attendance ID') + ":Link/Attendance:150",
		_('Attendance Date') + ':Data:150',
		_('Employee ID') + ':Data:100',
		_('Employee Name') + ':Data:200',
		_('Employee Category') + ':Data:200',
		_('In Time') + ':Data:200',
		_('Out Time') + ':Data:200',  
		_('Attended Shift') + ':Data:150'
		# _('Assign Shift') + ':Data:150',
	]
	return columns

def get_data(filters):
	data = []

	condition = "attendance_date between '%s' and '%s'" % (filters.from_date, filters.to_date)

	if filters.employee:
		condition += " and employee = '%s'" % filters.employee

	query = f"""
		select * from `tabAttendance`
		where {condition}
		and (in_time is not null or out_time is not null)
		and (shift is null or shift = '')
		order by attendance_date ASC
	"""

	attendance = frappe.db.sql(query, as_dict=True)

	for att in attendance:
		row = [
			att.name,
			format_date(att.attendance_date),
			att.employee,
			att.employee_name,
			att.employee_category,
			att.in_time or '',
			att.out_time or '',
			att.shift or '',           
			# att.actual_shift or ''    
		]
		data.append(row)

	return data


def get_employees(filters):
	conditions = ''
	if filters.employee:
		conditions += "and employee = '%s' " % filters.employee

	employees = frappe.db.sql("""SELECT * FROM `tabEmployee` WHERE status = 'Active' %s""" % conditions, as_dict=True)
	left_employees = frappe.db.sql("""SELECT * FROM `tabEmployee` WHERE status = 'Left' AND relieving_date >= '%s' %s""" % (filters.from_date, conditions), as_dict=True)
	employees.extend(left_employees)
	return employees
