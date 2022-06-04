from lib2to3.pytree import convert
from os import name
from termios import EXTA
from time import strptime
from traceback import print_tb
import frappe
from frappe.share import add
# from infac.mark_attendance import mark_attendance_from_checkin
from numpy import empty
import pandas as pd
import json
import datetime
from frappe.permissions import check_admin_or_system_manager
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from datetime import date, timedelta,time
from frappe.utils.background_jobs import enqueue
from frappe.utils import get_url_to_form
import math


def mark_att():
    # from_date = add_days(today(),-1)
    # to_date = today()
    from_date = '2022-05-23'
    to_date = '2022-05-24'
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) between '%s' and '%s' order by time """%(from_date,to_date),as_dict=True)
    for c in checkins:
        mark_attendance_from_checkin(c.name,c.employee,c.time)
    # mark_wh_ot(from_date,to_date)
    # mark_absent(from_date,to_date)
    # ot_incentive(from_date,to_date)


def mark_attendance_from_checkin(checkin,employee,time):
    att_date = time.date()
    att_time = time.time()
    print(att_date)
    if att_time < datetime.strptime('12:00:00','%H:%M:%S').time():
        shift = frappe.db.get_value('Shift Assignment',{'employee':employee,'start_date':att_date,'docstatus':('!=','2')},'shift_type')
        if shift not in ('G','A'):
            yesterday = add_days(att_date,-1)
            y_shift = frappe.db.get_value('Shift Assignment',{'employee':employee,'start_date':yesterday,'docstatus':('!=','2')},'shift_type')
            if y_shift in ('C','B'):
                att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':yesterday,'docstatus':('!=',2)})
                if att:
                    frappe.db.set_value('Attendance',att,'out_time',time)
                    frappe.db.set_value("Employee Checkin",checkin, "attendance", att)
                    frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                else:
                    doc = frappe.new_doc('Attendance')
                    doc.employee = employee
                    doc.attendance_date = yesterday
                    doc.status = 'Absent'
                    doc.shift = y_shift
                    doc.out_time = time
                    doc.total_wh = ''
                    doc.late_hours = ''
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
                    frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
            elif shift == None:
                shift = 'G'
                att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=',2)})
                if not att:
                    doc = frappe.new_doc('Attendance')
                    doc.employee = employee
                    doc.attendance_date = att_date
                    doc.status = 'Present'
                    doc.shift = shift
                    doc.in_time = time
                    doc.out_time = ''
                    doc.total_wh = ''
                    doc.late_hours = ''
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
                    frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                else:
                    frappe.db.set_value('Attendance',att,'out_time',time)
                    frappe.db.set_value("Employee Checkin",checkin, "attendance", att)
                    frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
            else:
                att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=',2)})
                if not att:
                    doc = frappe.new_doc('Attendance')
                    doc.employee = employee
                    doc.attendance_date = att_date
                    doc.status = 'Present'
                    doc.shift = shift
                    doc.in_time = time
                    doc.out_time = ''
                    doc.total_wh = ''
                    doc.late_hours = ''
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
                    frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                else:
                    frappe.db.set_value('Attendance',att,'out_time',time)
                    frappe.db.set_value("Employee Checkin",checkin, "attendance", att)
                    frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
        else:
            if shift == None:
                shift = 'G'
            att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=',2)})
            if not att:
                doc = frappe.new_doc('Attendance')
                doc.employee = employee
                doc.attendance_date = att_date
                doc.status = 'Present'
                doc.shift = shift
                doc.in_time = time
                doc.out_time = ''
                doc.total_wh = ''
                doc.late_hours = ''
                doc.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
                frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
            else:
                frappe.db.set_value('Attendance',att,'out_time',time)
                frappe.db.set_value("Employee Checkin",checkin, "attendance", att)
                frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
    else:
        shift = frappe.db.get_value('Shift Assignment',{'employee':employee,'start_date':att_date,'docstatus':('!=','2')},'shift_type')
        if shift == None:
            shift = 'G'
        att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=',2)})
        if not att:
            doc = frappe.new_doc('Attendance')
            doc.employee = employee
            doc.attendance_date = att_date
            doc.status = 'Present'
            doc.shift = shift
            doc.in_time = time
            doc.out_time = ''
            doc.total_wh = ''
            doc.late_hours = ''
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
            frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
        else:
            frappe.db.set_value('Attendance',att,'out_time',time)
            frappe.db.set_value("Employee Checkin",checkin, "attendance", att)
            frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
            

@frappe.whitelist()    
def mark_absent(from_date,to_date):
    if to_date == today():
        to_date = add_days(to_date,-1)
    no_of_days = date_diff(add_days(to_date, 1),from_date )
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    for date in dates:
        employee = frappe.db.get_all('Employee',{'status':'Active','date_of_joining':['<=',from_date]})
        for emp in employee:
            hh = check_holiday(date,emp.name)
            if not hh:
                if not frappe.db.exists('Attendance',{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')}):
                    att = frappe.new_doc('Attendance')
                    att.employee = emp.name
                    att.status = 'Absent'
                    att.attendance_date = date
                    att.total_wh = '00:00:00'
                    att.extra_hours = '00:00:00'
                    att.late_hours ='00:00:00'
                    att.save(ignore_permissions=True)
                    att.submit()
                    frappe.db.commit()

def mark_wh_ot(from_date,to_date):
    # from_date = '2022-03-05'
    # to_date = '2022-03-05'
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['name','shift','in_time','out_time','employee','attendance_date','permission_request'])
    for att in attendance:
        if att.in_time and att.out_time:
            hh = check_holiday(att.attendance_date,att.employee)
            if not hh:  
                total_wh = att.out_time - att.in_time
                print(type(att.in_time))
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
                wh = round(hr/3600,1)
                print(att.name)
                if not att.permission_request:
                    if wh < 4:
                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                    elif wh >= 4 and wh < 8:
                        frappe.db.set_value('Attendance',att.name,'status','Half Day')   
                    elif  wh >= 8:
                        frappe.db.set_value('Attendance',att.name,'status','Present')
                shift_end_time = frappe.db.get_value('Shift Type',att.shift,'end_time')
                shift_end_time = pd.to_datetime(str(shift_end_time)).time()
                shift_start_time = frappe.db.get_value('Shift Type',att.shift,'start_time')
                shift_start_time = pd.to_datetime(str(shift_start_time)).time()
                total_shift_hours = frappe.db.get_value('Shift Type',att.shift,'total_hours')
                in_date = att.in_time.date()
                out_date = att.out_time.date()
                shift_end_datetime = datetime.combine(out_date,shift_end_time)
                shift_start_datetime = datetime.combine(in_date,shift_start_time)
                if shift_start_datetime:
                    late_hour = pd.to_datetime('00:00:00').time()
                    late_hr = 0
                    if att.in_time > shift_start_datetime:
                        late_hour = att.in_time - shift_start_datetime
                        hr = sum([a*b for a,b in zip(ftr, map(int,str(late_hour).split(':')))])
                        late_hr = round(hr/3600,1)
                    frappe.db.set_value('Attendance',att.name,'late_hrs',late_hr)
                    frappe.db.set_value('Attendance',att.name,'late_hours',late_hour)
                    # Late hours set of Condition Round Up Into The Late Deduct
                    actual_late_hour = frappe.db.get_value('Attendance',att.name,'late_hours')
                    if actual_late_hour:
                        late_deduct_hour = actual_late_hour.seconds//3600
                        late_deduct_minute = ((actual_late_hour.seconds//60)%60)
                        deducted_minute = late_deduct_minute
                        deducted_hour = late_deduct_hour
                        if late_deduct_minute >= 1 and late_deduct_minute <= 5:
                            deducted_minute = 5
                        elif late_deduct_minute >= 6  and late_deduct_minute <=10:
                            deducted_minute = 10
                        elif late_deduct_minute >= 11 and late_deduct_minute <= 15:
                            deducted_minute = 15
                        elif late_deduct_minute >= 16 and late_deduct_minute <= 20:
                            deducted_minute = 20
                        elif late_deduct_minute >= 21 and late_deduct_minute <= 25:
                            deducted_minute = 25
                        elif late_deduct_minute >= 26 and late_deduct_minute <= 30:
                            deducted_minute = 30
                        elif late_deduct_minute >= 31 and late_deduct_minute <= 35:
                            deducted_minute = 35
                        elif late_deduct_minute >= 36 and late_deduct_minute <= 40:
                            deducted_minute = 40
                        elif late_deduct_minute >= 41 and late_deduct_minute <= 45:
                            deducted_minute = 45
                        elif late_deduct_minute >= 46 and late_deduct_minute <= 50:
                            deducted_minute = 50 
                        elif late_deduct_minute >= 51 and late_deduct_minute <= 55:
                            deducted_minute = 55    
                        elif late_deduct_minute >= 56 and late_deduct_minute <= 60:
                            deducted_hour = late_deduct_hour +1
                            deducted_minute = 00
                        late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute)+':00'
                        time = datetime.strptime(str(late_deducted_time),'%H:%M:%S')
                        time_change = time.strftime('%H:%M')
                        frappe.db.set_value('Attendance',att.name,'late_deduct',time_change)      
                     
                if shift_end_time:
                    extra_hrs =pd.to_datetime('00:00:00').time()
                    ot_hr = 0
                    if att.out_time > shift_end_datetime:
                        if total_wh > total_shift_hours:
                            extra_hrs = att.out_time - shift_end_datetime
                            hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                            extras = round(hr/3600,1)
                            if extras > 1:
                                ot_hr = math.floor(extras * 2) / 2
                    frappe.db.set_value('Attendance',att.name,'ot_hrs',ot_hr)
                    frappe.db.set_value('Attendance',att.name,'extra_hours',extra_hrs)
                    frappe.db.set_value('Attendance',att.name,'total_wh',total_wh)
                    frappe.db.set_value('Attendance',att.name,'working_hours',wh)
                else:
                    none_time = pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'ot_hrs',0)
                    frappe.db.set_value('Attendance',att.name,'extra_hours',none_time)
                    frappe.db.set_value('Attendance',att.name,'total_wh',none_time)
                    frappe.db.set_value('Attendance',att.name,'working_hours',0)   
            else:
                total_wh = att.out_time - att.in_time
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
                wh = round(hr/3600,1)
                if wh < 4:
                    frappe.db.set_value('Attendance',att.name,'status','Absent')
                elif wh >= 4 and wh < 8:
                   frappe.db.set_value('Attendance',att.name,'status','Half Day')   
                elif  wh >= 8:
                    frappe.db.set_value('Attendance',att.name,'status','Present')
                if wh > 0:
                    ot_hr = (math.floor(wh * 2) / 2) - 0.5
                    frappe.db.set_value('Attendance',att.name,'ot_hrs',ot_hr)
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'extra_hours',none_time)
                    frappe.db.set_value('Attendance',att.name,'total_wh',total_wh)
                    frappe.db.set_value('Attendance',att.name,'working_hours',wh)
                else:
                    none_time =pd.to_datetime('00:00:00').time()
                    frappe.db.set_value('Attendance',att.name,'ot_hrs',0)
                    frappe.db.set_value('Attendance',att.name,'extra_hours',none_time)
                    frappe.db.set_value('Attendance',att.name,'total_wh',none_time)
                    frappe.db.set_value('Attendance',att.name,'working_hours',0)
                
                in_date = att.in_time.date()
                shift_start_time = frappe.db.get_value('Shift Type',att.shift,'start_time')
                shift_start_time = pd.to_datetime(str(shift_start_time)).time()
                shift_start_datetime = datetime.combine(in_date,shift_start_time)
                if shift_start_datetime:
                    late_hour = pd.to_datetime('00:00:00').time()
                    late_hr = 0
                    if att.in_time > shift_start_datetime:
                        late_hour = att.in_time - shift_start_datetime
                        hr = sum([a*b for a,b in zip(ftr, map(int,str(late_hour).split(':')))])
                        late_hr = round(hr/3600,1)
                    frappe.db.set_value('Attendance',att.name,'late_hrs',late_hr)
                    frappe.db.set_value('Attendance',att.name,'late_hours',late_hour) 
        else:
            none_time =pd.to_datetime('00:00:00').time()
            frappe.db.set_value('Attendance',att.name,'extra_hours',none_time)
            frappe.db.set_value('Attendance',att.name,'total_wh',none_time)
            frappe.db.set_value('Attendance',att.name,'late_hours',none_time)
            frappe.db.set_value('Attendance',att.name,'late_hrs',0)

def check_holiday(date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"


def ot_incentive(from_date,to_date):
    employee = frappe.db.get_all('Employee',{'Status':'Active','incentive_category':'Yes'},['designation','employee'])
    for emp in employee:
        attendance = frappe.db.get_all('Attendance',{'employee':emp.employee,'attendance_date':('between',(from_date,to_date))},['name','ot_hrs'])
        for att in attendance:
            if att:
                if att.ot_hrs < 4.5:
                    frappe.db.set_value('Attendance',att.name,'3_hrs',att.ot_hrs)
                    frappe.db.set_value('Attendance',att.name,'3_hrs_amount','125')
                elif att.ot_hrs > 4.5 and att.ot_hrs < 12:
                    frappe.db.set_value('Attendance',att.name,'3_hrs',att.ot_hrs)
                    frappe.db.set_value('Attendance',att.name,'3_hrs_amount','150')
                elif att.ot_hrs > 12:
                    frappe.db.set_value('Attendance',att.name,'3_hrs',att.ot_hrs)
                    frappe.db.set_value('Attendance',att.name,'3_hrs_amount','250')
