# Copyright (c) 2021, teampro and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
import datetime
from datetime import datetime,timedelta
import datetime as dt
from frappe.share import add
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today,time_diff_in_hours,get_datetime,get_time
from frappe import _
import pandas as pd
import math
from dateutil.relativedelta import relativedelta, MO
import dateutil.relativedelta


class PermissionRequest(Document):

    # def after_insert(self):
    #     user_roles = frappe.get_roles(frappe.session.user)
    #     hr = "HR User" in user_roles
    #     # admin = "Administrator" in user_roles
    #     if (not hr):
    #         allowed_days1 = frappe.db.get_value("HR Time Settings", None, "permission_validation_dates")
    #         allowed_days = int(allowed_days1 or 0)
    #         current_date = today()
    #         if isinstance(current_date, str):
    #             current_date = datetime.strptime(current_date, "%Y-%m-%d").date()

    #         def is_working_day(check_date):
    #             return not check_holiday(check_date,check_date, self.employee_id)

    #         days_count = 0
    #         earliest_allowed = current_date
    #         while days_count < allowed_days:
    #             earliest_allowed = add_days(earliest_allowed, -1)
    #             if is_working_day(earliest_allowed):
    #                 days_count += 1

    #         if not self.permission_date:
    #             return

    #         if isinstance(self.permission_date, str):
    #             miss_date = datetime.strptime(self.permission_date, "%Y-%m-%d").date()
    #         else:
    #             miss_date = self.permission_date

    #         if miss_date < earliest_allowed:
    #             frappe.throw(
    #                 _("Permission are allowed only for up to the previous {0} working days.")
    #                 .format(allowed_days)
    #             )

    def after_insert(self):
        user_roles = frappe.get_roles(frappe.session.user)
        hr = "HR User" in user_roles

        # Should this restriction also apply to HR Users?
        apply_to_hr = cint(frappe.db.get_single_value(
            "HR Time Settings", "apply_permission_time_restriction_to_hr"
        ))

        if hr and not apply_to_hr:
            return

        if not self.permission_date or not self.shift:
            return

        shift_start_time = frappe.db.get_value("Shift Type", self.shift, "start_time")
        if not shift_start_time:
            return

        shift_datetime = datetime.combine(getdate(self.permission_date), get_time(shift_start_time))

        min_hours_before = flt(frappe.db.get_single_value(
            "HR Time Settings", "permission_min_hours_before_shift"
        )) or 4

        cutoff_datetime = shift_datetime - timedelta(hours=min_hours_before)

        if now_datetime() > cutoff_datetime:
            frappe.throw(
                _("Permission Request must be submitted at least {0} hour(s) before the Shift Start Time ({1}).")
                .format(min_hours_before, shift_datetime.strftime("%d-%m-%Y %H:%M:%S"))
            )
            
    def on_submit(self):
        att = frappe.db.exists('Attendance',{'attendance_date':self.permission_date,'employee':self.employee_id})
        if att:
            att_late_hours = self.late_hours()
            late_hour = att_late_hours[0]['late_hours']
            att_late_hr = self.late_hours()
            late_hr = att_late_hr[0]['late_hr']
            late_entry = self.late_hours()
            late_check = late_entry[0]['late_entry']
            att_late_deduct = self.late_dedcut_calculate()
            late_deduct = att_late_deduct[0]['late_deduct']
            att = frappe.get_doc('Attendance',att)
            att.status = 'Present'
            att.late_hours = late_hour 
            att.late_hrs = late_hr
            att.late_deduct = late_deduct
            att.permission_request = self.name
            att.late_entry = late_check
            att.save(ignore_permissions=True)
            frappe.db.commit()
        # else:
        #     frappe.throw(_('Employee %s have no attendance for that day'%(self.employee_id)))

    def late_hours(self):
        datalist = []
        data = {}
        att = frappe.db.exists('Attendance',{'attendance_date':self.permission_date,'employee':self.employee_id})
        if att:
            if self.session == 'First Half':
                att_in_time = frappe.db.get_value('Attendance',{'attendance_date':self.permission_date,'employee':self.employee_id},['in_time'])
                if att_in_time:
                    in_time = get_time(att_in_time)
                    combine_date_time = datetime.combine(getdate(self.permission_date), get_time(self.to_time))
                    datetime_format = get_datetime(combine_date_time)
                    permission_to_time = get_time(datetime_format)
                    if in_time > permission_to_time:
                        late_hours = att_in_time - datetime_format
                        late_hr = time_diff_in_hours(att_in_time,datetime_format)
                        data.update({
                            'late_hours':late_hours,
                            'late_hr':late_hr,
                            'late_entry':1,
                        })
                        datalist.append(data.copy())
                    else:
                        late_hours = get_time('00:00:00')
                        late_hr = '0.0'
                        data.update({
                            'late_hours':late_hours,
                            'late_hr':late_hr,
                            'late_entry':0,
                        })
                        datalist.append(data.copy())
                else:
                    late_hours = get_time('00:00:00')
                    late_hr = '0.0'
                    data.update({
                        'late_hours':late_hours,
                        'late_hr':late_hr,
                        'late_entry':0,
                    })
                    datalist.append(data.copy())
                #     frappe.throw(_('Employee %s have no In Time to calculate the late Hours'%(self.employee_id)))     
            elif self.session == 'Second Half':   
                att_out_time = frappe.db.get_value('Attendance',{'attendance_date':self.permission_date,'employee':self.employee_id},['out_time'])
                if att_out_time:
                    out_time = get_time(att_out_time)
                    combine_date_time = datetime.combine(getdate(self.permission_date), get_time(self.from_time))
                    datetime_format = get_datetime(combine_date_time)
                    permission_from_time = get_time(datetime_format)
                    if  permission_from_time > out_time:
                        frappe.errprint(permission_from_time)
                        late_hours = datetime_format - att_out_time 
                        late_hr = time_diff_in_hours(datetime_format,att_out_time)
                        data.update({
                            'late_hours':late_hours,
                            'late_hr':late_hr,
                            'late_entry':1,
                        })
                        datalist.append(data.copy())
                    else:
                        late_hours = get_time('00:00:00')
                        late_hr = '0.0'
                        data.update({
                            'late_hours':late_hours,
                            'late_hr':late_hr,
                            'late_entry':0,
                        })
                        datalist.append(data.copy())
                else:
                    late_hours = get_time('00:00:00')
                    late_hr = '0.0'
                    data.update({
                        'late_hours':late_hours,
                        'late_hr':late_hr,
                        'late_entry':0,
                    })
                    datalist.append(data.copy())
                #     frappe.throw(_('Employee %s have no Out Time to calculate the late Hours'%(self.employee_id)))  
        # else:
        #     frappe.throw(_('Employee %s have no Attendance for that Day'%(self.employee_id)) )         
        return datalist             

    @frappe.whitelist()
    def get_endtime1(Self,start_time):
        time = datetime.strptime(start_time, "%H:%M:%S")
        end_time = timedelta(hours=2) + time
        return str(end_time.time())
    
    @frappe.whitelist()
    def get_endtime2(Self,end_time):
        time = datetime.strptime(end_time, "%H:%M:%S")
        start_time = time - timedelta(hours=2)
        return str(start_time.time())
    
    def late_dedcut_calculate(self):
        datalist = []
        data = {}
        late_hours_calcu = self.late_hours()
        late_deduct = late_hours_calcu[0]['late_hours']
        late_entry = late_hours_calcu[0]['late_entry']
        # late_deduct_hours = get_time(late_deduct)
        if late_entry == 1:
            late_deduct_hour = late_deduct.seconds//3600
            late_deduct_minute = ((late_deduct.seconds//60)%60)
            deducted_minute = late_deduct_minute
            deducted_hour = late_deduct_hour
            if late_deduct_minute >= 1 and late_deduct_minute <= 5:
                deducted_minute = 5
            elif late_deduct_minute >= 6  and late_deduct_minute <=10:
                deducted_minute = 10
            elif late_deduct_minute >= 11 and late_deduct_minute <= 15:
                deducted_minute = 15
            elif late_deduct_minute >= 16 and late_deduct_minute <= 20:
                deducted_minute = 20
            elif late_deduct_minute >= 21 and late_deduct_minute <= 25:
                deducted_minute = 25
            elif late_deduct_minute >= 26 and late_deduct_minute <= 30:
                deducted_minute = 30
            elif late_deduct_minute >= 31 and late_deduct_minute <= 35:
                deducted_minute = 35
            elif late_deduct_minute >= 36 and late_deduct_minute <= 40:
                deducted_minute = 40
            elif late_deduct_minute >= 41 and late_deduct_minute <= 45:
                deducted_minute = 45
            elif late_deduct_minute >= 46 and late_deduct_minute <= 50:
                deducted_minute = 50 
            elif late_deduct_minute >= 51 and late_deduct_minute <= 55:
                deducted_minute = 55    
            elif late_deduct_minute >= 56 and late_deduct_minute <= 60:
                deducted_hour = late_deduct_hour +1
                deducted_minute = 00
            late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute)+':00'
            time = datetime.strptime(str(late_deducted_time),'%H:%M:%S')
            tm = time.strftime('%H:%M')
            data.update({
                'late_deduct':tm
            })
            datalist.append(data.copy())
        else:   
            data.update({
                'late_deduct':''
            })
            datalist.append(data.copy())
            return datalist 
        return datalist
   
    # def validate(self):
    #     payroll_start_day = frappe.db.get_value('Payroll Dates Automatic',{'name':'PAYDATE0001'},['payroll_start_date'])
    #     payroll_end_day = frappe.db.get_value('Payroll Dates Automatic',{'name':'PAYDATE0001'},['payroll_end_date'])
    #     per_count = frappe.db.sql(""" select count(*) from  `tabPermission Request` where employee_id = '%s' and permission_date  between '%s' and '%s' and "docstatus": ["in", [0, 1]] """%(self.employee_id,payroll_start_day,payroll_end_day),as_dict=True)[0]
    #     for per in per_count.values():
    #         if per >= 2:
    #             frappe.throw("Only 2 permissions are allowed for a month")
    #         # else:
    #         #     frappe.log_error('Less than Permission for a month')    
    #     self.validate_one_permission_per_day()

    def validate(self):
        payroll_start_day = frappe.db.get_value('Payroll Dates Automatic',{'name':'PAYDATE0001'},['payroll_start_date'])
        payroll_end_day = frappe.db.get_value('Payroll Dates Automatic',{'name':'PAYDATE0001'},['payroll_end_date'])
   
        # Get allowed limit from HR Time Setting
        allowed_count = frappe.db.get_single_value("HR Time Settings", "permission_days_allowed" ) or 0

        if self.is_new():
            # Count existing permissions
            per_count = frappe.db.sql("""
                SELECT COUNT(*) as count
                FROM `tabPermission Request`
                WHERE employee_id = %s
                AND permission_date BETWEEN %s AND %s
                AND docstatus IN (0, 1)
            """, (self.employee_id, payroll_start_day, payroll_end_day), as_dict=True)[0]["count"]

            if per_count >= allowed_count:
                frappe.throw(f"Only {allowed_count} permissions are allowed for this period")

        self.validate_one_permission_per_day()


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
         
    def validate_one_permission_per_day(self):
        if frappe.db.exists("Permission Request", { "employee_id": self.employee_id, "permission_date": self.permission_date, "session": self.session,
                            "docstatus": ["!=", 2],"workflow_state": ["!=", "Rejected"], "name": ["!=", self.name]}):
            frappe.throw("You are already applied Permission for the same day")

    def on_cancel(self):
        if self.docstatus == 2:
            att = frappe.db.exists('Attendance',{'attendance_date':self.permission_date,'employee':self.employee_id,'permission_request':self.name})
            if att:
                frappe.db.set_value('Attendance',att,'permission_request','')   

    # def on_update(self):
    #     frappe.errprint("Level")
    #     # If workflow_state didn't change, do nothing
    #     if not self.has_value_changed("workflow_state"):
    #         return

    #     user = frappe.session.user
    #     time = now_datetime()

    #     # LEVEL 1 → LEVEL 2
    #     if self.workflow_state == "Superior Pending" and not self.level_1_timing:
    #         frappe.errprint("Level 2")
    #         self.level_1_timing = f"{user} at {time}"

    #     # LEVEL 2 → LEVEL 3
    #     elif self.workflow_state == "Approved" and not self.level_2_timing:
    #         self.level_2_timing = f"{user} at {time}"

    #     # FINAL APPROVAL
    #     elif self.workflow_state == "Approved" and not self.approved_timing:
    #         self.approved_timing = f" {user} at {time}"

    #     # REJECTION (from any level)
    #     elif self.workflow_state == "Rejected" and not self.rejected_timing:
    #         self.rejected_timing = f"{user} at {time}"


    # def on_update(self):
    #     frappe.errprint("Level")

    #     # If workflow_state didn't change, do nothing
    #     if not self.has_value_changed("workflow_state"):
    #         return

    #     user = frappe.session.user
    #     time = now_datetime()

    #     updated = False  # 👈 add this

    #     # LEVEL 1 → LEVEL 2
    #     if self.workflow_state == "Superior Pending" and not self.level_1_timing:
    #         frappe.errprint("Level 2")
    #         self.level_1_timing = f"{user} at {time}"
    #         updated = True

    #     # LEVEL 2 → LEVEL 3
    #     elif self.workflow_state == "Approved" and not self.level_2_timing:
    #         self.level_2_timing = f"{user} at {time}"
    #         updated = True

    #     # FINAL APPROVAL
    #     elif self.workflow_state == "Approved" and not self.approved_timing:
    #         self.approved_timing = f"{user} at {time}"
    #         updated = True

    #     # REJECTION
    #     elif self.workflow_state == "Rejected" and not self.rejected_timing:
    #         self.rejected_timing = f"{user} at {time}"
    #         updated = True

    #     # 🔥 THIS is the magic line
    #     if updated:
    #         self.save(ignore_permissions=True)
    
    #session automactically marked based on from_time
    @frappe.whitelist()
    def get_session(self):
        if self.from_time:
            from_time = datetime.strptime(self.from_time,'%H:%M:%S').time()
            session  = self.get_session_based_on_time(from_time)
            return session
        


    def is_between(self,time, time_range):
        if time_range[1] < time_range[0]:
            return time >= time_range[0] or time <= time_range[1]
        return time_range[0] <= time <= time_range[1]

    def get_session_based_on_time(self,from_time):
        from datetime import datetime
        from datetime import date, timedelta,time
        nowtime = datetime.now()

        fh_min_time = frappe.db.get_value('Shift Type',{'name':self.shift},'min_time')
        fh_max_time = frappe.db.get_value('Shift Type',{'name':self.shift},'max_time')
        sh_min_time = frappe.db.get_value('Shift Type',{'name':self.shift},'sh_min_time')
        sh_max_time = frappe.db.get_value('Shift Type',{'name':self.shift},'sh_max_time')

        fh_min = get_time(fh_min_time)
        fh_max = get_time(fh_max_time)
        sh_min = get_time(sh_min_time)
        sh_max = get_time(sh_max_time)

        fh_session = [time(hour=fh_min.hour, minute=fh_min.minute, second=fh_min.second),time(hour=fh_max.hour, minute=fh_max.minute,second=fh_max.second)]
        sh_session = [time(hour=sh_min.hour, minute=sh_min.minute, second=sh_min.second),time(hour=sh_max.hour, minute=sh_max.minute,second=sh_max.second)]
        session = ''
        if self.is_between(from_time,fh_session):
            session = 'First Half'
        if self.is_between(from_time,sh_session):
            session = 'Second Half'
        return session 
    
    @frappe.whitelist()
    def show_html(self):
        html = "<h2><center>PERMISSION REQUEST</center></h2><table class='table table-bordered'><tr><th style=font-size:16px;>From Date</th><th style=font-size:16px;>To Date</th></tr><tr><td><h3>%s</h3></td><td><h3>%s</h3></td></tr><tr><th style=font-size:16px;>From Time</th><th style=font-size:16px;>To Time</th></tr><tr><td><h3>%s</h3></td><td><h3>%s</h3></td></tr></table>"%(frappe.utils.format_date(self.permission_date),frappe.utils.format_date(self.permission_date),frappe.utils.format_time(self.from_time), frappe.utils.format_time(self.to_time))
        return html
                        
    
@frappe.whitelist()
def permission_validation(emp,att_date):
    attendance = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['status'])
    return attendance
      
