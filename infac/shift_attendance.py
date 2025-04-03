from os import name, pread
from selectors import EpollSelector
from time import strptime
from traceback import print_tb
import frappe
import pandas as pd
import json
import datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
import requests
from datetime import date, timedelta,time
from frappe.utils import get_url_to_form
import math
from frappe.utils.background_jobs import enqueue
from erpnext.hr.utils import get_holiday_dates_for_employee

def mark_att_manual_today():
    start_date = '2024-08-25'
    end_date = '2024-08-25'
    att = frappe.db.sql(""" update `tabEmployee Checkin` set skip_auto_attendance = 0 where date(time) between %s and %s """,(start_date, end_date), as_dict=True)
    return "Ok"

def mark_att_today():
    # from_date = add_days(today(),-1)
    # to_date = today()
    from_date = '2024-08-25'
    to_date = '2024-08-25'
    # employee = 'SMS0085'
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) between '%s' and '%s'  order by time   """%(from_date,to_date),as_dict=True)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            #the below mthod to mark the checkin in attendance application for IN and OUT Punches
            mark_attendance_from_checkin(c.name,c.employee,c.time)
    #the below method to mark the Employees do not have punches.       
    mark_absent(from_date,to_date)
    #the below method to mark the IN and OUT Punches of Total Working and OT Hours 
    mark_wh_ot(from_date,to_date)
    #the below method to calculate the Staff Categories Employees working as Overtime to calculate the Incentive Amount
    mark_incentive_amount_staff_categories(from_date,to_date)
    #this below method to check the Employee have assigned shift assignment and marked in attendance..
    mark_assigned_shift(from_date,to_date)
    #this below method to mark the IN time Based on which shift will comes the actual Shift
    mark_attended_shift(from_date,to_date)
    #the below method to mark the assigned shift and actual shift matched or not,not matched employees mark as absent
    mark_status_as_absent(from_date,to_date)
    #the below method when a employee have only one punches in attendance it will mark as absent.
    mark_single_punch_as_absent(from_date,to_date)
    #the below method if an employee comes in week-off or Holiday Days that day Present
    mark_attendance_as_present_mark_holiday(from_date,to_date)
    #the below method employee week-off and holiday date attendance moved to Holiday Attendance Doctype
    check_holiday_moved_to_holiday_attendance(from_date,to_date)
    #th below method Employee status mark as Half Day the Late Hours,Late Deduct,Late HR will be Empty
    make_late_hours_empty(from_date,to_date)

def mark_att_manual():
    from_date = '2024-07-01'
    to_date = '2024-07-02'
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s'  order by time   """%(from_date,to_date),as_dict=True)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            #the below mthod to mark the checkin in attendance application for IN and OUT Punches
            mark_attendance_from_checkin(c.name,c.employee,c.time)
    #the below method to mark the Employees do not have punches.       
    mark_absent(from_date,to_date)
    #the below method to mark the IN and OUT Punches of Total Working and OT Hours 
    mark_wh_ot(from_date,to_date)
    #the below method to calculate the Staff Categories Employees working as Overtime to calculate the Incentive Amount
    mark_incentive_amount_staff_categories(from_date,to_date)
    #this below method to check the Employee have assigned shift assignment and marked in attendance..
    mark_assigned_shift(from_date,to_date)
    #this below method to mark the IN time Based on which shift will comes the actual Shift
    mark_attended_shift(from_date,to_date)
    #the below method to mark the assigned shift and actual shift matched or not,not matched employees mark as absent
    mark_status_as_absent(from_date,to_date)
    #the below method when a employee have only one punches in attendance it will mark as absent.
    mark_single_punch_as_absent(from_date,to_date)
    #the below method if an employee comes in week-off or Holiday Days that day Present
    mark_attendance_as_present_mark_holiday(from_date,to_date)
    #the below method employee week-off and holiday date attendance moved to Holiday Attendance Doctype
    check_holiday_moved_to_holiday_attendance(from_date,to_date)
    #th below method Employee status mark as Half Day the Late Hours,Late Deduct,Late HR will be Empty
    make_late_hours_empty(from_date,to_date)

