from __future__ import print_function
from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from decimal import ROUND_UP
from hmac import new
from itertools import count
from lib2to3.pytree import convert
from math import perm
from operator import neg
from pickle import TRUE
from re import A
import time
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



@frappe.whitelist()
def earned_leave():
    given_date = datetime.today().date()
    first_day_of_month = given_date.replace(day=1)
    previous_month = add_months(first_day_of_month,-1)
    from_date = add_days(previous_month,20)
    to_date = add_days(first_day_of_month,19)
    leave_allocation = frappe.db.get_all('Leave Allocation',{'leave_type':'Earned Leave'},['name','employee','new_leaves_allocated'])
    for leave in leave_allocation:
        att = frappe.db.get_all('Attendance',{'Status':'Present','attendance_date':('between',(from_date,to_date)),'employee':leave.employee},['employee','status'])
        value = len(att) // 20
        new_leave_allocate = leave.new_leaves_allocated + value
        frappe.db.set_value('Leave Allocation',leave.name,'new_leaves_allocated',new_leave_allocate)

        
@frappe.whitelist()
def bulk_shift_assignment_from_csv(filename):
    # below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    # Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    # Path in the system
    filepath = get_file(filename)
    # CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    for pp in pps:
        print(pp[0])
        # date = '2022-02-21'
        # d = 1
        # for i in range(31):
        #     print(date)
        #     print(pp[d])
        #     if pp[d] not in ('-',None):
        #         if not frappe.db.exists('Shift Assignment',{'employee':pp[0],'start_date':date}):
        #             doc = frappe.new_doc('Shift Assignment')
        #             doc.employee = pp[0]
        #             doc.start_date = date,
        #             doc.end_date = date
        #             doc.shift_type  = pp[d]
        #             doc.save(ignore_permissions=True)
        #     date = add_days(date,1)
            # d += 1


@frappe.whitelist()
def bulk_shift_assign_cancel(filename):
    from frappe.utils.file_manager import get_file
    _file = frappe.get_doc("File", {"file_name": filename})
    filepath = get_file(filename)
    pps = read_csv_content(filepath[1])
    for pp in pps:
        # print(pp[0])
        # print(pp[1])
        if pp[0] not in ('-',None):
            checkin = frappe.db.sql(""" delete from `tabAttendance`  where attendance_date = '%s'  and employee = '%s'  """%(pp[1],pp[0]),as_dict=1)
            print(checkin)
            # shift = frappe.db.exists('Shift Assignment',{'employee':pp[0],'start_date':pp[1]},['shift_type'])
            # if shift:
            #     print('yes')  
            #     cancel = frappe.db.set_value('Shift Assignment',shift,'docstatus',2)

            # else:
                # print('no')
            #     doc = frappe.new_doc('Shift Assignment')
            #     doc.employee = pp[0]
            #     doc.start_date = pp[1]
            #     doc.end_date = pp[1]
            #     doc.shift_type = pp[2]
            #     doc.save(ignore_permissions=TRUE)


            # print(shift)


