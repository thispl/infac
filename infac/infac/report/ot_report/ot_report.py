# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from six import string_types
import frappe
import json
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
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
        _("Employee") + ":Data:120",
        _("Employee Name") + ":Data:120",
        _("Attendance Dsate") + ":Data:120",
        _("Shift") + ":Data:80",
        _("OT Hours") + ":Data:100",
    ]
    return columns

def get_attendance(filters):
    data = []
    row = []
    attendance = frappe.get_all('Attendance',{'status':'Present','attendance_date':('between',(filters.from_date,filters.to_date))},['*'])
    for att in attendance:
        if att.ot_hrs:
            row = [att.employee,att.employee_name,att.attendance_date,att.shift,att.ot_hrs]
            data.append(row)
    return data
