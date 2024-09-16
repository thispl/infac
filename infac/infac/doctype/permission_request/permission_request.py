# Copyright (c) 2021, teampro and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
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
        else:
            frappe.throw(_('Employee %s have no attendance for that day'%(self.employee_id)))

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
        else:
            frappe.throw(_('Employee %s have no Attendance for that Day'%(self.employee_id)) )         
        return datalist             


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
   
    def validate(self):
        payroll_start_day = frappe.db.get_value('Payroll Dates Automatic',{'name':'PAYDATE0001'},['payroll_start_date'])
        payroll_end_day = frappe.db.get_value('Payroll Dates Automatic',{'name':'PAYDATE0001'},['payroll_end_date'])
        per_count = frappe.db.sql(""" select count(*) from  `tabPermission Request` where employee_id = '%s' and permission_date  between '%s' and '%s' and docstatus = '1' """%(self.employee_id,payroll_start_day,payroll_end_day),as_dict=True)[0]
        for per in per_count.values():
            if per >= 2:
                frappe.throw("Only 2 permissions are allowed for a month")
            else:
                frappe.log_error('Less than Permission for a month')    

    def on_cancel(self):
        if self.docstatus == 2:
            att = frappe.db.exists('Attendance',{'attendance_date':self.permission_date,'employee':self.employee_id,'permission_request':self.name})
            if att:
                frappe.db.set_value('Attendance',att,'permission_request','')   

    
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
@frappe.whitelist()
def get_time_difference(permission_date,from_time,to_time):
    permission_date = datetime.strptime(permission_date,'%Y-%m-%d')
    from_time = datetime.strptime(from_time,'%H:%M:%S').time()
    to_time = datetime.strptime(to_time,'%H:%M:%S').time()
    from_time = datetime.combine(permission_date, from_time)
    to_time = datetime.combine(permission_date, to_time)
    total_hours = to_time - from_time
    ftr = [3600,60,1]
    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_hours).split(':')))])
    perm_hr = round(hr/3600,1)
    return total_hours, perm_hr

#employee validation for permission_application
# @frappe.whitelist()
# def get_employee_validation(emp):
#     employee = frappe.db.get_value('Employee',{'status':'Active','name':emp},['employment_type'])
#     if employee != 'STAFF':
#         frappe.throw(_('Permission Application Only Apply for STAFF Employees'))
#     return "Not Allowed"   
