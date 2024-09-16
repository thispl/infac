# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from email import message
import re
from frappe import _
import frappe
from frappe.model.document import Document
from datetime import date, timedelta, datetime,time
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,today, format_date)
import pandas as pd
import math
from frappe.utils import add_months, cint, flt, getdate, time_diff_in_hours




class AttendanceRegularize(Document):

    def on_submit(self):
        status = self.validate_total_wh()
        att_status = status[0]['status']
        att_working_hours = self.validate_total_wh()
        working_hours = att_working_hours[0]['att_wh']
        att_total_wh = self.validate_total_wh()
        total_wh = att_total_wh[0]['total_wh_att']
        att_extra_hours = self.validate_extra_hour()
        extra_hours = att_extra_hours[0]['extra_hrs_time']
        att_ot_hr = self.validate_extra_hour()
        ot_hr = att_ot_hr[0]['ot_hr']
        att_late_hours = self.validate_late_hour()
        late_hour = att_late_hours[0]['late_hour_time']
        att_late_hr = self.validate_late_hour()
        late_hr = att_late_hr[0]['late_hr']
        att_late_deduct = self.validate_late_hour()
        late_deduct = att_late_deduct[0]['late_deduct']
        update_shift_in_time = self.updated_shift()
        shift_in_time = update_shift_in_time[0]['get_shift_start_time']
        update_shift_out_time = self.updated_shift()
        shift_out_time = update_shift_out_time[0]['get_shift_end_time']

        hh = self.validate_check_holiday()
        if not hh:
            att = frappe.db.exists('Attendance',{'employee':self.employee,'attendance_date':self.attendance_date,'docstatus':('!=','2')})
            if att:
                leave_application = frappe.db.get_value('Attendance',{'name':att,'docstatus':('!=','2')},['leave_application'])
                if not leave_application:
                    attendance = frappe.get_doc('Attendance',{'name':att})
                    attendance.status = att_status
                    attendance.in_time = self.corrected_in
                    attendance.out_time = self.corrected_out
                    attendance.shift = self.corrected_shift
                    attendance.working_hours = working_hours
                    attendance.total_wh = total_wh
                    attendance.extra_hours = extra_hours
                    attendance.ot_hrs = ot_hr
                    attendance.late_hours = late_hour
                    attendance.late_hrs = late_hr
                    attendance.late_deduct = late_deduct
                    attendance.shift_type = self.corrected_shift
                    attendance.shift_in_time = shift_in_time
                    attendance.shift_out_time = shift_out_time
                    attendance.actual_shift = self.corrected_shift
                    attendance.actual_in_time = self.corrected_in
                    attendance.actual_out_time = self.corrected_out
                    attendance.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value('Attendance',att,'matched_status','Matched')
                    frappe.db.set_value('Attendance',att,'attendance_regularize',self.name)
                else:
                    frappe.throw(_('Employee %s Applied Leave on %s'%(self.employee,format_date(self.attendance_date))))    
        else:
            att = frappe.db.exists('Attendance',{'name':self.attendance_marked})
            if att:
                total_working_hour = self.validate_total_wh()
                total_wh = total_working_hour[0]['total_wh']
                ftr = [3600,60,1]
                hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
                wh = round(hr/3600,1)
                if wh > 0:
                    none_time =pd.to_datetime('00:00:00').time()
                    holiday_ot_hr = (math.floor(wh * 2) / 2) - 0.5
                    attendance = frappe.get_doc('Attendance',{'name':self.attendance_marked})
                    attendance.status = 'Present'
                    attendance.in_time = self.corrected_in
                    attendance.out_time = self.corrected_out
                    attendance.shift = self.corrected_shift
                    attendance.working_hours = working_hours
                    attendance.total_wh = total_wh
                    attendance.extra_hours = total_wh
                    attendance.ot_hrs = holiday_ot_hr
                    attendance.shift_type = self.corrected_shift
                    attendance.shift_in_time = shift_in_time
                    attendance.shift_out_time = shift_out_time
                    attendance.actual_shift = self.corrected_shift
                    attendance.actual_in_time = self.corrected_in
                    attendance.actual_out_time = self.corrected_out
                    attendance.save(ignore_permissions=True)
                    frappe.db.commit()
                    frappe.db.set_value('Attendance',self.attendance_marked,'status','Present')
                    frappe.db.set_value('Attendance',self.attendance_marked,'matched_status','Matched')
                    frappe.db.set_value('Attendance',self.attendance_marked,'attendance_regularize',self.name)
                    frappe.db.set_value('Attendance',self.attendance_marked,'regularize_marked','1')
            else:
                holidat_att = frappe.db.exists('Holiday Attendance',{'employee':self.employee,'attendance_date':self.attendance_date})
                if holidat_att:
                    total_working_hour = self.validate_total_wh()
                    total_wh = total_working_hour[0]['total_wh']
                    ftr = [3600,60,1]
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
                    wh = round(hr/3600,1)
                    if wh > 0:
                        none_time =pd.to_datetime('00:00:00').time()
                        holiday_ot_hr = (math.floor(wh * 2) / 2) - 0.5
                        attendance = frappe.get_doc('Holiday Attendance',{'name':holidat_att})
                        attendance.status = 'Present'
                        attendance.in_time = self.corrected_in
                        attendance.out_time = self.corrected_out
                        attendance.shift = self.corrected_shift
                        attendance.working_hours = working_hours
                        attendance.total_wh = total_wh
                        attendance.extra_hours = total_wh
                        attendance.ot_hrs = holiday_ot_hr
                        attendance.shift_type = self.corrected_shift
                        attendance.shift_in_time = shift_in_time
                        attendance.shift_out_time = shift_out_time
                        attendance.actual_shift = self.corrected_shift
                        attendance.actual_in_time = self.corrected_in
                        attendance.actual_out_time = self.corrected_out
                        attendance.save(ignore_permissions=True)
                        frappe.db.commit()
                        frappe.db.set_value('Holiday Attendance',self.attendance_marked,'status','Present')
                        frappe.db.set_value('Holiday Attendance',self.attendance_marked,'matched_status','Matched')
                        frappe.db.set_value('Holiday Attendance',self.attendance_marked,'attendance_regularize',self.name)
                else:
                    frappe.throw(_("Employee has Attendance for the date %s"%(self.attendance_date)))

                        
    
    def on_cancel(self):
        att = frappe.db.exists('Attendance',{'employee':self.employee,'attendance_date':self.attendance_date})
        if att:
            att_reg = frappe.db.get_value('Attendance',{'name':att},['attendance_regularize'])
            if att_reg == self.name:
                frappe.db.sql(""" update `tabAttendance` set attendance_regularize = '' where name = '%s' and docstatus != 2 """%(att))
                frappe.db.sql(""" update `tabAttendance` set matched_status = 'Unmatched' where name = '%s' and docstatus != 2 """%(att))

    def updated_shift(self):
        datalist = []
        data = {}
        get_shift_start_time = frappe.db.get_value('Shift Type',{'name':self.corrected_shift},['start_time'])
        get_shift_end_time = frappe.db.get_value('Shift Type',{'name':self.corrected_shift},['end_time'])
        data.update({
            'get_shift_start_time':get_shift_start_time,
            'get_shift_end_time':get_shift_end_time
        })
        datalist.append(data.copy())
        return datalist

    def validate_total_wh(self):
        datalist = []
        data = {}
        work_hour = time_diff_in_hours(self.corrected_out,self.corrected_in)
        str_in_time = datetime.strptime(str(self.corrected_in),'%Y-%m-%d %H:%M:%S')
        str_out_time = datetime.strptime(str(self.corrected_out),'%Y-%m-%d %H:%M:%S')
        total_wh = str_out_time - str_in_time
        if work_hour < 4.0:
            status = 'Absent'
        elif work_hour >= 4.0 and work_hour < 5.99:
            status = 'Half Day'
        elif work_hour >= 6.0:
            status = 'Present'	
        total_wh_att = datetime.strptime(str(total_wh),'%H:%M:%S').strftime('%H:%M')
        ftr = [3600,60,1]
        hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
        att_wh = round(hr/3600,1)
        data.update({
            'status':status,
            'total_wh':total_wh,
            'att_wh':att_wh,
            'total_wh_att':total_wh_att,
        })
        datalist.append(data.copy())
        return datalist  

    def validate_late_hour(self):
        datalist = []
        data = {}
        shift_start_time = frappe.db.get_value('Shift Type',self.corrected_shift,'start_time')
        shift_start_time = pd.to_datetime(str(shift_start_time)).time() 
        att_in_time = datetime.strptime(str(self.corrected_in),'%Y-%m-%d %H:%M:%S')
        str_in_date = att_in_time.date()
        shift_start_datetime = datetime.combine(str_in_date,shift_start_time)
        attendance = frappe.db.get_value('Attendance',{'employee':self.employee,'attendance_date':self.attendance_date},['permission_request'])
        if attendance:
            check_per_shift = frappe.db.get_value('Permission Request',{'name':attendance},['shift'])
            if check_per_shift != self.corrected_shift:
                if shift_start_datetime:
                    late_hour = pd.to_datetime('00:00:00').time()
                    late_hr = 0
                    ftr = [3600,60,1]
                    if att_in_time > shift_start_datetime:
                        late_hour = att_in_time - shift_start_datetime
                        late_hour_time = datetime.strptime(str(late_hour),'%H:%M:%S').strftime('%H:%M') 
                        hr = sum([a*b for a,b in zip(ftr, map(int,str(late_hour).split(':')))])
                        late_hr = round(hr/3600,1)
                        try:
                            actual_late_hour = late_hour_time
                            late_deduct = self.validate_late_deduct(actual_late_hour)
                        except:
                            actual_late_hour = late_hour
                            late_deduct = self.validate_late_deduct(actual_late_hour)
                        data.update({
                            'late_hour_time':late_hour_time,
                            'late_hr':late_hr,
                            'late_deduct':late_deduct
                        })
                        datalist.append(data.copy())
                    else:
                        data.update({
                            'late_hour_time':'',
                            'late_hr':'',
                            'late_deduct':''
                        })
                        datalist.append(data.copy())
            else:
                message = 'Employee Permission Applied so late will not be calculated'
                error_log = frappe.log_error('Permission Applied',message)
                data.update({
                    'error_log':error_log,
                    'late_hour_time':'',
                    'late_hr':'',
                    'late_deduct':''
                })
                datalist.append(data.copy())   
        else:
            if shift_start_datetime:
                late_hour = pd.to_datetime('00:00:00').time()
                late_hr = 0
                ftr = [3600,60,1]
                if att_in_time > shift_start_datetime:
                    late_hour = att_in_time - shift_start_datetime
                    late_hour_time = datetime.strptime(str(late_hour),'%H:%M:%S').strftime('%H:%M') 
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(late_hour).split(':')))])
                    late_hr = round(hr/3600,1)
                    try:
                        actual_late_hour = late_hour_time
                        late_deduct = self.validate_late_deduct(actual_late_hour)
                    except:
                        actual_late_hour = late_hour
                        late_deduct = self.validate_late_deduct(actual_late_hour)
                    data.update({
                        'late_hour_time':late_hour_time,
                        'late_hr':late_hr,
                        'late_deduct':late_deduct
                    })
                    datalist.append(data.copy())
                else:
                    data.update({
                        'late_hour_time':'',
                        'late_hr':'',
                        'late_deduct':''
                    })
                    datalist.append(data.copy())
        return datalist

    def validate_late_deduct(self,actual_late_hour):
        late_deduct_hour = actual_late_hour.seconds //3600
        late_deduct_minute = ((actual_late_hour.seconds//60)%60)
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
        str_time = datetime.strptime(str(late_deducted_time),'%H:%M:%S')
        get_str_time = str_time.strftime('%H:%M') 
        return get_str_time

    def validate_extra_hour(self):
        datalist = []
        data = {}
        ftr = [3600,60,1]
        shift_end_time = frappe.db.get_value('Shift Type',self.corrected_shift,'end_time')
        shift_end_time = pd.to_datetime(str(shift_end_time)).time()
        total_shift_hours = frappe.db.get_value('Shift Type',self.corrected_shift,'total_hours')
        att_out_time = datetime.strptime(str(self.corrected_out),'%Y-%m-%d %H:%M:%S')
        str_out_date = att_out_time.date()
        previous_day = add_days(str_out_date,-1)
        if getdate(str_out_date) > getdate(self.attendance_date):
        # if str(str_out_date) > self.attendance_date:
            if self.corrected_shift == 'B':
                shift_end_date_time = datetime.combine(previous_day,shift_end_time)
                if shift_end_date_time:
                    extra_hrs = pd.to_datetime('00:00:00').time()
                    ot_hr = 0 
                    if att_out_time > shift_end_date_time:
                        total_wh_method = self.validate_total_wh()
                        total_wh = total_wh_method[0]['total_wh']
                        if total_wh > total_shift_hours:
                            extra_hrs = att_out_time - shift_end_date_time
                            hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                            extras = round(hr/3600,1)
                            if extras >= 1:
                                ot_hr = math.floor(extras * 2) / 2
            elif self.corrected_shift == 'G':  
                shift_end_date_time = datetime.combine(previous_day,shift_end_time)
                if shift_end_date_time:
                    extra_hrs = pd.to_datetime('00:00:00').time()
                    ot_hr = 0 
                    if att_out_time > shift_end_date_time:
                        total_wh_method = self.validate_total_wh()
                        total_wh = total_wh_method[0]['total_wh']
                        if total_wh > total_shift_hours:
                            extra_hrs = att_out_time - shift_end_date_time
                            hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                            extras = round(hr/3600,1)
                            if extras >= 1.0:
                                ot_hr = math.floor(extras * 2) / 2     
            elif self.corrected_shift == 'A':  
                shift_end_date_time = datetime.combine(previous_day,shift_end_time)
                if shift_end_date_time:
                    extra_hrs = pd.to_datetime('00:00:00').time()
                    ot_hr = 0 
                    if att_out_time > shift_end_date_time:
                        total_wh_method = self.validate_total_wh()
                        total_wh = total_wh_method[0]['total_wh']
                        if total_wh > total_shift_hours:
                            extra_hrs = att_out_time - shift_end_date_time
                            hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                            extras = round(hr/3600,1)
                            if extras >= 1:
                                ot_hr = math.floor(extras * 2) / 2                                      
            else:
                shift_end_date_time = datetime.combine(str_out_date,shift_end_time)
                if shift_end_date_time:
                    extra_hrs = pd.to_datetime('00:00:00').time()
                    ot_hr = 0 
                    if att_out_time > shift_end_date_time:
                        total_wh_method = self.validate_total_wh()
                        total_wh = total_wh_method[0]['total_wh']
                        if total_wh > total_shift_hours:
                            frappe.errprint(att_out_time)
                            frappe.errprint(shift_end_date_time)
                            extra_hrs = att_out_time - shift_end_date_time
                            hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                            extras = round(hr/3600,1)
                            # frappe.errprint(extra_hrs)
                            # frappe.errprint(extras)
                            if extras >= 1:
                                frappe.errprint(shift_end_date_time)
                                ot_hr = math.floor(extras * 2) / 2
        else:
            shift_end_date_time = datetime.combine(str_out_date,shift_end_time)
            if shift_end_date_time:
                extra_hrs = pd.to_datetime('00:00:00').time()
                ot_hr = 0 
                if att_out_time > shift_end_date_time:
                    total_wh_method = self.validate_total_wh()
                    total_wh = total_wh_method[0]['total_wh']
                    if total_wh > total_shift_hours:
                        extra_hrs = att_out_time - shift_end_date_time
                        hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                        extras = round(hr/3600,1)
                        if extras >= 1:
                            ot_hr = math.floor(extras * 2) / 2
    
                                    
        extra_hrs_time = datetime.strptime(str(extra_hrs),'%H:%M:%S').strftime('%H:%M')                
        data.update({
            'extra_hrs_time':extra_hrs_time,
            'ot_hr':ot_hr
        })     
        datalist.append(data.copy()) 
        return datalist    

    def validate_check_holiday(self):
        holiday_list = frappe.db.get_value('Employee',self.employee,'holiday_list')
        holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
        left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,self.attendance_date),as_dict=True)
        if holiday:
            if holiday[0].weekly_off == 1:
                return "WW"
            else:
                return "HH"

