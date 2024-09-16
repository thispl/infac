# Copyright (c) 2023, teampro and contributors
# For license information, please see license.txt

from __future__ import print_function
import frappe
from frappe.model.document import Document
from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from calendar import month_abbr
from decimal import ROUND_UP
from hmac import new
from itertools import count
from lib2to3.pytree import convert
from math import perm
from operator import neg
from pickle import TRUE
from re import A
import time
from frappe.utils.data import month_diff
from frappe.utils.file_manager import get_file
from datetime import timedelta
from time import strftime, strptime
from stat import FILE_ATTRIBUTE_REPARSE_POINT
from traceback import print_tb
from wsgiref.util import shift_path_info
# from tkinter.filedialog import SaveAs
import frappe
from frappe.utils import time_diff_in_hours 

from frappe.share import add, remove
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,today,get_time, format_date)
import datetime
from datetime import datetime   
from datetime import timezone
from frappe.utils.csvutils import read_csv_content 
from frappe import permissions
from datetime import datetime,timedelta,date,time
from dateutil.relativedelta import relativedelta
from frappe.utils.user import get_user_fullname
import math
import pandas as pd
from frappe.utils import get_first_day, get_last_day, format_datetime, get_url_to_form
import dateutil.relativedelta
from frappe import throw,_


class AttendanceMigrationTool(Document):
	pass


# @frappe.whitelist()
# def holiday_att_to_att(from_date,to_date):
# 	frappe.errprint('hi')

@frappe.whitelist()
def holiday_att_to_att(document,from_date):
    track = frappe.new_doc("Attendance Migrate Toll Tracker")
    track.name1 = frappe.session.user
    track.save()
    frappe.db.commit()
    if document == 'Move Holiday Attendance to Attendance':
        attendance = frappe.db.sql("""select employee from `tabAttendance` where attendance_date = '%s' and docstatus = '1' """%(from_date),as_dict=1)
        for a in attendance:
            del_hol_att = frappe.db.sql("""delete from `tabHoliday Attendance` where employee = '%s' and attendance_date = '%s' """%(a.employee,from_date))
        hol_att = frappe.db.sql("""select employee from `tabHoliday Attendance` where attendance_date = '%s' and docstatus != '2' """%(from_date),as_dict=1)
        for u in hol_att:
            del_att = frappe.db.sql("""delete from `tabAttendance` where employee = '%s' and attendance_date = '%s' and docstatus = '0' """%(u.employee,from_date))
        holiday_att = frappe.db.sql("""select * from `tabHoliday Attendance` where attendance_date = '%s' and docstatus != '2' """%(from_date),as_dict=1)
        for h in holiday_att:
            att = frappe.new_doc("Attendance")
            att.name = h.attendance_name
            att.attendance_name = h.attendance_name
            att.employee = h.employee
            att.employee_name = h.employee_name
            att.employee_category = h.employee_category
            att.status = h.status
            att.attendance_date = h.attendance_date
            att.shift = h.shift
            att.total_wh = h.total_wh
            att.late_hours = h.late_hours
            att.in_time = h.in_time
            att.out_time = h.out_time
            att.extra_hours = h.extra_hours
            att.ot_hrs = h.ot_hrs
            att.late_hrs = h.late_hrs
            att.late_deduct = h.late_deduct
            att.miss_punch_marked = h.miss_punch_marked
            att.permission_request = h.permission_request
            att.on_duty_marked = h.on_duty_marked
            att.single_punch_regularization = h.single_punch_regularization
            att.shift_type = h.shift_type
            att.shift_in_time = h.shift_in_time
            att.shift_out_time = h.shift_out_time
            att.actual_shift = h.actual_shift
            att.actual_in_time = h.actual_in_time
            att.actual_out_time = h.actual_out_time
            att.matched_status = h.matched_status
            att.attendance_regularize = h.attendance_regularize
            att.save()
            frappe.db.commit()
        delete_holiday_att = frappe.db.sql("""delete from `tabHoliday Attendance` where attendance_date = '%s' """%(from_date))
    elif document == 'Move Attendance to Holiday Attendance':
        core_attendance = frappe.db.sql("""select * from `tabAttendance` where attendance_date = '%s' and docstatus = '0' """%(from_date),as_dict=1)
        for h in core_attendance:
            att = frappe.new_doc("Holiday Attendance")
            att.name = h.attendance_name
            att.attendance_name = h.attendance_name
            att.employee = h.employee
            att.employee_name = h.employee_name
            att.employee_category = h.employee_category
            att.status = h.status
            att.attendance_date = h.attendance_date
            att.shift = h.shift
            att.total_wh = h.total_wh
            att.late_hours = h.late_hours
            att.in_time = h.in_time
            att.out_time = h.out_time
            att.extra_hours = h.extra_hours
            att.ot_hrs = h.ot_hrs
            att.late_hrs = h.late_hrs
            att.late_deduct = h.late_deduct
            att.miss_punch_marked = h.miss_punch_marked
            att.permission_request = h.permission_request
            att.on_duty_marked = h.on_duty_marked
            att.single_punch_regularization = h.single_punch_regularization
            att.shift_type = h.shift_type
            att.shift_in_time = h.shift_in_time
            att.shift_out_time = h.shift_out_time
            att.actual_shift = h.actual_shift
            att.actual_in_time = h.actual_in_time
            att.actual_out_time = h.actual_out_time
            att.matched_status = h.matched_status
            att.attendance_regularize = h.attendance_regularize
            att.save()
            frappe.db.commit()
        delete_core_att = frappe.db.sql("""delete from `tabAttendance` where attendance_date = '%s' and docstatus = '0' """%(from_date))
    else:
        frappe.throw(_("Kindly select the Migration From"))

    return 'ok'
 