def mark_att():
    from_date = add_days(today(),-1)
    to_date = today()
    # from_date = '2023-12-21'
    # to_date = '2023-12-26'
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where skip_auto_attendance = 0 and date(time) between '%s' and '%s'  order by time   """%(from_date,to_date),as_dict=True)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            #the below mthod to mark the checkin in attendance application for IN and OUT Punches
            mark_attendance_from_checkin(c.name,c.employee,c.time)
    #the below method to mark the Employees do not have punches.       
    mark_absent(from_date,to_date)
    #the below method to mark the IN and OUT Punches of Total Working and OT Hours 
    mark_wh_ot(from_date,to_date)
    #the below method to calculate the Staff Categories Employees working as Overtime to calculate the Incentive Amount
    mark_incentive_amount_staff_categories(from_date,to_date)
    #this below method to check the Employee have assigned shift assignment and marked in attendance..
    mark_assigned_shift(from_date,to_date)
    #this below method to mark the IN time Based on which shift will comes the actual Shift
    mark_attended_shift(from_date,to_date)
    #the below method to mark the assigned shift and actual shift matched or not,not matched employees mark as absent
    mark_status_as_absent(from_date,to_date)
    #the below method when a employee have only one punches in attendance it will mark as absent.
    mark_single_punch_as_absent(from_date,to_date)
    #the below method if an employee comes in week-off or Holiday Days that day Present
    mark_attendance_as_present_mark_holiday(from_date,to_date)
    #the below method employee week-off and holiday date attendance moved to Holiday Attendance Doctype
    check_holiday_moved_to_holiday_attendance(from_date,to_date)
    #th below method Employee status mark as Half Day the Late Hours,Late Deduct,Late HR will be Empty
    make_late_hours_empty(from_date,to_date)

def mark_attendance_from_checkin(checkin,employee,time):
    att_date = time.date()
    att_time = time.time()
    print(att_date)
    if att_time < datetime.strptime('12:00:00','%H:%M:%S').time():
        shift = frappe.db.get_value('Shift Assignment',{'employee':employee,'start_date':att_date,'docstatus':('!=','2')},'shift_type')
        if shift not in ('G','A','B'):
            yesterday = add_days(att_date,-1)
            get_shift_previous_day = frappe.db.get_value('Shift Assignment',{'start_date':yesterday,'employee':employee,'docstatus':('!=','2')},['shift_type'])
            if get_shift_previous_day == 'C':
                previous_day_att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':yesterday,'docstatus':('!=',2)})
                if not previous_day_att:
                    doc = frappe.new_doc('Attendance')
                    doc.employee = employee
                    doc.attendance_date = att_date
                    doc.status = 'Absent'
                    doc.shift = 'C'
                    doc.in_time = time
                    doc.out_time = ''
                    doc.total_wh = '00:00'
                    doc.late_hours = '00:00'
                    doc.extra_hours = '00:00'
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
                    frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                else:
                    frappe.db.set_value('Attendance',previous_day_att,'out_time',time)
                    frappe.db.set_value('Attendance',previous_day_att,'status','Present') 
                    frappe.db.set_value("Employee Checkin",checkin, "attendance", previous_day_att)
                    frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
            else:
                if get_shift_previous_day == None:
                    get_shift_previous_day = 'G'
                att = frappe.db.exists('Attendance',{'employee':employee,'attendance_date':att_date,'docstatus':('!=',2)})
                if not att:
                    doc = frappe.new_doc('Attendance')
                    doc.employee = employee
                    doc.attendance_date = att_date
                    doc.status = 'Absent'
                    doc.shift = get_shift_previous_day
                    doc.in_time = time
                    doc.out_time = ''
                    doc.total_wh = '00:00'
                    doc.late_hours = '00:00'
                    doc.extra_hours = '00:00'
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
                    frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
                else:
                    frappe.db.set_value('Attendance',att,'out_time',time)
                    frappe.db.set_value('Attendance',att,'status','Present') 
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
                doc.status = 'Absent'
                doc.shift = shift
                doc.in_time = time
                doc.out_time = ''
                doc.total_wh = '00:00'
                doc.late_hours = '00:00'
                doc.extra_hours = '00:00'
                doc.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
                frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
            else:
                frappe.db.set_value('Attendance',att,'out_time',time)
                frappe.db.set_value('Attendance',att,'status','Present') 
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
            doc.status = 'Absent'
            doc.shift = shift
            doc.in_time = time
            doc.out_time = ''
            doc.total_wh = '00:00'
            doc.late_hours = '00:00'
            doc.extra_hours = '00:00'
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.db.set_value("Employee Checkin",checkin, "attendance", doc.name)
            frappe.db.set_value('Employee Checkin',checkin,'skip_auto_attendance','1')
        else:
            frappe.db.set_value('Attendance',att,'out_time',time)
            frappe.db.set_value('Attendance',att,'status','Present') 
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
                on_duty = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')},['on_duty_marked'])
                if not on_duty:
                    if not frappe.db.exists('Attendance',{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')}):
                        att = frappe.new_doc('Attendance')
                        att.employee = emp.name
                        att.status = 'Absent'
                        att.attendance_date = date
                        att.total_wh = '00:00:00'
                        att.extra_hours = '00:00:00'
                        att.late_hours ='00:00:00'
                        att.save(ignore_permissions=True)
                        frappe.db.commit()
@frappe.whitelist()                    
def mark_wh_ot(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for att in attendance:
        if not att.attendance_regularize:
            if not att.leave_application:
                if not att.permission_request:
                    if not att.on_duty_marked:
                        if not att.miss_punch_marked:
                            if att.in_time and att.out_time:
                                hh = check_holiday(att.attendance_date,att.employee)
                                if not hh:
                                    total_wh = att.out_time - att.in_time
                                    try:
                                        wh = time_diff_in_hours(att.out_time,att.in_time)
                                        frappe.db.set_value('Attendance',att.name,'total_wh',total_wh)
                                        frappe.db.set_value('Attendance',att.name,'working_hours',wh)
                                    except:
                                        wh = 0.0
                                        frappe.db.set_value('Attendance',att.name,'total_wh','00:00')
                                        frappe.db.set_value('Attendance',att.name,'working_hours','0.0')
                                    if wh < 4.0:
                                        frappe.db.set_value('Attendance',att.name,'status','Absent')
                                    elif wh >= 4.0 and wh < 5.99:
                                        frappe.db.set_value('Attendance',att.name,'status','Half Day')   
                                    elif  wh >= 6.0:
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
                                        if att.in_time > shift_start_datetime and att.status == "Present":
                                            late_hour = att.in_time - shift_start_datetime
                                            late_hr = time_diff_in_hours(att.in_time,shift_start_datetime)
                                            frappe.db.set_value('Attendance',att.name,'late_hrs',late_hr)
                                            frappe.db.set_value('Attendance',att.name,'late_hours',late_hour)
                                        else:
                                            frappe.db.set_value('Attendance',att.name,'late_hrs','0.0')
                                            frappe.db.set_value('Attendance',att.name,'late_hours','00:00')

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
                                            get_late_time = datetime.strptime(str(late_deducted_time),'%H:%M:%S')
                                            late_deduct = get_late_time.strftime('%H:%M')
                                            frappe.db.set_value('Attendance',att.name,'late_deduct',late_deduct)  
                                            frappe.db.set_value('Attendance',att.name,'late_entry','1') 
                                            frappe.db.set_value('Attendance',att.name,'status','Present')   
                                    
                                    if shift_end_datetime:
                                        extra_hrs = pd.to_datetime('00:00:00').time()
                                        ot_hr = 0
                                        if att.out_time > shift_end_datetime:
                                            extra_hrs = att.out_time - shift_end_datetime
                                            extras = time_diff_in_hours(att.out_time,shift_end_datetime)
                                            if extras > 1.0:
                                                ot_hr = math.floor(extras * 2) / 2
                                                frappe.db.set_value('Attendance',att.name,'ot_hrs',ot_hr)
                                                frappe.db.set_value('Attendance',att.name,'extra_hours',extra_hrs)
                                                frappe.db.set_value('Attendance',att.name,'total_wh',total_wh)
                                                frappe.db.set_value('Attendance',att.name,'working_hours',wh)
                                            else:
                                                none_time = pd.to_datetime('00:00:00').time()
                                                frappe.db.set_value('Attendance',att.name,'ot_hrs',0)
                                                frappe.db.set_value('Attendance',att.name,'extra_hours',extra_hrs)
                                                frappe.db.set_value('Attendance',att.name,'total_wh',total_wh)
                                                frappe.db.set_value('Attendance',att.name,'working_hours',wh)   
                                        else:
                                            none_time = pd.to_datetime('00:00:00').time()
                                            frappe.db.set_value('Attendance',att.name,'ot_hrs',0)
                                            frappe.db.set_value('Attendance',att.name,'extra_hours','00:00')
                                # holiday or week-off days as total wh as ot hr
                                else:
                                    total_wh = att.out_time - att.in_time
                                    wh = time_diff_in_hours(att.out_time,att.in_time)
                                    frappe.db.set_value('Attendance',att.name,'status','Present')
                                    if wh > 0:
                                        #0.5 Hours Lunch Break we reduc e in total ot hr
                                        ot_hr = (math.floor(wh * 2) / 2) - 0.5
                                        none_time =pd.to_datetime('00:00:00').time()
                                        frappe.db.set_value('Attendance',att.name,'ot_hrs',ot_hr)  
                                        frappe.db.set_value('Attendance',att.name,'extra_hours',total_wh)
                                        frappe.db.set_value('Attendance',att.name,'total_wh',total_wh)
                                        frappe.db.set_value('Attendance',att.name,'working_hours',wh)
                                    else:
                                        none_time =pd.to_datetime('00:00:00').time()
                                        frappe.db.set_value('Attendance',att.name,'ot_hrs',0)
                                        frappe.db.set_value('Attendance',att.name,'extra_hours',none_time)
                                        frappe.db.set_value('Attendance',att.name,'total_wh',none_time)
                                        frappe.db.set_value('Attendance',att.name,'working_hours',0)
              
def check_holiday(date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    frappe.errprint(holiday_list)
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    frappe.errprint(holiday)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"

@frappe.whitelist()
def enqueue_mark_att(from_date,to_date):
    enqueue(mark_incentive_amount_staff_categories, queue='default',timeout=6000, event='ot_incentive',from_date=from_date,to_date=to_date)

@frappe.whitelist()
def mark_incentive_amount_staff_categories(from_date,to_date):
    employee = frappe.db.get_all('Employee',{'Status':'Active','incentive_category':'Yes'},['*'])
    for emp in employee:
        attendance = frappe.db.sql(""" select ot_hrs,name from `tabAttendance` where attendance_date between '%s' and '%s' and employee = '%s' and docstatus != '2'  """%(from_date,to_date,emp.name),as_dict=True)
        for att in attendance:
            e_slap_ot_start = frappe.db.get_single_value('Attendance Settings','e_slap_ot_start')
            t_slap_ot_start = frappe.db.get_single_value('Attendance Settings','t_slap_ot_start')
            m_slap_ot_start = frappe.db.get_single_value('Attendance Settings','m_slap_ot_start')
            e_slap_ot_end = frappe.db.get_single_value('Attendance Settings','e_slap_ot_end')
            t_slap_ot_end = frappe.db.get_single_value('Attendance Settings','t_slap_ot_end')
            m_slap_ot_end = frappe.db.get_single_value('Attendance Settings','m_slap_ot_end')

            if att.ot_hrs >= e_slap_ot_start and att.ot_hrs < e_slap_ot_end:
                frappe.db.set_value('Attendance',att.name,'e_slap_ot_hrs',att.ot_hrs)
                e_slap_amount = frappe.db.get_single_value('Attendance Settings','e_slap_ot_incentive_amount')
                frappe.db.set_value('Attendance',att.name,'e_slap_incentive_amount',e_slap_amount)
            elif att.ot_hrs >= t_slap_ot_start and att.ot_hrs < t_slap_ot_end:
                frappe.db.set_value('Attendance',att.name,'t_slap_ot_hrs',att.ot_hrs)
                t_slap_amount = frappe.db.get_single_value('Attendance Settings','t_slap_ot_incentive_amount')
                frappe.db.set_value('Attendance',att.name,'t_slap_incentive_amount',t_slap_amount)
            elif att.ot_hrs > m_slap_ot_start:   
                frappe.db.set_value('Attendance',att.name,'m_slap_ot_hrs',att.ot_hrs)
                m_slap_amount = frappe.db.get_single_value('Attendance Settings','m_slap_ot_incentive_amount')
                frappe.db.set_value('Attendance',att.name,'m_slap_incentive_amount',m_slap_amount)
    return "OT Updated"        
                
def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

def get_actual_shift(get_shift_time):
    from datetime import datetime
    from datetime import date, timedelta,time
    nowtime = datetime.now()
    shift_A_time = [time(hour=5, minute=0, second=0),time(hour=7, minute=30, second=0)]
    shift_G_time = [time(hour=7, minute=31, second=0),time(hour=12, minute=00, second=0)]
    shift_B_time = [time(hour=13, minute=00, second=0),time(hour=18, minute=30, second=0)]
    shift_C_time = [time(hour=20, minute=0, second=1),time(hour=23, minute=59, second=0)]
    shift = ''
    if is_between(get_shift_time,shift_A_time):
        shift = 'A'
    if is_between(get_shift_time,shift_G_time):
        shift = 'G'
    if is_between(get_shift_time,shift_B_time):
        shift = 'B'
    if is_between(get_shift_time,shift_C_time):
        shift = 'C'
    return shift    

def get_employees_attendance(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    return attendance

def mark_assigned_shift(from_date,to_date):
    get_attendance = get_employees_attendance(from_date,to_date)
    for att in get_attendance:
        if not att.attendance_regularize:
            shift = frappe.db.exists('Shift Assignment',{'start_date':att.attendance_date,'employee':att.employee,'docstatus':('!=','2')})
            if shift:
                get_shift = frappe.db.get_value('Shift Assignment',{'start_date':att.attendance_date,'employee':att.employee,'docstatus':('!=','2')},['shift_type'])
                get_shift_start_time = frappe.db.get_value('Shift Type',{'name':get_shift},['start_time'])
                get_shift_end_time = frappe.db.get_value('Shift Type',{'name':get_shift},['end_time'])
                frappe.db.set_value('Attendance',att.name,'shift_type',get_shift)
                frappe.db.set_value('Attendance',att.name,'shift_in_time',get_shift_start_time)
                frappe.db.set_value('Attendance',att.name,'shift_out_time',get_shift_end_time)
            else:
                get_shift_start_time = frappe.db.get_value('Shift Type',{'name':"G"},['start_time'])
                get_shift_end_time = frappe.db.get_value('Shift Type',{'name':"G"},['end_time'])
                frappe.db.set_value('Attendance',att.name,'shift_type',"G")
                frappe.db.set_value('Attendance',att.name,'shift_in_time',get_shift_start_time)
                frappe.db.set_value('Attendance',att.name,'shift_out_time',get_shift_end_time)

def mark_attended_shift(from_date,to_date):
    get_attendance = get_employees_attendance(from_date,to_date)
    for att in get_attendance:
        if not att.attendance_regularize:
            if att.in_time:
                get_shift_time = pd.to_datetime(str(att.in_time)).time()
                attended_shift = get_actual_shift(get_shift_time)
                frappe.db.set_value('Attendance',att.name,'actual_shift',attended_shift)
                frappe.db.set_value('Attendance',att.name,'actual_in_time',format_datetime(att.in_time))
                if att.out_time:
                    frappe.db.set_value('Attendance',att.name,'actual_out_time',format_datetime(att.out_time))
                else:
                    frappe.db.set_value('Attendance',att.name,'actual_out_time','-')
            else:
                frappe.db.set_value('Attendance',att.name,'actual_shift','')
                frappe.db.set_value('Attendance',att.name,'actual_in_time','')
                frappe.db.set_value('Attendance',att.name,'actual_out_time','')

def mark_status_as_absent(from_date,to_date):
    get_attendance = get_employees_attendance(from_date,to_date)
    for att in get_attendance:
        if not att.leave_application:
            if not att.attendance_regularize:
                if att.actual_shift:
                    if att.shift_type == att.actual_shift:
                        frappe.db.set_value('Attendance',att.name,'matched_status','Matched')
                        frappe.db.set_value('Attendance',att.name,'status','Present')
                    else:
                        frappe.db.set_value('Attendance',att.name,'matched_status','Unmatched')
                        frappe.db.set_value('Attendance',att.name,'status','Absent') 
                else:
                    frappe.db.set_value('Attendance',att.name,'matched_status','Unmatched')
                    frappe.db.set_value('Attendance',att.name,'status','Absent') 
    return "Completed"            

def mark_single_punch_as_absent(from_date,to_date):
    get_attendance = get_employees_attendance(from_date,to_date)
    for att in get_attendance:
        if not att.leave_application:
            if not att.attendance_regularize:
                if att.matched_status == 'Matched':
                    if att.in_time and not att.out_time:
                        frappe.db.set_value('Attendance',att.name,'status','Absent') 
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Present') 
                else:
                    frappe.db.set_value('Attendance',att.name,'status','Absent')      

@frappe.whitelist()
def check_holiday_moved_to_holiday_attendance(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for att in attendance:
        if att.in_time and att.out_time:
            hh = check_holiday(att.attendance_date,att.employee)
            if hh:
                hd_att = frappe.db.exists('Holiday Attendance',{'attendance_date':att.attendance_date,'employee':att.employee,'docstatus':('!=','2')})
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
                frappe.db.sql(""" delete from `tabAttendance` where name = '%s' """%(att.name))    
    return "Holiday Attendance"                

def make_late_hours_empty(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for att in attendance:
        if att.status == 'Half Day':
            frappe.db.set_value('Attendance',att.name,'late_hours','00:00')
            frappe.db.set_value('Attendance',att.name,'late_hrs','')
            frappe.db.set_value('Attendance',att.name,'late_deduct','')

def mark_attendance_as_present_mark_holiday(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    if attendance:
        for att in attendance:
            if att.in_time and att.out_time:
                hh = check_holiday(att.attendance_date,att.employee)
                if hh:
                    holiday_att = frappe.get_doc('Attendance',att.name)
                    holiday_att.status = 'Present'
                    holiday_att.shift_type = ''
                    holiday_att.shift_in_time = ''
                    holiday_att.shift_out_time = ''
                    holiday_att.actual_shift = ''
                    holiday_att.actual_in_time = ''
                    holiday_att.actual_out_time = ''
                    holiday_att.matched_status = ''
                    holiday_att.save(ignore_permissions=True)
                    frappe.db.commit()
    else:
        holiday_attendance = frappe.db.get_all('Holiday Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2'),'employee':'BSA0032'},['*']) 
        if holiday_attendance:
            for att in holiday_attendance:
                if att.in_time and att.out_time:
                    hh = check_holiday(att.attendance_date,att.employee)
                    if hh:
                        holiday_att = frappe.get_doc('Holiday Attendance',att.name)
                        holiday_att.status = 'Present'
                        holiday_att.shift_type = ''
                        holiday_att.shift_in_time = ''
                        holiday_att.shift_out_time = ''
                        holiday_att.actual_shift = ''
                        holiday_att.actual_in_time = ''
                        holiday_att.actual_out_time = ''
                        holiday_att.matched_status = ''
                        holiday_att.save(ignore_permissions=True)
                        frappe.db.commit()          