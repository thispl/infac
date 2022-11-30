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
        _('Attendance ID') +':Data:150',_('Employee ID') +':Data:100',_('Employee Name') +':Data:200',_('Employee Category') +':Data:200',_('Attendance Date') +':Data:150',
        _('Assign Shift') +':Data:150',_('Attended Shift') +':Data:150'
    ]
    return columns

def get_data(filters):
    data = []
    if filters.employee:
        # attendance = frappe.db,sql("")
        attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date)),'status':'Absent','employee':filters.employee},['*'])
    if not filters.employee:    
        attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date)),'status':'Absent'},['*'])
    for att in attendance:
        if att.in_time:
            row = [att.name,att.employee,att.employee_name,att.employee_category,format_date(att.attendance_date),att.shift_type,att.actual_shift]
            data.append(row)
    return data	