@frappe.whitelist()
def get_assigned_shift_details(emp,att_date):
    datalist = []
    data = {}
    if frappe.db.exists('Shift Assignment',{'start_date':att_date,'employee':emp}):
        shift_assign = frappe.db.get_value('Shift Assignment',{'start_date':att_date,'employee':emp},['shift_type'])
        shift_start_time = frappe.db.get_value('Shift Type',{'name':shift_assign},['start_time'])
        shift_end_time = frappe.db.get_value('Shift Type',{'name':shift_assign},['end_time'])
        data.update({
            'shift_assign':shift_assign,
            'shift_start_time':shift_start_time,
            'shift_end_time':shift_end_time
        })
        datalist.append(data.copy())
    else:
        shift_assign = "G"
        shift_start_time = frappe.db.get_value('Shift Type',{'name':shift_assign},['start_time'])
        shift_end_time = frappe.db.get_value('Shift Type',{'name':shift_assign},['end_time'])
        data.update({
            'shift_assign':shift_assign,
            'shift_start_time':shift_start_time,
            'shift_end_time':shift_end_time
        })
        datalist.append(data.copy())
    return datalist		


@frappe.whitelist()
def get_attendance(emp,att_date):
    datalist = []
    data = {}
    if frappe.db.exists('Attendance',{'employee':emp,'attendance_date':att_date}):
        if frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['in_time']):
            in_time = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['in_time']).strftime('%H:%M:%S') 
        else:
            in_time = '-'    
        if frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['out_time']):
            out_time = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['out_time']).strftime('%H:%M:%S')   
        else:
            out_time = '-'
        data.update({
            'in_time':in_time,
            'out_time':out_time,
        })
        datalist.append(data.copy())

    elif frappe.db.exists('Holiday Attendance',{'employee':emp,'attendance_date':att_date}):
        if frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['in_time']):
            in_time = frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['in_time']).strftime('%H:%M:%S') 
        else:
            in_time = '-'    
        if frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['out_time']):
            out_time = frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['out_time']).strftime('%H:%M:%S')   
        else:
            out_time = '-'
        data.update({
            'in_time':in_time,
            'out_time':out_time,
        })
        datalist.append(data.copy())
    else:
        frappe.throw(_("Employee has No Checkins for the day"))
        data.update({
            'in_time':'No In Time',
            'out_time':'',
        })
        datalist.append(data.copy())
    return datalist    

