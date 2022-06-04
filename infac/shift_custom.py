from datetime import datetime
import frappe
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from frappe.utils.data import today

@frappe.whitelist()
def wrong_shift_mark_as_absent():
    from_date = today()
    yesterday = add_days(from_date,-1)
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',('2022-05-23','2022-05-24'))},['name','shift','employee','attendance_date','in_time'])
    for att in attendance:
        if att.shift:
            shift = frappe.db.get_value('Shift Assignment',{"start_date":att.attendance_date,'employee':att.employee},['shift_type'])
            if shift != att.shift:
                frappe.db.set_value('Attendance',att.name,'status','Absent')
                # frappe.db.set_value('Attendance',{'name':att.name,'in_time':att.in_time},'hidden',hidden)
                print('yes')
                
    