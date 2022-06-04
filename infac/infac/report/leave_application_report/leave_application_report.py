# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from infac.infac.report.attendance_register.attendance_register import get_columns

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = []
	columns+=[
		_('User ID ') +':Data/:150',_('Application Date') +':Data/:150',_('Employee') +':Data/:150',_('Employee Name') +':Data/:150',
		_('Department') +':Data/:150',
	]
	return columns

def get_data(filters):
	data = []
	dates = get_dates(filters.from_date,filters.to_date)
	for date in dates:
		if filters.employee:
			user_id = frappe.db.sql(""" select owner,posting_date,name,employee_name,department from `tabLeave Application` where posting_date = %s and employee = '%s' """%(date,filters.employee),as_dict=1)
		else:
			user_id = frappe.db.sql(""" select owner,posting_date,name,employee_name,department from `tabLeave Application` where posting_date = %s """%(date),as_dict=1)	
			row = ['','','','','']
			# for user in user_id:	
			# 	row = [user.owner,user.posting_date,user.name,user.employee_name,user.department]
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

	employees = frappe.db.sql("""select name,employee_name,employee_category,department,designation from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
	return employees	      	


