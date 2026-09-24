# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from re import S
from time import strftime, strptime
import frappe
import math
import pandas as pd
from frappe.utils import now_datetime
from frappe.model.document import Document
import frappe,os,base64
import requests
import datetime
import json,calendar
from datetime import datetime,timedelta,date,time
import datetime as dt
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from frappe.desk.notifications import delete_notification_count_for
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today
from frappe import _


class MissPunchApplication(Document):

    def after_insert(self):
        user_roles = frappe.get_roles(frappe.session.user)
        hr = "HR User" in user_roles
        # admin = "Administrator" in user_roles
        if (not hr):
            allowed_days1 = frappe.db.get_value("HR Time Settings", None, "miss_punch_validation_dates")
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

            if not self.date:
                return

            if isinstance(self.date, str):
                miss_date = datetime.strptime(self.date, "%Y-%m-%d").date()
            else:
                miss_date = self.date

            if miss_date < earliest_allowed:
                frappe.throw(
                    _("Miss Punch applications are allowed only for up to the previous {0} working days.")
                    .format(allowed_days)
                )

    def on_submit(self):
        att = frappe.db.exists('Attendance',{'attendance_date':self.date,'employee':self.employee})
        if att:
            att_doc = frappe.get_doc("Attendance", att)
            self.db_set("previous_in_time", att_doc.in_time)
            self.db_set("previous_out_time", att_doc.out_time)
            # self.db_set("shift", att_doc.shift)

            frappe.db.set_value('Attendance',att,'in_time',self.in_time)
            frappe.db.set_value('Attendance',att,'out_time',self.out_time)
            frappe.db.set_value('Attendance',att,'shift',self.shift)
            frappe.db.set_value('Attendance',att,'working_hours',self.working_hours)
            frappe.db.set_value('Attendance',att,'total_wh',self.twh)
            frappe.db.set_value('Attendance',att,'extra_hours',self.extra_hours)
            frappe.db.set_value('Attendance',att,'ot_hrs',self.ot_hours)
            frappe.db.set_value("Attendance",att,"status","Present")
            frappe.db.set_value('Attendance',att,'miss_punch_marked',self.name)
            # frappe.db.set_value('Attendance',att,'late_hours','00:00')
            # frappe.db.set_value('Attendance',att,'late_hrs','')
            # frappe.db.set_value('Attendance',att,'late_deduct','00:00')
            self.attendance = att
    
    def on_cancel(self):
        if self.docstatus == 2:
            att = frappe.db.exists('Attendance',{'attendance_date':self.date,'employee':self.employee,'miss_punch_marked':self.name})
            frappe.db.set_value('Attendance',att,'miss_punch_marked','')

    #while After Save the document the below process is working
    def validate(self):
        in_time = datetime.strptime(str(self.in_time),'%Y-%m-%d %H:%M:%S')
        out_time = datetime.strptime(str(self.out_time),'%Y-%m-%d %H:%M:%S')

        # Calulating the in_time and out_time 
        total_working_hour = out_time - in_time
        ftr = [3600,60,1]
        hr = sum([a*b for a,b in zip(ftr, map(int,str(total_working_hour).split(':')))])
        wh = round(hr/3600,1)

        #assign the round off total_working_hours in working_hours
        self.working_hours = wh

        #Assign the total_working_hours in twh
        self.twh = total_working_hour

        # Based on Total Working Hours to get a OT Hours
        shift_end_time = frappe.db.get_value('Shift Type',self.shift,'end_time')
        shift_end_time = pd.to_datetime(str(shift_end_time)).time() 
        string_datetime = datetime.strptime(str(self.out_time),'%Y-%m-%d %H:%M:%S')
        get_date = string_datetime.date()
        shift_end_datetime = datetime.combine(get_date,shift_end_time)
        total_shift_hours = frappe.db.get_value('Shift Type',self.shift,'total_hours')
        if shift_end_time:
            extra_hrs =pd.to_datetime('00:00:00').time()  
            ot_hr = 0 
            if string_datetime > shift_end_datetime:
                if self.twh > total_shift_hours:
                    extra_hrs = string_datetime - shift_end_datetime
                    convert_hour_min = datetime.strptime(str(extra_hrs),'%H:%M:%S').strftime('%H:%M')
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(convert_hour_min).split(':')))])
                    extras = round(hr/3600,1)
                    if extras > 1:
                        ot_hr = math.floor(extras * 2) / 2
                        self.ot_hours = ot_hr
                        self.extra_hours = convert_hour_min
        
        if frappe.db.exists('Attendance',{'employee':self.employee,'attendance_date':self.date}):
            in_time = frappe.db.get_value('Attendance',{'employee':self.employee,'attendance_date':self.date},['in_time'])
            out_time = frappe.db.get_value('Attendance',{'employee':self.employee,'attendance_date':self.date},['out_time'])
            if in_time and out_time:
                frappe.throw(_("Checkin and Checkout are already recorded for this date"))
            if not in_time and not out_time:
                frappe.throw(_("Checkin and Checkout are missing for this date."))

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
    #This is the While cancel the document to remove the Miss Punch ID in Attendance
    
    def before_insert(self):
        current_user = frappe.session.user
        current_time = now_datetime()
        self.created_by = current_user  
        self.created_on= current_time 
         
         
    def on_cancel(self):
        att = frappe.db.exists('Attendance',{'attendance_date':self.date,'employee':self.employee})
        
        if att:
            frappe.db.set_value('Attendance', att, 'in_time', self.previous_in_time)
            frappe.db.set_value('Attendance', att, 'out_time', self.previous_out_time)
            frappe.db.set_value('Attendance', att, 'shift', self.shift)
            frappe.db.set_value('Attendance', att, 'working_hours', 0)
            frappe.db.set_value('Attendance', att, 'total_wh', "00:00")
            frappe.db.set_value('Attendance', att, 'extra_hours', "00:00")
            frappe.db.set_value('Attendance', att, 'ot_hrs', '0.0')
            frappe.db.set_value('Attendance', att, 'status', "Absent")
            frappe.db.set_value('Attendance', att, 'miss_punch_marked', '')

    @frappe.whitelist()
    def show_html(self):
        html = "<h2><center>MISS PUNCH APPLICATION</center></h2><table class='table table-bordered'><tr><th style=font-size:16px;>From Date</th><th style=font-size:16px;>To Date</th></tr><tr><td><h3>%s</h3></td><td><h3>%s</h3></td></tr><tr><th style=font-size:16px;>From Time</th><th style=font-size:16px;>To Time</th></tr><tr><td><h3>%s</h3></td><td><h3>%s</h3></td></tr></table>"%(frappe.utils.format_date(self.date),frappe.utils.format_date(self.date),frappe.utils.format_time(self.in_time), frappe.utils.format_time(self.out_time))
        return html      

