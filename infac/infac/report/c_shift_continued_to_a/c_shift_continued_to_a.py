# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint

def execute(filters=None):
	columns = get_columns()
	data = []
	attendance = get_attendance(filters)
	for att in attendance:
		data.append(att)
	return columns, data


def get_columns():
	columns = [
		_('Employee ID') +':Data:200',_('Employee Name') +':Data:200',_('Department') +':Data:200',_('Employee Category') +':Data:200',_('Attendance Date')
	]
	return columns


def get_attendance(filters):
	data = []
	#get the total employees from Employee MIS
	employee =  get_employees(filters)
	for emp in employee:
		#By using Emp in for loop to take Emp ID to set into the Attendance
		attendance = frappe.db.get_all('Attendance',{'Status':'Present','attendance_date':('between',(filters.from_date,filters.to_date)),'employee':emp.name,'shift':'C'},['*'])
		for att in attendance:
			shift_type = frappe.db.get_value('Shift Type',{'name':'C'},['total_hours'])
			#Comparing the attendane_tota_wh and C shift_total_wh
			if att.total_wh:
				if att.total_wh > shift_type:
					row = [emp.name,emp.employee_name,emp.department,emp.employee_category,att.attendance_date.strftime('%d-%m-%Y')]
					#By Append the above row to data 
					data.append(row)
	#Return the data 			
	return data			

def get_employees(filters):
    conditions = ''
    left_employees = []
    if filters.employee:
        conditions += "and employee = '%s' " % (filters.employee)

    employees = frappe.db.sql("""select name, employee_name, department,employee_category,date_of_joining from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
    left_employees = frappe.db.sql("""select name, employee_name, department,employee_category, date_of_joining from `tabEmployee` where status = 'Left' and relieving_date >= '%s' %s """ %(filters.from_date,conditions),as_dict=True)
    employees.extend(left_employees)
    return employees