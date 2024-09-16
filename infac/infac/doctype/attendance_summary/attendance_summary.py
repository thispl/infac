# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr, add_days, date_diff,format_datetime,format_date,getdate
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today,time_diff_in_hours,get_datetime,get_time

from datetime import date, timedelta, datetime, time

class AttendanceSummary(Document):
    pass

@frappe.whitelist()
def get_data_mobile(emp,start_date,end_date):
    
    no_of_days = date_diff(add_days(end_date, 1), start_date)
    dates = [add_days(start_date, i) for i in range(0, no_of_days)]

    emp_name = frappe.db.get_value('Employee',{'employee_number':emp},['employee_name'])
    emp_dept = frappe.db.get_value('Employee',{'employee_number':emp},['department'])

    data = "<table class='table table-bordered=1'>"
    data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px'><b><center>EMP ID</center></b></td><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px'colspan=1><b><center>%s</center></b></td><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px'><b><center>DEPT</center></b></td><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px' colspan=1><b><center>%s</center></b></td><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px'colspan='1'><b><center>EMP NAME</center></b></td><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px;' colspan=1><b><center>%s</center></b></td></tr>"%(emp,emp_dept,emp_name)
    data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 2px solid black;background-color:#F14105;padding:1px'><b><center>Date</center></b></td><td style = 'border: 2px solid black;background-color:#F14105;padding:1px'colspan=1><b><center>In Time</center></b></td><td style = 'border: 2px solid black;background-color:#F14105;padding:1px'colspan=1><b><center>Out Time</center></b></td><td style = 'border: 2px solid black;background-color:#F14105;padding:1px'colspan='1'><b><center>Status</center></b></td><td style = 'border: 2px solid black;background-color:#F14105;padding:1px'colspan=4><b><center>Applications</center></b></td></tr>"
    for date in dates:
        dt = format_date(date)
        in_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},['in_time']) or ''
        if in_time:
            att_in_time = get_time(in_time)
        else:
            att_in_time = '-'    
        out_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},'out_time') or ''
        if out_time:
            att_out_time = get_time(out_time)
        else:
            att_out_time = '-'    
        status = get_status(emp,date)
        if status != 'P':
            data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' nowrap>%s</td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px'>%s</td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' nowrap><centre>%s</centre></td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px'><centre>%s</centre></td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' colspan=4><a href='http://103.103.9.11/app/miss-punch-application/new-miss-punch-application-1'><button style='background-color: #4CAF50; color: white; font-size: 4px; padding: 1px 2px';>MP</button></a>&nbsp<a href='http://103.103.9.11/app/permission-request/new-permission-request-1'><button style='background-color: #4CAF50; color: white; font-size: 5px; padding: 1px 2px;'>PR</button></a>&nbsp<a href='http://103.103.9.11/app/leave-application/new-leave-application-1'><button style='background-color: #4CAF50; color: white;font-size: 5px; padding: 1px 2px;'>L</button></a>&nbsp<a href='http://103.103.9.11/app/on-duty-application/new-on-duty-application-1'><button style='background-color: #4CAF50; color: white; font-size: 5px; padding: 1px 2px;'>OD</button></a></td></tr>"%(dt,att_in_time,att_out_time,status)
        else: 
            data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' nowrap>%s</td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px'>%s</td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' nowrap><centre>%s</centre></td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px'><centre>%s</centre></td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' colspan=4></td></tr>"%(dt,att_in_time,att_out_time,status)   
    return data  

