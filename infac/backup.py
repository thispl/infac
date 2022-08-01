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



#Attendance Register Report Code Total Backup

from __future__ import unicode_literals
from functools import total_ordering
from itertools import count
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide

import pandas as pd

status_map = {
    'Permission Request' :'PR',
    'On Duty':'OD',
    'Half Day':'HD',
    "Absent": "A",
	"Half Day": "HD",
	"Holiday": "HH",
	"Weekly Off": "WW",
    "Present": "P",
    "None" : "",
    "Leave Without Pay": "LOP",
    "Casual Leave": "CL",
    "Earned Leave": "EL",
    "Sick Leave": "SL",
    "Emergency -1": 'EML-1',
    "Emergency -2": 'EML-2',
    "Paternal Leave": 'PL',
    "Marriage Leave":'ML',
    "Paternity Leave":'PTL',
    "Education Leave":'EL',
    "Maternity Leave":'MTL',
    "Covid -19": "COV-19",
    "Privilege Leave": "PVL",
    "Compensatory Off": "C-OFF",
    "BEREAVEMENT LEAVE":'BL'
}
def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = []
    columns += [
        _("Employee ID") + ":Data/:150",_("Employee Name") + ":Data/:200",_("Department") + ":Data/:150",_("DOJ") + ":Date/:100",_("Status") + ":Data/:150",
    ]
    dates = get_dates(filters.from_date,filters.to_date)
    for date in dates:
        date = datetime.strptime(date,'%Y-%m-%d')
        day = datetime.date(date).strftime('%d')
        month = datetime.date(date).strftime('%b')
        columns.append(_(day + '/' + month) + ":Data/:70")
    columns.append(_("Present") + ":Data/:100")
    columns.append(_('Half Day') +':Data/:100')
    columns.append(_('On Duty') + ':Data/:100')
    columns.append(_('Permission') + ':Data/:100')
    columns.append(_("Absent") + ":Data/:100")
    columns.append(_('Weekoff')+ ':Data/:100')
    columns.append(_('Holiday')+ ':Data/:100')
    columns.append(_('Paid Leave')+ ':Data/:150')
    columns.append(_('LOP')+ ':Data/:100')
    columns.append(_('COFF')+ ':Data/:100')
    columns.append(_('OT')+ ':Data/:100')
    columns.append(_('Late')+ ':Data/:100')
    columns.append(_('Late Deduct')+ ':Data/:150')
    columns.append(_('Permission Hours')+ ':Data/:150')
    columns.append(_('Night Shift')+ ':Data/:150')
    
    return columns

