
from __future__ import unicode_literals
from six import string_types
import frappe
from datetime import datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,format_date)
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
from itertools import count
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta


def execute(filters=None):
    data = []
    columns = get_columns()
    attendance = get_attendance(filters)
    for att in attendance:
        data.append(att)
    return columns, data

def get_columns():
    columns = [
        _("Employee") + ":Data:120",_("Employee Name") + ":Data:150",_("Department") + ":Data:120",_("Attendance Date") + ":Data:150",_("Shift") + ":Data:100",
        _("Shift Time") + ":Data:120",_("In Time") + ":Data:170",_("Late minutes") + ":Data:170",
    ]
    return columns

def get_attendance(filters):
    data = []
    if filters.employee:
        attendance = frappe.get_all('Attendance',{'status':'Present','attendance_date':('between',(filters.from_date,filters.to_date)),'employee':filters.employee},['*'])
    else:
        attendance = frappe.get_all('Attendance',{'status':'Present','attendance_date':('between',(filters.from_date,filters.to_date))},['*'])
        late_by = ''
    for att in attendance:
        if att.shift and att.in_time:
            shift_time = frappe.get_value("Shift Type",{'name':att.shift},["start_time"])
            get_time = datetime.strptime(str(shift_time),'%H:%M:%S').strftime('%H:%M:%S')
            shift_start_time = dt.datetime.strptime(str(get_time),"%H:%M:%S")
            start_time = dt.datetime.combine(att.attendance_date,shift_start_time.time())
            st_time = start_time.strftime('%H:%M:%S')
            at_time = att.in_time.strftime('%H:%M:%S')
            if att.in_time > start_time:
                late_time = att.in_time - start_time
                row = [
                att.employee,
                att.employee_name,
                att.department,
                format_date(att.attendance_date),
                att.shift,
                st_time,
                at_time,
                late_time]
                data.append(row)
    return data