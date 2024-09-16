    # Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days,time_diff_in_hours
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime
import pandas as pd

status_map = {
    "Absent": "AA",
	"Half Day": "HD",
	"Holiday": "HH",
	"Weekly Off": "WW",
    "Present": "P",
    "None" : ""
}
def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = []
    columns += [
        _("Emp.ID") + ":Data/:100",_("Employee Name") + ":Data/:200",_("Employee Category"),_("Department") + ":Data/:150",_("DOJ") + ":Date/:100",_("Att. Date") + ":Date/:100",
        _("In Time") + ":Data/:100",_("Out Time") + ":Data/:100",_("Shift") + ":Data/:80",_("TWH") + ":Float/:80",_("OT") + ":Float/:80"
    ]
    
    return columns

def get_data(filters):
    data = []
    emp_status_map = []
    
    dates = get_dates(filters.from_date,filters.to_date)
    for date in dates:
        employees = get_employees(filters)
        for emp in employees:
            row = [emp.name,emp.employee_name,emp.employee_category,emp.department,emp.date_of_joining]
            row.append(date)
            hh = check_holiday(date,emp.name)
            if not hh:
                att = frappe.db.get_value("Attendance",{'attendance_date':date,'employee':emp.name},['status','in_time','out_time','shift','attendance_date','working_hours','ot_hrs']) or ''
                twh = 0
                ot = 0
                if att:
                    status = status_map.get(att[0], "")
                    if att[1] is not None:
                        row.append(att[1].strftime('%H:%M:%S'))
                    else:
                        row.append('-')
                    if att[2] is not None:
                        row.append(att[2].strftime('%H:%M:%S'))
                    else:
                        row.append('-')
                    row.append(att[3])
                    row.append(att[5])
                    row.append(att[6])
                else:
                    row += ['-','-','-','-','-','-','-']
                data.append(row)
            else:
                hd_att = frappe.db.get_value("Holiday Attendance",{'attendance_date':date,'employee':emp.name},['status','in_time','out_time','shift','attendance_date','ot_hrs']) or '' 
                twh = 0
                ot = 0
                if hd_att:
                    status = status_map.get(hd_att[0], "")
                    if hd_att[1] is not None:
                        row.append(hd_att[1].strftime('%H:%M:%S'))
                    else:
                        row.append('-')
                    if hd_att[2] is not None:
                        row.append(hd_att[2].strftime('%H:%M:%S'))
                    else:
                        row.append('-')
                    row.append(hd_att[3])
                    working_hours = time_diff_in_hours(hd_att[2],hd_att[1])
                    if working_hours:
                        row.append(working_hours)
                    else:
                        row.append(0.0)
                    row.append(hd_att[5])
                else:
                    row += ['-','-','-','-','-','-','-']
                data.append(row) 
    return data

def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

def get_employees(filters):
    conditions = ''
    if filters.department:
        conditions += "and department = '%s' " % filters.department
    if filters.employee_category:
        conditions += "and employee_category = '%s' "%filters.employee_category
    if filters.department:
        conditions += " and department = '%s' "%filters.department   
    if filters.employee:
        conditions += "and employee = '%s' " % filters.employee
    employees = frappe.db.sql("""select name, employee_name,employee_category, department, date_of_joining from `tabEmployee` where status = 'Active' %s"""%(conditions),as_dict=True)
    return employees


def check_holiday(date,emp):
    holiday_list = frappe.db.get_value('Company','Infac India Private Limited','default_holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"    