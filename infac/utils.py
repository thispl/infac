from email import message
import frappe
import datetime
import pandas as pd
import math
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,format_date)
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours   
from datetime import date, timedelta,time,datetime
from frappe import _




#late deduct calculation for Attendance
@frappe.whitelist()
def late_calculation(date):
    attendance = frappe.db.get_all('Attendance',['name','employee','in_time','out_time','attendance_date'])
    for att in attendance:
        actual_late_hours = frappe.db.get_value('Attendance',att.name,'late_hours')
        if actual_late_hours:
            late_deduct_hour = actual_late_hours.seconds//3600
            late_deduct_minute = ((actual_late_hours.seconds//60)%60)
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


@frappe.whitelist()
def mark_shift(att_time):
    get_time = datetime.strptime(att_time,'%Y-%m-%d %H:%M:%S').strftime('%H:%M')
    if datetime.strptime('05:30:00','%H:%M:%S').strftime('%H:%M') < get_time < datetime.strptime('07:30:00','%H:%M:%S').strftime('%H:%M'):
        return 'A'
    if datetime.strptime('07:31:00','%H:%M:%S').strftime('%H:%M') < get_time < datetime.strptime('11:00:00','%H:%M:%S').strftime('%H:%M'):
        return 'G'   
    elif datetime.strptime('12:30:00','%H:%M:%S').strftime('%H:%M') < get_time < datetime.strptime('15:00:00','%H:%M:%S').strftime('%H:%M'):
        return 'B'
    elif datetime.strptime('20:00:00','%H:%M:%S').strftime('%H:%M') < get_time < datetime.strptime('23:30:00','%H:%M:%S').strftime('%H:%M'):
        return 'C' 
    else:
        return ''        

#Attendance Request while saving below actions are working
@frappe.whitelist() 
def set_attendance(in_time,out_time,shift): 
    data = []    
    str_in_time = datetime.strptime(in_time,'%Y-%m-%d %H:%M:%S')
    str_out_time = datetime.strptime(out_time,'%Y-%m-%d %H:%M:%S')
    total_wh = str_out_time - str_in_time
    wh_time_change = datetime.strptime(str(total_wh),'%H:%M:%S').strftime('%H:%M')
    ftr = [3600,60,1]
    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
    wh = round(hr/3600,1)
    data.append(wh)
    data.append(wh_time_change)
   
    # return wh,wh_time_change
    #This is the late_hour,late_hr and late_deduct calculation below
    shift_start_time = frappe.db.get_value('Shift Type',shift,'start_time')
    shift_start_time_change = pd.to_datetime(str(shift_start_time)).time()
    att_in_time = datetime.strptime(in_time,'%Y-%m-%d %H:%M:%S')
    in_time_to_date = att_in_time.date()
    shift_start_date_time = datetime.combine(in_time_to_date,shift_start_time_change)
    if shift_start_date_time:
        late_hour = pd.to_datetime('00:00:00').time()
        late_hr = 0
        #This is the Late_hour and late_hr
        if att_in_time > shift_start_date_time:
            late_hour = att_in_time - shift_start_date_time
            late_hour_time = datetime.strptime(str(late_hour),'%H:%M:%S').strftime('%H:%M')      
            hr = sum([a*b for a,b in zip(ftr, map(int,str(late_hour).split(':')))])
            late_hr = round(hr/3600,1)  
            data.append(late_hour_time)
            data.append(late_hr)
        #This is the late_hour will be round off based on late_hour     
        actual_late_hour = late_hour
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
    #This is the out_time and shift_end_time based on total_wh, extra_hr and ot_hr 
    shift_end_time = frappe.db.get_value('Shift Type',shift,'end_time')
    shift_end_time_change = pd.to_datetime(str(shift_end_time)).time()
    att_out_time = datetime.strptime(out_time,'%Y-%m-%d %H:%M:%S')
    out_time_to_date = att_out_time.date()
    total_shift_hours = frappe.db.get_value('Shift Type',shift,'total_hours')
    shift_end_date_time = datetime.combine(out_time_to_date,shift_end_time_change)
    #Calculating the total_wh,extra_hr and ot_hr
    if shift_end_date_time:
        extra_hrs = pd.to_datetime('00:00:00').time()
        ot_hr = 0
        if att_out_time > shift_end_date_time:
            if total_wh > total_shift_hours:
                extra_hrs = att_out_time - shift_end_date_time
                extra_hrs_time = datetime.strptime(str(extra_hrs),'%H:%M:%S').strftime('%H:%M')
                hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                extras = round(hr/3600,1)
                frappe.errprint(extras)
                if extras > 1:
                    ot_hr = math.floor(extras * 2) / 2

    return data
    #This is the returning the output of wh,wh_time_change,late_hour_time,time_change,extra_hrs_time,ot_hr,late_hr
    # return wh,wh_time_change,late_hour_time


#While Attendance in Draft the below process working to compare the assign_shift and actual_shift
# @frappe.whitelist()
# def get_attendance(doc,method):
#     get_shift = frappe.db.get_value('Shift Assignment',{'employee':doc.employee,'start_date':doc.attendance_date},['shift_type'])
#     if get_shift:
#         doc.shift_type  = frappe.db.get_value('Shift Assignment',{'start_date':doc.attendance_date,'employee':doc.employee},['shift_type'])
#         get_shift_start_time = frappe.db.get_value('Shift Type',{'name':doc.shift_type},['start_time',])
#         get_shift_end_time = frappe.db.get_value('Shift Type',{'name':doc.shift_type},['end_time'])
#         doc.shift_in_time = get_shift_start_time
#         doc.shift_out_time = get_shift_end_time
#     else:
#         doc.shift_type = 'G'
#         doc.shift_in_time = frappe.db.get_value('Shift Type',{'name':'G'},['start_time'])
#         doc.shift_out_time = frappe.db.get_value('Shift Type',{'name':'G'},['end_time'])

#     if doc.in_time:
#         doc.actual_in_time = doc.in_time
#         doc.actual_out_time = doc.out_time
#         datetime_to_time = datetime.strptime(str(doc.in_time),'%Y-%m-%d %H:%M:%S').time()
#         doc.actual_shift = get_actual_shift(datetime_to_time)
#     else:
#         doc.actual_in_time = '' 
#         doc.actual_out_time = ''   
#         doc.actual_shift = 'NA' 
#     #checking the shift_type anAttendanced actual_shift is there in the field    
#     if doc.shift_type and doc.actual_shift:
#         if doc.shift_type == doc.actual_shift:
#             doc.matched_status = 'Matched'
#             doc.status = 'Present'
#         else:
#             doc.status = 'Absent'
#             frappe.errprint(doc.status)
#             # frappe.db.set_value('Attendance',doc.name,'status','Absent')   
#             doc.matched_status = 'Unmatched'
            
#     else:
#         doc.matched_status = 'Unmatched'     


# @frappe.whitelist()
# def mark_status_absent(doc,method):
#     if doc.matched_status ==  'Unmatched':
#         doc.status = 'Absent'   
#     doc.save(ignore_permissions=True)
#     frappe.db.commit()
    


# this is the comparsion of time between 
# def is_between(time, time_range):
#     if time_range[1] < time_range[0]:
#         return time >= time_range[0] or time <= time_range[1]
#     return time_range[0] <= time <= time_range[1]
# #this is the getting the actual shift based on assuming the time period to call this method above get_attendance method to mark the actual_shift
# def get_actual_shift(datetime_to_time):
#     from datetime import datetime
#     from datetime import date, timedelta,time
#     nowtime = datetime.now()
#     #this is the shift_time_range between [0] and [1] 
#     shift_A_time = [time(hour=5, minute=0, second=0),time(hour=7, minute=30, second=0)]
#     shift_G_time = [time(hour=7, minute=31, second=0),time(hour=12, minute=00, second=0)]
#     shift_B_time = [time(hour=13, minute=00, second=0),time(hour=18, minute=30, second=0)]
#     shift_C_time = [time(hour=20, minute=0, second=1),time(hour=23, minute=59, second=0)]
#     shift = ''
#     if is_between(datetime_to_time,shift_A_time):
#         shift = 'A'
#     if is_between(datetime_to_time,shift_G_time):
#         shift = 'G'
#     if is_between(datetime_to_time,shift_B_time):
#         shift = 'B'
#     if is_between(datetime_to_time,shift_C_time):
#         shift = 'C'
#     return shift


#validate Leave Type in Maternity & Paternity in leave_application
# @frappe.whitelist()
# def validate_leave_type(employee,leave_type):
#     if leave_type == 'Maternity Leave' or leave_type == 'Paternity Leave':
#         kids_count = frappe.db.get_value('Employee',{'status':'Active','name':employee},['number_of_kids'])
#         if kids_count > 2:
#             frappe.throw(_('As Per Policy %s limit has been reached'%leave_type))



#validate coff working_hour greater than 8
@frappe.whitelist()
def validate_coff(emp,att_date):
    data = []
    attendance = frappe.db.get_value('Attendance',{'attendance_date':att_date,'employee':emp},['in_time','out_time','working_hours','on_duty_marked'])
    if attendance[0] and attendance[1]:
        if attendance[2] < 8:
            data.append(frappe.throw(_('Employee Working Hours less than 8')))
        else:
            frappe.log_error('Employee Working Hours greater than 8')   
    elif attendance [3]:
        on_duty = frappe.db.get_value('On Duty Application',{'name':attendance[3]},['hours'])
        if on_duty:
            ftr = [3600,60,1]
            hr = sum([a*b for a,b in zip(ftr, map(int,str(on_duty).split(':')))])
            wh = round(hr/3600,1)
            if wh < 8:
                data.append(frappe.throw(_('Employee Working Hours less than 8')))
            else:
                frappe.log_error('Employee Working Hours greater than 8')     
    return data             


# @frappe.whitelist()
# def leave_validation(emp,from_date):
#     attendance = frappe.db.sql(""" select permission_request from `tabAttendance` where employee = '%s' and attendance_date = '%s' and permission_request is not null """%(emp,from_date))
#     return "Permission Marked"

@frappe.whitelist()
def emp_trainee_complete():
    employee = frappe.db.sql(""" select name,employee_name,date_of_joining,employment_type from `tabEmployee` where status = 'Active' and name = 'BSA0014'  """,as_dict=1)
    data = ''
    data+='<table class = table table-bordered >' 
    data += '<table class="table table-bordered"><tr rowspan = 3 ><th style="padding:1px;border: 1px solid black;" colspan=6><center><b>Employee on Training Period</b></center></th></tr>'
    data += '<table class="table table-bordered"><tr rowspan = 3 ><td style="padding:1px;border: 1px solid black;" colspan=4><center><b>Employee</b></center></td><td style="padding:1px;border: 1px solid black;" colspan=5><center><b>Eemployee Name</b></center></td><td style="padding:1px;border: 1px solid black;" colspan=5><center><b>Employment Type</b></center></td><td style="padding:1px;border: 1px solid black;" colspan=2><center><b>Training End Date</b></center></td></tr>'
    for emp in employee:
        current_date = datetime.today().date()
        training_end_date = add_months(emp.date_of_joining,12)
        mail_Sent_date = add_months(training_end_date,-1)
        if emp.employment_type:
            if training_end_date:
                data += '<tr><td colspan=4 style="border: 1px solid black;overflow-wrap: anywhere;"><center>%s</center></td><td colspan=4 style="border: 1px solid black;overflow-wrap: anywhere;"><center>%s</center></td><td colspan=4 style="border: 1px solid black;overflow-wrap: anywhere;"><center>%s</center></td><td colspan=4 style="border: 1px solid black;overflow-wrap: anywhere;"><center>%s</center></td></tr>'%(emp.name,emp.employee_name,emp.employment_type,format_date(training_end_date))
            else:
                frappe.log_error('Employee {0} has no Complete {0}  One Year'.format(emp.name,emp.employment_type))    
        else:
            frappe.log_error('Employee {0} has no Employment Type'.format(emp.name)) 
        if current_date == mail_Sent_date:
            print(emp.name)    
    data += '</table>' 
    if current_date ==  mail_Sent_date:
        frappe.sendmail(
            recipients=['jagadeesan.a@groupteampro.com'],
            subject=('Employee Trainee Completion'),
            message = """
                    Dear Sir,<br><br>
                    Kindly find the below Employee list whose Training date is going to be end <br>%s""" % (data)
        )          

@frappe.whitelist()
def leave_application(doc,method):
    if doc.half_day == 1:
        att =  frappe.db.exists('Attendance',{'employee':doc.employee,'attendance_date':doc.from_date})
        if att:
            att_status = frappe.db.get_value('Attendance',{'name':att},['status'])
            if att_status == 'Half Day':
                leave = frappe.get_doc('Attendance',att)
                leave.leave_type = doc.leave_type
                leave.leave_application = doc.name
                leave.save(ignore_permissions=True)
                leave.submit()
                frappe.db.commit()