#attendance Code Backup
# def mark_wh_ot(from_date,to_date):
#     # from_date = '2022-02-04'
#     # to_date = '2022-02-13'
#     attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['name','shift','in_time','out_time','employee','attendance_date'])
#     for att in attendance:
#         if att.in_time and att.out_time:
#             hh = check_holiday(att.attendance_date,att.employee)
#             if not hh:  
#                 total_wh = att.out_time - att.in_time
#                 ftr = [3600,60,1]
#                 hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
#                 wh = round(hr/3600,1)
#                 if wh < 4:
#                     frappe.db.set_value('Attendance',att.name,'status','Absent')
#                 elif wh >= 4 and wh < 8:
#                    frappe.db.set_value('Attendance',att.name,'status','Half Day')   
#                 elif  wh >= 8:
#                     frappe.db.set_value('Attendance',att.name,'status','Present')
#                 shift_end_time = frappe.db.get_value('Shift Type',att.shift,'end_time')
#                 shift_end_time = pd.to_datetime(str(shift_end_time)).time()
#                 total_late = frappe.db.get_value('Shift Type',att.shift,'start_time')
#                 total_late = pd.to_datetime(str(total_late)).time()
#                 total_shift_hours = frappe.db.get_value('Shift Type',att.shift,'total_hours')
#                 in_date = att.in_time.date()
#                 out_date = att.out_time.date()
#                 shift_end_datetime = datetime.combine(out_date,shift_end_time)
#                 shift_start_datetime = datetime.combine(in_date,total_late)
#                 if shift_end_time:
#                     extra_hrs =pd.to_datetime('00:00:00').time()
#                     ot_hr = 0
#                     if att.out_time > shift_end_datetime:
#                         if total_wh > total_shift_hours:
#                             extra_hrs = att.out_time - shift_end_datetime
#                             hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
#                             extras = round(hr/3600,1)
#                             if extras > 1:
#                                 ot_hr = math.floor(extras * 2) / 2
#                     frappe.db.set_value('Attendance',att.name,'ot_hrs',ot_hr)
#                     frappe.db.set_value('Attendance',att.name,'extra_hours',extra_hrs)
#                     frappe.db.set_value('Attendance',att.name,'total_wh',total_wh)
#                     frappe.db.set_value('Attendance',att.name,'working_hours',wh)
#                 else:
#                     none_time =pd.to_datetime('00:00:00').time()
#                     frappe.db.set_value('Attendance',att.name,'ot_hrs',0)
#                     frappe.db.set_value('Attendance',att.name,'extra_hours',none_time)
#                     frappe.db.set_value('Attendance',att.name,'total_wh',none_time)
#                     frappe.db.set_value('Attendance',att.name,'working_hours',0)
#             else:
#                 total_wh = att.out_time - att.in_time
#                 ftr = [3600,60,1]
#                 hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
#                 wh = round(hr/3600,1)
#                 if wh < 4:
#                     frappe.db.set_value('Attendance',att.name,'status','Absent')
#                 elif wh >= 4 and wh < 8:
#                    frappe.db.set_value('Attendance',att.name,'status','Half Day')   
#                 elif  wh >= 8:
#                     frappe.db.set_value('Attendance',att.name,'status','Present')
#                 if wh > 0:
#                     ot_hr = (math.floor(wh * 2) / 2) - 0.5
#                     frappe.db.set_value('Attendance',att.name,'ot_hrs',ot_hr)
#                     none_time =pd.to_datetime('00:00:00').time()
#                     frappe.db.set_value('Attendance',att.name,'extra_hours',none_time)
#                     frappe.db.set_value('Attendance',att.name,'total_wh',total_wh)
#                     frappe.db.set_value('Attendance',att.name,'working_hours',wh)
#                 else:
#                     none_time =pd.to_datetime('00:00:00').time()
#                     frappe.db.set_value('Attendance',att.name,'ot_hrs',0)
#                     frappe.db.set_value('Attendance',att.name,'extra_hours',none_time)
#                     frappe.db.set_value('Attendance',att.name,'total_wh',none_time)
#                     frappe.db.set_value('Attendance',att.name,'working_hours',0)
#         else:
#             none_time =pd.to_datetime('00:00:00').time()
#             frappe.db.set_value('Attendance',att.name,'extra_hours',none_time)
#             frappe.db.set_value('Attendance',att.name,'total_wh',none_time)


@frappe.whitelist()
def set_permission():
    date = '2022-03-21'
    d = 1
    for i in range(31):
        att = frappe.db.get_all('Attendance',{'attendance_date':date,},['name','employee','attendance_date','permission_request'])
        for a in att:
            on_duty = frappe.db.get_all('On Duty Application',{'od_date':date,},['employee','od_date'])
            for on in on_duty:
                if a.employee == on.employee:
                    [print('yes')]
        date = add_days(date,1)
        d += 1


@frappe.whitelist()
def on_duty():
    date = '2022-05-21'
    d = 1
    for i in range(31):
        att = frappe.db.get_all('Attendance',{'attendance_date':date},['name','employee','attendance_date'])
        for a in att:
            on_duty = frappe.db.exists('On Duty Application',{'od_date':date,'employee':a.employee},['employee','od_date'])
            if on_duty:
                frappe.db.set_value('Attendance',a.name,'on_duty_marked',on_duty)
                print(on_duty)
        date = add_days(date,1)
        d += 1  

@frappe.whitelist()
def attendance():
# # # #     # att = frappe.db.sql(""" select employee,shift_type,actual_shift from `tabAttendance` where attendance_date = '2022-05-23' and matched_status = 'Unmatched' """)
# # # #     # print(att)
    checkins = frappe.db.sql("""  delete from `tabAttendance` where attendance_date between  '2022-06-20' and '2022-07-23' and status!= 'On Leave' """)
    # print(checkins)
    # checkin = frappe.db.sql("""update `tabAttendance` set late_hours = '00:00'    where attendance_date  between '2022-05-21' and '2022-06-20'  and status = 'On Leave' """);
    # print(checkin)
    # att_cancel = frappe.db.sql(""" select count(*) from `tabAttendance`  where attendance_date between '2022-05-21' and '2022-06-20' and status = 'On Leave'  and late_hours > '00:00' """)
    # print(att_cancel)
    # checkin = frappe.db.sql("""  update `tabEmployee Checkin` set attendance = '' where date(time) between  '2022-06-20'  and '2022-07-23' """)
    # print(checkin)
    # checkin_remove = frappe.db.sql(""" select count(*) from  `tabEmployee Checkin`  where date(time) between '2022-06-20' and  '2022-07-23' """)
    # print(checkin_remove)

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
def previous_shift():
    from_date = '2022-07-25'
    week_start = add_days(from_date,-7)
    week_end = add_days(week_start,5)
    print(week_start)
    print(week_end)
   
   