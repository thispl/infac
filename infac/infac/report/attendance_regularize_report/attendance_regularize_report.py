# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

from operator import truediv
import frappe
from frappe import _, msgprint
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [
        _('Employee') +'Data:100',_('Employee Name') +':Data:150',_('Department') +':Data:200',_('Employee Category') +":Data:150",
        _('Attendance Date') +':Data:150',_('Assigned Shift') +':Data:150',_('Shift In Time') +':Data:150',_('Shift Out Time') +':Data:150',
        _('First In Time') +':Data:150',_('Last Out Time') + ':Data:150',_('Corrected In Time') +':Data:150',_('Corrected Out Time') + "Data:150",
        _('Corrected Shift') +':Data:150'
    ]
    return columns

def get_data(filters):
    data = []
    employees = get_employees(filters)
    for emp in employees:
        attendance_regularize = frappe.db.sql(""" select attendance_date,assigned_shift,shift_in_time,shift_out_time,first_in_time,
                                last_out_time,corrected_in,corrected_out,corrected_shift from `tabAttendance Regularize` where attendance_date between '%s' and '%s' and employee = '%s'  """%(filters.from_date,filters.to_date,emp.name),as_dict=True)
        for att in attendance_regularize: 
            if attendance_regularize:                        
                row = [emp.name,emp.employee_name,emp.department,emp.employee_category,format_date(att.attendance_date),att.assigned_shift,
                        att.shift_in_time,att.shift_out_time,att.first_in_time,att.last_out_time,format_datetime(att.corrected_in),
                        format_datetime(att.corrected_out),att.corrected_shift]
                data.append(row)
    return data

    


def get_employees(filters):
    conditions = ''
    if filters.department:
        conditions += "and department = '%s' " % filters.department
    left_employees = []
    if filters.employee:
        conditions += "and employee = '%s' " % (filters.employee)
    if filters.employee_category:
        conditions += "and employee_category = '%s' " % (filters.employee_category)

    employees = frappe.db.sql("""select name, employee_name, department,employee_category,date_of_joining from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
    left_employees = frappe.db.sql("""select name, employee_name, department,employee_category, date_of_joining from `tabEmployee` where status = 'Left' and relieving_date >= '%s' %s """ %(filters.from_date,conditions),as_dict=True)
    employees.extend(left_employees)
    return employees