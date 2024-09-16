# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		_('Attendance ID') +":Link/Attendance:150",
		_('Attendance Date') +':Data:150',
		_('Employee ID') +':Data:100',
		_('Employee Name') +':Data:200',
		_('Employee Category') +':Data:200',
		_('In Time')+':Data:200',
		_('Out Time')+':Data"200',
		_('Assign Shift') +':Data:150',
		_('Attended Shift') +':Data:150'
	]
	return columns

def get_data(filters):
	data = []
	if filters.employee:
		attendance = frappe.db.sql("""select * from `tabAttendance` where attendance_date between '%s' and '%s'  and matched_status != "Matched" and employee = '%s' order by attendance_date ASC """%(filters.from_date,filters.to_date,filters.employee),as_dict = True)
	else:
		attendance = frappe.db.sql("""select * from `tabAttendance` where attendance_date between '%s' and '%s'  and matched_status != "Matched" order by attendance_date ASC """%(filters.from_date,filters.to_date),as_dict = True)
	for att in attendance:
		if att.in_time or att.out_time :
			row = [
				att.name,
				format_date(att.attendance_date),
				att.employee,
				att.employee_name,
				att.employee_category,
				att.in_time or '',
				att.out_time  or '',
				att.shift_type,
				att.actual_shift
			]
			data.append(row)
	return data	


def get_employees(filters):
	conditions = ''
	if filters.employee:
		conditions += "and employee = '%s' " % filters.employee
	employees = frappe.db.sql("""select * from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
	left_employees = frappe.db.sql("""select * from `tabEmployee` where status = 'Left' and relieving_date >= '%s' %s """ %(filters.from_date,conditions),as_dict=True)
	employees.extend(left_employees)
	return employees


# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

# import frappe
# from frappe import _, msgprint
# from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form



# def execute(filters=None):
#     columns = get_columns(filters)
#     data = get_data(filters)
#     return columns, data

# def get_columns(filters):
#     columns = [
#         _('Attendance ID') +":Link/Attendance:150",_('Employee ID') +':Data:100',_('Employee Name') +':Data:200',_('Employee Category') +':Data:200',_('Attendance Date') +':Data:150',
#         _('In Time')+':Data:200',_('Out Time')+':Data"150',
#         _('Assign Shift') +':Data:150',_('Attended Shift') +':Data:150'
#     ]
#     return columns

# def get_data(filters):
#     data = []
#     employees = get_employees(filters)
#     for emp in employees: 
#         attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date)),'status':'Absent','employee':emp.name},['*'])
#         for att in attendance:
#             if att.in_time:
#                 row = [att.name,emp.name,emp.employee_name,emp.employee_category,format_date(att.attendance_date),att.in_time or '',att.out_time  or '',att.shift_type,att.actual_shift]
#                 data.append(row)
#     return data	


# def get_employees(filters):
#     conditions = ''
#     if filters.employee:
#         conditions += "and employee = '%s' " % filters.employee
#     employees = frappe.db.sql("""select name, employee_name,employee_category, department, date_of_joining from `tabEmployee` where status = 'Active' %s"""%(conditions),as_dict=True)
#     return employees