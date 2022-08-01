import frappe
from datetime import datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime) 
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form



@frappe.whitelist()
def miss_punch_mail_alert():
    data = ''
    data += 'Dear Sir,<br><br>Kindly Find the List of Employees for Face Punch was Missed<br><table class="table table-bordered">'
    data += '<table class="table table-bordered" ><tr><th>Employee ID</th><th>Employee Name</th><th>Employee Category</th><th>Department</th><th>Attendance Date</th><th>Shift</th></tr>'
    curreny_day = today()
    yesterday = add_days(today(),-1)
    employee = frappe.db.get_all('Employee',{'status':'Active'},['*'])
    for emp in employee:
        attendance = frappe.db.get_all('Attendance',{'status':'Present','attendance_date':yesterday,'employee':emp.name},['*'])
        for att in attendance:
            if att.in_time and not att.out_time:
                data += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (emp.name,emp.employee_name,emp.employee_category,emp.department,format_date(att.attendance_date),att.shift)
        data+='</table>'
    frappe.sendmail(
        recipients = 'jagadeesan.a@groupteampro.com',
        subject = 'Miss Punch Alert',
        message = data
    )