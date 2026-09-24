# Copyright (c) 2025, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
from frappe.utils import today,flt,add_days,date_diff,getdate,cint,formatdate
from frappe import _
from frappe.utils import formatdate

class OvertimeRequest(Document):
    def after_insert(self):
        user_roles = frappe.get_roles(frappe.session.user)
        hr = "HR User" in user_roles
        # admin = "Administrator" in user_roles
        if (not hr):
            allowed_days1 = frappe.db.get_value("HR Time Settings", None, "overtime_validation_dates")
            allowed_days = int(allowed_days1 or 0)
            current_date = today()
            if isinstance(current_date, str):
                current_date = datetime.strptime(current_date, "%Y-%m-%d").date()

            def is_working_day(check_date):
                return not check_holiday(check_date, self.employee)

            days_count = 0
            earliest_allowed = current_date
            while days_count < allowed_days:
                earliest_allowed = add_days(earliest_allowed, -1)
                if is_working_day(earliest_allowed):
                    days_count += 1

            if not self.ot_date:
                return

            if isinstance(self.ot_date, str):
                miss_date = datetime.strptime(self.ot_date, "%Y-%m-%d").date()
            else:
                miss_date = self.ot_date

            if miss_date < earliest_allowed:
                frappe.throw(
                    _("Overtime applications are allowed only for up to the previous {0} working days.")
                    .format(allowed_days)
                )

    def validate(self):
        if frappe.db.exists('Overtime Request',{'name':['!=',self.name],'employee':self.employee,"ot_date": self.ot_date,'docstatus':['!=',2],'workflow_state':['!=','Rejected']}):
            formatted_date = formatdate(self.ot_date, "dd-mm-yyyy")
            frappe.throw(f'Over Time Request for employee {self.employee} has already been recorded for the date {formatted_date}.')
        if float(self.ot_hours) == 0:
            frappe.throw(f"Employee <b>{self.employee}</b> must have Overtime hours greater than 0 to apply for OT.")
        

@frappe.whitelist()  
def check_holiday(date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"
        
@frappe.whitelist()  
def check_attendance(date,emp):
    if frappe.db.exists('Attendance', {"employee": emp, 'attendance_date': date, 'docstatus': ['!=', 2]}):
        att = frappe.db.get_value('Attendance', 
            {"employee": emp, 'attendance_date': date, 'docstatus': ['!=', 2]}, 
            ['in_time', 'out_time', 'ot_hrs'], 
            as_dict=True)
        return att['in_time'], att['out_time'], att['ot_hrs']
    else:
        return 'NO'