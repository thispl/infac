# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from unicodedata import name
import frappe
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
import frappe,os,base64
import requests
import datetime
import json,calendar
from datetime import datetime,timedelta,date,time
import datetime as dt
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from frappe.desk.notifications import delete_notification_count_for
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today
from frappe import _, set_value


class OnDutyApplication(Document):

    def after_insert(self):
        user_roles = frappe.get_roles(frappe.session.user)
        hr = "HR User" in user_roles
        # admin = "Administrator" in user_roles
        if (not hr):
            allowed_days1 = frappe.db.get_value("HR Time Settings", None, "on_duty_validation_dates")
            allowed_days = int(allowed_days1 or 0)
            current_date = today()
            if isinstance(current_date, str):
                current_date = datetime.strptime(current_date, "%Y-%m-%d").date()

            def is_working_day(check_date):
                return not check_holiday(check_date,check_date, self.employee)

            days_count = 0
            earliest_allowed = current_date
            while days_count < allowed_days:
                earliest_allowed = add_days(earliest_allowed, -1)
                if is_working_day(earliest_allowed):
                    days_count += 1

            if not self.od_date:
                return

            if isinstance(self.od_date, str):
                miss_date = datetime.strptime(self.od_date, "%Y-%m-%d").date()
            else:
                miss_date = self.od_date

            if miss_date < earliest_allowed:
                frappe.throw(
                    _("OD applications are allowed only for up to the previous {0} working days.")
                    .format(allowed_days)
                )

    def on_submit(self):
        att = frappe.db.exists('Attendance',{'attendance_date':self.od_date,'employee':self.employee})
        if att:
            frappe.db.set_value('Attendance',att,'status','Present')
            frappe.db.set_value('Attendance',att,'on_duty_marked',self.name)
            # att_mark = frappe.db.get_value('Attendance',{'employee':self.employee,'attendance_date':self.od_date,'docstatus':1},['status'])
            # frappe.errprint(att_mark)
            # if att_mark:
            # 	frappe.db.set_value('Attendnace',att,'on_duty_marked',self.name)
        # elif att:
        # 	frappe.db.set_value('Attendance',att,'status','Present')
        # 	frappe.db.set_value('Attendance',att,'on_duty_marked',self.name)
        else:
            attendance = frappe.new_doc('Attendance')
            attendance.employee = self.employee	
            attendance.attendance_date = self.od_date
            attendance.status = "Present"
            attendance.on_duty_marked = self.name
            attendance.total_wh = '00:00'
            attendance.extra_hours = '00:00'
            attendance.late_hours = '00:00'
            attendance.save(ignore_permissions = True)
            frappe.db.commit()

    def on_cancel(self):
        if self.docstatus == 2:
            att = frappe.db.exists('Attendance',{'attendance_date':self.od_date,'employee':self.employee,'on_duty_marked':self.name})
            if att:
                frappe.db.set_value('Attendance',att,'on_duty_marked','')

    def validate(self):
        # If workflow_state didn't change, do nothing
        if not self.has_value_changed("workflow_state"):
            return

        user = frappe.session.user
        time = now_datetime()
        if self.has_value_changed("workflow_state") and self.workflow_state == "Superior Pending":
            self.level_1_timing=now_datetime()
            self.level_1_approved_by=frappe.session.user
        if self.has_value_changed("workflow_state") and self.workflow_state == "Approved":
            self.level_2_timing=now_datetime()
            self.level_2_approved_by=frappe.session.user
        # if self.has_value_changed("workflow_state") and self.workflow_state == "Approved":
        #     self.approved_timing=now_datetime()
        #     self.approved=frappe.session.user
        if self.has_value_changed("workflow_state") and self.workflow_state == "Rejected":
            self.rejected_timing=now_datetime()
            self.rejected=frappe.session.user
     
    def before_insert(self):
        current_user = frappe.session.user
        current_time = now_datetime()
        self.created_by = current_user  
        self.created_on= current_time 
            
    @frappe.whitelist()
    def show_html(self):
        html = "<h2><center>ON DUTY APPLICATION</center></h2><table class='table table-bordered'><tr><th style=font-size:16px;>From Date</th><th style=font-size:16px;>To Date</th></tr><tr><td><h3>%s</h3></td><td><h3>%s</h3></td></tr><tr><th style=font-size:16px;>From Time</th><th style=font-size:16px;>To Time</th></tr><tr><td><h3>%s</h3></td><td><h3>%s</h3></td></tr></table>"%(frappe.utils.format_date(self.od_date),frappe.utils.format_date(self.od_date),frappe.utils.format_time(self.in_time), frappe.utils.format_time(self.out_time))
        return html

        
@frappe.whitelist()
def get_time_difference(od_date,in_time,out_time):
    frappe.errprint('TEST CHECK')
    od_date = datetime.strptime(od_date,'%Y-%m-%d')
    in_time = datetime.strptime(in_time,'%H:%M:%S').time()
    out_time = datetime.strptime(out_time,'%H:%M:%S').time()
    in_time = datetime.combine(od_date, in_time)
    out_time = datetime.combine(od_date, out_time)
    hours = out_time - in_time
    # frappe.errprint(total_hours)
    ftr = [3600,60,1]
    hr = sum([a*b for a,b in zip(ftr, map(int,str(hours).split(':')))])
    od_hr = round(hr/3600,1)
    return hours, od_hr
            
            
            
def check_holiday(from_date,to_date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date between '%s' and '%s' """%(holiday_list,from_date,to_date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"
            
        