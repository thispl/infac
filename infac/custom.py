from __future__ import print_function
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
from frappe.share import add, remove
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,today, format_date)
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
from frappe import _

#Attendance Automatic to run method 
def create_hooks():
    job = frappe.db.exists('Scheduled Job Type', 'mark_att')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")  
        sjt.update({
            "method" : 'infac.shift_attendance.mark_att',
            "frequency" : 'Cron',
            "cron_format" : '*/15 * * * *'
        })
        sjt.save(ignore_permissions=True)

#Miss Punch Application Mail Alert to HR and HOD
# def create_hooks():
#     job = frappe.db.exists('Scheduled Job Type', 'miss_punch_mail_alert')
#     if not job:
#         sjt = frappe.new_doc("Scheduled Job Type")  
#         sjt.update({
#             "method" : 'infac.email_alerts.miss_punch_mail_alert',
#             "frequency" : 'Cron',
#             "cron_format" : '*/15 * * * *'
#         })
#         sjt.save(ignore_permissions=True)

# @frappe.whitelist()
# def earned_leave():
#     given_date = datetime.today().date()
#     first_day_of_month = given_date.replace(day=1)
#     previous_month = add_months(first_day_of_month,-1)
#     from_date = add_days(previous_month,20)
#     to_date = add_days(first_day_of_month,19)
#     leave_allocation = frappe.db.get_all('Leave Allocation',{'leave_type':'Earned Leave'},['name','employee','new_leaves_allocated'])
#     for leave in leave_allocation:
#         att = frappe.db.get_all('Attendance',{'Status':'Present','attendance_date':('between',(from_date,to_date)),'employee':leave.employee},['employee','status'])
#         value = len(att) // 20
#         new_leave_allocate = leave.new_leaves_allocated + value
#         frappe.db.set_value('Leave Allocation',leave.name,'new_leaves_allocated',new_leave_allocate)
        

# @frappe.whitelist()
# def set_permission():
#     date = '2022-08-20'
#     d = 1
#     for i in range(31):
#         # per = frappe.db.get_all('Permission Request',{'permission_date':date},['employee_id','permission_date','name'])
#         # for p in per:
#         #     att = frappe.db.get_all('Attendance',{'employee':p.employee_id,'attendance_date':p.permission_date},['permission_request','employee','attendance_date'])
#         #     for a in att:
#         #         if a.permission_request is None:
#         #             print(a.employee) 
#         #             print(a.attendance_date)
#         att = frappe.db.get_all('Attendance',{'attendance_date':date,},['name','employee','attendance_date','permission_request'])
#         for a in att:
#             per = frappe.db.get_all('Permission Request',{'permission_date':a.attendance_date,'employee_id':a.employee},['employee_id','permission_date','name'])
#             for p in per:
#                 if a.permission_request != p.name:
#                     frappe.db.set_value('Attendance',a.name,'permission_request',p.name)
#         date = add_days(date,1)
#         d += 1

# @frappe.whitelist()
# def on_duty():
#     date = '2022-05-21'
#     d = 1
#     for i in range(31):
#         att = frappe.db.get_all('Attendance',{'attendance_date':date},['name','employee','attendance_date'])
#         for a in att:
#             on_duty = frappe.db.exists('On Duty Application',{'od_date':date,'employee':a.employee},['employee','od_date'])
#             if on_duty:
#                 frappe.db.set_value('Attendance',a.name,'on_duty_marked',on_duty)
#                 print(on_duty)
#         date = add_days(date,1)
#         d += 1  

# def delete_duplicate_checkins():
#     atts = frappe.db.sql("""select name,time,employee from `tabEmployee Checkin` where date(time) between '2022-03-22' and '2022-03-22' """,as_dict=True)
#     print(len(atts))
#     i = 0
#     for att in atts:
#         count = frappe.db.count("Employee Checkin",{'employee':att.employee,'time':att.time})
#         if count >= 2:
#             print(i)
#             frappe.delete_doc('Employee Checkin',att.name)
#             i += 1
#  if att:
#                     check_shift = frappe.db.get_value('Attendance',att,'actual_shift')
#                     print(check_shift)
#                     if check_shift == y_shift:
#                         frappe.db.set_value('Attendance',att,'out_time',time)
#                         frappe.db.set_value("Employee Checkin",checkin, "attendance", att)
#                         frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
#                     else:
#                         current_day = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=',2)})
#                         if not current_day:
#                             doc = frappe.new_doc('Attendance')
#                             doc.employee = employee
#                             doc.attendance_date = att_date
#                             doc.status = 'Present'
#                             doc.shift = check_shift  
#                             doc.in_time = time
#                             doc.total_wh = ''
#                             doc.extra_hours = ''
#                             doc.late_hours = ''
#                             doc.save(ignore_permissions=True)
#                             frappe.db.commit()
#                             frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
#                             frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
#                         else:
#                             frappe.db.set_value('Attendance',current_day,'out_time',time)
#                             frappe.db.set_value("Employee Checkin",checkin, "attendance", att)
#                             frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')


