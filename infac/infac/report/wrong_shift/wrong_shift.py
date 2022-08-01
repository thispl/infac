# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

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
        _('Attendance ID') +':Data:100',_('Employee ID') +':Data:100',_('Employee Name') +':Data:200',_('Employee Category') +':Data:200',_('DOB') +':Data:150',_('Attendance Date') +':Data:150',
        _('Assign Shift') +':Data:150',_('Attended Shift') +':Data:150'
    ]
    return columns

def get_attendance(filters):
    data = []
    employee = get_employees(filters)
    for emp in employee:
        attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date)),'matched_status':'Unmatched','employee':emp.name},['*'])
        for att in attendance:
            if att.in_time :
                if att.shift_type and att.actual_shift:
                    row = [att.name,emp.name,emp.employee_name,emp.employee_category,format_date(emp.date_of_birth),format_date(att.attendance_date),att.shift_type,att.actual_shift]
                    data.append(row)
    return data	

def get_employees(filters):
    conditions = ''
    left_employees = []
    if filters.employee:
        conditions += "and employee = '%s' " % (filters.employee)
    
    employees = frappe.db.sql("""select name, employee_name, department,employee_category,date_of_joining,date_of_birth from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
    left_employees = frappe.db.sql("""select name, employee_name, department,employee_category, date_of_joining from `tabEmployee` where status = 'Left' and relieving_date >= '%s' %s """ %(filters.from_date,conditions),as_dict=True)
    employees.extend(left_employees)
    return employees