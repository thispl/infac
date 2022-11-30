# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from six import string_types
import frappe
import json
import datetime
from datetime import datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,format_date)
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
        _("Employee") + ":Data:120",_("Employee Name") + ":Data:150",_("Attendance Date") + ":Data:150",_("Shift") + ":Data:100",
        _("Shift Time") + ":Data:120",_("In Time") + ":Data:170",
    ]
    return columns

def get_attendance(filters):
    data = []
    if filters.employee:
        attendance = frappe.get_all('Attendance',{'status':'Present','attendance_date':('between',(filters.from_date,filters.to_date)),'employee':filters.employee},['*'])
        late_by = ''
        for att in attendance:
            if att.shift and att.in_time:
                shift_start_time = frappe.db.get_value("Shift Type",att.shift,"start_time")
                shift_start = pd.to_datetime(str(shift_start_time)).time()
                if att.in_time.time() > shift_start:
                    row = [att.employee,att.employee_name,format_date(att.attendance_date),att.shift,shift_start_time,att.in_time]
                    data.append(row)
    else:
        attendance = frappe.get_all('Attendance',{'status':'Present','attendance_date':('between',(filters.from_date,filters.to_date))},['*'])
        late_by = ''
        for att in attendance:
            if att.shift and att.in_time:
                shift_start_time = frappe.db.get_value("Shift Type",att.shift,"start_time")
                shift_start = pd.to_datetime(str(shift_start_time)).time()
                if att.in_time.time() > shift_start:
                    row = [att.employee,att.employee_name,format_date(att.attendance_date),att.shift,shift_start_time,format_datetime(att.in_time)]
                    data.append(row)
    return data