# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

from __future__ import print_function, unicode_literals
from six import string_types
import frappe
import json
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime,date
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
from itertools import count

def execute(filters=None):
    columns = get_columns()
    data = []
    row = []
    # conditions, filters = get_conditions(filters)
    attendance = get_attendance(filters)
    for att in attendance:
        data.append(att)
    return columns, data

def get_columns():
    columns = [
        _("Employee") + ":Link/Employee:150",
        _("Employee Name") + ":Data:180",
        _('Employee Category') + ":Data:180",
        _("Department") + ":Data:180",
        _("Absent Dates") + ":Data:450",
        _("Total Absent Days") + ":Data:70"
    ]
    return columns

def get_attendance(filters):
    row = []
    attendance = frappe.db.sql("""Select * From `tabAttendance` Where status in ('Absent','On Leave') and attendance_date between '%s' and '%s and %s order by employee'"""% (filters.from_date,filters.to_date,filters.employee), as_dict=1)
    if not filters.employee:
        employee = frappe.get_all("Employee",{'status':'Active','employee_category':('not in',['Management','Hirco Cook','General Motors','Driver'])},['*'])
    else:
        employee = frappe.get_all("Employee",{'name':filters.employee,'status':'Active'},['*'])
    for emp in employee:
        att_date = []
        for att in attendance:
            if emp.name == att.employee:
                if att.attendance_date  == date.today():
                    today_in_time = frappe.get_value('Attendance',{'employee':att.employee,'attendance_date':att.attendance_date},'in_time')
                    if not today_in_time:
                        att_date += [att.attendance_date.strftime("%d-%m-%Y")]
                else:
                    att_date += [att.attendance_date.strftime("%d-%m-%Y")]
                att_list = (','.join(att_date))
        count = len(att_date)
        if count:
            row += [(emp.name,emp.employee_name,emp.employee_category,emp.department,att_list,count)]
    return row

# def get_conditions(filters):
#     conditions = ""
#     if filters.get("employee"): conditions += " and employee = %(employee)s"
#     return conditions, filters
