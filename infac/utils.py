import frappe
import datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours   
from datetime import date, timedelta,time,datetime



#late deduct calculation for Attendance
@frappe.whitelist()
def late_calculation(date):
    attendance = frappe.db.get_all('Attendance',['name','employee','in_time','out_time','attendance_date'])
    for att in attendance:
        actual_late_hours = frappe.db.get_value('Attendance',att.name,'late_hours')
        if actual_late_hours:
            late_deduct_hour = actual_late_hours.seconds//3600
            late_deduct_minute = ((actual_late_hours.seconds//60)%60)
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

            frappe.db.set_value('Attendance',att.name,'late_deduct',time_change)    


@frappe.whitelist() 
def set_attendance(in_time,out_time):
    str_in_time = datetime.strptime(in_time,'%Y-%m-%d %H:%M:%S')
    str_out_time = datetime.strptime(out_time,'%Y-%m-%d %H:%M:%S')
    total_wh = str_out_time - str_in_time
    time_change = datetime.strptime(str(total_wh),'%H:%M:%S').strftime('%H:%M')
    ftr = [3600,60,1]
    hr = sum([a*b for a,b in zip(ftr, map(int,str(total_wh).split(':')))])
    wh = round(hr/3600,1)

    return wh,time_change