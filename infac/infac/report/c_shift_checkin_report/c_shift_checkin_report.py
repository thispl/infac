# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

from ssl import ALERT_DESCRIPTION_USER_CANCELLED
from webbrowser import get
import frappe
from frappe import _, msgprint
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form


def execute(filters=None):
    columns = get_columns()
    data = []
    attendance = get_attendance(filters)
    for att in attendance:
        data.append(att)
    return columns, data

def get_columns():
    columns = [
        _('Employee') +':Data:150',_('Employee Name') +':Data:150',_('Employee Category') +':Data:150',_('Department') +':Data:100',_('Attendance Date') +':Data:150',
        _('Check-in Time') +':Data:150',_('Check -Out Time') +':Data:200'
    ]
    return columns

def get_attendance(filters):
    data = []
    employee = get_employees(filters)
    for emp in employee:
        attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date)),'shift':'C','employee':emp.name},['*'])
        for att in attendance:
            if att:
                row = [emp.name,emp.first_name,emp.employee_category,emp.department,format_date(att.attendance_date),att.in_time.strftime('%H:%M:%S'),att.out_time]
                data.append(row)
    return data			
    # if filters.employee:
    # 	frappe.db.get_all('Attendance',{'employee':filters.employee,'shift':'C','attendance_date':('between',(filters.from_date,filters.to_date))},['*'])

    # elif filters.employee_category:
    # 	frappe.db.get_all('Attendance',{'employee':filters.employee,'shift':'C','employee_category':filters.employee_category,'attendance_date':('between',(filters.from_date,filters.to_date))},['*'])	
    # else:
    # 	frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date)),'shift':'C'},['*'])

    # attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date)),'shift':'C'},['*'])

    # for att in attendance:
    # 	if att:
    # 		row = [att.employee,att.employee_name,att.employee_category,att.attendance_date.strftime('%d-%m-%Y'),att.in_time.strftime('%H:%M:%S'),att.out_time]
    # 		data.append(row)
    # return data		

def get_employees(filters):
    conditions = ''
    left_employees = []
    if filters.employee:
        conditions += "and employee = '%s' " % (filters.employee)
        
    if filters.employee_category:
        conditions += "and employee_category = '%s' " % (filters.employee_category)
    
    employees = frappe.db.sql("""select name, employee_name, department,employee_category,date_of_joining from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
    left_employees = frappe.db.sql("""select name, employee_name, department,employee_category, date_of_joining from `tabEmployee` where status = 'Left' and relieving_date >= '%s' %s """ %(filters.from_date,conditions),as_dict=True)
    employees.extend(left_employees)
    return employees


