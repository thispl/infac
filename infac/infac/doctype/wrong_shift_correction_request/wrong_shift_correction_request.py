# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from operator import truediv
import frappe
from frappe.model.document import Document
import datetime
from datetime import date, timedelta,time,datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,today, format_date)
import pandas as pd
import math

class WrongShiftCorrectionRequest(Document):

    def validate(self):
        if self.actual_out_time:
            correct_shift = frappe.db.exists('Shift Assignment',{'employee':self.employee,'start_date':self.attendance_date},['shift_type'])
            if correct_shift:
                if self.assigned_shift == self.corrected_shift:
                    self.corrected_shift = self.corrected_shift
                else:
                    frappe.db.set_value('Shift Assignment',correct_shift,'shift_type',self.corrected_shift)    
            else:
                shift_assign = frappe.new_doc('Shift Assignment')
                shift_assign.employee = self.employee
                shift_assign.shift_type = self.corrected_shift
                shift_assign.start_date = self.attendance_date
                shift_assign.end_date = self.attendance_date
                shift_assign.save(ignore_permissions=True)     
                shift_assign.submit()
                frappe.db.commit()   

            str_in_time = datetime.strptime(str(self.actual_in_time),'%Y-%m-%d %H:%M:%S')
            str_out_time = datetime.strptime(str(self.actual_out_time),'%Y-%m-%d %H:%M:%S')
            total_wh = str_out_time - str_in_time
            wh_time_change = datetime.strptime(str(total_wh),'%H:%M:%S').strftime('%H:%M')
            self.total_wh = wh_time_change
            ftr = [3600,60,1]
            hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
            wh = round(hr/3600,1)
            self.working_hour = wh

            shift_end_time = frappe.db.get_value('Shift Type',self.attended_shift,'end_time')
            shift_end_time_change = pd.to_datetime(str(shift_end_time)).time()

            att_out_time = datetime.strptime(str(self.actual_out_time),'%Y-%m-%d %H:%M:%S')
            out_time_to_date = att_out_time.date()

            total_shift_hours = frappe.db.get_value('Shift Type',self.attended_shift,'total_hours')

            shift_end_date_time = datetime.combine(out_time_to_date,shift_end_time_change)
            #Calculating the total_wh,extra_hr and ot_hr
            if shift_end_date_time:
                extra_hrs = pd.to_datetime('00:00:00').time()
                ot_hr = 0
                if att_out_time > shift_end_date_time:
                    if total_wh > total_shift_hours:
                        extra_hrs = att_out_time - shift_end_date_time
                        extra_hrs_time = datetime.strptime(str(extra_hrs),'%H:%M:%S').strftime('%H:%M')
                        self.extra_hour = extra_hrs_time
                        hr = sum([a*b for a,b in zip(ftr, map(int,str(extra_hrs).split(':')))])
                        extras = round(hr/3600,1)
                        if extras > 1:
                            ot_hr = math.floor(extras * 2) / 2
                            self.ot_hour = ot_hr


            shift_start_time = frappe.db.get_value('Shift Type',self.attended_shift,'start_time')
            shift_start_time_change = pd.to_datetime(str(shift_start_time)).time()
            att_in_time = datetime.strptime(str(self.actual_in_time),'%Y-%m-%d %H:%M:%S')
            in_time_to_date = att_in_time.date()
            shift_start_date_time = datetime.combine(in_time_to_date,shift_start_time_change)
            if shift_start_date_time:
                late_hour = pd.to_datetime('00:00:00').time()
                late_hr = 0
                #This is the Late_hour and late_hr
                if att_in_time > shift_start_date_time:
                    late_hour = att_in_time - shift_start_date_time
                    late_hour_time = datetime.strptime(str(late_hour),'%H:%M:%S').strftime('%H:%M') 
                    self.late_hours = late_hour_time     
                    hr = sum([a*b for a,b in zip(ftr, map(int,str(late_hour).split(':')))])
                    late_hr = round(hr/3600,1) 
                    self.late_hr = late_hr 
                    
                #This is the late_hour will be round off based on late_hour 
                # if self.corrected_shift == 'A':
                try:
                    actual_late_hour = self.late_hours
                    if actual_late_hour:
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
                        time = datetime.strptime(str(late_deducted_time),'%H:%M:%S')
                        time_change = time.strftime('%H:%M')   
                        self.late_deduct = time_change  
                except:
                    actual_late_hour = late_hour
                    if actual_late_hour:
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
                        time = datetime.strptime(str(late_deducted_time),'%H:%M:%S')
                        time_change = time.strftime('%H:%M')   
                        self.late_deduct = time_change 


                # elif self.corrected_shift == 'B':    
                #     actual_late_hour = self.late_hours 
                #     if actual_late_hour:
                #         late_deduct_hour = actual_late_hour.seconds //3600   
                #         late_deduct_minute = ((actual_late_hour.seconds//60)%60)
                #         deducted_minute = late_deduct_minute
                #         deducted_hour = late_deduct_hour
                #         if late_deduct_minute >= 1 and late_deduct_minute <= 5:
                #             deducted_minute = 5
                #         elif late_deduct_minute >= 6  and late_deduct_minute <=10:
                #             deducted_minute = 10
                #         elif late_deduct_minute >= 11 and late_deduct_minute <= 15:
                #             deducted_minute = 15
                #         elif late_deduct_minute >= 16 and late_deduct_minute <= 20:
                #             deducted_minute = 20
                #         elif late_deduct_minute >= 21 and late_deduct_minute <= 25:
                #             deducted_minute = 25
                #         elif late_deduct_minute >= 26 and late_deduct_minute <= 30:
                #             deducted_minute = 30
                #         elif late_deduct_minute >= 31 and late_deduct_minute <= 35:
                #             deducted_minute = 35
                #         elif late_deduct_minute >= 36 and late_deduct_minute <= 40:
                #             deducted_minute = 40
                #         elif late_deduct_minute >= 41 and late_deduct_minute <= 45:
                #             deducted_minute = 45
                #         elif late_deduct_minute >= 46 and late_deduct_minute <= 50:
                #             deducted_minute = 50 
                #         elif late_deduct_minute >= 51 and late_deduct_minute <= 55:
                #             deducted_minute = 55    
                #         elif late_deduct_minute >= 56 and late_deduct_minute <= 60:
                #             deducted_hour = late_deduct_hour +1
                #             deducted_minute = 00
                #         late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute)+':00'
                #         time = datetime.strptime(str(late_deducted_time),'%H:%M:%S')
                #         time_change = time.strftime('%H:%M')   
                #         self.late_deduct = time_change 
                        
                # elif self.corrected_shift == 'G':    
                #     actual_late_hour = self.late_hours 
                #     if actual_late_hour:
                #         late_deduct_hour = actual_late_hour.seconds //3600   
                #         late_deduct_minute = ((actual_late_hour.seconds//60)%60)
                #         deducted_minute = late_deduct_minute
                #         deducted_hour = late_deduct_hour
                #         if late_deduct_minute >= 1 and late_deduct_minute <= 5:
                #             deducted_minute = 5
                #         elif late_deduct_minute >= 6  and late_deduct_minute <=10:
                #             deducted_minute = 10
                #         elif late_deduct_minute >= 11 and late_deduct_minute <= 15:
                #             deducted_minute = 15
                #         elif late_deduct_minute >= 16 and late_deduct_minute <= 20:
                #             deducted_minute = 20
                #         elif late_deduct_minute >= 21 and late_deduct_minute <= 25:
                #             deducted_minute = 25
                #         elif late_deduct_minute >= 26 and late_deduct_minute <= 30:
                #             deducted_minute = 30
                #         elif late_deduct_minute >= 31 and late_deduct_minute <= 35:
                #             deducted_minute = 35
                #         elif late_deduct_minute >= 36 and late_deduct_minute <= 40:
                #             deducted_minute = 40
                #         elif late_deduct_minute >= 41 and late_deduct_minute <= 45:
                #             deducted_minute = 45
                #         elif late_deduct_minute >= 46 and late_deduct_minute <= 50:
                #             deducted_minute = 50 
                #         elif late_deduct_minute >= 51 and late_deduct_minute <= 55:
                #             deducted_minute = 55    
                #         elif late_deduct_minute >= 56 and late_deduct_minute <= 60:
                #             deducted_hour = late_deduct_hour +1
                #             deducted_minute = 00
                #         late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute)+':00'
                #         time = datetime.strptime(str(late_deducted_time),'%H:%M:%S')
                #         time_change = time.strftime('%H:%M')   
                #         self.late_deduct = time_change               
                # else:
                #     actual_late_hour =  late_hour
                #     if actual_late_hour:
                #         late_deduct_hour = actual_late_hour.seconds //3600   
                #         late_deduct_minute = ((actual_late_hour.seconds//60)%60)
                #         deducted_minute = late_deduct_minute
                #         deducted_hour = late_deduct_hour
                #         if late_deduct_minute >= 1 and late_deduct_minute <= 5:
                #             deducted_minute = 5
                #         elif late_deduct_minute >= 6  and late_deduct_minute <=10:
                #             deducted_minute = 10
                #         elif late_deduct_minute >= 11 and late_deduct_minute <= 15:
                #             deducted_minute = 15
                #         elif late_deduct_minute >= 16 and late_deduct_minute <= 20:
                #             deducted_minute = 20
                #         elif late_deduct_minute >= 21 and late_deduct_minute <= 25:
                #             deducted_minute = 25
                #         elif late_deduct_minute >= 26 and late_deduct_minute <= 30:
                #             deducted_minute = 30
                #         elif late_deduct_minute >= 31 and late_deduct_minute <= 35:
                #             deducted_minute = 35
                #         elif late_deduct_minute >= 36 and late_deduct_minute <= 40:
                #             deducted_minute = 40
                #         elif late_deduct_minute >= 41 and late_deduct_minute <= 45:
                #             deducted_minute = 45
                #         elif late_deduct_minute >= 46 and late_deduct_minute <= 50:
                #             deducted_minute = 50 
                #         elif late_deduct_minute >= 51 and late_deduct_minute <= 55:
                #             deducted_minute = 55    
                #         elif late_deduct_minute >= 56 and late_deduct_minute <= 60:
                #             deducted_hour = late_deduct_hour +1
                #             deducted_minute = 00
                #         late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute)+':00'
                #         time = datetime.strptime(str(late_deducted_time),'%H:%M:%S')
                #         time_change = time.strftime('%H:%M')   
                #         self.late_deduct = time_change  

        else:
            frappe.throw("Employee has not Out Time")    

    def on_submit(self):
        if self.total_wh:
            frappe.db.set_value('Attendance',self.attendance_marked,'total_wh',self.total_wh)
        else:
           frappe.db.set_value('Attendance',self.attendance_marked,'total_wh','') 
        if self.working_hour:   
            frappe.db.set_value('Attendance',self.attendance_marked,'working_hours',self.working_hour)
        else:
            frappe.db.set_value('Attendance',self.attendance_marked,'working_hours','')
        if self. extra_hour:       
            frappe.db.set_value('Attendance',self.attendance_marked,'extra_hours',self.extra_hour)
        else:
            frappe.db.set_value('Attendance',self.attendance_marked,'extra_hours','00:00') 
        if self.ot_hour:       
            frappe.db.set_value('Attendance',self.attendance_marked,'ot_hrs',self.ot_hour)
        else:
            frappe.db.set_value('Attendance',self.attendance_marked,'ot_hrs','0.0')   
        if self.late_hours:     
            frappe.db.set_value('Attendance',self.attendance_marked,'late_hours',self.late_hours)
        else:
            frappe.db.set_value('Attendance',self.attendance_marked,'late_hours','00:00')    
        if self.late_hr:    
            frappe.db.set_value('Attendance',self.attendance_marked,'late_hrs',self.late_hr)
        else:
            frappe.db.set_value('Attendance',self.attendance_marked,'late_hrs','')
        if self.late_deduct:        
            frappe.db.set_value('Attendance',self.attendance_marked,'late_deduct',self.late_deduct)
        else:
            frappe.db.set_value('Attendance',self.attendance_marked,'late_deduct','')    
        frappe.db.set_value('Attendance',self.attendance_marked,'shift',self.attended_shift)  
        frappe.db.set_value('Attendance',self.attendance_marked,'status','Present')  
        frappe.db.set_value('Attendance',self.attendance_marked,'shift_type',self.attended_shift)
        frappe.db.set_value('Attendance',self.attendance_marked,'matched_status','Matched')
        frappe.db.set_value('Attendance',self.attendance_marked,'out_time',self.actual_out_time)
        # if self.corrected_shift == 'C':
        #     next_day_att = self.actual_out_time
        # if self.corrected_shift == 'C':
        #     frappe.db.set_value('Attendance',self.attendance_marked,'out_time',self.actual_out_time)
        #     get_date = self.corrected_shift
        #     day = get_date.date()
        #     att = frappe.db.exists()


@frappe.whitelist()
def mark_attendance(attendance_date,emp,shift,out_time):
    data = []
    try:
        if shift == 'C':
            if out_time:
                data.append(out_time)
            else:    
                next_day = add_days(attendance_date,1)
                att_check = frappe.db.get_value('Attendance',{'employee':emp,'attendance_date':next_day},['in_time','out_time','name'])
                if att_check:
                    data.append(att_check[0])
                    data.append(att_check[1])
                    data.append(att_check[2])
                    data.append(shift)
                else:
                    data.append(frappe.throw("Employee has not next day In Time"))
            return data
    except:
        return data   

