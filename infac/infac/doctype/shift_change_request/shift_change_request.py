# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe.model.document import Document
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)

class ShiftChangeRequest(Document):
    pass
    
@frappe.whitelist()
def shift_change(emp,start_date,end_date,name,shift):
    check_shift = frappe.db.exists('Shift Assignment',{'name':name,})
    if check_shift:
        frappe.db.set_value('Shift Assignment',check_shift,'shift_type',shift)
    else:
        doc = frappe.new_doc('Shift Assignment')
        doc.employee = emp
        doc.shift_type = shift
        doc.start_date = start_date
        doc.end_date = end_date
        doc.save(ignore_permissions=True)
        doc.submit()
        frappe.db.commit()    
    return "shift_changed"    

@frappe.whitelist()   
def remove_checkins(att_date,shift):
    data = []
    if shift == 'C':
        next_date = add_days(att_date,1)
        emp_checkin = frappe.db.sql(""" update  `tabEmployee Checkin` set skip_auto_attendance = 0  where date(time) between '%s' and '%s' and employee = '%s' """%(att_date,next_date,emp))
        # data.append(emp_checkin)
    return data 
        # c_att_delete = frappe.db.sql("""  delete from `tabAttendance` where attendance_date = '%s' and employee = '%s """%(att_date,emp))

    # else:
    #     emp_checkins = frappe.db.sql(""" update  `tabEmployee Checkin` set skip_auto_attendance = 0  and attendance = '' where date(time)  = '%s' and employee = '%s' """%(att_date,emp))
    #     att_delete = frappe.db.sql("""  delete from `tabAttendance` where attendance_date = '%s' and employee = '%s """%(att_date,emp))  
   