def get_data(filters):
    data = []
    emp_status_map = []
    employees = get_employees(filters)
    for emp in employees:
        dates = get_dates(filters.from_date,filters.to_date)
        row1 = [emp.name,emp.employee_name,emp.department,emp.date_of_joining,""]
        row2 = ['',"","","","","In Time"]
        row3 = ['',"","","","","Out Time"]
        row4 = ['',"","","","","Shift"]
        row5 = ['',"","","","","Late"]
        row6 = ['',"","","","","Late Deduct"]
        row7 = ['',"","","","","TWH"]
        row8 = ['',"","","","","OT"]
        total_present = 0
        total_half_day = 0
        total_absent = 0
        total_holiday = 0
        total_weekoff = 0
        total_ot = 0
        total_od = 0
        total_permission = 0
        total_lop = 0
        total_paid_leave = 0
        total_combo_off = 0
        c_shift = 0
        # total_late = pd.to_datetime('00:00:00').time()
        total_late = timedelta(0,0,0)
        total_late_deduct = timedelta(0,0)
        ww = 0
        twh = 0
        ot = 0
        for date in dates:
            att = frappe.db.get_value("Attendance",{'attendance_date':date,'employee':emp.name},['status','in_time','out_time','shift','total_wh','ot_hrs','late_hrs','leave_type','employee_category','on_duty_marked','permission_request','leave_type','late_hours','employee','attendance_date','name','late_deduct']) or ''
            if att:
                status = status_map.get(att[0], "")
                if att[9]:
                    hh = check_holiday(date,emp.name)
                    if hh:
                        if hh == 'WW':
                            total_weekoff +=1
                        elif hh == 'HH':
                            total_holiday +=1   
                        row1.append(hh)
                    else:    
                        row1.append('OD')
                        total_od = total_od + 1  
                elif att[10]:
                    hh = check_holiday(date,emp.name)
                    if hh:
                        if hh == 'WW':
                            total_weekoff +=1
                        elif hh == 'HH':
                            total_holiday +=1   
                        row1.append(hh)
                    else:      
                        row1.append('P/P')
                        total_present +=  1
                        total_permission += 1    
                elif status == 'Present':
                    hh = check_holiday(date,emp.name)
                    if hh:
                        # if hh == 'WW':
                        #     total_weekoff +=1
                        if hh == 'HH':
                            total_holiday +=1   
                        row1.append(hh)   
                    else:  
                        row1.append('P' or '-')
                        total_present = total_present + 1   
                elif status == 'Half Day':
                    hh = check_holiday(date,emp.name)
                    if hh:
                        if hh == 'WW':
                            total_weekoff += 1
                        elif hh == 'HH':
                            total_holiday += 1
                        row1.append(hh)
                    else:
                        if att[11]:
                            row1.append('P/L')
                            total_present = total_present + 0.5
                            total_paid_leave = total_paid_leave + 0.5
                        else:
                            row1.append('P/A')
                            total_present = total_present + 0.5
                            total_half_day = total_half_day + 0.5
                elif status == 'Absent':
                    hh = check_holiday(date,emp.name)
                    if hh:
                        if hh == 'WW':
                            total_weekoff += 1
                        elif hh == 'HH':
                            total_holiday += 1
                        row1.append(hh)
                    else: 
                        row1.append('A')
                        total_absent = total_absent + 1                         
                elif att[7]:
                    hh = check_holiday(date,emp.name)
                    if hh:
                        if hh == 'WW':
                            total_weekoff += 1
                        elif hh == 'HH':
                            total_holiday += 1
                        row1.append(hh)
                    else:    
                        status = status_map.get(att[7], "")
                        if status != 'LOP':
                            if status == 'C-OFF':
                                total_combo_off += 1
                            else:
                                total_paid_leave += 1
                        else:                        
                            total_lop += 1
                        row1.append(status)
                else:
                    row1.append('-')
                if att[1] is not None and att[0] != 'Absent':
                    row2.append(att[1].strftime('%H:%M'))
                else:
                    row2.append('-')
                if att[2] is not None and att[0] != 'Absent':
                    row3.append(att[2].strftime('%H:%M'))
                else:
                    row3.append('-')
                
                if att[3]:
                    row4.append(att[3])
                else:
                    row4.append('-')

                if att[3] == 'C':
                    c_shift += 1   

                #This is the Late Hours Condition    
                if att[12]:
                    frappe.errprint(att[15])
                    hh = check_holiday(date,emp.name)
                    if hh:
                        if hh == 'WW':
                            total_weekoff += 1
                        elif hh == 'HH':
                            total_holiday += 1
                        row5.append('-')    
                    else:    
                        late = datetime.strptime(str(att[12]),'%H:%M:%S').strftime('%H:%M')
                        row5.append(late)
                        total_late = total_late + att[12]
                else:
                    row5.append('-')

                #This is the Late Deduct condition        
                if att[16]:
                    hh = check_holiday(date,emp.name)
                    if hh:
                        if hh == 'WW':
                            total_weekoff += 1
                        elif hh == 'HH':
                            total_holiday += 1
                        row6.append('-')
                    else:
                        str_time = datetime.strptime(att[16],'%H:%M').time()
                        time_time_delta = timedelta(hours=str_time.hour,minutes=str_time.minute,seconds=0)
                        row6.append(att[16]) 
                        #late_deduct column to add_time
                        total_late_deduct = total_late_deduct + time_time_delta
                    
                else:
                    row6.append('-')      

                if att[4] is not None and att[0] != 'Absent':
                    hh = att[4].seconds//3600
                    mm = (att[4].seconds//60)%60
                    twh = str(hh) + ":" + str(mm)
                    row7.append(twh) 
                else:
                    row7.append('-')    

                if att[5]:    
                    row8.append(att[5])
                    total_ot += att[5]
                else:
                    row8.append('-')
                                 
            else:
                # frappe.errprint('No Present')
                hh = check_holiday(date,emp.name)
                if hh:
                    if hh == 'WW': 
                        total_weekoff += 1
                    elif hh == 'HH':
                        total_holiday += 1
                    row1.append(hh)
                else:
                    row1.append('-')

                row2.append('-')
                row3.append('-')
                row4.append('-')
                row5.append('-')
                row6.append('-')
                row7.append('-')
                row8.append('-')

        permission_hours = frappe.db.sql("""select sum(hours) as sum from `tabPermission Request` where permission_date between '%s' and '%s' and employee_id = '%s' and docstatus = '1' """%(filters.from_date,filters.to_date,emp.name),as_dict=True)[0].sum or 0
        row1.extend([total_present,total_half_day,total_od,total_permission,total_absent,total_weekoff,total_holiday,total_paid_leave,total_lop,total_combo_off,total_ot,total_late,total_late_deduct,permission_hours,c_shift or ""])
        row2.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row3.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row4.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row5.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row6.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row7.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row8.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])



        data.append(row1)
        data.append(row2)
        data.append(row3)
        data.append(row4)
        data.append(row5)
        data.append(row6)
        data.append(row7)
        data.append(row8)
    return data

def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

