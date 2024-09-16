# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from re import S
from time import strftime, strptime
import frappe
import math
import pandas as pd
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

    def on_submit(self):
        att = frappe.db.exists('Attendance',{'attendance_date':self.date,'employee':self.employee})
        if att:
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
        #late hours process of miss punch application                 

    #This is the While cancel the document to remove the Miss Punch ID in Attendance
    def on_cancel(self):
        att = frappe.db.exists('Attendance',{'attendance_date':self.date,'employee':self.employee})
        if att:
            frappe.db.set_value('Attendance',att,'miss_punch_marked','')      

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
    else:
        frappe.throw(_("Employee has No Attendance on %s"%(formatdate(att_date))))
        data.update({
            'in_time':'',
            'out_time':'',
        })
        datalist.append(data.copy())
    return datalist    