#This is the Permission Validation of 2 Hours Each Employee
@frappe.whitelist()
def validate_time(from_time,hour):
    datalist = []
    data = {}
    if hour == '0.5':
        per_from_time = datetime.strptime(from_time,'%H:%M:%S')
        per_to_time = relativedelta(minutes=30)+ per_from_time
        get_time = datetime.strptime(str(per_to_time),'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
        data.update({
            'get_time':get_time
        })
        datalist.append(data.copy())
    elif hour == '1':
        per_from_time = datetime.strptime(from_time,'%H:%M:%S')
        per_to_time = relativedelta(hours=1)+ per_from_time
        get_time = datetime.strptime(str(per_to_time),'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
        data.update({
            'get_time':get_time
        })
        datalist.append(data.copy())
    elif hour == '1.5':
        per_from_time = datetime.strptime(from_time,'%H:%M:%S')
        per_to_time = relativedelta(hours=1.5)+ per_from_time
        get_time = datetime.strptime(str(per_to_time),'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
        data.update({
            'get_time':get_time
        })
        datalist.append(data.copy())
    elif hour == '2':
        per_from_time = datetime.strptime(from_time,'%H:%M:%S')
        per_to_time = relativedelta(hours=2)+ per_from_time
        get_time = datetime.strptime(str(per_to_time),'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
        data.update({
            'get_time':get_time
        })
        datalist.append(data.copy())
    else:
        data.append(frappe.msgprint('Please Select the Permission Hour'))      
    return datalist    
            

#This is the time difference between from and to time
# @frappe.whitelist()
# def get_time_difference(permission_date,from_time,to_time):
#     permission_date = datetime.strptime(permission_date,'%Y-%m-%d')
#     try:
#         from_time_obj = datetime.strptime(from_time, '%H:%M:%S').time()
#     except ValueError:
#         from_time_obj = datetime.strptime(from_time, '%H:%M').time()

#     try:
#         to_time_obj = datetime.strptime(to_time, '%H:%M:%S').time()
#     except ValueError:
#         to_time_obj = datetime.strptime(to_time, '%H:%M').time()

#     # from_time = datetime.strptime(from_time,'%H:%M').time()
#     # to_time = datetime.strptime(to_time,'%H:%M').time()
#     # from_time = datetime.combine(permission_date, from_time)
#     # to_time = datetime.combine(permission_date, to_time)
#     from_time = datetime.combine(permission_date, from_time_obj)
#     to_time = datetime.combine(permission_date, to_time_obj)
#     total_hours = to_time - from_time
#     ftr = [3600,60,1]
#     hr = sum([a*b for a,b in zip(ftr, map(int,str(total_hours).split(':')))])
#     perm_hr = round(hr/3600,1)
#     return total_hours, perm_hr

@frappe.whitelist()
def get_time_difference(permission_date, from_time, to_time):
    permission_date = datetime.strptime(permission_date, '%Y-%m-%d')

    # Handle both HH:MM and HH:MM:SS formats
    def parse_time(time_str):
        try:
            return datetime.strptime(time_str, '%H:%M:%S').time()
        except ValueError:
            return datetime.strptime(time_str, '%H:%M').time()

    from_time_obj = parse_time(from_time)
    to_time_obj = parse_time(to_time)

    # Combine date and time
    from_dt = datetime.combine(permission_date, from_time_obj)
    to_dt = datetime.combine(permission_date, to_time_obj)

    # Calculate total hours
    total_delta = to_dt - from_dt
    total_seconds = total_delta.total_seconds()
    perm_hr = round(total_seconds / 3600, 1)

    return {
        "total_hours": str(total_delta),   # "1:30:00"
        "perm_hr": perm_hr                 # 1.5
    }

#employee validation for permission_application
# @frappe.whitelist()
# def get_employee_validation(emp):
#     employee = frappe.db.get_value('Employee',{'status':'Active','name':emp},['employment_type'])
#     if employee != 'STAFF':
#         frappe.throw(_('Permission Application Only Apply for STAFF Employees'))
#     return "Not Allowed"   


def check_holiday(from_date,to_date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date between '%s' and '%s' """%(holiday_list,from_date,to_date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"
        
def on_update(doc, method):
    pass 

import frappe
from frappe import _
from frappe.model.workflow import apply_workflow

@frappe.whitelist()
def incharge_approve(docname, approved_through):
    doc = frappe.get_doc("Permission Request", docname)
    doc.db_set("approved_through", approved_through, update_modified=True)
    apply_workflow(doc, "Approve")
    frappe.db.commit()
    return {"status": "success"}