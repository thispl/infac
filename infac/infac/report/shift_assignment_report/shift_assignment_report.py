# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from datetime import date, timedelta, datetime,time


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [
        _('Employee') +':Data:100',_('Employee Name') +':Data:150',_('Department') +':Data:150',_('Department Line') +':Data:150',_('Employee Category') +':Data:150',
        _('Shift Date') +':Data:100',
    ]
    return columns

def get_data(filters):
    data = []
    if filters.department:
        shift = frappe.db.sql(""" select * from `tabShift Assignment` where start_date between '%s' and '%s' and department = '%s' and docstatus != '2' """%(filters.from_date,filters.to_date,filters.department),as_dict=True)
        for s in shift:
            data.append([s.employee,s.employee_name,s.department,s.department_line,s.employee_category,s.shift_type])
    else:
        shift = frappe.db.sql(""" select * from `tabShift Assignment` where start_date between '%s' and '%s'  and docstatus != '2' """%(filters.from_date,filters.to_date),as_dict=True)
        for s in shift:
            data.append([s.employee,s.employee_name,s.department,s.department_line,s.employee_category,s.shift_type])
    return data    


def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates


def get_employees(filters):
    conditions = ''
    if filters.department:
        conditions += "and department = '%s' " % filters.department
    left_employees = []
    if filters.employee:
        conditions += "and employee = '%s' " % (filters.employee)
    if filters.employee_category:
        conditions += "and employee_category = '%s' " % (filters.employee_category)

    employees = frappe.db.sql("""select name, employee_name, department,department_line,employee_category,date_of_joining from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
    left_employees = frappe.db.sql("""select name, employee_name, department,employee_category, date_of_joining from `tabEmployee` where status = 'Left' and relieving_date >= '%s' %s """ %(filters.from_date,conditions),as_dict=True)
    employees.extend(left_employees)
    return employees   