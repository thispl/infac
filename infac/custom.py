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
    
@frappe.whitelist()
def inactive_employee(doc,method):
    if doc.status=="Active":
        if doc.relieving_date:
            throw(_("Please remove the relieving date for the Active Employee."))

@frappe.whitelist()
def update_employee_no(name,employee_number):
    emp = frappe.get_doc("Employee",name)
    emps=frappe.get_all("Employee",{"status":"Active"},['*'])
    for i in emps:
        if emp.employee_number == employee_number:
            pass
        elif i.employee_number == employee_number:
            frappe.throw(f"Employee Number already exists for {i.name}")
        else:
            frappe.db.set_value("Employee",name,"employee_number",employee_number)
            frappe.rename_doc("Employee", name, employee_number, force=1)
            return employee_number


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

@frappe.whitelist()
def update_reg():
    # frappe.db.set_value("Attendance",'HR-ATT-2025-20926','total_wh',0)
    frappe.db.set_value("Attendance Regularize",'ATR134499','docstatus',0)