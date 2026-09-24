# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr, add_days, date_diff,format_datetime,format_date,getdate, format_time
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today,time_diff_in_hours,get_datetime,get_time

from datetime import date, timedelta, datetime, time

class AttendanceSummary(Document):
    pass

# @frappe.whitelist()
# def get_data_mobile(emp,start_date,end_date):
    
#     no_of_days = date_diff(add_days(end_date, 1), start_date)
#     dates = [add_days(start_date, i) for i in range(0, no_of_days)]

#     emp_name = frappe.db.get_value('Employee',{'employee_number':emp},['employee_name'])
#     emp_dept = frappe.db.get_value('Employee',{'employee_number':emp},['department'])

#     data = "<table class='table table-bordered' style='border-collapse: collapse;>"
#     # data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px; text-align: center; '><b><center>EMP ID</center></b></td><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px ; text-align: center;'colspan=1><b><center>%s</center></b></td><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px; text-align: center;'><b><center>DEPT</center></b></td><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px; text-align: center;' colspan=1><b><center>%s</center></b></td><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px; text-align: center;'colspan='1'><b><center>EMP NAME</center></b></td><td style = 'border: 2px solid black;background-color:#AEB6BF;padding:1px;; text-align: center;' colspan=1><b><center>%s</center></b></td></tr>"%(emp,emp_dept,emp_name)
#     data += """
#     <tr style='font-size:5px; padding:1px'>
#         <td style='border: 2px solid black; background-color:#AEB6BF; padding:1px; text-align: center;width: 70px;'><b>EMP ID</b></td>
#         <td style='border: 2px solid black; background-color:#AEB6BF; padding:1px; text-align: center;width: 150px;' colspan='1'><b>%s</b></td>
        
#         <td style='border: 2px solid black; background-color:#AEB6BF; padding:1px; text-align: center;width: 80px;'><b>DEPT</b></td>
#         <td style='border: 2px solid black; background-color:#AEB6BF; padding:1px; text-align: center;' colspan='1'><b>%s</b></td>
        
#         <td style='border: 2px solid black; background-color:#AEB6BF; padding:1px; text-align: center;width: 100px;' colspan='1'><b>EMP NAME</b></td>
#         <td style='border: 2px solid black; background-color:#AEB6BF; padding:1px; text-align: center;width: 150px;' colspan='1'><b>%s</b></td>
#     </tr>
#     """ % (emp, emp_dept, emp_name)

#     data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 2px solid black;background-color:#F14105;padding:1px; text-align: center;'><b><center>Date</center></b></td><td style = 'border: 2px solid black;background-color:#F14105;padding:1px; text-align: center;'colspan=1><b><center>In Time</center></b></td><td style = 'border: 2px solid black;background-color:#F14105;padding:1px; text-align: center;'colspan=1><b><center>Out Time</center></b></td><td style = 'border: 2px solid black;background-color:#F14105;padding:1px; text-align: center;'colspan='1'><b><center>Status</center></b></td><td style = 'border: 2px solid black;background-color:#F14105;padding:1px; text-align: center;'colspan=4><b><center>Applications</center></b></td></tr>"
#     for date in dates:
#         dt = format_date(date)
#         in_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},['in_time']) or ''
#         if in_time:
#             att_in_time = get_time(in_time)
#         else:
#             att_in_time = '-'    
#         out_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},'out_time') or ''
#         if out_time:
#             att_out_time = get_time(out_time)
#         else:
#             att_out_time = '-'    
#         status = get_status(emp,date)
#         if status != 'P':
#             data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' nowrap>%s</td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px'>%s</td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' nowrap><centre>%s</centre></td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px'><centre>%s</centre></td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' colspan=4></td></tr>"%(dt,att_in_time,att_out_time,status)
#         else: 
#             data += "<tr style='font-size:5px;padding:1px'><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' nowrap>%s</td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px'>%s</td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' nowrap><centre>%s</centre></td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px'><centre>%s</centre></td><td style = 'border: 1px solid black;border-left: 2px solid black;padding:1px' colspan=4></td></tr>"%(dt,att_in_time,att_out_time,status)   
#     return data  

