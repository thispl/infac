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
from frappe.utils import time_diff_in_hours 
from frappe.utils.background_jobs import enqueue

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
from frappe.model.rename_doc import rename_doc


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
   
                    
def check_holiday(from_date,to_date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date between '%s' and '%s' """%(holiday_list,from_date,to_date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"
    

@frappe.whitelist()
def error():
    checkin = frappe.db.sql("""delete from `tabError Log` """,as_dict = True)
    print(checkin)

@frappe.whitelist()
def update_ssa():
    emp = frappe.db.sql("""select  * from `tabEmployee` where status = "Active" and employee_category = "NAPS - DAT" and  date_of_joining > "2023-05-21"  """,as_dict = True)
    for e in emp:
        if not frappe.db.exists("Salary Structure Assignment",{'employee':e.name,'docstatus':1}):
            print(e.name,e.date_of_joining)
        else:
            doc = frappe.get_doc("Salary Structure Assignment",{'employee':e.name,'docstatus':1})
            print(doc.employee,doc.base)

@frappe.whitelist()
def enqueue_att_reg_bulk_upload_csv(filename):
    from frappe.utils.background_jobs import enqueue
    frappe.enqueue(
        att_reg_bulk_upload_csv, # python function or a module path as string
        queue="long", # one of short, default, long
        timeout=36000, # pass timeout manually
        is_async=True, # if this is True, method is run in worker
        now=False, # if this is True, method is run directly (not in a worker) 
        job_name='Attendance Regularize', # specify a job name
        enqueue_after_commit=False, # enqueue the job after the database commit is done at the end of the request
        filename=filename, # kwargs are passed to the method as arguments
    )   

@frappe.whitelist()
def att_reg_bulk_upload_csv(filename):
    frappe.errprint("HI")
    from frappe.utils.file_manager import get_file
    _file = frappe.get_doc("File", {"file_url": filename})
    filepath = get_file(filename)
    pps = read_csv_content(filepath[1])
    for pp in pps:
        in_time = '-'
        out_time = '-'
        frappe.errprint(pp[0])
        if frappe.db.exists('Shift Assignment',{'start_date':pp[1],'employee':pp[0],'docstatus':1}):
            shift_assign = frappe.db.get_value('Shift Assignment',{'start_date':pp[1],'employee':pp[0]},['shift_type'])
        else:
            shift_assign = "G"
        shift_start_time = frappe.db.get_value('Shift Type',{'name':shift_assign},['start_time'])
        shift_end_time = frappe.db.get_value('Shift Type',{'name':shift_assign},['end_time'])
        if frappe.db.exists('Attendance',{'employee':pp[0],'attendance_date':pp[1]}):
            if frappe.db.get_value('Attendance',{'employee':pp[0],'attendance_date':pp[1]},['in_time']):
                in_time = frappe.db.get_value('Attendance',{'employee':pp[0],'attendance_date':pp[1]},['in_time']).strftime('%H:%M:%S') 
            else:
                in_time = '-'    
            if frappe.db.get_value('Attendance',{'employee':pp[0],'attendance_date':pp[1]},['out_time']):
                out_time = frappe.db.get_value('Attendance',{'employee':pp[0],'attendance_date':pp[1]},['out_time']).strftime('%H:%M:%S')   
            else:
                out_time = '-'
        elif frappe.db.exists('Holiday Attendance',{'employee':pp[0],'attendance_date':pp[1]}):
            if frappe.db.get_value('Holiday Attendance',{'employee':pp[0],'attendance_date':pp[1]},['in_time']):
                in_time = frappe.db.get_value('Holiday Attendance',{'employee':pp[0],'attendance_date':pp[1]},['in_time']).strftime('%H:%M:%S') 
            else:
                in_time = '-'    
            if frappe.db.get_value('Holiday Attendance',{'employee':pp[0],'attendance_date':pp[1]},['out_time']):
                out_time = frappe.db.get_value('Holiday Attendance',{'employee':pp[0],'attendance_date':pp[1]},['out_time']).strftime('%H:%M:%S')   
            else:
                out_time = '-'
        if not frappe.db.exists('Attendance Regularize',{'employee':pp[0],'attendance_date':pp[1],'docstatus':1}):
            ar = frappe.new_doc('Attendance Regularize')
            ar.employee = pp[0]
            ar.attendance_date = pp[1]
            ar.assigned_shift = shift_assign
            ar.shift_in_time = shift_start_time
            ar.shift_out_time = shift_end_time
            ar.first_in_time = in_time
            ar.last_out_time = out_time
            ar.corrected_in = pp[2]
            ar.corrected_out = pp[3]
            ar.corrected_shift = pp[4]
            ar.save(ignore_permissions=True)
            ar.submit()
            frappe.db.commit()    
    return 'ok'  
    
# @frappe.whitelist()
# def inactive_employee(doc,method):
#     if doc.status=="Active":
#         if doc.relieving_date:
#             throw(_("Please remove the relieving date for the Active Employee."))

# @frappe.whitelist()
# def update_employee_no(name,employee_number):
#     emp = frappe.get_doc("Employee",name)
#     emps=frappe.get_all("Employee",{"status":"Active"},['*'])
#     for i in emps:
#         if emp.employee_number == employee_number:
#             pass
#         elif i.employee_number == employee_number:
#             frappe.throw(f"Employee Number already exists for {i.name}")
#         else:
#             frappe.db.set_value("Employee",name,"employee_number",employee_number)
#             frappe.rename_doc("Employee", name, employee_number, force=1)
#             return employee_number


@frappe.whitelist()
def find_department():
    emp =frappe.get_all("Employee",{'status':"Left"},['*'])
    for e in emp:
        if not frappe.db.exists("Department",{'name':e.department}):
            print(e.name)

@frappe.whitelist()
def update_ec_att():
    ec = frappe.db.sql("""update `tabEmployee Checkin` set skip_auto_attendance = 0 where date(time) between "2023-11-21" and "2023-12-21"  """,as_dict = True)
    print(ec)
    ec = frappe.db.sql("""update `tabEmployee Checkin` set attendance = 0 where date(time) between "2023-11-21" and "2023-12-21"  """,as_dict = True)
    print(ec)

@frappe.whitelist()

def mark_late_exit():
    from_date = '2024-07-25'
    to_date = '2024-07-25'
    employee = 'E2014'
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2'),'employee':employee},['*'])
    frappe.errprint(attendance)
    for att in attendance:
        if att.attendance_regularize:
            if not att.leave_application:
                if att.permission_request:
                    if not att.on_duty_marked:
                        if not att.miss_punch_marked:
                            if att.in_time and att.out_time:
                                shift_end_time = frappe.db.get_value('Shift Type', att.shift, 'end_time')
                                shift_start_time = frappe.db.get_value('Shift Type', att.shift, 'start_time')
                                
                                if shift_end_time and shift_start_time:
                                    shift_end_time = pd.to_datetime(str(shift_end_time)).time()
                                    shift_start_time = pd.to_datetime(str(shift_start_time)).time()
                                    frappe.errprint(shift_end_time)

                                    in_date = att.in_time.date()
                                    out_date = att.out_time.date()
                                    shift_end_datetime = datetime.combine(out_date, shift_end_time)
                                    out_time = frappe.utils.get_datetime(att.out_time)
                                    frappe.errprint(out_time)

                                    shift_actual_out_time=datetime.combine(out_date, shift_end_time)
                                    frappe.errprint(shift_actual_out_time)
                                    early_exit_duration = shift_actual_out_time - out_time
                                    frappe.errprint(early_exit_duration)
                                    # new_var = time_diff_in_hours(shift_actual_out_time,out_time)
                                    # frappe.errprint(new_var)
                                    hours = frappe.db.get_value('Permission Request',{'name':att.permission_request,'session':'Second Half'},'hours')
                                    
                                    if att.permission_request and hours:
                                        time_parts = list(map(int, hours.split(':')))
                                        hours = timedelta(hours=time_parts[0], minutes=time_parts[1], seconds=time_parts[2])
                                        frappe.errprint(hours)
                                        if ((hours.seconds//60)%60) <= ((early_exit_duration.seconds//60)%60):
                                            frappe.db.set_value('Attendance',att.name,'early_exit_time','00:00')
                                            frappe.db.set_value('Attendance', att.name, 'early_exit_hours','')
                                            frappe.db.set_value('Attendance',att.name,'early_exit',0)
                                            frappe.errprint("Permission")
                                            # early_exit_duration = early_exit_duration - hours
                                            # frappe.errprint(early_exit_duration)
                                        else:
                                            early_exit_duration = early_exit_duration - hours
                                            if early_exit_duration.total_seconds() > 0:
                                                late_deduct_hour = early_exit_duration.seconds//3600
                                                frappe.errprint(late_deduct_hour)
                                                late_deduct_minute = ((early_exit_duration.seconds//60)%60)
                                                frappe.errprint(late_deduct_minute)
                                                deducted_minute = late_deduct_minute
                                                deducted_hour = late_deduct_hour
                                                if 1 <= late_deduct_minute <= 5:
                                                    deducted_minute = 5
                                                elif 6 <= late_deduct_minute <= 10:
                                                    deducted_minute = 10
                                                elif 11 <= late_deduct_minute <= 15:
                                                    deducted_minute = 15
                                                elif 16 <= late_deduct_minute <= 20:
                                                    deducted_minute = 20
                                                elif 21 <= late_deduct_minute <= 25:
                                                    deducted_minute = 25
                                                elif 26 <= late_deduct_minute <= 30:
                                                    deducted_minute = 30
                                                elif 31 <= late_deduct_minute <= 35:
                                                    deducted_minute = 35
                                                elif 36 <= late_deduct_minute <= 40:
                                                    deducted_minute = 40
                                                elif 41 <= late_deduct_minute <= 45:
                                                    deducted_minute = 45
                                                elif 46 <= late_deduct_minute <= 50:
                                                    deducted_minute = 50
                                                elif 51 <= late_deduct_minute <= 55:
                                                    deducted_minute = 55
                                                elif 56 <= late_deduct_minute <= 60:
                                                    deducted_hour = late_deduct_hour + 1
                                                    deducted_minute = 0
                                                
                                                
                                                frappe.errprint(deducted_hour)
                                                frappe.errprint(deducted_minute)
                                                late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute)
                                                
                                                frappe.errprint(late_deducted_time)
                                                frappe.db.set_value('Attendance',att.name,'early_exit_time',early_exit_duration)
                                                frappe.db.set_value('Attendance', att.name, 'early_exit_hours', late_deducted_time)
                                                frappe.db.set_value('Attendance',att.name,'early_exit',1)
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Present')
                                            
                                        
                
                                    else:
                                        if early_exit_duration.total_seconds() > 0:
                                                late_deduct_hour = early_exit_duration.seconds//3600
                                                frappe.errprint(late_deduct_hour)
                                                late_deduct_minute = ((early_exit_duration.seconds//60)%60)
                                                frappe.errprint(late_deduct_minute)
                                                deducted_minute = late_deduct_minute
                                                deducted_hour = late_deduct_hour
                                                if 1 <= late_deduct_minute <= 5:
                                                    deducted_minute = 5
                                                elif 6 <= late_deduct_minute <= 10:
                                                    deducted_minute = 10
                                                elif 11 <= late_deduct_minute <= 15:
                                                    deducted_minute = 15
                                                elif 16 <= late_deduct_minute <= 20:
                                                    deducted_minute = 20
                                                elif 21 <= late_deduct_minute <= 25:
                                                    deducted_minute = 25
                                                elif 26 <= late_deduct_minute <= 30:
                                                    deducted_minute = 30
                                                elif 31 <= late_deduct_minute <= 35:
                                                    deducted_minute = 35
                                                elif 36 <= late_deduct_minute <= 40:
                                                    deducted_minute = 40
                                                elif 41 <= late_deduct_minute <= 45:
                                                    deducted_minute = 45
                                                elif 46 <= late_deduct_minute <= 50:
                                                    deducted_minute = 50
                                                elif 51 <= late_deduct_minute <= 55:
                                                    deducted_minute = 55
                                                elif 56 <= late_deduct_minute <= 60:
                                                    deducted_hour = late_deduct_hour + 1
                                                    deducted_minute = 0
                                                
                                                
                                                frappe.errprint(deducted_hour)
                                                frappe.errprint(deducted_minute)
                                                late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute)
                                                
                                                frappe.errprint(late_deducted_time)
                                                frappe.db.set_value('Attendance',att.name,'early_exit_time',early_exit_duration)
                                                frappe.db.set_value('Attendance', att.name, 'early_exit_hours', late_deducted_time)
                                                frappe.db.set_value('Attendance',att.name,'early_exit',1)
                                                frappe.db.set_value('Attendance', att.name, 'status', 'Present')
                                            
                                        
                                    #     frappe.db.set_value('Attendance',att.name,'early_exit_time','00:00')
                                    #     frappe.db.set_value('Attendance', att.name, 'early_exit_hours','')
                                    #     frappe.db.set_value('Attendance',att.name,'early_exit',0)
                
                        else:
                            frappe.db.set_value('Attendance',att.name,'early_exit_time','00:00')
                            frappe.db.set_value('Attendance', att.name, 'early_exit_hours','')
                            frappe.db.set_value('Attendance',att.name,'early_exit',0)
                    else:
                        frappe.db.set_value('Attendance',att.name,'early_exit_time','00:00')
                        frappe.db.set_value('Attendance', att.name, 'early_exit_hours','')
                        frappe.db.set_value('Attendance',att.name,'early_exit',0)
                
            else:
                frappe.db.set_value('Attendance',att.name,'early_exit_time','00:00')
                frappe.db.set_value('Attendance', att.name, 'early_exit_hours','')
                frappe.db.set_value('Attendance',att.name,'early_exit',0)
        # else:
        #     frappe.db.set_value('Attendance',att.name,'early_exit_time','00:00')
        #     frappe.db.set_value('Attendance', att.name, 'early_exit_hours', '')
        #     frappe.db.set_value('Attendance',att.name,'early_exit',0)
    return "ok"

# @frappe.whitelist()
# def update_actual_shift(doc,method):
#     if doc.docstatus==0:
#         if doc.shift:
#             doc.actual_shift=doc.shift


@frappe.whitelist()
def update_reg():
    att=frappe.db.get_all('Attendance',{'attendance_date':('between',('2025-08-07','2025-08-08'))},['in_time','out_time','name'])
    for a in att:
        if a.in_time and a.out_time:
            if a.in_time > a.out_time:
                print(a.name)


# @frappe.whitelist()
# def validate_leave(doc, method):
#     user_roles = frappe.get_roles(frappe.session.user)
#     hr = "HR User" in user_roles
#     # admin = "Administrator" in user_roles
#     if (not hr):
#         allowed_days1 = frappe.db.get_value("HR Time Settings", None, "leave_validation_dates")
#         allowed_days = int(allowed_days1 or 0)
#         current_date = today()
#         if isinstance(current_date, str):
#             current_date = datetime.strptime(current_date, "%Y-%m-%d").date()

#         def is_working_day(check_date):
#             return not check_holiday(check_date,check_date, doc.employee)

#         days_count = 0
#         earliest_allowed = current_date
#         while days_count < allowed_days:
#             earliest_allowed = add_days(earliest_allowed, -1)
#             if is_working_day(earliest_allowed):
#                 days_count += 1

#         if not doc.to_date:
#             return

#         if isinstance(doc.to_date, str):
#             miss_date = datetime.strptime(doc.to_date, "%Y-%m-%d").date()
#         else:
#             miss_date = doc.to_date

#         if miss_date < earliest_allowed:
#             frappe.throw(
#                 _("Leave applications are allowed only for up to the previous {0} working days.")
#                 .format(allowed_days)
#             )


# @frappe.whitelist()
# def validate_comp_off(doc, method):
#         user_roles = frappe.get_roles(frappe.session.user)
#         hr = "HR User" in user_roles
#         # admin = "Administrator" in user_roles
#         if (not hr):
#             allowed_days1 = frappe.db.get_value("HR Time Settings", None, "comp_off_validation_dates")
#             allowed_days = int(allowed_days1 or 0)
#             current_date = today()
#             if isinstance(current_date, str):
#                 current_date = datetime.strptime(current_date, "%Y-%m-%d").date()

#             def is_working_day(check_date):
#                 return not check_holiday(check_date,check_date, doc.employee)

#             days_count = 0
#             earliest_allowed = current_date
#             while days_count < allowed_days:
#                 earliest_allowed = add_days(earliest_allowed, -1)
#                 if is_working_day(earliest_allowed):
#                     days_count += 1

#             if not doc.work_from_date:
#                 return

#             if isinstance(doc.work_from_date, str):
#                 miss_date = datetime.strptime(doc.work_from_date, "%Y-%m-%d").date()
#             else:
#                 miss_date = doc.work_from_date

#             if miss_date < earliest_allowed:
#                 frappe.throw(
#                     _("Compensatory Leave Request applications are allowed only for up to the previous {0} working days.")
#                     .format(allowed_days)
#                 )


# @frappe.whitelist()
# def create_scheduled_job_1():
#     job = frappe.db.exists('Scheduled Job Type', 'auto_approve_permission')
#     if not job:
#         emc = frappe.new_doc("Scheduled Job Type")
#         emc.update({
#             "method": 'infac.mail_alerts_custom.auto_approve_permission',
#             "frequency": 'Cron',
#             "cron_format": '50 14 * * *'
#         })
#         emc.save(ignore_permissions=True)

# create Schedule Job Type
@frappe.whitelist()
def create_schedule_job_type():
	job = frappe.db.exists('Scheduled Job Type', 'process_today_checkins_fast')
	if not job:
		sjt = frappe.new_doc("Scheduled Job Type")
		sjt.update({
			"method": 'infac.mail_alerts_custom.process_today_checkins_fast',
			"frequency": 'Cron',
			"cron_format": '*/30 * * * *'
		})
		sjt.save(ignore_permissions=True)

# @frappe.whitelist()
# def cron_failed_method():
#     cutoff_time = datetime.now() - timedelta(minutes=5)
#     failed_jobs = frappe.get_all(
#         "Scheduled Job Log",
#         filters={
#             "status": "Failed",
#             "creation": [">=", cutoff_time],
#             "scheduled_job_type": ["!=", "video.update_youtube_data"]
#         },
#         fields=["scheduled_job_type"]
#     )
#     unique_job_types = set()
#     for job in failed_jobs:
#         unique_job_types.add(job['scheduled_job_type'])

#     for job_type in unique_job_types:
#         frappe.sendmail(
#             recipients = ["jenisha.p@groupteampro.com","pavithra.s@groupteampro.com","gifty.p@groupteampro.com","sivarenisha.m@groupteampro.com"],
#             subject = 'Failed Cron List - INFAC',
#             message = 'Dear Sir / Mam <br> Kindly find the below failed Scheduled Job  %s'%(job_type)
#         )
from datetime import datetime, time, timedelta
@frappe.whitelist()
def to_time(value):
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return time(hour=hours, minute=minutes, second=seconds)
    elif isinstance(value, time):
        return value
    else:
        raise TypeError(f"Expected time or timedelta, got {type(value)}")

# @frappe.whitelist() 
# def mark_wh_ot_new():
#     # from_date=add_days(from_date,-1)
#     attendance = frappe.db.get_all('Attendance',{'name':'HR-ATT-2025-185012'},['name'])
#     for a in attendance:
#         att=frappe.get_doc('Attendance',a.name)        
#         att_status =''
#         total_wh = '00:00'
#         wh ='00:00'
#         late_hr = ''
#         late_hour ='00:00'
#         late_deduct = ''
#         late_entry = 0
#         ot_hr = '0'
#         extra_hrs = '00:00'

#         doj=frappe.db.get_value('Employee',{'name':att.employee},['date_of_joining'])
#         if att.attendance_date >= getdate(doj):
#             if att.miss_punch_marked:
#                 miss_p=frappe.get_doc('Miss Punch Application',att.miss_punch_marked)
#                 frappe.db.set_value('Attendance',att.name,'in_time',miss_p.in_time)
#                 frappe.db.set_value('Attendance',att.name,'out_time',miss_p.out_time)
#             if att.attendance_regularize:
#                 att_reg=frappe.get_doc('Attendance Regularize',att.attendance_regularize)
#                 frappe.db.set_value('Attendance',att.name,'in_time',att_reg.corrected_in)
#                 frappe.db.set_value('Attendance',att.name,'out_time',att_reg.corrected_out)
#                 frappe.db.set_value('Attendance',att.name,'shift',att_reg.corrected_shift)
#             if not att.leave_application:
#                 if att.in_time and att.out_time and att.shift:
#                     in_time = att.in_time
#                     out_time = att.out_time
                    

#                     if att.on_duty_marked and not att.attendance_regularize:
#                         od = frappe.get_doc('On Duty Application', att.on_duty_marked)

#                         in_time_val = to_time(od.in_time)
#                         out_time_val = to_time(od.out_time)

#                         if od.shift in ['G', 'A', 'B']:
#                             od_in = datetime.combine(od.od_date, in_time_val)
#                             od_out = datetime.combine(od.od_date, out_time_val)
#                         else:
#                             if in_time_val < time(6, 0, 0):
#                                 od_in = datetime.combine(add_days(od.od_date, 1), in_time_val)
#                                 od_out = datetime.combine(add_days(od.od_date, 1), out_time_val)
#                             elif out_time_val < time(6, 0, 0):
#                                 od_in = datetime.combine(od.od_date, in_time_val)
#                                 od_out = datetime.combine(add_days(od.od_date, 1), out_time_val)
#                             else:
#                                 od_in = datetime.combine(od.od_date, in_time_val)
#                                 od_out = datetime.combine(od.od_date, out_time_val)

#                         if od_in < in_time:
#                             in_time = od_in
#                         if od_out > out_time:
#                             out_time = od_out

#                     if att.permission_request:
#                         perm=frappe.get_doc('Permission Request',att.permission_request)
#                         in_time_val = to_time(perm.from_time)
#                         out_time_val = to_time(perm.to_time)
#                         if perm.session=='First Half':
#                             perm_in=datetime.combine(perm.permission_date,in_time_val)
#                             if perm_in < in_time:
#                                 in_time=perm_in
#                         else:
#                             if perm.shift=='C':
#                                 perm_out=datetime.combine(add_days(perm.permission_date,1),out_time_val)
#                             else:
#                                 perm_out=datetime.combine(perm.permission_date,out_time_val)
#                             if perm_out > out_time:
#                                 out_time=perm_out
#                     hh = check_holiday(att.attendance_date,att.attendance_date, att.employee)
#                     if not hh:
#                         total_wh = out_time - in_time
#                         wh = time_diff_in_hours(out_time, in_time)

#                         att_status='Absent'
#                         if wh < 4.0:
#                             att_status='Absent'
#                         elif 4.0 <= wh < 6.0:
#                             att_status='Half Day'
#                         elif wh >= 6.0:
#                             att_status='Present'
                        
#                         shift_end_time = frappe.db.get_value('Shift Type', att.shift, 'end_time')
#                         shift_end_time = pd.to_datetime(str(shift_end_time)).time()
#                         shift_start_time = frappe.db.get_value('Shift Type', att.shift, 'start_time')
#                         shift_start_time = pd.to_datetime(str(shift_start_time)).time()
#                         total_shift_hours = frappe.db.get_value('Shift Type', att.shift, 'total_hours')
#                         in_date = in_time.date()
#                         out_date = out_time.date()

#                         if att.shift == 'C':
#                             shift_end_datetime = datetime.combine(add_days(in_date,1),shift_end_time)
#                         else:
#                             shift_end_datetime = datetime.combine(in_date,shift_end_time)
#                         shift_start_datetime = datetime.combine(in_date, shift_start_time)

#                         if shift_start_datetime:
#                             late_hour = pd.to_datetime('00:00:00').time()
#                             late_hr = 0
#                             if in_time > shift_start_datetime and att.status == "Present":
#                                 late_hour = in_time - shift_start_datetime
#                                 late_hr = time_diff_in_hours(in_time, shift_start_datetime)
                                
#                             else:
#                                 late_hr='0.0'
#                                 late_hour='00:00'
                               
#                             actual_late_hour = frappe.db.get_value('Attendance', att.name, 'late_hours')
#                             if actual_late_hour:
#                                 late_deduct_hour = actual_late_hour.seconds // 3600
#                                 late_deduct_minute = ((actual_late_hour.seconds // 60) % 60)
#                                 deducted_minute = late_deduct_minute
#                                 deducted_hour = late_deduct_hour

#                                 if 1 <= late_deduct_minute <= 5:
#                                     deducted_minute = 5
#                                 elif 6 <= late_deduct_minute <= 10:
#                                     deducted_minute = 10
#                                 elif 11 <= late_deduct_minute <= 15:
#                                     deducted_minute = 15
#                                 elif 16 <= late_deduct_minute <= 20:
#                                     deducted_minute = 20
#                                 elif 21 <= late_deduct_minute <= 25:
#                                     deducted_minute = 25
#                                 elif 26 <= late_deduct_minute <= 30:
#                                     deducted_minute = 30
#                                 elif 31 <= late_deduct_minute <= 35:
#                                     deducted_minute = 35
#                                 elif 36 <= late_deduct_minute <= 40:
#                                     deducted_minute = 40
#                                 elif 41 <= late_deduct_minute <= 45:
#                                     deducted_minute = 45
#                                 elif 46 <= late_deduct_minute <= 50:
#                                     deducted_minute = 50 
#                                 elif 51 <= late_deduct_minute <= 55:
#                                     deducted_minute = 55    
#                                 elif 56 <= late_deduct_minute <= 60:
#                                     deducted_hour = late_deduct_hour + 1
#                                     deducted_minute = 0

#                                 late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute) + ':00'
#                                 get_late_time = datetime.strptime(str(late_deducted_time), '%H:%M:%S')
#                                 late_deduct = get_late_time.strftime('%H:%M')
#                                 late_deduct=late_deduct
#                                 late_entry=1
#                                 att_status='Present'
#                         if shift_end_datetime:
#                             if out_time > shift_end_datetime:
#                                 extra_hrs = out_time - shift_end_datetime
#                                 extras = time_diff_in_hours(out_time, shift_end_datetime)
#                                 if extras > 1.0:
#                                     ot_hr = math.floor(extras * 2) / 2
#                                 else:
#                                     ot_hr=0                                   
#                             else:
#                                 ot_hr=0
#                                 extra_hrs='00:00'                          
#                     else:
#                         total_wh = out_time - in_time
#                         wh = time_diff_in_hours(out_time, in_time)
#                         frappe.db.set_value('Attendance', att.name, 'status', 'Present')
#                         if wh > 0:
#                             ot_hr = (math.floor(wh * 2) / 2) - 0.5  
#                             extra_hrs=total_wh
#                             total_wh=total_wh
#                         else:
#                             ot_hr=0
#                             extra_hrs='00:00'
#                             total_wh='00:00'
#                             wh=0
#                 else:
#                     ot_hr=0
#                     extra_hrs='00:00'
#                     total_wh='00:00'
#                     wh=0
#                     att_status='Absent'
#                 frappe.db.set_value("Attendance",att.name, "total_wh", total_wh)
#                 frappe.db.set_value("Attendance",att.name, "working_hours", wh)
#                 frappe.db.set_value("Attendance",att.name, "status", att_status)
#                 frappe.db.set_value("Attendance",att.name, "late_hrs", late_hr)
#                 frappe.db.set_value("Attendance",att.name, "late_hours", late_hour)
#                 frappe.db.set_value("Attendance",att.name, "late_deduct", late_deduct)
#                 frappe.db.set_value("Attendance",att.name, "late_entry", late_entry)
#                 frappe.db.set_value("Attendance",att.name, "ot_hrs", ot_hr)
#                 frappe.db.set_value("Attendance",att.name, "extra_hours", extra_hrs)

# @frappe.whitelist()
# def add_salary_history(doc, method):
#     """Add a new row to Salary History when any salary component changes.
#     Works for manual updates and bulk import."""
#     # if not doc.get("__islocal__"):
#     #     salary_fields = [
#     #         "basic", "hra", "gross_salary", "special_allowance", "conveyance_allowance",
#     #         "welfare_allowance_amount", "attendance_bonus", "higher_education_allowance_amount",
#     #         "supr_allowance", "other_allowances", "proposed_salary", "performance_allowance",
#     #         "medical_allowance", "heat_allowance", "grade_allowance", "fixed_salary", "washing_allowance" ]
#     #     updated = False
#     #     for f in salary_fields:
#     #         if f in doc.changed_values:
#     #             updated = True
#     #             break
#     #     if updated:
#     #         row = doc.append("salary_history", {})
#     #         row.effective_date = frappe.utils.nowdate()
#     #         row.basic = doc.basic or 0
#     #         row.hra = doc.hra or 0
#     #         row.gross_salary = doc.gross_salary or 0
#     #         row.special_allowance = doc.special_allowance or 0
#     #         row.conveyance_allowance = doc.conveyance_allowance or 0
#     #         row.welfare_allowance = doc.welfare_allowance_amount or 0
#     #         row.attendance_bonus = doc.attendance_bonus or 0
#     #         row.higher_education_allowance = doc.higher_education_allowance_amount or 0
#     #         row.supervisory_allowance = doc.supr_allowance or 0
#     #         row.other_allowance = doc.other_allowances or 0
#     #         row.proposed_salary = doc.proposed_salary or 0
#     #         row.performance_allowance = doc.performance_allowance or 0
#     #         row.medical_allowance = doc.medical_allowance or 0
#     #         row.heat_allowance = doc.heat_allowance or 0
#     #         row.grade_allowance = doc.grade_allowance or 0
#     #         row.fixed_salary = doc.fixed_salary or 0
#     #         row.washing_allowance = doc.washing_allowance or 0
#     # if doc.get("__islocal__"):
#     if not doc.name or doc.is_new():
#         return
    
#     else:
#         salary_fields = [
#             "basic", "hra", "gross_salary", "special_allowance", "conveyance_allowance",
#             "welfare_allowance_amount", "attendance_bonus", "higher_education_allowance_amount",
#             "supr_allowance", "other_allowances", "proposed_salary", "performance_allowance",
#             "medical_allowance", "heat_allowance", "grade_allowance", "fixed_salary", "washing_allowance"
#         ]

#         old_doc = frappe.get_doc("Employee", doc.name)
#         updated = False
#         for f in salary_fields:
#             old_value = old_doc.get(f) or 0
#             new_value = doc.get(f) or 0
#             if old_value != new_value:
#                 updated = True
#                 break
#         if updated:
#             row = doc.append("salary_history", {})
#             row.effective_date = nowdate()
#             for f in salary_fields:
#                 row.set(f, old_doc.get(f) or 0)

@frappe.whitelist()
def submit_attendance():
    from_date = "2025-10-11"
    to_date = "2025-10-20"

    attendances = frappe.get_all(
        "Attendance",
        filters={
            "attendance_date": ["between", [from_date, to_date]],
            "docstatus": 0
        },
        pluck="name"
    )

    print(f"Found {len(attendances)} draft Attendance records between {from_date} and {to_date}")

    for name in attendances:
        try:
            doc = frappe.get_doc("Attendance", name)
            doc.submit()
            frappe.db.commit()
            print(f"Submitted: {name}")
        except Exception as e:
            print(f"Error submitting {name}: {e}")

    print("Done submitting all draft Attendance records!")

@frappe.whitelist()
def rename_department_enqueue():
    frappe.enqueue(
        method=rename_department,
        queue='long',
        timeout=3600, 
        job_name='Rename Department - Background Job'
    )
    return "Rename process started in background. Check background jobs for status."


@frappe.whitelist()
def rename_department():
    rename_doc("Department", "Production - INFAC", "Production", force=True)
    frappe.db.commit() 
    return "Rename Completed"



# @frappe.whitelist()
# def show_html(from_date=None, to_date=None):
#     html = "<h2><center>Leave Application</center></h2><table class='table table-bordered'><tr><th style=font-size:16px;>From Date</th><th style=font-size:16px;>To Date</th></tr><tr><td><h3>%s</h3></td><td><h3>%s</h3></td></tr></table>" % (
#         frappe.utils.format_date(from_date),
#         frappe.utils.format_date(to_date)
#     )
#     return html


@frappe.whitelist()
def delete_duplicate_data():
    today = frappe.utils.nowdate()

    duplicate_groups = frappe.db.sql("""
        SELECT 
            employee,
            DATE_FORMAT(time, '%%H:%%i:%%s') AS time_only,
            COUNT(*) AS cnt
        FROM `tabEmployee Checkin`
        WHERE DATE(time) = %s
          AND log_type != ''
        GROUP BY employee, time_only
        HAVING cnt > 1
    """, (today,), as_dict=True)

    if not duplicate_groups:
        return "No duplicates found."

    for group in duplicate_groups:
        emp = group.employee
        time_only = group.time_only

        entries = frappe.db.sql("""
            SELECT name
            FROM `tabEmployee Checkin`
            WHERE employee = %s
              AND DATE_FORMAT(time, '%%H:%%i:%%s') = %s
              AND DATE(time) = %s
            ORDER BY name ASC
        """, (emp, time_only, today), as_dict=True)

        
        to_delete = [e.name for e in entries[1:]]  

        if to_delete:
            print(to_delete)
            for i in to_delete:
                checkin=frappe.get_doc("Employee Checkin",i)
                checkin.delete()
                # frappe.db.delete("Employee Checkin", {"name": ["in", to_delete]})

    frappe.db.commit()
    return "Duplicate check-ins removed successfully."


@frappe.whitelist()
def delete_duplicate_data_checkin():
    from_date = "2025-12-23"
    to_date   = "2025-12-24"
    duplicate_groups = frappe.db.sql("""
        SELECT 
            employee,
            DATE(time) AS check_date,
            DATE_FORMAT(time, '%%H:%%i:%%s') AS time_only,
            COUNT(*) AS cnt
        FROM `tabEmployee Checkin`
        WHERE DATE(time) BETWEEN %s AND %s
          AND log_type != ''
        GROUP BY employee, check_date, time_only
        HAVING cnt > 1
    """, (from_date, to_date), as_dict=True)

    if not duplicate_groups:
        return "No duplicates found."

    total_deleted = 0
    for group in duplicate_groups:
        emp = group.employee
        check_date = group.check_date
        time_only = group.time_only

        entries = frappe.db.sql("""
            SELECT name, time
            FROM `tabEmployee Checkin`
            WHERE employee = %s
              AND DATE(time) = %s
              AND DATE_FORMAT(time, '%%H:%%i:%%s') = %s
            ORDER BY time ASC
        """, (emp, check_date, time_only), as_dict=True)
        # print(entries)
        for e in entries[1:]:
            frappe.delete_doc("Employee Checkin", e.name, force=1)
            # print(e.name)
            total_deleted += 1
            

    frappe.db.commit()
    return f"Duplicate check-ins removed successfully. Deleted: {total_deleted}"

from frappe.utils import get_datetime

@frappe.whitelist()
def update_shift_in_checkin(doc, method):

    dt = get_datetime(doc.time)

    start_of_day = datetime.combine(dt.date(), datetime.min.time())
    end_of_day = datetime.combine(dt.date(), datetime.max.time())

    # get all checkins for the day
    checkins = frappe.db.get_all(
        "Employee Checkin",
        filters={
            "log_type": "IN",
            "time": ["between", [start_of_day, end_of_day]],
            "employee":doc.employee
        },
        fields=["name", "time", "late_entry"],
        order_by="time asc"
    )

    if not checkins:
        return

    # first IN
    first_in = checkins[0]

    # reset late entry for remaining INs
    for c in checkins[1:]:
        if c.late_entry == 1:
            frappe.db.set_value("Employee Checkin", c.name, "late_entry", 0)

    frappe.errprint(first_in.name)
    f_in = frappe.get_doc("Employee Checkin", first_in.name)
    f_time = get_datetime(f_in.time)
    att_time = f_time.time()

    shift = get_actual_shift_start(att_time)
    f_in.shift = shift

    if shift:
        shift_start = frappe.db.get_value("Shift Type", shift, "start_time")

        if isinstance(shift_start, timedelta):
            shift_start_time = (datetime.min + shift_start).time()
        else:
            shift_start_time = shift_start

        grace_time = (
            datetime.combine(f_time.date(), shift_start_time) +
            timedelta(minutes=1)
        ).time()

        f_in.late_entry = 1 if att_time >= grace_time else 0

    
    f_in.save(ignore_permissions=True)
    f_in.reload()


@frappe.whitelist()
def get_actual_shift_start(get_shift_time):
    shift1 = frappe.db.get_value('Shift Type',{'name':'A'},['checkin_start_time','checkin_end_time'])
    shift2 = frappe.db.get_value('Shift Type',{'name':'B'},['checkin_start_time','checkin_end_time'])
    shift3 = frappe.db.get_value('Shift Type',{'name':'C'},['checkin_start_time','checkin_end_time'])
    shift4 = frappe.db.get_value('Shift Type',{'name':'G'},['checkin_start_time','checkin_end_time'])
    att_time_seconds = get_shift_time.hour * 3600 + get_shift_time.minute * 60 + get_shift_time.second
    shift = ''
    if shift4[0].total_seconds() < att_time_seconds < shift4[1].total_seconds():
        shift = 'G'
    elif (shift1[0].total_seconds() < att_time_seconds < shift1[1].total_seconds()):
        shift = 'A'
    elif shift2[0].total_seconds() < att_time_seconds < shift2[1].total_seconds():
        shift = 'B'
    elif shift3[0].total_seconds() < att_time_seconds < shift3[1].total_seconds():
        shift = 'C'
    
    return shift

# def update_status_on_workflow(doc, method):

#     if doc.workflow_state == "Approved":
#         doc.status = "Approved"
#     elif doc.workflow_state == "Rejected":
#         doc.status = "Rejected"

# def while_cancel(doc, method):
#     doc.status = "Cancelled"
#     doc.db_update()

@frappe.whitelist()
def process_today_checkins_fast():
    from datetime import datetime, timedelta
    from frappe.utils import today, get_datetime

    dt = get_datetime(today())
    start_of_day = datetime.combine(dt.date(), datetime.min.time())
    end_of_day = datetime.combine(dt.date(), datetime.max.time())

    # Efficient SQL query instead of get_all
    records = frappe.db.sql("""
        SELECT name, employee, time, late_entry
        FROM `tabEmployee Checkin`
        WHERE log_type = 'IN'
        AND time BETWEEN %s AND %s
        ORDER BY employee ASC, time ASC
    """, (start_of_day, end_of_day), as_dict=True)

    if not records:
        return "No checkins today"

    current_emp = None
    first_done = False

    for r in records:
        # New employee block
        if r.employee != current_emp:
            current_emp = r.employee
            first_done = False

        # First IN
        if not first_done:
            first_done = True

            f_time = get_datetime(r.time)
            att_time = f_time.time()

            # Get shift
            shift = get_actual_shift_start(att_time)
            ass_shift = frappe.db.get_value("Shift Assignment",{"employee": r.employee, "start_date": ["<=", f_time.date()],"end_date": [">=", f_time.date()],"docstatus": 1 },"shift_type")

            existing_shift = frappe.db.get_value("Employee Checkin", r.name, "shift")

            # Only set if shift is found AND field is empty
            # if shift and not existing_shift:
            frappe.db.set_value("Employee Checkin", r.name, "shift", shift)
                
            frappe.db.set_value("Employee Checkin", r.name, "assigned_shift", ass_shift)

            # Compute late entry
            if shift:
                shift_start = frappe.db.get_value("Shift Type", shift, "start_time")

                if isinstance(shift_start, timedelta):
                    shift_start_time = (datetime.min + shift_start).time()
                else:
                    shift_start_time = shift_start

                grace_time = (
                    datetime.combine(f_time.date(), shift_start_time) +
                    timedelta(minutes=1)
                ).time()

                is_late = 1 if att_time >= grace_time else 0

                frappe.db.set_value("Employee Checkin", r.name, "late_entry", is_late)

        # Remaining INs
        # else:
        #     frappe.db.set_value("Employee Checkin", r.name, {
        #         "late_entry": 0,
        #         "shift": "",
        #         "assigned_shift":""
        #     })

    return "Processed successfully (FAST version)"



# @frappe.whitelist()
# def process_yesterday_checkins_manual():
#     import frappe
#     from datetime import datetime, timedelta
#     from frappe.utils import today, add_days, get_datetime
#     from frappe.utils import getdate

#     process_date = getdate("2026-02-16")

#     dt = get_datetime(process_date)
#     start_of_day = datetime.combine(dt.date(), datetime.min.time())
#     end_of_day = datetime.combine(dt.date(), datetime.max.time())

#     frappe.logger().info(f"Manual Yesterday Checkin Process Started for {process_date}")

#     records = frappe.db.sql("""
#         SELECT name, employee, time
#         FROM `tabEmployee Checkin`
#         WHERE log_type = 'IN'
#         AND time BETWEEN %s AND %s
#         ORDER BY employee ASC, time ASC
#     """, (start_of_day, end_of_day), as_dict=True)

#     if not records:
#         return f"No checkins found for {process_date}"

#     current_emp = None
#     first_done = False

#     for r in records:

#         # New employee block
#         if r.employee != current_emp:
#             current_emp = r.employee
#             first_done = False

#         # First IN only
#         if not first_done:
#             first_done = True

#             f_time = get_datetime(r.time)
#             att_time = f_time.time()

#             shift = get_actual_shift_start(att_time)

#             ass_shift = frappe.db.get_value(
#                 "Shift Assignment",
#                 {
#                     "employee": r.employee,
#                     "start_date": ["<=", f_time.date()],
#                     "end_date": [">=", f_time.date()],
#                     "docstatus": 1
#                 },
#                 "shift_type"
#             )

#             frappe.db.set_value("Employee Checkin", r.name, {
#                 "shift": shift,
#                 "assigned_shift": ass_shift
#             })

#             if shift:
#                 shift_start = frappe.db.get_value("Shift Type", shift, "start_time")

#                 if isinstance(shift_start, timedelta):
#                     shift_start_time = (datetime.min + shift_start).time()
#                 else:
#                     shift_start_time = shift_start

#                 grace_time = (
#                     datetime.combine(f_time.date(), shift_start_time)
#                     + timedelta(minutes=1)
#                 ).time()

#                 is_late = 1 if att_time >= grace_time else 0

#                 frappe.db.set_value("Employee Checkin", r.name, "late_entry", is_late)

#     frappe.db.commit()

#     return f"Manual Process Completed for {process_date}"


@frappe.whitelist()
def process_manual_checkins_shift():

    import frappe
    from datetime import datetime, timedelta
    from frappe.utils import getdate, get_datetime

    start_date = getdate("2026-03-03")
    end_date = getdate("2026-03-03")

    if start_date > end_date:
        return "From Date cannot be greater than To Date"

    current_date = start_date

    while current_date <= end_date:

        start_of_day = datetime.combine(current_date, datetime.min.time())
        end_of_day = datetime.combine(current_date, datetime.max.time())

        records = frappe.db.sql("""
            SELECT name, employee, time
            FROM `tabEmployee Checkin`
            WHERE log_type = 'IN'
            AND time BETWEEN %s AND %s
            ORDER BY employee ASC, time ASC
        """, (start_of_day, end_of_day), as_dict=True)

        current_emp = None
        first_done = False

        for r in records:

            if r.employee != current_emp:
                current_emp = r.employee
                first_done = False

            if not first_done:
                first_done = True

                f_time = get_datetime(r.time)
                att_time = f_time.time()

                shift = get_actual_shift_start(att_time)

                ass_shift = frappe.db.get_value(
                    "Shift Assignment",
                    {
                        "employee": r.employee,
                        "start_date": ["<=", f_time.date()],
                        "end_date": [">=", f_time.date()],
                        "docstatus": 1
                    },
                    "shift_type"
                )

                frappe.db.set_value("Employee Checkin", r.name, {
                    "shift": shift,
                    "assigned_shift": ass_shift
                })

                if shift:
                    shift_start = frappe.db.get_value("Shift Type", shift, "start_time")

                    if isinstance(shift_start, timedelta):
                        shift_start_time = (datetime.min + shift_start).time()
                    else:
                        shift_start_time = shift_start

                    grace_time = (
                        datetime.combine(f_time.date(), shift_start_time)
                        + timedelta(minutes=1)
                    ).time()

                    is_late = 1 if att_time >= grace_time else 0

                    frappe.db.set_value("Employee Checkin", r.name, "late_entry", is_late)

        current_date += timedelta(days=1)

    frappe.db.commit()

    return f"Manual Process Completed from {start_date} to {end_date}"


# from frappe.model.workflow import apply_workflow

# @frappe.whitelist()
# def auto_approve_permission():
#     permissions = frappe.get_all(
#         "Permission Request",
#         filters={
#             "workflow_state": "Superior Pending",
#             "docstatus": 0
#         },
#         pluck="name"
#     )
#     for name in permissions:
#         doc = frappe.get_doc("Permission Request", name)
#         doc.workflow_state = "Approved"
#         doc.save(ignore_permissions=True)
#         doc.submit()
#         frappe.db.commit()

# @frappe.whitelist()
# def permission_approval_12_25():
#     permissions = frappe.get_all(
#         "Permission Request",
#         filters={
#             "workflow_state": "Superior Pending",
#             "docstatus": 0
#         },
#         pluck="name"
#     )
#     for name in permissions:
#         doc = frappe.get_doc("Permission Request", name)
#         doc.workflow_state = "Approved"
#         doc.save(ignore_permissions=True)
#         doc.submit()
#         frappe.db.commit()

# @frappe.whitelist()
# def permission_approval_20_55():
#     permissions = frappe.get_all(
#         "Permission Request",
#         filters={
#             "workflow_state": "Superior Pending",
#             "docstatus": 0
#         },
#         pluck="name"
#     )
#     for name in permissions:
#         doc = frappe.get_doc("Permission Request", name)
#         doc.workflow_state = "Approved"
#         doc.save(ignore_permissions=True)
#         doc.submit()
#         frappe.db.commit()

# @frappe.whitelist()
# def permission_approval_03_15():
#     permissions = frappe.get_all(
#         "Permission Request",
#         filters={
#             "workflow_state": "Superior Pending",
#             "docstatus": 0
#         },
#         pluck="name"
#     )
#     for name in permissions:
#         doc = frappe.get_doc("Permission Request", name)
#         doc.workflow_state = "Approved"
#         doc.save(ignore_permissions=True)
#         doc.submit()
#         frappe.db.commit()


# @frappe.whitelist()
# def create_schedule_job():

#     timings = {
#         "permission_approval_12_25": {
#             "cron": "25 12 * * *",
#             "method": "infac.mail_alerts_custom.permission_approval_12_25"
#         },
#         "permission_approval_20_55": {
#             "cron": "55 20 * * *",
#             "method": "infac.mail_alerts_custom.permission_approval_20_55"
#         },
#         "permission_approval_03_15": {
#             "cron": "15 3 * * *",
#             "method": "infac.mail_alerts_custom.permission_approval_03_15"
#         }
#     }

#     for job_name, data in timings.items():
#         if not frappe.db.exists("Scheduled Job Type", data["method"]):
#             sjt = frappe.new_doc("Scheduled Job Type")
#             sjt.update({
#                 "method": data["method"],
#                 "frequency": "Cron",
#                 "cron_format": data["cron"]
#             })
#             sjt.insert(ignore_permissions=True)



# @frappe.whitelist()
# def auto_approve_permission():
#     permissions = frappe.get_all( "Permission Request", filters={ "workflow_state": "Superior","docstatus": 0 },pluck="name" )
#     for per in permissions:
#         doc = frappe.get_doc("Permission Request", per)
#         permission_date = doc.permission_date
#         employee = doc.employee_id
#         attendance_exists = frappe.db.exists( "Attendance",{"employee": employee,"attendance_date": permission_date,"docstatus": 1 })
        
#         if not attendance_exists:
#             continue

#         doc.workflow_state = "Approved"
#         doc.save(ignore_permissions=True)
#         doc.submit()

#     frappe.db.commit()

import frappe
from frappe.utils import add_days, date_diff
from datetime import datetime, date


def get_dates(from_date, to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    return [add_days(from_date, i) for i in range(no_of_days)]


@frappe.whitelist()
def allocate_el():
    today = datetime.now().date()

    to_date = add_days(today, -1) 
    prev_month = add_days(today.replace(day=1), -1)
    from_date = prev_month.replace(day=21)

    if today.month == 12 and today.day >= 21:
        start_year = today.year
    else:
        start_year = today.year - 1

    el_from_date = date(start_year, 12, 21)
    el_to_date   = date(start_year + 1, 12, 20)
    employees = frappe.db.get_all("Employee",{"status": "Active","employment_type": ("in", ("STAFF", "WORKER"))},["name", "company"] )
    # employees = frappe.db.get_all("Employee",{"status": "Active","employment_type": "STAFF"},["name", "company"] )
    for emp in employees:
        emp_id = emp.name
        # company = emp.company
        present_count = 0
        for d in get_dates(from_date, to_date):
            if frappe.db.exists("Attendance",{"employee": emp_id,"attendance_date": d,"status": "Present","docstatus": ["!=", 2] }):
                present_count += 1
        if present_count <= 0:
            continue 
        el_to_add = round(present_count / 20, 2)
        allocation_name = frappe.db.get_value( "Leave Allocation",{"employee": emp_id,"leave_type": "Earned Leave","from_date": el_from_date,"to_date": el_to_date,"docstatus": 1  }, "name" )
        if not allocation_name:
            alloc = frappe.new_doc("Leave Allocation")
            alloc.employee = emp_id
            alloc.leave_type = "Earned Leave"
            alloc.from_date = el_from_date
            alloc.to_date = el_to_date
            alloc.new_leaves_allocated = el_to_add
            alloc.total_leaves_allocated = el_to_add
            alloc.insert(ignore_permissions=True)
            alloc.submit()
        else:
            alloc = frappe.get_doc("Leave Allocation", allocation_name)
            alloc.new_leaves_allocated += el_to_add
            alloc.total_leaves_allocated += el_to_add
            alloc.save(ignore_permissions=True)

    frappe.db.commit()

# @frappe.whitelist()
# def allocate_el():
#     today = datetime.now().date()
#     to_date = add_days(today, -1) 
#     prev_month = add_days(today.replace(day=1), -1)
#     from_date = prev_month.replace(day=21)
#     # today = datetime.strptime('2025-11-21', '%Y-%m-%d').date()
#     # from_date = date(2025, 10, 21)
#     # to_date = date(2025, 11, 20)
#     # employees = ['112233']
    
#     if today.month == 12 and today.day >= 21:
#         start_year = today.year
#     else:
#         start_year = today.year - 1

#     el_from_date = date(start_year, 12, 21)
#     el_to_date   = date(start_year + 1, 12, 20)
#     employees = frappe.db.get_all("Employee",{"status": "Active","employee_category": ("in", ("Staff", "Worker"))},["name", "company"] )
#     for emp in employees:
#         emp_id = emp
#         present_count = 0
#         for d in get_dates(from_date, to_date):
#             if frappe.db.exists("Attendance",{"employee": emp_id,"attendance_date": d,"status": "Present","docstatus": ["!=", 2] }):
#                 present_count += 1
#                 # present_count = 20

#         if present_count <= 0:
#             continue

#         el_to_add = round(present_count / 20, 2)

#         allocation_name = frappe.db.get_value("Leave Allocation",{"employee": emp_id,"leave_type": "Earned Leave","from_date": el_from_date,"to_date": el_to_date,"docstatus": 1}, "name")

#         # print(f"Employee: {emp_id}, Present Days: {present_count}, EL to Add: {el_to_add}, Allocation Found: {allocation_name}")

#         if not allocation_name:
#             # print("Creating new allocation")
#             alloc = frappe.new_doc("Leave Allocation")
#             alloc.employee = emp_id
#             alloc.leave_type = "Earned Leave"
#             alloc.from_date = el_from_date
#             alloc.to_date = el_to_date
#             alloc.new_leaves_allocated = el_to_add
#             alloc.total_leaves_allocated = el_to_add
#             alloc.insert(ignore_permissions=True)
#             alloc.submit()
#         else:
#             # print(f"Updating existing allocation: {allocation_name}")
#             alloc = frappe.get_doc("Leave Allocation", allocation_name)
#             alloc.new_leaves_allocated += el_to_add
#             alloc.total_leaves_allocated += el_to_add
#             alloc.save(ignore_permissions=True)


@frappe.whitelist()
def el_allocation():
	enqueue(allocate_el, queue='long', timeout=6000)


@frappe.whitelist()
def delete_attendance():
    att_name = "HR-ATT-2025-237057"

    frappe.db.sql("""
        UPDATE `tabAttendance`
        SET
            total_wh   = '00:00:00',
            extra_hours = '00:00:00'
        WHERE name = %s
    """, (att_name,))

    frappe.db.commit()

    att = frappe.get_doc("Attendance", att_name)

    if att.docstatus == 1:
        att.flags.ignore_validate = True
        att.flags.ignore_validate_update_after_submit = True
        att.flags.ignore_on_update = True
        att.cancel()


    # frappe.delete_doc(
    #     "Attendance",
    #     att.name,
    #     force=1,
    #     ignore_links=True,
    #     ignore_permissions=True
    # )

    # frappe.db.commit()
    return f"Attendance {att_name} cancelled & deleted successfully"




@frappe.whitelist()
def delete_attendance_settings(attendance_id):
    if not attendance_id:
        frappe.throw("Attendance ID is required")

    frappe.db.sql("""
        UPDATE `tabAttendance`
        SET
            total_wh = '00:00:00',
            extra_hours = '00:00:00'
        WHERE name = %s
    """, (attendance_id,))

    frappe.db.commit()

    att = frappe.get_doc("Attendance", attendance_id)

    if att.docstatus == 1:
        att.flags.ignore_validate = True
        att.flags.ignore_validate_update_after_submit = True
        att.cancel()

    return f"Attendance {attendance_id} cancelled successfully"


# @frappe.whitelist()
# def additional_salary_validation(doc, method):
#     add_sal = frappe.db.exists("Additional Salary",{"employee":doc.employee,"payroll_date":doc.payroll_date,"salary_component":doc.salary_component,"docstatus":1,"name":["!=",doc.name]})
#     if add_sal:
#         frappe.throw(frappe._(f"Additional Salary already exists for this Employee "
#                 f"{doc.employee}, Payroll Date {doc.payroll_date}"
#                 f" and Salary Component {doc.salary_component}."
#             ))
        

# @frappe.whitelist()
# def validate_halfday_leave(doc, method):
#     if doc.half_day:
#         existing_leave = frappe.db.exists("Leave Application", {"employee": doc.employee,"from_date": doc.from_date,"to_date": doc.to_date,"leave_type": doc.leave_type,"half_day": 1,"docstatus": ["!=", 2],"name": ["!=", doc.name] })
#         if existing_leave:
#             frappe.throw(_("You have already applied a Half-Day leave for this date with the same Leave Type."),
#                 frappe.ValidationError
#             )


# import frappe
# from erpnext.hr.doctype.leave_application.leave_application import get_leave_details_for_payslip

# @frappe.whitelist()
# def get_payslip_leave_balance(employee, start_date, end_date):
#     leave_details = get_leave_details_for_payslip(
#         employee=employee,
#         start_date=start_date,
#         end_date=end_date
#     )
#     return leave_details.get("leave_balance", {})

# @frappe.whitelist()
# def leave_approval_tracking(doc, method):
#     # Run only if workflow_state changed
#     if not doc.has_value_changed("workflow_state"):
#         return

#     current_user = frappe.session.user
#     current_time = now_datetime()

#     # Level 1 Approval
#     if doc.workflow_state == "Superior Pending":
#         doc.level_1_timing = current_time
#         doc.level_1_approved_by = current_user

#     # Level 2 Approval (Final Approval)
#     elif doc.workflow_state == "Approved":
#         doc.level_2_timing = current_time
#         doc.level_2_approved_by = current_user

#     # Rejected حالة
#     elif doc.workflow_state == "Rejected":
#         doc.rejected_timing = current_time
#         doc.rejected_by = current_user


import frappe
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request


#Firebase Access Token
def get_access_token():
    file_path = frappe.get_site_path("private", "files", "firebase-key.json")

    credentials = service_account.Credentials.from_service_account_file(
        file_path,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )

    credentials.refresh(Request())
    return credentials.token

import frappe

@frappe.whitelist(allow_guest=True)
def update_fcm_token(token=None):

    user = frappe.session.user

    frappe.log_error(
        f"User={user}, Token={token}",
        "FCM Debug"
    )

    if user == "Guest":
        frappe.throw("User not logged in")

    frappe.db.set_value("User", user, "fcm_token", token)
    frappe.db.commit()

    return "Token Updated"


# @frappe.whitelist()
# def update_fcm_token(token):
#     user = frappe.session.user

#     if user == "Guest":
#         return "Not Logged In"

#     frappe.db.set_value("User", user, "fcm_token", token)
#     return "Token Updated"


# Send Notification
# @frappe.whitelist()
# def send_push_notification(token, title, message):

    
#     try:
#         access_token = get_access_token()

#         project_id = "infac-notification"

#         url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

#         headers = {
#             "Authorization": "Bearer " + access_token,
#             "Content-Type": "application/json"
#         }

#         payload = {
#             "message": {
#                 "token": token,
#                 "notification": {
#                     "title": title,
#                     "body": message
#                 }
#             }
#         }

#         response = requests.post(url, json=payload, headers=headers)

#         return response.json()

#     except Exception as e:
#         frappe.log_error(str(e), "FCM Error")
#         return {"error": str(e)}

@frappe.whitelist()
def send_push_notification(token, title, message, data=None):
    try:
        access_token = get_access_token()
        project_id = "infac-notification"
        url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        }

        payload = {
            "message": {
                "token": token,
                "notification": {
                    "title": title,
                    "body": message
                }
            }
        }

        if data:
            # FCM data payload values must all be strings
            payload["message"]["data"] = {k: str(v) for k, v in data.items()}

        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    except Exception as e:
        frappe.log_error(str(e), "FCM Error")
        return {"error": str(e)}

@frappe.whitelist()
def send_notification_to_user(user, title, message):
    frappe.log_error(
        f"Notification sent to {user} - {title}",
        "FCM Notification"
    )

    token = frappe.db.get_value("User", user, "fcm_token")

    if not token:
        return "No token found for user"

    return send_push_notification(token, title, message)

# def leave_approved_notification(doc, method=None):
#     frappe.log_error("HOOK FIRED", "FCM Hook Test")  # ← must be inside here
#     try:
#         frappe.log_error(
#             f"Leave notification triggered for {doc.employee}",
#             "FCM Step 1 - Triggered"
#         )

#         employee = frappe.get_doc("Employee", doc.employee)

#         if not employee.user_id:
#             frappe.log_error(
#                 f"No user_id for employee {doc.employee}",
#                 "FCM Step 2 - No User"
#             )
#             return

#         frappe.log_error(
#             f"User found: {employee.user_id}",
#             "FCM Step 2 - User OK"
#         )

#         token = frappe.db.get_value("User", employee.user_id, "fcm_token")

#         if not token:
#             frappe.log_error(
#                 f"No FCM token for user {employee.user_id}",
#                 "FCM Step 3 - No Token"
#             )
#             return

#         frappe.log_error(
#             f"Token found: {token}",
#             "FCM Step 3 - Token OK"
#         )

#         title = "Leave Approved"
#         message = "Your leave from {} to {} has been approved.".format(
#             str(doc.from_date), str(doc.to_date)
#         )

#         result = send_push_notification(token, title, message)

#         frappe.log_error(
#             f"FCM Result: {result}",
#             "FCM Step 4 - Result"
#         )

#     except Exception as e:
#         frappe.log_error(str(e), "FCM Leave Notification Error")


def get_fcm_token_for(value):
    """
    Resolve an Incharge/Superior field value to an FCM token.
    Works whether the field links to Employee or directly to User.
    """
    if not value:
        return None

    user_id = value

    # If it's an Employee ID, fetch the linked user
    if frappe.db.exists("Employee", value):
        user_id = frappe.db.get_value("Employee", value, "user_id")

    if not user_id:
        return None

    return frappe.db.get_value("User", user_id, "fcm_token")


# def leave_workflow_notification(doc, method=None):
#     try:
#         if not doc.has_value_changed("workflow_state"):
#             return

#         state = doc.workflow_state

#         frappe.log_error(
#             f"Workflow state changed to '{state}' for {doc.name}",
#             "FCM Workflow Debug"
#         )

#         # Map workflow state -> (field on Leave Application, title, message)
#         state_config = {
#             "Incharge Pending": {
#                 "field": "incharge",   # <-- replace with your actual fieldname
#                 "title": "Leave Approval Pending",
#                 "message": f"Leave application {doc.name} needs your approval as Incharge."
#             },
#             "Superior Pending": {
#                 "field": "superior",   # <-- replace with your actual fieldname
#                 "title": "Leave Approval Pending",
#                 "message": f"Leave application {doc.name} needs your approval as Superior."
#             },
#             "Approved": {
#                 "field": "employee",
#                 "title": "Leave Approved",
#                 "message": "Your leave from {} to {} has been approved.".format(
#                     str(doc.from_date), str(doc.to_date)
#                 )
#             },
#             "Rejected": {
#                 "field": "employee",
#                 "title": "Leave Rejected",
#                 "message": "Your leave from {} to {} has been rejected.".format(
#                     str(doc.from_date), str(doc.to_date)
#                 )
#             },
#         }

#         config = state_config.get(state)
#         if not config:
#             return

#         target = doc.get(config["field"])
#         if not target:
#             frappe.log_error(
#                 f"No value in '{config['field']}' for {doc.name}",
#                 "FCM Workflow - No Target"
#             )
#             return

#         token = get_fcm_token_for(target)
#         if not token:
#             frappe.log_error(
#                 f"No FCM token resolved for '{target}' ({config['field']}) on {doc.name}",
#                 "FCM Workflow - No Token"
#             )
#             return

#         result = send_push_notification(token, config["title"], config["message"])

#         frappe.log_error(
#             f"FCM result for state '{state}' on {doc.name}: {result}",
#             "FCM Workflow - Result"
#         )

#     except Exception as e:
#         frappe.log_error(str(e), "FCM Workflow Notification Error")

def leave_workflow_notification(doc, method=None):
    try:
        # New Leave Application created directly in Incharge Pending
        if doc.is_new() and doc.workflow_state == "Incharge Pending":
            target = doc.incharge

            if target:
                token = get_fcm_token_for(target)
                if token:
                    send_push_notification(
                        token,
                        "Leave Application Pending for your Approval",
                        build_leave_message(doc),
                        data={"doctype": "Leave Application", "docname": doc.name}
                    )
            return

        # Existing workflow state changes
        if not doc.has_value_changed("workflow_state"):
            return

        state = doc.workflow_state

        state_config = {
            "Incharge Pending": {
                "field": "incharge",
                "title": "Leave Application Pending for your Approval",
                "message": build_leave_message(doc)
            },
            "Superior Pending": {
                "field": "superior",
                "title": "Leave Application Pending for your Approval",
                "message": build_leave_message(doc)
            },
            "Approved": {
                "field": "employee",
                "title": "Leave Application Approved",
                "message": build_leave_message(doc, note="Your leave has been Approved.")
            },
            "Rejected": {
                "field": "employee",
                "title": "Leave Application Rejected",
                "message": build_leave_message(doc, note="Your leave has been Rejected.")
            },
        }

        config = state_config.get(state)
        if not config:
            return

        target = doc.get(config["field"])
        if not target:
            frappe.log_error(f"No value in '{config['field']}' for {doc.name}", "FCM Workflow - No Target")
            return

        token = get_fcm_token_for(target)
        if not token:
            frappe.log_error(f"No FCM token resolved for '{target}' on {doc.name}", "FCM Workflow - No Token")
            return

        result = send_push_notification(
            token,
            config["title"],
            config["message"],
            data={"doctype": "Leave Application", "docname": doc.name}
        )

        frappe.log_error(f"FCM result for '{state}' on {doc.name}: {result}", "FCM Workflow - Result")

    except Exception as e:
        frappe.log_error(str(e), "FCM Workflow Notification Error")
        
def build_leave_message(doc, note="Pending for your Approval"):
    return (
        f"ID: {doc.name}\n"
        f"Employee: {doc.employee}\n"
        f"Employee Name: {doc.employee_name}\n"
        f"From Date: {doc.from_date}\n"
        f"To Date: {doc.to_date}\n"
        f"Total Leave Days: {doc.total_leave_days}\n"
        f"{note}"
    )