@frappe.whitelist()
def get_data_system(emp,from_date,to_date):

    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]

    emp_details = frappe.db.get_value('Employee',emp,['employee_name','department'])

    data = "<table class='table table-bordered=1'>"
    data += "<tr><td style = 'border: 1px solid black;background-color:#AEB6BF '><b>EMP ID</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF ;'colspan=2><b>%s</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF ;'><b>EMP Name</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF ;' colspan=2><b>%s</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF ;'><b>Dept</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF ;' colspan= 3><b>%s</b></td></tr>"%(emp,emp_details[0],emp_details[1])
    data += "<tr><td style = 'border: 1px solid black;background-color:#F5B7B1 'colspan=6><b><center>Attendance</center></b></td><td style = 'border: 1px solid black;background-color:#F5B7B1 'colspan=4><b><center>Total Hours</center></b></td><tr>"
    data += "<tr><td style = 'border: 1px solid black;background-color:#AEB6BF'><b>Date</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;width:5%'><b>Day</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;'><b>Shift</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;'><b>In Time</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;'><b>Out Time</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;'><b>Status</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;width:5%' colspan=1><b><center>TWH</center></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;width: 5%;'><b><center>OT Hours</center></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;'colspan=1><b><center>Late</center></b></td></tr>"

    for date in dates:
        dt = datetime.strptime(date,'%Y-%m-%d')
        d = dt.strftime('%d-%b')
        day = datetime.date(dt).strftime('%a')
        in_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},'in_time') or ''
        out_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},'out_time') or ''
        shift = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':date},'shift') or ''
        status_format = get_status(emp,date) 
        twh = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['total_wh']) or ''
        ot_hrs = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['ot_hrs'])or ''
        late_hrs = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['late_deduct']) or ''
        if status_format == 'P':
            data += "<tr><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'><centre></centre></td></tr>"%(d,day,shift or '',(format_datetime(in_time)) or '',(format_datetime(out_time)) or '',status_format,twh,ot_hrs,late_hrs)
        else:
            data += "<tr><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'><centre><button style='background-color: #4CAF50; color: white; font-size: 15px;'>MP</button>&nbsp&nbsp<button style='background-color: #4CAF50; color: white; font-size: 15px;'>PM</button>&nbsp&nbsp<button style='background-color: #4CAF50; color: white; font-size: 15px;'>L</button>&nbsp&nbsp<button style='background-color: #4CAF50; color: white; font-size: 15px;'>OD</button></centre></td></tr>"%(d,day,shift or '',(format_datetime(in_time)) or '',(format_datetime(out_time)) or '',status_format,twh,ot_hrs,late_hrs)
    data += "</table>"
    return data
        
def check_holiday(date):
    holiday_list = frappe.db.get_value('Company','Infac India Private Limited','default_holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"

def get_status(emp,date):
    status = ''
    if frappe.db.exists('Attendance',{'employee':emp,'attendance_date':date,'docstatus':['!=','2']}):
        att = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':date,'docstatus':['!=','2']},['status','leave_type','on_duty_marked','permission_request','miss_punch_marked']) or ''
        if att:
            if att[0] == 'Present':
                hh = check_holiday(date)
                if att[2]:
                    if hh:
                        if hh == 'WW':
                            status = "WW"
                        elif hh == 'HH':
                            status = "HH"  
                    else:
                        status = "OD"
                elif att[3]:  
                    hh = check_holiday(date)
                    if hh:
                        if hh == 'WW':
                            status = "WW"
                        else:
                            hh == 'HH' 
                    else:
                        status = "P/P"
                elif att[4]: 
                    hh = check_holiday(date)
                    if hh:
                        if hh == 'WW':
                            status = "WW"
                        else:
                            hh == 'HH' 
                    else:
                        status = "P"
                else:
                    if hh:
                        if hh == 'WW':
                            status = "WW"
                        elif hh == 'HH':
                            status = "HH"  
                    else:
                        status = "P"
            elif att[0] == "Absent":
                hh = check_holiday(date)
                if hh:
                    if hh == 'WW':
                       status = "WW"
                    elif hh == 'HH':
                        status = "HH"  
                else:
                    status = "A"
            elif att[0] == "Half Day":
                hh = check_holiday(date)
                if hh:
                    if hh == 'WW':
                       status = "WW"
                    elif hh == 'HH':
                        status = "HH" 
                elif att[2]:
                    status == "P/OD"
                else:
                    if att[1] == 'Casual Leave':
                        status = "P/CL"
                    elif att[1] == "Sick Leave":
                        status = "P/SL"
                    elif att[1] == "Earned Leave":
                        status = "P/EL"
                    elif att[1] == "Leave Without Pay":
                        status = "P/LOP"  
                    elif att[1] == "":
                        status = "P/A" 
            elif att[0] == "On Leave":
                hh = check_holiday(date)
                if hh:
                    if hh == 'WW':
                       status = "WW"
                    elif hh == 'HH':
                       status = 'HH'
                else:
                    if att[1] == 'Casual Leave':
                        status = "CL"
                    elif att[1] == "Sick Leave":
                        status = "SL"
                    elif att[1] == "Earned Leave":
                        status = "EL"
                    elif att[1] == "Leave Without Pay":
                        status = "LOP"    
    else:
        holiday_list = frappe.db.get_value('Company','Infac India Private Limited','default_holiday_list')
        holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
        left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
        if holiday:
            if holiday[0].weekly_off == 1:
                return "WW"
            else:
                return "HH"                
    return status