@frappe.whitelist()
def get_data_mobile(emp, start_date, end_date):
    no_of_days = date_diff(add_days(end_date, 1), start_date)
    dates = [add_days(start_date, i) for i in range(0, no_of_days)]

    emp_name = frappe.db.get_value('Employee', {'employee_number': emp}, 'employee_name')
    emp_dept = frappe.db.get_value('Employee', {'employee_number': emp}, 'department')

    data = "<div style='width:100%; overflow-x:auto;'><table class='table table-bordered' style='border-collapse: collapse;table-layout: fixed; width: 100%;'>"
    
    # Header row for employee details
    data += f"""
    <tr style='font-size:5px; padding:1px'>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>EMP ID</b></td>
        <td colspan='2' style='border: 1px solid black; background-color:#AEB6BF; padding:1px;text-align: center;'><b>{emp}</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>EMP Name</b></td>
        <td colspan='2' style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: enter;'><b>{emp_name}</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>Dept</b></td>
        <td colspan='3' style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>{emp_dept}</b></td>
    </tr>
    """

    # Header for attendance
    data += """
    <tr style='font-size:5px;width: 100%;line-height: 1; padding: 0; margin: 0; '>
        <td colspan='10' style='border: 1px solid black; background-color:#F5B7B1; text-align: center;padding:2px 0; line-height:1;'><b>Attendance</b></td>
    </tr>
    <tr style='font-size:5px;width: 100%; '>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>Attendance Date</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>Day</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>Working</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>In Time</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>Out Time</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>Shift</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>Status</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>TWH</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>OT Hrs</b></td>
        <td style='border: 1px solid black; background-color:#AEB6BF; padding:1px; text-align: center;'><b>Late</b></td>
    </tr>
    """

    for date in dates:
        # dt_obj = getdate(date)
        # # d = dt_obj.strftime('%d-%b')
        # d = dt.strftime('%d-%m-%Y')
        # day = dt_obj.strftime('%a')
        # working = check_working(date)

        # in_time = frappe.db.get_value('Attendance', {'employee': emp, "attendance_date": date}, 'in_time') or ''
        # out_time = frappe.db.get_value('Attendance', {'employee': emp, "attendance_date": date}, 'out_time') or ''
        # shift = frappe.db.get_value('Attendance', {'employee': emp, 'attendance_date': date}, 'shift') or ''
        # status_format = get_status(emp, date)
        # twh = frappe.db.get_value('Attendance', {'attendance_date': date, 'employee': emp}, 'total_wh') or ''
        # ot_hrs = frappe.db.get_value('Attendance', {'attendance_date': date, 'employee': emp}, 'ot_hrs') or ''
        # late_hrs = frappe.db.get_value('Attendance', {'attendance_date': date, 'employee': emp}, 'late_hours') or ''

        # if isinstance(late_hrs, timedelta):
        #     total_seconds = int(late_hrs.total_seconds())
        #     hours = total_seconds // 3600
        #     minutes = (total_seconds % 3600) // 60
        #     late_hrs = f"{hours:02}:{minutes:02}"
        #     if late_hrs == "00:00":
        #         late_hrs = ""

        # # Highlight 'P' if less than 8 hours
        # if status_format == 'P':
        #     wh_in_seconds = 0
        #     if twh:
        #         parts = str(twh).split(":")
        #         if len(parts) == 3:
        #             hours, minutes, seconds = map(int, parts)
        #             wh_in_seconds = hours * 3600 + minutes * 60 + seconds

        #     if wh_in_seconds < 8 * 3600:
        #         status_html = "<span style='color:red;'>P</span>"
        #     else:
        #         status_html = "P"
        # else:
        #     status_html = status_format

        dt = datetime.strptime(date,'%Y-%m-%d')
        d = dt.strftime('%d-%b')
        day = datetime.date(dt).strftime('%a')
        working=check_working(date)
        in_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},'in_time') or ''
        
        out_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},'out_time') or ''
        shift = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':date},'shift') or ''
        status_format = get_status(emp,date) 
        twh = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['total_wh']) or ''
        if isinstance(twh, timedelta):
            total_seconds = int(twh.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            twh = f"{hours:02}:{minutes:02}"
            
        # ot_hrs = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['ot_hrs'])or ''
        ot_hrs = frappe.db.get_value('Overtime Request',{'docstatus': 1,'ot_date':date,'employee':emp,},['ot_hours'])or ''

        late_hrs = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['late_hours']) or ''
        if isinstance(late_hrs, timedelta):
            total_seconds = int(late_hrs.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            late_hrs = f"{hours:02}:{minutes:02}"
            if late_hrs == "00:00":
                late_hrs = ""
        if status_format == 'P':
            wh_in_seconds = 0
            if twh:
                time_parts = str(twh).split(":")
                if len(time_parts) == 2:
                    hours, minutes = map(int, time_parts)
                    wh_in_seconds = hours * 3600 + minutes * 60 
            eight_hours_in_seconds = 8 * 3600

            if wh_in_seconds < eight_hours_in_seconds:
                # status_html = "<span style='color:Black;'>P</span>"
                status_html = "P"
                status_td_style = "background-color: #FF7276; color: Black; text-align: center; border: 1px solid black;"
            else:
                # status_html = "P"
                status_html = "P"
                status_td_style = "text-align: center; border: 1px solid black;"

            data += "<tr style='font-size:5px;'>" \
                        "<td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                        "<td style='border: 1px solid black;padding:2px 0; line-height:1; text-align: center;'>%s</td>" \
                        "<td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                        "<td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                        "<td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                        "<td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                        "<td style='border: 1px solid black;text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                        "<td style='text-align: center;padding:2px 0; line-height:1; %s'>%s</td>" \
                        "<td style='border: 1px solid black;text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                        "<td style='border: 1px solid black;text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                        "</tr>" % (d, day, working or "", format_time(in_time) or '', format_time(out_time) or '', shift or '', status_html, status_td_style,twh, ot_hrs, late_hrs)
        elif status_format == 'A':
                status_html = "A"
                status_td_style = "background-color: #FF7276; color: Black; text-align: center; border: 1px solid black;"
                data += "<tr style='font-size:5px;line-height: 1; padding: 0; margin: 0;'>" \
                    "<td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                    "<td style='border: 1px solid black;padding:2px 0; line-height:1; text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                    "<td style='text-align: center; padding:2px 0; line-height:1;%s'>%s</td>" \
                    "<td style='border: 1px solid black;text-align: center;padding:2px 0; line-height:1;'>%s</td>" \
                    "<td style='border: 1px solid black;padding:2px 0; line-height:1;'>%s</td>" \
                    "<td style='border: 1px solid black;padding:2px 0; line-height:1;'>%s</td>" \
                    "</tr>" % (d, day, working or "", format_time(in_time) or '', format_time(out_time) or '', shift or '', status_td_style,status_html, twh, ot_hrs, late_hrs)
        
        else:
            data += "<tr style='font-size:5px;'><td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td><td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'>%s</td><td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'><centre>%s</centre></td><td style='border: 1px solid black;text-align: center;padding:2px 0; line-height:1;'>%s</td><td style='border: 1px solid black;text-align: center;padding:2px 0; line-height:1;'>%s</td><td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'><centre>%s</centre></td><td style='border: 1px solid black; text-align: center;padding:2px 0; line-height:1;'><centre>%s</centre></td><td style='border: 1px solid black;padding:2px 0; line-height:1;'>%s</td><td style='border: 1px solid black;padding:2px 0; line-height:1;'>%s</td><td style='border: 1px solid black;padding:2px 0; line-height:1;'>%s</td></tr>" % (d, day, working or " ", format_time(in_time) or '', format_time(out_time) or '', shift or '', status_format, twh, ot_hrs, late_hrs)


        # data += f"""
        # <tr style='font-size:12px;'>
        #     <td style='border: 1px solid black; text-align: center;'>{d}</td>
        #     <td style='border: 1px solid black; text-align: center;'>{day}</td>
        #     <td style='border: 1px solid black; text-align: center;'>{working or ''}</td>
        #     <td style='border: 1px solid black; text-align: center;'>{format_time(in_time) if in_time else ''}</td>
        #     <td style='border: 1px solid black; text-align: center;'>{format_time(out_time) if out_time else ''}</td>
        #     <td style='border: 1px solid black; text-align: center;'>{shift or ''}</td>
        #     <td style='border: 1px solid black; text-align: center;'>{status_html}</td>
        #     <td style='border: 1px solid black; text-align: center;'>{twh or ''}</td>
        #     <td style='border: 1px solid black; text-align: center;'>{ot_hrs or ''}</td>
        #     <td style='border: 1px solid black; text-align: center;'>{late_hrs or ''}</td>
        # </tr>
        # """

    data += "</table></div>"
    return data


@frappe.whitelist()
def get_data_system(emp,from_date,to_date):
    
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]

    emp_details = frappe.db.get_value('Employee',emp,['employee_name','department'])

    data = "<table class='table table-bordered=1'>"
    data += "<tr ><td style = 'border: 1px solid black;background-color:#AEB6BF; text-align: center; '><b>EMP ID</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF ; text-align: center;'colspan=2><b>%s</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF ; text-align: center;'><b>EMP Name</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF ; text-align: center;' colspan=2><b>%s</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF ; text-align: center;width: 40px; '><b>Dept</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF ; text-align: center;' colspan= 4><b>%s</b></td></tr>"%(emp,emp_details[0],emp_details[1])
    # data += "<tr><td style = 'border: 1px solid black;background-color:#F5B7B1 'colspan=6><b><center>Attendance</center></b></td><td style = 'border: 1px solid black;background-color:#F5B7B1 'colspan=4><b><center>Total Hours</center></b></td><tr>"
    data += "<tr><td style = 'border: 1px solid black;background-color:#F5B7B1 'colspan=11><b><center>Attendance</center></b></td>"
    # data += "<tr><td style = 'border: 1px solid black;background-color:#AEB6BF'><b>Date</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;width:5%'><b>Day</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;'><b>Shift</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;'><b>In Time</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;'><b>Out Time</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;'><b>Status</b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;width:5%' colspan=1><b><center>TWH</center></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;width: 5%;'><b><center>OT Hours</center></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;'colspan=1><b><center>Late</center></b></td></tr>"
    data += "<tr width:100%;><td style = 'border: 1px solid black;background-color:#AEB6BF; text-align: center;padding:1px;width:100px;'><b><centre>Attendance Date</centre></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;width:5%'><b><centre>Day</centre></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF; text-align: center;'><b><centre>Working</centre></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF; text-align: center;'><b><centre>In Time</centre></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF; text-align: center;'><b><centre>Out Time</centre></b><td style = 'border: 1px solid black;background-color:#AEB6BF; text-align: center;'><b><centre>Shift</centre></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF; text-align: center;'><b><centre>Status</centre></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;width:5%' ><b><center>TWH</center></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;width: 5%;'><b><center>OT Hours</center></b></td><td style = 'border: 1px solid black;background-color:#AEB6BF;' ><b><center>Late</center></b></td></td></tr>"

    for date in dates:
        dt = datetime.strptime(date,'%Y-%m-%d')
        d = dt.strftime('%d-%b')
        day = datetime.date(dt).strftime('%a')
        working=check_working(date)
        in_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},'in_time') or ''
        
        out_time = frappe.db.get_value('Attendance' ,{'employee':emp,"attendance_date":date},'out_time') or ''
        shift = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':date},'shift') or ''
        status_format = get_status(emp,date) 
        twh = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['total_wh']) or ''
        if isinstance(twh, timedelta):
            total_seconds = int(twh.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            twh = f"{hours:02}:{minutes:02}"
            
        # ot_hrs = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['ot_hrs'])or ''
        ot_hrs = frappe.db.get_value('Overtime Request',{'docstatus': 1,'ot_date':date,'employee':emp,},['ot_hours'])or ''
        late_hrs = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp},['late_hours']) or ''
        if isinstance(late_hrs, timedelta):
            total_seconds = int(late_hrs.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            late_hrs = f"{hours:02}:{minutes:02}"
            if late_hrs == "00:00":
                late_hrs = ""
        if status_format == 'P':
            wh_in_seconds = 0
            if twh:
                time_parts = str(twh).split(":")
                if len(time_parts) == 2:
                    hours, minutes = map(int, time_parts)
                    wh_in_seconds = hours * 3600 + minutes * 60 
            eight_hours_in_seconds = 8 * 3600

            if wh_in_seconds < eight_hours_in_seconds:
                # status_html = "<span style='color:Black;'>P</span>"
                status_html = "P"
                status_td_style = "background-color: #FF7276; color: Black; text-align: center; border: 1px solid black;"
            else:
                # status_html = "P"
                status_html = "P"
                status_td_style = "text-align: center; border: 1px solid black;"

            # data += "<tr><td style='border: 1px solid black; text-align: center;'>%s</td><td style='border: 1px solid black;'>%s</td><td style='border: 1px solid black; text-align: center;'>%s</td><td style='border: 1px solid black;text-align: center;'>%s</td><td style='border: 1px solid black;text-align: center;'>%s</td><td style='border: 1px solid black; text-align: center;'>%s</td><td style='border: 1px solid black; text-align: center;'>%s</td><td style='border: 1px solid black;'>%s</td><td style='border: 1px solid black;'>%s</td><td style='border: 1px solid black;'>%s</td></tr>" % (
            #     d, day, working or " ", format_time(in_time) or '', format_time(out_time) or '', shift or '', status_html, twh, ot_hrs, late_hrs)
            data += "<tr>" \
                    "<td style='border: 1px solid black; text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black;text-align: center;'>%s</td>" \
                    "<td style='%s'>%s</td>" \
                    "<td style='border: 1px solid black;'>%s</td>" \
                    "<td style='border: 1px solid black;'>%s</td>" \
                    "</tr>" % (d, day, working or "", format_time(in_time) or '', format_time(out_time) or '', shift or '', status_html, status_td_style,twh, ot_hrs, late_hrs)
        # else:
        #     data += "<tr><td style='border: 1px solid black; text-align: center;'>%s</td><td style='border: 1px solid black;'>%s</td><td style='border: 1px solid black; text-align: center;'><centre>%s</centre></td><td style='border: 1px solid black;text-align: center;'>%s</td><td style='border: 1px solid black;text-align: center;'>%s</td><td style='border: 1px solid black; text-align: center;'><centre>%s</centre></td><td style='border: 1px solid black; text-align: center;'><centre>%s</centre></td><td style='border: 1px solid black;'>%s</td><td style='border: 1px solid black;'>%s</td><td style='border: 1px solid black;'>%s</td></tr>" % (d, day, working or " ", format_time(in_time) or '', format_time(out_time) or '', shift or '', status_format, twh, ot_hrs, late_hrs)
     
      
        elif status_format == 'A':
                # status_html = "P"
                status_html = "A"
                status_td_style = "background-color: #FF7276; color: Black; text-align: center; border: 1px solid black;"
                data += "<tr>" \
                    "<td style='border: 1px solid black; text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black; text-align: center;'>%s</td>" \
                    "<td style='%s'>%s</td>" \
                    "<td style='border: 1px solid black;text-align: center;'>%s</td>" \
                    "<td style='border: 1px solid black;'>%s</td>" \
                    "<td style='border: 1px solid black;'>%s</td>" \
                    "</tr>" % (d, day, working or "", format_time(in_time) or '', format_time(out_time) or '', shift or '', status_td_style,status_html, twh, ot_hrs, late_hrs)
        else:
            data += "<tr><td style='border: 1px solid black; text-align: center;'>%s</td><td style='border: 1px solid black;'>%s</td><td style='border: 1px solid black; text-align: center;'><centre>%s</centre></td><td style='border: 1px solid black;text-align: center;'>%s</td><td style='border: 1px solid black;text-align: center;'>%s</td><td style='border: 1px solid black; text-align: center;'><centre>%s</centre></td><td style='border: 1px solid black; text-align: center;'><centre>%s</centre></td><td style='border: 1px solid black;'>%s</td><td style='border: 1px solid black;'>%s</td><td style='border: 1px solid black;'>%s</td></tr>" % (d, day, working or " ", format_time(in_time) or '', format_time(out_time) or '', shift or '', status_format, twh, ot_hrs, late_hrs)
     

    data += "</table>"
    return data
        
def check_holiday(date):
    holiday_list = frappe.db.get_value('Company','Infac India Private Limited','default_holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off, `tabHoliday`.description from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            # return holiday[0].description
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
                            status = "OFF"
                        elif hh == 'HH':
                            status = "HH"  
                    else:
                        status = "OD"
                elif att[3]:  
                    hh = check_holiday(date)
                    if hh:
                        if hh == 'WW':
                            status = "OFF"
                        else:
                            hh == 'HH' 
                    else:
                        status = "P/P"
                elif att[4]: 
                    hh = check_holiday(date)
                    if hh:
                        if hh == 'WW':
                            status = "OFF"
                        else:
                            hh == 'HH' 
                    else:
                        status = "P"
                else:
                    if hh:
                        if hh == 'WW':
                            status = "OFF"
                        elif hh == 'HH':
                            status = "HH"  
                    else:
                        status = "P"
            elif att[0] == "Absent":
                hh = check_holiday(date)
                if hh:
                    if hh == 'WW':
                       status = "OFF"
                    elif hh == 'HH':
                        status = "HH"  
                else:
                    status = "A"
            elif att[0] == "Half Day":
                hh = check_holiday(date)
                if hh:
                    if hh == 'WW':
                       status = "OFF"
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
                        status = "HD/LOP"    
                    elif att[1] == "Compensatory Off":
                        status = "P/C-Off"  
                    elif att[1] == "":
                        status = "HD/A"
                             
                    else :
                        status = "HD"    
            elif att[0] == "On Leave":
                hh = check_holiday(date)
                if hh:
                    if hh == 'WW':
                       status = "OFF"
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
                    elif att[1] == "Compensatory Off":
                        status = "C-Off"    
    else:
        holiday_list = frappe.db.get_value('Company','Infac India Private Limited','default_holiday_list')
        holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off , `tabHoliday`.description from `tabHoliday List` 
        left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
        if holiday:
            if holiday[0].weekly_off == 1:
                return "OFF"
            else:
                return "HH" 
                # return holiday[0].description               
    return status

def check_working(date):
    holiday_list = frappe.db.get_value('Company','Infac India Private Limited','default_holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"
    else:
        return "W"