def get_employees(filters):
    conditions = ''
    # if filters.department:
    #     conditions += "and department = '%s' " % filters.department
    # if filters.employee_type:
    #     conditions += "and employee_type = '%s' "%filters.employee_type
    left_employees = []
    if filters.employee:
        conditions += "and employee = '%s' " % (filters.employee)
    if filters.employee_category:
        conditions += "and employee_category = '%s' " % (filters.employee_category)

    employees = frappe.db.sql("""select name, employee_name, department,employee_category,date_of_joining from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
    left_employees = frappe.db.sql("""select name, employee_name, department,employee_category, date_of_joining from `tabEmployee` where status = 'Left' and relieving_date >= '%s' %s """ %(filters.from_date,conditions),as_dict=True)
    employees.extend(left_employees)
    frappe.errprint(employees)
    return employees
  
@frappe.whitelist()
def get_to_date(from_date):
    day = from_date[-2:]
    if int(day) > 21:
        d = add_days(get_last_day(from_date),21)
        return d
    if int(day) <= 21:
        d = add_days(get_first_day(from_date),21)
        return d

def check_holiday(date,emp):
    holiday_list = frappe.db.get_value('Company','Infac India Private Limited','default_holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        # elif holiday[0].att == 1:
        #     return 'C-OFF'         
        else:
            return "HH"


#latest Code for attendance
def mark_attendance_from_checkin(checkin,employee,time):
    att_date = time.date()
    att_time = time.time()
    print(att_date)
    if att_time < datetime.strptime('12:00:00','%H:%M:%S').time():
        cur_shift_assign = frappe.db.exists('Shift Assignment',{'employee':employee,'start_date':att_date,'docstatus':('!=','2')})
        if cur_shift_assign:
            shift = frappe.db.get_value('Shift Assignment',cur_shift_assign,'shift_type')
            if shift not in ('G','A'):
                yesterday = add_days(att_date,-1)
                y_shift = frappe.db.get_value('Shift Assignment',{'employee':employee,'start_date':yesterday,'docstatus':('!=','2')},'shift_type')
                if y_shift == 'B':
                    previous_day = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':yesterday,'docstatus':('!=',2)})
                    if not previous_day:
                        current_day = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=',2)})
                        if not current_day:
                            doc = frappe.new_doc('Attendance')
                            doc.employee = employee
                            doc.attendance_date = att_date
                            doc.status = 'Present'
                            doc.shift = "B"
                            doc.in_time = time
                            doc.total_wh = ''
                            doc.extra_hours = ''
                            doc.late_hours = ''
                            doc.save(ignore_permissions=True)
                            frappe.db.commit()
                            frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
                            frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                       
                        else:
                            frappe.db.set_value('Attendance',current_day,'out_time',time)
                            frappe.db.set_value("Employee Checkin",checkin, "attendance", current_day)
                            frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                    
                    else:        
                        frappe.db.set_value('Attendance',previous_day,'out_time',time)
                        frappe.db.set_value("Employee Checkin",checkin, "attendance", previous_day)
                        frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                      
            #     elif y_shift == 'C':
            #         previous_day = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':yesterday,'docstatus':('!=',2)})
            #         if not previous_day:
            #             current_day = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=',2)})
            #             if not current_day:
            #                 doc = frappe.new_doc('Attendance')
            #                 doc.employee = employee
            #                 doc.attendance_date = att_date
            #                 doc.status = 'Present'
            #                 doc.shift = y_shift
            #                 doc.in_time = time
            #                 doc.total_wh = ''
            #                 doc.extra_hours = ''
            #                 doc.late_hours = ''
            #                 doc.save(ignore_permissions=True)
            #                 frappe.db.commit()
            #                 frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
            #                 frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                          
            #             else:
            #                 frappe.db.set_value('Attendance',current_day,'out_time',time)
            #                 frappe.db.set_value("Employee Checkin",checkin, "attendance", current_day)
            #                 frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                            
            #         else:        
            #             frappe.db.set_value('Attendance',previous_day,'out_time',time)
            #             frappe.db.set_value("Employee Checkin",checkin, "attendance", previous_day)
            #             frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                
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
                        doc.extra_hours = ''
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
                        doc.extra_hours = ''
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
                # if shift == None:
                #     shift = 'G'
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
                    doc.extra_hours = ''
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
                doc.shift = 'G'
                doc.in_time = time
                doc.out_time = ''
                doc.total_wh = ''
                doc.extra_hours = ''
                doc.late_hours = ''
                doc.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
                frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                return doc
           
            else:
                frappe.db.set_value('Attendance',att,'out_time',time)
                frappe.db.set_value("Employee Checkin",checkin, "attendance", att)
                frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')  
                return att
           
    else:
        shift = frappe.db.get_value('Shift Assignment',{'employee':employee,'start_date':date,'docstatus':('!=','2')},'shift_type')
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
            doc.extra_hours = ''
            doc.late_hours = ''
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
            frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
   
        else:
            frappe.db.set_value('Attendance',att,'out_time',time)
            frappe.db.set_value("Employee Checkin",checkin, "attendance", att)
            frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')  
     
