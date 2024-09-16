# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from functools import total_ordering
from itertools import count
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days,date_diff,format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
import pandas as pd

def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = []
    columns += [
        _("Employee ID") + ":Data/:100",
        _("Employee Name") + ":Data/:200",
        _("Department") + ":Data/:150",
        _("DOJ") + ":Date/:100",
        _("Att Date") + ":Date/:100",
        _("E-Slap OT Hrs") + ":Data/:100",_("Amount") + ":Data/:100",_("T-Slap OT Hrs") + ":Data/:100",_("Amount") + ":Data/:100",_("M-Slap OT Hrs") + ":Data/:80",_("Amount") + ":Data/:100",
        # _("Total OT Hrs") + ":Data/:100",_("Total Amount") + ":Data/:100",
    ]
    return columns

def get_data(filters):
    data = []
    total_ot_hours = 0.0
    employees = get_employees(filters)
    for emp in employees: 
        attendance = frappe.db.sql(""" select * from `tabAttendance` where employee = '%s' and attendance_date between '%s' and '%s' and employee_category = 'Master Staff' and docstatus != '2' """%(emp.name,filters.from_date,filters.to_date),as_dict=1) 
        for att in attendance:
            if att.attendance_date: 
                row = [emp.name,emp.employee_name,emp.department,emp.date_of_joining,format_date(att.attendance_date),'','','','','','']
            # att.e_slap_ot_hrs,att.e_slap_incentive_amount,att.t_slap_ot_hrs,att.t_slap_incentive_amount,att.m_slap_ot_hrs,att.m_slap_incentive_amount,
                    # total_ot_hours,total_amount]
            data.append(row)
    return data	

def get_employees(filters):
    conditions = ''
    if filters.employee:
        conditions += "and employee = '%s' " % filters.employee
    employees = frappe.db.sql("""select name, employee_name,employee_category, department, date_of_joining from `tabEmployee` where status = 'Active' and employee_category = 'Master Staff'%s"""%(conditions),as_dict=True)
    return employees