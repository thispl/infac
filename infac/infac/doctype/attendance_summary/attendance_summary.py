# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr, add_days, date_diff,format_datetime
from datetime import date, timedelta, datetime, time

class AttendanceSummary(Document):
    pass

@frappe.whitelist()
def get_data_mobile(emp,from_date,to_date):
    data = {}
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]

    emp_name = frappe.db.get_value('Employee',{'employee_number':emp},['employee_name'])
    emp_dept = frappe.db.get_value('Employee',{'employee_number':emp},['department'])
    for date in dates:
        att_list = frappe.db.sql("""select status,leave_type,attendance_date,in_time,out_time,shift,total_wh,ot_hrs,late_deduct,on_duty_marked,permission_request,miss_punch_marked from `tabAttendance` where docstatus = 0 and employee = '%s' and attendance_date between '%s' and '%s'"""%(emp,from_date,to_date),as_dict = 1)
        data.update({
            'emp':emp,
            'emp_name':emp_name,
            'emp_dept':emp_dept,
            'att_list':att_list
        })          
    return data  

@frappe.whitelist()
def get_data_system(emp,from_date,to_date):

    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]

    emp_details = frappe.db.get_value('Employee',emp,['employee_name','department'])

    data = "<table class='table table-bordered=1'>"
    data += "<tr><td style = 'border: 1px solid black;background-color:#a4a8a8'><b>ID</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;'colspan=2><b>%s</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;'><b>Name</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;' colspan=2><b>%s</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;'><b>Dept</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;' colspan= 2><b>%s</b></td></tr>"%(emp,emp_details[0],emp_details[1])
    data += "<tr><td style = 'border: 1px solid black;'colspan=6><b><center>Attendance</center></b></td><td style = 'border: 1px solid black;'colspan=3><b><center>Total Hours</center></b></td><tr>"
    data += "<tr><td style = 'border: 1px solid black;background-color:#a4a8a8'><b>Date</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;'><b>Day</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;'><b>Shift</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;'><b>In Time</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;'><b>Out Time</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;'><b>Status</b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;' colspan=1><b><center>TWH</center></b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;'  colspan=1><b><center>OT Hours</center></b></td><td style = 'border: 1px solid black;background-color:#a4a8a8;'  colspan=1><b><center>Late</center></b></td></tr>"

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

        data += "<tr><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td></tr>"%(d,day,shift or '',(format_datetime(in_time)) or '',(format_datetime(out_time)) or '',status_format,twh,ot_hrs,late_hrs)
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