@frappe.whitelist()
def attendance_marked(emp,att_date):
    datalist = []
    data = {}
    actual_shift = ''
    att_id = ''
    if frappe.db.exists('Attendance',{'employee':emp,'attendance_date':att_date}):
        if frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['in_time']):
            in_time = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['in_time'])
            actual_shift = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['shift'])
            att_id = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['name'])
        else:
            in_time = ''   
        if frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['out_time']):
            out_time = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['out_time'])
            actual_shift = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['shift'])
            att_id = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':att_date},['name'])
        else:
            out_time = ''
        data.update({
            'in_time':in_time,
            'out_time':out_time,
            'actual_shift':actual_shift,
            'att_id':att_id
        })
        datalist.append(data.copy())
    elif frappe.db.exists('Holiday Attendance',{'employee':emp,'attendance_date':att_date}):
        if frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['in_time']):
            in_time = frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['in_time'])
            actual_shift = frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['actual_shift'])
            # att_id = frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['name'])
        else:
            in_time = ''   
        if frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['out_time']):
            out_time = frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['out_time'])
            actual_shift = frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['actual_shift'])
            # att_id = frappe.db.get_value('Holiday Attendance',{'employee':emp,'attendance_date':att_date},['name'])
        else:
            out_time = ''
        data.update({
            'in_time':in_time,
            'out_time':out_time,
            'actual_shift':actual_shift,
            # 'att_id':att_id
        })
        datalist.append(data.copy())   
    else:
        # frappe.throw(_("Employee has No Checkins for the day"))
        data.update({
            'in_time':'-',
            'out_time':'-',
            'actual_shift':'-',
        })
        datalist.append(data.copy())
    return datalist 



    



