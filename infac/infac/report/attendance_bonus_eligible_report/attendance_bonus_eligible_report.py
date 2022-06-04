# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from six import string_types
import frappe
import json
import datetime
from datetime import datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
from itertools import count
import pandas as pd

def execute(filters=None):
    data = []
    columns = get_columns()
    attendance = get_attendance(filters)
    for att in attendance:
        data.append(att)
    return columns, data

def get_columns():
    columns = [
        _("Employee") + ":Data:100",
        _("Employee Name") + ":Data:200",
        _("Department") + ":Data:160",
        _("Present Days") + ":Data:100",
        _("Working Days") + ":Data:100",
        _("Attendance Bonus") + ":Data:120",
    ]
    return columns

def get_attendance(filters):
    data =[]
    if not filters.employee:
        employee = frappe.get_all("Employee",{'status':'Active'},['*'])
    else:
        employee = frappe.get_all("Employee",{'employee':filters.employee,'status':'Active'},['*'])
    eligibility = ''
    for emp in employee:
        count = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status = 'Present' and attendance_date between '%s' and '%s'""" % (emp.employee,filters.from_date,filters.to_date),as_dict=True)[0].count
        working_days = frappe.db.get_value('Salary Slip',{'employee':emp.employee},['total_working_days'])
        if working_days:
            if count == working_days or count == working_days -1:
                eligibility = 'Eligible'
                row = [emp.employee,emp.employee_name,emp.department,count,working_days,eligibility]
                data.append(row)
    return data