# @frappe.whitelist()
# def get_attendance(emp,att_date):
#     datalist = []
#     data = {}
#     if frappe.db.exists('Attendance',{'employee':emp,'attendance_date':att_date}):
#         if frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['in_time']):
#             in_time = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['in_time'])
#         else:
#             in_time = ''    
#         if frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['out_time']):
#             out_time = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['out_time'])
#         else:
#             out_time = ''
#         if frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['shift']):
#             shift = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['shift'])
#         else:
#             shift = '' 
#         data.update({
#             'in_time':in_time,
#             'out_time':out_time,
#             'shift':shift
#         })
#         datalist.append(data.copy())
#     else:
#         frappe.throw(_("Employee has No Attendance on %s"%(formatdate(att_date))))
#         data.update({
#             'in_time':'',
#             'out_time':'',
#         })
#         datalist.append(data.copy())
#     return datalist   


@frappe.whitelist()
def get_attendance(emp,att_date):
    datalist = []
    data = {}
    if frappe.db.exists('Attendance',{'employee':emp,'attendance_date':att_date}):
        if frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['in_time']):
            in_time = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['in_time'])
        else:
            in_time = ''    
        if frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['out_time']):
            out_time = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['out_time'])
        else:
            out_time = ''
        if frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['shift']):
            shift = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['shift'])
        else:
            shift = '' 
        
        data.update({
            'in_time':in_time,
            'out_time':out_time,
            'shift':shift
        })
        datalist.append(data.copy())
        if in_time and out_time:
            frappe.msgprint(_("Check-in and check-out are already recorded for this date."))

        if not in_time and not out_time:
            frappe.throw(_("Checkin and Checkout are missing for this date."))
    else:
        frappe.throw(_("Employee has No Attendance on %s"%(formatdate(att_date))))
        data.update({
            'in_time':'',
            'out_time':'',
        })
        datalist.append(data.copy())
    return datalist  



def check_holiday(from_date,to_date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date between '%s' and '%s' """%(holiday_list,from_date,to_date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"
