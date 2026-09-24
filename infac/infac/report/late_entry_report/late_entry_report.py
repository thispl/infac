
# from __future__ import unicode_literals
# from six import string_types
# import frappe
# from datetime import datetime
# from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
# 	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,format_date)
# from calendar import monthrange
# from frappe import _, msgprint
# from frappe.utils import flt
# from frappe.utils import cstr, cint, getdate
# from itertools import count
# import pandas as pd
# import datetime as dt
# from datetime import datetime, timedelta


# def execute(filters=None):
#     data = []
#     columns = get_columns()
#     attendance = get_attendance(filters)
#     for att in attendance:
#         data.append(att)
#     return columns, data

# def get_columns():
#     columns = [
#         _("Employee") + ":Data:120",_("Employee Name") + ":Data:150",_("Department") + ":Data:120",_("Attendance Date") + ":Data:150",_("Shift") + ":Data:100",
#         _("Shift Time") + ":Data:120",_("In Time") + ":Data:170",_("Late minutes") + ":Data:170",
#     ]
#     return columns

# def get_attendance(filters):
#     data = []
#     if filters.employee:
#         attendance = frappe.get_all('Attendance',{'status':'Present','attendance_date':('between',(filters.from_date,filters.to_date)),'employee':filters.employee},['*'])
#     else:
#         attendance = frappe.get_all('Attendance',{'status':'Present','attendance_date':('between',(filters.from_date,filters.to_date))},['*'])
#         late_by = ''
#     for att in attendance:
#         if att.shift and att.in_time:
#             shift_time = frappe.get_value("Shift Type",{'name':att.shift},["start_time"])
#             get_time = datetime.strptime(str(shift_time),'%H:%M:%S').strftime('%H:%M:%S')
#             shift_start_time = dt.datetime.strptime(str(get_time),"%H:%M:%S")
#             start_time = dt.datetime.combine(att.attendance_date,shift_start_time.time())
#             st_time = start_time.strftime('%H:%M')
#             at_time = att.in_time.strftime('%H:%M')
#             if att.in_time > start_time:
#                 late_time = att.in_time - start_time
#                 total_seconds = late_time.total_seconds()
#                 hours = int(total_seconds // 3600)
#                 minutes = int((total_seconds % 3600) // 60)
#                 late_time_str = f"{hours:02d}:{minutes:02d}"
#                 row = [
#                 att.employee,
#                 att.employee_name,
#                 att.department,
#                 format_date(att.attendance_date),
#                 att.shift,
#                 st_time,
#                 at_time,
#                 late_time_str]
#                 data.append(row)
#     return data

from __future__ import unicode_literals
import frappe
from frappe.utils import format_datetime
from datetime import datetime, time, timedelta

def execute(filters=None):
    columns = get_columns()
    data = get_late_checkins(filters)
    return columns, data


def get_columns():
    return [
        "Employee:Data:120",
        "Employee Name:Data:150",
        "Department:Data:120",
        "Date:Data:120",
        "Shift:Data:120",
        "Start Time:Data:120",
        "In Time:Data:120",
        "Late Minutes:Data:80",
    ]

def get_late_checkins(filters):
    conditions = {
        "log_type": "IN",
        "late_entry": 1
    }

    if filters.get("from_date") and filters.get("to_date"):
        conditions["time"] = ("between", (filters.from_date, filters.to_date))

    if filters.get("employee"):
        conditions["employee"] = filters.employee

    checkins = frappe.get_all(
        "Employee Checkin",
        filters=conditions,
        fields=[
            "employee",
            "employee_name",
            "department",
            "time",
            "shift"
        ],
        order_by="time asc"
    )

    data = []

    for row in checkins:
        start_time_str = ""
        late_minutes = 0

        if row.shift:
            shift_start = frappe.get_value("Shift Type", row.shift, "start_time")

            if shift_start:
                # ✅ HANDLE timedelta → time
                if isinstance(shift_start, timedelta):
                    total_seconds = int(shift_start.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    shift_start_time = time(hours, minutes)
                else:
                    shift_start_time = shift_start

                # ✅ format start time
                start_time_str = shift_start_time.strftime("%H:%M")

                # ✅ build datetime
                shift_datetime = datetime.combine(
                    row.time.date(),
                    shift_start_time
                )

                # ✅ late minutes
                if row.time > shift_datetime:
                    diff = row.time - shift_datetime
                    late_minutes = int(diff.total_seconds() // 60)

        data.append([
            row.employee,
            row.employee_name,
            row.department,
            row.time.date(),
            row.shift,
            start_time_str,
            row.time.strftime("%H:%M"),
            late_minutes
        ])

    return data