@frappe.whitelist()
def set_shift():
    att_reg = frappe.db.get_all('Attendance Regularize',{'docstatus':'1'},['corrected_shift','attendance_date','employee'])
    for att in att_reg:
       attendance = frappe.db.exists('Attendance',{'attendance_date':att.attendance_date,'employee':att.employee})
       if attendance:
        status = frappe.db.get_value('Attendance',{'name':attendance},['matched_status'])
        set_status = frappe.db.set_value('Attendance',attendance,'matched_status','Matched')
        print(set_status)

@frappe.whitelist()
def get_month_time():
    payroll_last_day = add_days(get_first_day(today()),19)
    now = datetime.now()
    day = now + dateutil.relativedelta.relativedelta(months=-1)
    payroll_first_day = add_days(get_first_day(day),20)
    print(payroll_first_day)
    print(payroll_last_day)
   
@frappe.whitelist()
def hd_att():
    add_sal = frappe.db.sql(""" update `tabAttendance` set 5_hrs_amount = 0 where attendance_date between '2022-08-21' and '2022-09-20' and employee  = 'S248'   """) 
    print(add_sal) 
    # hd_att = frappe.db.sql(""" delete from  `tabHoliday Attendance` where attendance_date between '2022-11-06' and '2022-11-06' """) 
    # print(hd_att) 

@frappe.whitelist()
def c_shift():
    from_date = '2022-08-21'
    to_date = '2022-09-20'
    att = frappe.db.sql(""" select count(*) from `tabAttendance` where attendance_date between '2022-08-21' and '2022-09-20' and employee = 'CS256' and shift = 'C' """)
    print(att)

@frappe.whitelist()
def holiday_att():
    from_date = '2022-10-24'
    to_date = '2022-10-24'
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date))},['*'])
    for att in attendance:
        hh = check_holiday(att.attendance_date,att.employee)
        if hh:
            hd_att = frappe.db.exists('Holiday Attendance',{'attendance_date':att.attendance_date,'employee':att.employee})
            if not hd_att:
                doc = frappe.new_doc('Holiday Attendance')
                doc.employee = att.employee
                doc.attendance_date = att.attendance_date
                doc.status = att.status
                doc.shift = att.shift
                doc.in_time = att.in_time
                doc.out_time = att.out_time
                doc.total_wh = att.total_wh
                doc.late_hours = att.late_hours
                doc.leave_type = att.leave_type
                doc.leave_application = att.leave_application
                doc.employee_name = att.employee_name
                doc.attendance_request = att.attendance_request
                doc.extra_hours = att.extra_hours
                doc.ot_hrs = att.ot_hrs
                doc.late_hrs = att.late_hrs
                doc.late_deduct = att.late_deduct
                doc.miss_punch_marked = att.miss_punch_marked
                doc.on_duty_marked = doc.on_duty_marked 
                doc.permission_request = att.permission_request
                doc.single_punch_regularization = att.single_punch_regularization
                doc.shift_type = att.shift_type
                doc.shift_in_time = att.shift_in_time
                doc.shift_out_time = att.shift_out_time
                doc.actual_shift = att.actual_shift
                doc.actual_in_time = att.actual_in_time
                doc.actual_out_time = att.actual_out_time
                doc.matched_status = att.matched_status
                doc.attendance_regularize = att.attendance_regularize
                doc.attendance_name = att.name
                doc.save(ignore_permissions=True)
                frappe.db.commit()
                attendance = frappe.db.sql(""" delete from `tabAttendance` where name '%s' """%(att.name))
                    
def check_holiday(date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"


@frappe.whitelist()
def salary_check():
    salary = frappe.db.sql("""  delete from  `tabAttendance`  where  attendance_date between '2022-11-29' and '2022-11-30' and status != 'On Leave'  """)
    # salary_component = frappe.db.sql(""" update `tabSalary Structure` set salary_component = '' where name = 'Diploma Trainees- Structure'  """)
    # at_bonus = frappe.db.sql(""" update  `tabSalary Structure` set salary_slip_based_on_timesheet = 0  where name  = 'Diploma Trainees- Structure' """)
    # print(at_bonus)
    print(salary)
    # print(salary_component)