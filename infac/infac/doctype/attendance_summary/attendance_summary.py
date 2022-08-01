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

    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    
    emp_details = frappe.db.get_value('Employee',emp,['employee_name','department'])
    data = "<table class='table table-bordered=1'>"
    data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 2px solid black;background-color:#ffedcc;padding:1px'><b><center>ID</center></b></td><td style = 'border: 2px solid black;background-color:#ffedcc;padding:1px'colspan=2><b><center>%s</center></b></td><td style = 'border: 2px solid black;background-color:#ffedcc;padding:1px'><b><center>Name</center></b></td><td style = 'border: 2px solid black;background-color:#ffedcc;padding:1px' colspan=2><b><center>%s</center></b></td><td style = 'border: 2px solid black;background-color:#ffedcc;padding:1px'><b><center>Dept</center></b></td><td style = 'border: 2px solid black;background-color:#ffedcc;padding:1px' colspan=2><b><center>%s</center></b></td></tr>"%(emp,emp_details[0],emp_details[1])
    data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 2px solid black;padding:1px;background-color:#ffedcc'colspan=6><b><center>Attendance</center></b></td><td style ='border: 2px solid black;padding:1px;background-color:#ffedcc' colspan=3><b><center>Total Hours</center></b></td><tr>"
    data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 2px solid black;border-right: 1px solid black;background-color:#ffedcc;padding:1px'><b><center>Date</center></b></td><td style = 'border: 1px solid black;border-bottom: 2px solid black;background-color:#ffedcc;padding:1px'><b><center>Day</center></b></td><td style = 'border: 1px solid black;border-bottom: 2px solid black;background-color:#ffedcc;padding:1px'><b><center>Shift</center></b></td><td style = 'border: 1px solid black;border-bottom: 2px solid black;background-color:#ffedcc;padding:1px'><b><center>In Time</center></b></td><td style = 'border: 1px solid black;border-bottom: 2px solid black;background-color:#ffedcc;padding:1px'><b><center>Out Time</center></b></td><td style = 'border: 2px solid black;border-left: 1px;background-color:#ffedcc;padding:1px'><b><center>Status</center></b></td><td style = 'border: 1px solid black;border-bottom: 2px solid black;background-color:#ffedcc;padding:1px'><b><center>TWH</center></b></td><td style = 'border: 1px solid black;border-bottom: 2px solid black;background-color:#ffedcc;padding:1px'><b><center>OT Hours</center></b></td><td style = 'border: 2px solid black;border-left: 1px;background-color:#ffedcc;padding:1px'><b><center>Late</center</b></td></tr>"
    
    for date in dates:
        dt = datetime.strptime(date,'%Y-%m-%d')
        d = dt.strftime('%d-%b')
        day = datetime.date(dt).strftime('%a')
        holiday  = check_holiday(date)
        in_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},'in_time') or ''
        out_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},'out_time') or ''
        status_format = get_status(emp,date) 
        twh = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['total_wh']) or ''
        ot_hrs = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['ot_hrs'])or ''
        late_hrs = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['late_deduct']) or ''

        data += "<tr><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td><td style = 'border: 1px solid black;'>%s</td></tr>"%(d,day,holiday or 'W',(format_datetime(in_time)) or '',(format_datetime(out_time)) or '',status_format,twh,ot_hrs,late_hrs)
    data += "</table>"
    return data

@frappe.whitelist()
def get_data_system(emp,from_date,to_date):

    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]

    emp_details = frappe.db.get_value('Employee',emp,['employee_name','department'])

    data = "<table class='table table-bordered=1'>"
    data += "<tr><td style = 'border: 1px solid black;background-color:#ffedcc'><b>ID</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;'colspan=2><b>%s</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;'><b>Name</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;' colspan=2><b>%s</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;'><b>Dept</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;' colspan= 2><b>%s</b></td></tr>"%(emp,emp_details[0],emp_details[1])
    data += "<tr><td style = 'border: 1px solid black;'colspan=6><b><center>Attendance</center></b></td><td style = 'border: 1px solid black;'colspan=3><b><center>Total Hours</center></b></td><tr>"
    data += "<tr><td style = 'border: 1px solid black;background-color:#ffedcc'><b>Date</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;'><b>Day</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;'><b>Shift</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;'><b>In Time</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;'><b>Out Time</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;'><b>Status</b></td><td style = 'border: 1px solid black;background-color:#ffedcc;' colspan=1><b><center>TWH</center></b></td><td style = 'border: 1px solid black;background-color:#ffedcc;'  colspan=1><b><center>OT Hours</center></b></td><td style = 'border: 1px solid black;background-color:#ffedcc;'  colspan=1><b><center>Late</center></b></td></tr>"

    for date in dates:
        dt = datetime.strptime(date,'%Y-%m-%d')
        d = dt.strftime('%d-%b')
        day = datetime.date(dt).strftime('%a')
        # holiday  = check_holiday(date)
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
                if hh:
                    if hh == 'WW':
                       status = "WW"
                    else:
                        hh == 'HH'
                        status = "HH"  
                else:
                    status = "P"
            elif att[0] == "Absent":
                hh = check_holiday(date)
                if hh:
                    if hh == 'WW':
                       status = "WW"
                    else:
                        hh == 'HH' 
                else:
                    status = "A"
            elif att[0] == "Half Day":
                hh = check_holiday(date)
                if hh:
                    if hh == 'WW':
                       status = "WW"
                    else:
                        hh == 'HH' 
                else:
                    if att[1]:
                        status = "P/L"
                    else:
                        status = "P/A" 
            elif att[0] == "On Leave":
                hh = check_holiday(date)
                if hh:
                    if hh == 'WW':
                       status = "WW"
                    else:
                        hh == 'HH' 
                else:
                    if att[1] == 'Casual Leave':
                        status = "CL"
                    elif att[1] == "Sick Leave":
                        status = "SL"
                    elif att[1] == "Earned Leave":
                        status = "EL"
                    elif att[1] == "Leave Without Pay":
                        status = "LOP"     
            elif att[2]:
                hh = check_holiday(date)
                if hh:
                    if hh == 'WW':
                       status = "WW"
                    else:
                        hh == 'HH' 
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

    return status

# status_map = {
#    'Permission Request' :'PR',
#     'On Duty':'OD',
#     'Half Day':'HD',
#     "Absent": "A",
# 	"Half Day": "HD",
# 	"Holiday": "HH",
# 	"Weekly Off": "WW",
#     "Present": "P",
#     "None" : "",
#     "Leave Without Pay": "LOP",
#     "Casual Leave": "CL",
#     "Earned Leave": "EL",
#     "Sick Leave": "SL",
#     "Emergency -1": 'EML-1',
#     "Emergency -2": 'EML-2',
#     "Paternal Leave": 'PL',
#     "Marriage Leave":'ML',
#     "Paternity Leave":'PTL',
#     "Education Leave":'EL',
#     "Maternity Leave":'MTL',
#     "Covid -19": "COV-19",
#     "Privilege Leave": "PVL",
#     "Compensatory Off": "C-OFF",
#     "BEREAVEMENT LEAVE":'BL'
#     }

