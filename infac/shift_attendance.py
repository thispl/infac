import frappe
import pandas as pd
import datetime
from frappe.utils.data import ceil, get_time, get_year_start
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from datetime import datetime
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
from datetime import date, timedelta,time
from frappe.utils import get_url_to_form
import math
from frappe.utils.background_jobs import enqueue
from erpnext.hr.utils import get_holiday_dates_for_employee
from frappe.utils import get_timedelta


def mark_att_manual():
    # from_date = add_days(today(),-1)
    # to_date = today()
    from_date ="2026-08-27"
    to_date ="2026-08-29"
    checkins = frappe.db.sql("""select time,employee,name,log_type from `tabEmployee Checkin` where date(time) between '%s' and '%s'  order by time   """%(from_date,to_date),as_dict=True)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            #the below mthod to mark the checkin in attendance application for IN and OUT Punches
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    #the below method to mark the Employees do not have punches.       
    mark_absent(from_date,to_date)
    #the below method to mark the IN and OUT Punches of Total Working and OT Hours 
    mark_wh_ot_new(from_date,to_date)
    #the below method to calculate the Staff Categories Employees working as Overtime to calculate the Incentive Amount
    # mark_incentive_amount_staff_categories(from_date,to_date)
    #this below method to check the Employee have assigned shift assignment and marked in attendance..
    mark_assigned_shift(from_date,to_date)
    #this below method to mark the IN time Based on which shift will comes the actual Shift
    mark_attended_shift(from_date,to_date)
    #the below method to mark the assigned shift and actual shift matched or not,not matched employees mark as absent
    mark_status_as_absent(from_date,to_date)
    # #the below method if an employee comes in week-off or Holiday Days that day Present
    mark_attendance_as_present_mark_holiday(from_date,to_date)
    # #the below method employee week-off and holiday date attendance moved to Holiday Attendance Doctype
    check_holiday_moved_to_holiday_attendance(from_date,to_date)
    # #th below method Employee status mark as Half Day the Late Hours,Late Deduct,Late HR will be Empty
    make_late_hours_empty(from_date,to_date)
    mark_late_entry(from_date, to_date)

    return "Completed" 

def mark_att():
    from_date = add_days(today(),-1)
    to_date = today()
    # from_date ="2026-04-09"
    # to_date ="2026-04-10"
    checkins = frappe.db.sql("""select time,employee,name,log_type from `tabEmployee Checkin` where date(time) between '%s' and '%s'  order by time   """%(from_date,to_date),as_dict=True)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            #the below mthod to mark the checkin in attendance application for IN and OUT Punches
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    #the below method to mark the Employees do not have punches.       
    mark_absent(from_date,to_date)
    #the below method to mark the IN and OUT Punches of Total Working and OT Hours 
    mark_wh_ot_new(from_date,to_date)
    #the below method to calculate the Staff Categories Employees working as Overtime to calculate the Incentive Amount
    # mark_incentive_amount_staff_categories(from_date,to_date)
    #this below method to check the Employee have assigned shift assignment and marked in attendance..
    mark_assigned_shift(from_date,to_date)
    #this below method to mark the IN time Based on which shift will comes the actual Shift
    mark_attended_shift(from_date,to_date)
    #the below method to mark the assigned shift and actual shift matched or not,not matched employees mark as absent
    mark_status_as_absent(from_date,to_date)
    # #the below method if an employee comes in week-off or Holiday Days that day Present
    mark_attendance_as_present_mark_holiday(from_date,to_date)
    # #the below method employee week-off and holiday date attendance moved to Holiday Attendance Doctype
    check_holiday_moved_to_holiday_attendance(from_date,to_date)
    # #th below method Employee status mark as Half Day the Late Hours,Late Deduct,Late HR will be Empty
    make_late_hours_empty(from_date,to_date)
    mark_late_entry(from_date, to_date)

    return "Completed" 


@frappe.whitelist()
def mark_att_for_att_setting(from_date,to_date):
    checkins = frappe.db.sql("""select name,employee,time,log_type from `tabEmployee Checkin` where date(time) between '%s' and '%s'  order by time   """%(from_date,to_date),as_dict=True)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    mark_absent(from_date,to_date)
    mark_wh_ot_new(from_date,to_date)
    # mark_incentive_amount_staff_categories(from_date,to_date)
    mark_assigned_shift(from_date,to_date)
    mark_attended_shift(from_date,to_date)
    mark_status_as_absent(from_date,to_date)
    mark_attendance_as_present_mark_holiday(from_date,to_date)
    check_holiday_moved_to_holiday_attendance(from_date,to_date)
    make_late_hours_empty(from_date,to_date)
    mark_late_entry(from_date, to_date)
    
    
    return "Completed"

@frappe.whitelist()
def run_attendance_process(from_date, to_date):
    frappe.enqueue(
        "infac.shift_attendance.mark_att_for_att_setting",
        queue="long",
        timeout=6000,
        from_date=from_date,
        to_date=to_date
    )

    return "Queued"

@frappe.whitelist()
def mark_att_for_att_setting_emp(from_date,to_date,employee):
    checkins = frappe.db.sql("""select name,employee,time,log_type from `tabEmployee Checkin` where date(time) between '%s' and '%s' and employee='%s'  order by time   """%(from_date,to_date,employee),as_dict=True)
    for c in checkins:
        employee_exsits = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee_exsits:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
            # mark_attendance_from_checkin_att_sett(c.name,c.employee,c.time,c.log_type)
    mark_absent_with_emp(from_date,to_date,employee)
    mark_wh_ot_with_emp(from_date,to_date,employee)
    mark_incentive_amount_staff_categories_emp(from_date,to_date,employee)
    mark_assigned_shift_emp(from_date,to_date,employee)
    mark_attended_shift_emp(from_date,to_date,employee)
    mark_status_as_absent_emp(from_date,to_date,employee)
    mark_attendance_as_present_mark_holiday_emp(from_date,to_date,employee)
    check_holiday_moved_to_holiday_attendance_emp(from_date,to_date,employee)
    make_late_hours_empty_emp(from_date,to_date,employee)
    mark_late_entry_emp(from_date, to_date, employee)
    return "Completed"


@frappe.whitelist()
def mark_att_for_emp(from_date,to_date,employee):
    checkins = frappe.db.sql("""select name,employee,time,log_type from `tabEmployee Checkin` where date(time) between '%s' and '%s' and employee='%s'  order by time   """%(from_date,to_date,employee),as_dict=True)
    for c in checkins:
        employee_exsits = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee_exsits:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
            # mark_attendance_from_checkin_att_sett(c.name,c.employee,c.time,c.log_type)
    mark_absent_with_emp(from_date,to_date,employee)
    mark_wh_ot_with_emp(from_date,to_date,employee)
    mark_incentive_amount_staff_categories_emp(from_date,to_date,employee)
    mark_assigned_shift_emp(from_date,to_date,employee)
    mark_attended_shift_emp(from_date,to_date,employee)
    mark_status_as_absent_emp(from_date,to_date,employee)
    mark_attendance_as_present_mark_holiday_emp(from_date,to_date,employee)
    check_holiday_moved_to_holiday_attendance_emp(from_date,to_date,employee)
    make_late_hours_empty_emp(from_date,to_date,employee)
    mark_late_entry_emp(from_date, to_date, employee)
    return "Completed"

@frappe.whitelist()
def mark_att_with_emp_manual():
    from_date ="2026-04-09"
    to_date ="2026-04-09"
    employee="TT0199"
    checkins = frappe.db.sql("""select name,employee,time,log_type from `tabEmployee Checkin` where date(time) between '%s' and '%s' and employee='%s'  order by time   """%(from_date,to_date,employee),as_dict=True)
    for c in checkins:
        employee_exsits = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee_exsits:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
            # mark_attendance_from_checkin_att_sett(c.name,c.employee,c.time,c.log_type)
    mark_absent_with_emp(from_date,to_date,employee)
    mark_wh_ot_with_emp(from_date,to_date,employee)
    mark_incentive_amount_staff_categories_emp(from_date,to_date,employee)
    mark_assigned_shift_emp(from_date,to_date,employee)
    mark_attended_shift_emp(from_date,to_date,employee)
    mark_status_as_absent_emp(from_date,to_date,employee)
    mark_attendance_as_present_mark_holiday_emp(from_date,to_date,employee)
    check_holiday_moved_to_holiday_attendance_emp(from_date,to_date,employee)
    make_late_hours_empty_emp(from_date,to_date,employee)
    mark_late_entry_emp(from_date, to_date, employee)
    return "Completed"

def mark_att1():
    from_date = add_days(today(),-2)
    to_date = today()
    checkins = frappe.db.sql("""select name,employee,time,log_type from `tabEmployee Checkin` where date(time) between '%s' and '%s'  order by time   """%(from_date,to_date),as_dict=True)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    mark_absent(from_date,to_date)
    mark_wh_ot_new(from_date,to_date)
    mark_incentive_amount_staff_categories(from_date,to_date)
    mark_assigned_shift(from_date,to_date)
    mark_attended_shift(from_date,to_date)
    mark_status_as_absent(from_date,to_date)
    mark_attendance_as_present_mark_holiday(from_date,to_date)
    check_holiday_moved_to_holiday_attendance(from_date,to_date)
    make_late_hours_empty(from_date,to_date)
    mark_late_entry(from_date, to_date)


# @frappe.whitelist()  
# def mark_attendance_from_checkin(checkin,employee,time,log_type):
#     att_time = time.time()
#     att_date = time.date()
#     if log_type=='IN':
#         checkins = frappe.db.sql("""select time,name from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s'  order by time ASC """%(employee,att_date),as_dict=True)
#         if checkins:
#             att = frappe.db.exists('Attendance',{"employee":employee,'attendance_date':att_date,'docstatus':['!=','2']})   
#             if not att:
#                 att = frappe.new_doc("Attendance")
#                 att.employee = employee
#                 att.attendance_date = att_date
#                 att.shift = get_actual_shift_start(get_time(checkins[0].time))
#                 att.actual_shift= get_actual_shift_start(get_time(checkins[0].time))
#                 att.status = 'Absent'
#                 att.in_time = checkins[0].time
#                 att.total_wh = '00:00'
#                 att.late_hours = '00:00'
#                 att.extra_hours = '00:00'
#                 permission_request = frappe.db.get_value("Permission Request",{"employee_id": employee,"permission_date": att_date,"docstatus": 1},"name")
#                 if permission_request:
#                     att.permission_request = permission_request
#                 att.save(ignore_permissions=True)
#                 frappe.db.commit()
#                 for c in checkins:
#                     frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
#                     frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
#                 return att  
#             else:
#                 att = frappe.get_doc("Attendance",att)
#                 if att.docstatus == 0:
#                     att.in_time =checkins[0]['time']
                    
#                     # if not att.shift:
#                     att.shift = get_actual_shift_start(get_time(checkins[0]['time']))
#                     att.actual_shift=get_actual_shift_start(get_time(checkins[0]['time']))
#                     print('att')
#                     print(att)
#                     att.save(ignore_permissions=True)
#                     frappe.db.commit()
#                     for c in checkins:
#                         frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
#                         frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
#                     return att 
    
#     if log_type == 'OUT':
#         if get_time(att_time) < datetime.strptime('12:00', '%H:%M').time():
#             max_out = datetime.strptime('12:00', '%H:%M').time()
#             checkins = frappe.db.sql("""
#                 SELECT time,name FROM `tabEmployee Checkin`
#                 WHERE employee = %s
#                 AND log_type = 'OUT'
#                 AND DATE(time) = %s
#                 AND TIME(time) < %s
#                 ORDER BY time ASC
#             """, (employee, att_date, max_out), as_dict=True)

#             if checkins:
#                 current_day_in = frappe.db.sql("""SELECT time,name,employee FROM `tabEmployee Checkin` WHERE employee = %s AND log_type = 'IN' AND DATE(time) = %s AND TIME(time) < %s ORDER BY time ASC """, (employee, att_date, checkins[-1]['time']), as_dict=True)
#                 if current_day_in:
#                     if frappe.db.exists('Attendance', {'employee': employee, 'attendance_date': att_date, 'docstatus': ('!=', 2)}):
#                         att = frappe.get_doc('Attendance', {'employee': employee, 'attendance_date': att_date, 'docstatus': ('!=', 2)})
#                         if att.in_time:
#                             if checkins[-1]['time'] < att.in_time:
#                                 return
#                             if att.in_time < checkins[-1]['time']:
#                                 att.out_time = checkins[-1]['time']
#                                 if not att.shift:
#                                     att.shift = get_actual_shift(get_time(checkins[-1].time))
#                                     att.actual_shift= get_actual_shift(get_time(checkins[-1].time))
#                                 else:
#                                     att.actual_shift=att.shift
#                         else:
#                             att.out_time = checkins[-1]['time']
#                             if not att.shift:
#                                 att.shift = get_actual_shift(get_time(checkins[-1].time))
#                                 att.actual_shift=get_actual_shift(get_time(checkins[-1].time))
#                             else:
#                                 att.actual_shift=att.shift
#                         att.save(ignore_permissions=True)
#                         frappe.db.commit()
#                     else:
#                         att = frappe.new_doc("Attendance")
#                         att.employee = employee
#                         att.attendance_date = att_date
#                         if not att.shift:
#                             att.shift = get_actual_shift(get_time(checkins[0].time))
#                             att.actual_shift=get_actual_shift(get_time(checkins[0].time))
#                         else:
#                             att.actual_shift=att.shift
#                         att.status = 'Absent'
#                         att.out_time = checkins[-1].time
#                         att.total_wh = '00:00'
#                         att.late_hours = '00:00'
#                         att.extra_hours = '00:00'
#                         permission_request = frappe.db.get_value("Permission Request",{"employee_id": employee,"permission_date": att_date,"docstatus": 1},"name")
#                         if permission_request:
#                             att.permission_request = permission_request
#                         att.save(ignore_permissions=True)
#                         frappe.db.commit()
#                         for c in checkins:
#                             frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
#                             frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
#                         return att  
                        
#                 else:
#                     yesterday = add_days(att_date, -1)
#                     if frappe.db.exists('Attendance', {'employee': employee, 'attendance_date': yesterday, 'docstatus': ('!=', 2)}):
#                         att = frappe.get_doc('Attendance', {'employee': employee, 'attendance_date': yesterday, 'docstatus': ('!=', 2)})
#                         if att.shift in ['C','B']:
#                             if att.in_time:
#                                 if att.in_time < checkins[-1]['time']:
#                                     att.status = 'Absent'
#                                     att.out_time = checkins[-1]['time']
#                                     att.total_wh = '00:00'
#                                     att.late_hours = '00:00'
#                                     att.extra_hours = '00:00'
#                                     print(att.name)
#                                     print(att.employee)
#                                     print(att.attendance_date)
#                                     att.save(ignore_permissions=True)
#                                     frappe.db.commit()
        
#         else:
#             checkins = frappe.db.sql("""select time,name from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s'  order by time ASC """%(employee,att_date),as_dict=True)
#             if checkins:
#                 att = frappe.db.exists('Attendance',{"employee":employee,'attendance_date':att_date,'docstatus':['!=','2']})   
#                 if not att:
#                     att = frappe.new_doc("Attendance")
#                     att.employee = employee
#                     att.attendance_date = att_date
#                     if not att.shift:
#                         att.shift = get_actual_shift(get_time(checkins[-1].time))
#                         att.actual_shift=get_actual_shift(get_time(checkins[-1].time))
#                     else:
#                         att.actual_shift=att.shift
#                     att.status = 'Absent'
#                     att.out_time = checkins[-1].time
#                     att.total_wh = '00:00'
#                     att.late_hours = '00:00'
#                     att.extra_hours = '00:00'
#                     permission_request = frappe.db.get_value("Permission Request",{"employee_id": employee,"permission_date": att_date,"docstatus": 1},"name")
#                     if permission_request:
#                         att.permission_request = permission_request
#                     att.save(ignore_permissions=True)
#                     frappe.db.commit()
#                     for c in checkins:
#                         frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
#                         frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
#                     return att  
#                 else:
#                     att = frappe.get_doc("Attendance",att)
#                     if att.docstatus == 0:
#                         att.out_time =checkins[-1]['time']
#                         if not att.shift:
#                             att.shift = get_actual_shift(get_time(checkins[-1]['time']))
#                             att.actual_shift=get_actual_shift(get_time(checkins[-1]['time']))
#                         else:
#                             att.actual_shift=att.shift
#                         att.save(ignore_permissions=True)
#                         frappe.db.commit()
#                         for c in checkins:
#                             frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
#                             frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
#                         return att 

#     # if log_type == 'OUT':
#     #     if get_time(att_time) < datetime.strptime('12:00', '%H:%M').time():
#     #         max_out = datetime.strptime('12:00', '%H:%M').time()
#     #         checkins = frappe.db.sql("""
#     #             SELECT time,name FROM `tabEmployee Checkin`
#     #             WHERE employee = %s
#     #             AND log_type = 'OUT'
#     #             AND DATE(time) = %s
#     #             AND TIME(time) < %s
#     #             ORDER BY time ASC
#     #         """, (employee, att_date, max_out), as_dict=True)

#     #         if checkins:
#     #             current_day_in = frappe.db.sql("""SELECT time,name,employee FROM `tabEmployee Checkin` WHERE employee = %s AND log_type = 'IN' AND DATE(time) = %s AND TIME(time) < %s ORDER BY time ASC """, (employee, att_date, checkins[-1]['time']), as_dict=True)
#     #             if current_day_in:
#     #                 if frappe.db.exists('Attendance', {'employee': employee, 'attendance_date': att_date, 'docstatus': ('!=', 2)}):
#     #                     att = frappe.get_doc('Attendance', {'employee': employee, 'attendance_date': att_date, 'docstatus': ('!=', 2)})
#     #                     if att.in_time:
#     #                         if checkins[-1]['time'] > att.in_time:
#     #                             if att.in_time < checkins[-1]['time']:
#     #                                 att.out_time = checkins[-1]['time']
#     #                                 if not att.shift:
#     #                                     att.shift = get_actual_shift(get_time(checkins[-1].time))
#     #                                     att.actual_shift= get_actual_shift(get_time(checkins[-1].time))
#     #                                 else:
#     #                                     att.actual_shift=att.shift
#     #                         else:
#     #                             frappe.logger().info(f"Skipped OUT {checkins[-1]['time']} <= IN {att.in_time} for {employee}")
#     #                     else:
#     #                         att.out_time = checkins[-1]['time']
#     #                         if not att.shift:
#     #                             att.shift = get_actual_shift(get_time(checkins[-1].time))
#     #                             att.actual_shift=get_actual_shift(get_time(checkins[-1].time))
#     #                         else:
#     #                             att.actual_shift=att.shift
#     #                     att.save(ignore_permissions=True)
#     #                     frappe.db.commit()
#     #                 else:
#     #                     att = frappe.new_doc("Attendance")
#     #                     att.employee = employee
#     #                     att.attendance_date = att_date
#     #                     if not att.shift:
#     #                         att.shift = get_actual_shift(get_time(checkins[0].time))
#     #                         att.actual_shift=get_actual_shift(get_time(checkins[0].time))
#     #                     else:
#     #                         att.actual_shift=att.shift
#     #                     att.status = 'Absent'
#     #                     att.out_time = checkins[-1]['time']
#     #                     att.total_wh = '00:00'
#     #                     att.late_hours = '00:00'
#     #                     att.extra_hours = '00:00'
#     #                     att.save(ignore_permissions=True)
#     #                     frappe.db.commit()
#     #                     for c in checkins:
#     #                         frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
#     #                         frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
#     #                     return att  
                            
#     #             else:
#     #                 yesterday = add_days(att_date, -1)
#     #                 if frappe.db.exists('Attendance', {'employee': employee, 'attendance_date': yesterday, 'docstatus': ('!=', 2)}):
#     #                     att = frappe.get_doc('Attendance', {'employee': employee, 'attendance_date': yesterday, 'docstatus': ('!=', 2)})
#     #                     if att.shift in ['C','B']:
#     #                         if att.in_time:
#     #                             if checkins[-1]['time'] > att.in_time:
#     #                                 att.status = 'Absent'
#     #                                 att.out_time = checkins[-1]['time']
#     #                                 att.total_wh = '00:00'
#     #                                 att.late_hours = '00:00'
#     #                                 att.extra_hours = '00:00'
#     #                                 print(att.name)
#     #                                 att.save(ignore_permissions=True)
#     #                                 frappe.db.commit()
            
#     # else:
#     #     checkins = frappe.db.sql("""select time,name from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s'  order by time ASC """%(employee,att_date),as_dict=True)
#     #     if checkins:
#     #         att = frappe.db.exists('Attendance',{"employee":employee,'attendance_date':att_date,'docstatus':['!=','2']})   
#     #         if not att:
#     #             att = frappe.new_doc("Attendance")
#     #             att.employee = employee
#     #             att.attendance_date = att_date
#     #             if not att.shift:
#     #                 att.shift = get_actual_shift(get_time(checkins[-1].time))
#     #                 att.actual_shift=get_actual_shift(get_time(checkins[-1].time))
#     #             else:
#     #                 att.actual_shift=att.shift
#     #             att.status = 'Absent'
#     #             att.out_time = checkins[-1].time
#     #             att.total_wh = '00:00'
#     #             att.late_hours = '00:00'
#     #             att.extra_hours = '00:00'
#     #             att.save(ignore_permissions=True)
#     #             frappe.db.commit()
#     #             for c in checkins:
#     #                 frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
#     #                 frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
#     #             return att  
#     #         else:
#     #             att = frappe.get_doc("Attendance",att)
#     #             if att.docstatus == 0:
#     #                 # ✅ final fix check here
#     #                 if att.in_time and checkins[-1]['time'] <= att.in_time:
#     #                     frappe.logger().info(f"Skipped OUT {checkins[-1]['time']} <= IN {att.in_time} for {employee}")
#     #                 else:
#     #                     att.out_time =checkins[-1]['time']
#     #                     if not att.shift:
#     #                         att.shift = get_actual_shift(get_time(checkins[-1]['time']))
#     #                         att.actual_shift=get_actual_shift(get_time(checkins[-1]['time']))
#     #                     else:
#     #                         att.actual_shift=att.shift
#     #                     att.save(ignore_permissions=True)
#     #                     frappe.db.commit()
#     #                     for c in checkins:
#     #                         frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
#     #                         frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
#     #                     return att  


@frappe.whitelist()
def mark_attendance_from_checkin_att_sett(checkin, employee, time, log_type):

    att_time = time.time()
    att_date = time.date()

    # ✅ Common validation
    def is_valid_punch(in_time, out_time):
        if in_time and out_time:
            return out_time > in_time
        return True

    # =========================================================
    # 🔹 IN LOGIC
    # =========================================================
    if log_type == 'IN':
        checkins = frappe.db.sql("""
            SELECT time, name 
            FROM `tabEmployee Checkin`
            WHERE employee = %s 
            AND log_type = 'IN' 
            AND DATE(time) = %s
            ORDER BY time ASC
        """, (employee, att_date), as_dict=True)

        if not checkins:
            return

        first_in = checkins[0]['time']

        att_name = frappe.db.exists('Attendance', {
            "employee": employee,
            "attendance_date": att_date,
            "docstatus": ['!=', 2]
        })

        # 🔹 Create Attendance
        if not att_name:
            att = frappe.new_doc("Attendance")
            att.employee = employee
            att.attendance_date = att_date
            att.shift = get_actual_shift_start(get_time(first_in))
            att.actual_shift = att.shift
            att.status = 'Absent'

            # ✅ Validate IN vs OUT
            if att.out_time and first_in >= att.out_time:
                return

            att.in_time = first_in

        # 🔹 Update Attendance
        else:
            att = frappe.get_doc("Attendance", att_name)

            if att.docstatus != 0:
                return

            # ✅ Validate
            if att.out_time and first_in >= att.out_time:
                frappe.errprint("Invalid IN Time")
                return

            att.in_time = first_in

            if not att.shift:
                att.shift = get_actual_shift_start(get_time(first_in))
                att.actual_shift = att.shift

        # Common fields
        att.total_wh = '00:00'
        att.late_hours = '00:00'
        att.extra_hours = '00:00'

        permission_request = frappe.db.get_value(
            "Permission Request",
            {"employee_id": employee, "permission_date": att_date, "docstatus": 1},
            "name"
        )
        if permission_request:
            att.permission_request = permission_request

        att.save(ignore_permissions=True)
        frappe.db.commit()

        # Link checkins
        for c in checkins:
            frappe.db.set_value('Employee Checkin', c.name, {
                'skip_auto_attendance': 1,
                'attendance': att.name
            })

        return att

    # =========================================================
    # 🔹 OUT LOGIC
    # =========================================================
    if log_type == 'OUT':

        checkins = frappe.db.sql("""
            SELECT time, name 
            FROM `tabEmployee Checkin`
            WHERE employee = %s 
            AND log_type = 'OUT'
            AND DATE(time) = %s
            ORDER BY time ASC
        """, (employee, att_date), as_dict=True)

        if not checkins:
            return

        last_out = checkins[-1]['time']

        att_name = frappe.db.exists('Attendance', {
            "employee": employee,
            "attendance_date": att_date,
            "docstatus": ['!=', 2]
        })

        # 🔹 Create Attendance
        if not att_name:
            att = frappe.new_doc("Attendance")
            att.employee = employee
            att.attendance_date = att_date
            att.shift = get_actual_shift(get_time(last_out))
            att.actual_shift = att.shift
            att.status = 'Absent'

            # ✅ Prevent invalid OUT (no IN exists yet → allow)
            att.out_time = last_out

        # 🔹 Update Attendance
        else:
            att = frappe.get_doc("Attendance", att_name)

            if att.docstatus != 0:
                return

            # ✅ STRICT VALIDATION
            if att.in_time and last_out <= att.in_time:
                frappe.errprint("Invalid OUT Time")
                return

            att.out_time = last_out

            if not att.shift:
                att.shift = get_actual_shift(get_time(last_out))
                att.actual_shift = att.shift

        # Common fields
        att.total_wh = '00:00'
        att.late_hours = '00:00'
        att.extra_hours = '00:00'

        permission_request = frappe.db.get_value(
            "Permission Request",
            {"employee_id": employee, "permission_date": att_date, "docstatus": 1},
            "name"
        )
        if permission_request:
            att.permission_request = permission_request

        att.save(ignore_permissions=True)
        frappe.db.commit()

        # Link checkins
        for c in checkins:
            frappe.db.set_value('Employee Checkin', c.name, {
                'skip_auto_attendance': 1,
                'attendance': att.name
            })

        return att
    

@frappe.whitelist()  
def mark_attendance_from_checkin(checkin,employee,time,log_type):
    frappe.errprint("HI Checkin")
    att_time = time.time()
    att_date = time.date()
    if log_type=='IN':
        checkins = frappe.db.sql("""select time,name from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s'  order by time ASC """%(employee,att_date),as_dict=True)
        if checkins:
            att = frappe.db.exists('Attendance',{"employee":employee,'attendance_date':att_date,'docstatus':['!=','2']})   
            if not att:
                att = frappe.new_doc("Attendance")
                att.employee = employee
                att.attendance_date = att_date
                att.shift = get_actual_shift_start(get_time(checkins[0].time))
                att.actual_shift= get_actual_shift_start(get_time(checkins[0].time))
                att.status = 'Absent'
                # att.in_time = checkins[0].time
                in_time = checkins[0]['time']

                if att.out_time:
                    if in_time >= att.out_time:
                        # frappe.errprint("Invalid IN Time: Later than OUT Time")
                        return

                att.in_time = in_time
                att.total_wh = '00:00'
                att.late_hours = '00:00'
                att.extra_hours = '00:00'
                permission_request = frappe.db.get_value("Permission Request",{"employee_id": employee,"permission_date": att_date,"docstatus": 1},"name")
                if permission_request:
                    att.permission_request = permission_request
                att.save(ignore_permissions=True)
                frappe.db.commit()
                for c in checkins:
                    frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
                    frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
                return att  
            else:
                att = frappe.get_doc("Attendance",att)
                if att.docstatus == 0:
                    att.in_time =checkins[0]['time']
                    
                    # if not att.shift:
                    att.shift = get_actual_shift_start(get_time(checkins[0]['time']))
                    att.actual_shift=get_actual_shift_start(get_time(checkins[0]['time']))
                    print('att')
                    print(att)
                    print(att.employee)
                    print(att.attendance_date)
                    att.save(ignore_permissions=True)
                    frappe.db.commit()
                    for c in checkins:
                        frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
                        frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
                    return att 
    
    if log_type == 'OUT':
        if get_time(att_time) < datetime.strptime('12:00', '%H:%M').time():
            max_out = datetime.strptime('12:00', '%H:%M').time()
            checkins = frappe.db.sql("""
                SELECT time,name FROM `tabEmployee Checkin`
                WHERE employee = %s
                AND log_type = 'OUT'
                AND DATE(time) = %s
                AND TIME(time) < %s
                ORDER BY time ASC
            """, (employee, att_date, max_out), as_dict=True)

            if checkins:
                current_day_in = frappe.db.sql("""SELECT time,name,employee FROM `tabEmployee Checkin` WHERE employee = %s AND log_type = 'IN' AND DATE(time) = %s AND TIME(time) < %s ORDER BY time ASC """, (employee, att_date, checkins[-1]['time']), as_dict=True)
                if current_day_in:
                    if frappe.db.exists('Attendance', {'employee': employee, 'attendance_date': att_date, 'docstatus': ('!=', 2)}):
                        att = frappe.get_doc('Attendance', {'employee': employee, 'attendance_date': att_date, 'docstatus': ('!=', 2)})
                        if att.in_time:
                            if checkins[-1]['time'] < att.in_time:
                                return
                            # if att.in_time:
                            #     out_time = checkins[-1]['time']

                            #     if out_time <= att.in_time:
                            #         frappe.errprint("Invalid OUT Time")
                            #         return

                            #     att.out_time = out_time

                            if att.in_time < checkins[-1]['time']:
                                frappe.errprint("check")
                                att.out_time = checkins[-1]['time']
                                if not att.shift:
                                    att.shift = get_actual_shift(get_time(checkins[-1].time))
                                    att.actual_shift= get_actual_shift(get_time(checkins[-1].time))
                                else:
                                    att.actual_shift=att.shift
                        else:
                            frappe.errprint("check 2")
                            att.out_time = checkins[-1]['time']
                            if not att.shift:
                                att.shift = get_actual_shift(get_time(checkins[-1].time))
                                att.actual_shift=get_actual_shift(get_time(checkins[-1].time))
                            else:
                                att.actual_shift=att.shift
                        att.save(ignore_permissions=True)
                        frappe.db.commit()
                    else:
                        att = frappe.new_doc("Attendance")
                        att.employee = employee
                        att.attendance_date = att_date
                        if not att.shift:
                            att.shift = get_actual_shift(get_time(checkins[0].time))
                            att.actual_shift=get_actual_shift(get_time(checkins[0].time))
                        else:
                            att.actual_shift=att.shift
                        att.status = 'Absent'
                        att.out_time = checkins[-1].time
                        # out_time = checkins[-1]['time']

                        # frappe.errprint(f"IN TIME: {att.in_time}")
                        # frappe.errprint(f"OUT TIME: {out_time}")

                        # if att.in_time:
                        #     if out_time <= att.in_time:
                        #         frappe.errprint("OUT punch earlier than IN. Ignoring.")
                        #         return

                        #     if (out_time - att.in_time) <= timedelta(seconds=30):
                        #         frappe.errprint("OUT punch within 30s of IN. Ignoring.")
                        #         return

                        # att.out_time = out_time
                        att.total_wh = '00:00'
                        att.late_hours = '00:00'
                        att.extra_hours = '00:00'
                        permission_request = frappe.db.get_value("Permission Request",{"employee_id": employee,"permission_date": att_date,"docstatus": 1},"name")
                        if permission_request:
                            att.permission_request = permission_request
                        att.save(ignore_permissions=True)
                        frappe.db.commit()
                        for c in checkins:
                            frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
                            frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
                        return att  
                        
                else:
                    yesterday = add_days(att_date, -1)
                    if frappe.db.exists('Attendance', {'employee': employee, 'attendance_date': yesterday, 'docstatus': ('!=', 2)}):
                        att = frappe.get_doc('Attendance', {'employee': employee, 'attendance_date': yesterday, 'docstatus': ('!=', 2)})
                        if att.shift in ['C','B']:
                            if att.in_time:
                                if att.in_time < checkins[-1]['time']:
                                    att.status = 'Absent'
                                    att.out_time = checkins[-1]['time']
                                    att.total_wh = '00:00'
                                    att.late_hours = '00:00'
                                    att.extra_hours = '00:00'
                                    print(att.name)
                                    print(att.employee)
                                    print(att.attendance_date)
                                    att.save(ignore_permissions=True)
                                    frappe.db.commit()
        
        else:
            print("1")
            checkins = frappe.db.sql("""select time,name from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s'  order by time ASC """%(employee,att_date),as_dict=True)
            if checkins:
                att = frappe.db.exists('Attendance',{"employee":employee,'attendance_date':att_date,'docstatus':['!=','2']})   
                if not att:
                    att = frappe.new_doc("Attendance")
                    att.employee = employee
                    att.attendance_date = att_date
                    if not att.shift:
                        att.shift = get_actual_shift(get_time(checkins[-1].time))
                        att.actual_shift=get_actual_shift(get_time(checkins[-1].time))
                    else:
                        att.actual_shift=att.shift
                    att.status = 'Absent'
                    att.out_time = checkins[-1].time
                    att.total_wh = '00:00'
                    att.late_hours = '00:00'
                    att.extra_hours = '00:00'
                    permission_request = frappe.db.get_value("Permission Request",{"employee_id": employee,"permission_date": att_date,"docstatus": 1},"name")
                    if permission_request:
                        att.permission_request = permission_request
                    att.save(ignore_permissions=True)
                    frappe.db.commit()
                    for c in checkins:
                        frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
                        frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
                    return att  
                else:
                    att = frappe.get_doc("Attendance",att)
                    if att.docstatus == 0:
                        print("12")
                        att.out_time =checkins[-1]['time']
                        # if att.in_time and out_time <= att.in_time:
                        #     att.out_time = ""
                        #     print(att.out_time , "1")
                        #     att.total_wh = '00:00'
                        #     # att.save(ignore_permissions=True)
                        # else:
                        #     att.out_time = out_time 
                        #     print(att.out_time , "2")
                        print(att.in_time)
                        print(att.out_time)
                        if not att.shift:
                            print("HI")
                            att.shift = get_actual_shift(get_time(checkins[-1]['time']))
                            att.actual_shift=get_actual_shift(get_time(checkins[-1]['time']))
                        else:
                            print("HI1")
                            att.actual_shift=att.shift
                        print(att.employee)
                        print(att.attendance_date)
                        print("HH")    
                        att.save(ignore_permissions=True)
                        print('att')
                        print(att)
                        print(att.employee)
                        print(att.attendance_date)
                        frappe.db.commit()
                        for c in checkins:
                            frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
                            frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
                        return att 

    
@frappe.whitelist()    
def mark_absent(from_date,to_date):
    print("hello")
    from_date = add_days(today(),-2)
    if to_date == today():
        to_date = add_days(to_date,-1)
    no_of_days = date_diff(add_days(to_date, 1),from_date )
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    for date in dates:
        employee = frappe.db.get_all('Employee',{'status':'Active','date_of_joining':['<=',from_date]})
        for emp in employee:
            hh = check_holiday(date,emp.name)
            if not hh:
                on_duty = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')},['on_duty_marked'])
                if not on_duty:
                    if not frappe.db.exists('Attendance',{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')}):
                        att = frappe.new_doc('Attendance')
                        att.employee = emp.name
                        att.status = 'Absent'
                        att.attendance_date = date
                        att.total_wh = '00:00:00'
                        att.extra_hours = '00:00:00'
                        att.late_hours ='00:00:00'
                        att.save(ignore_permissions=True)
                        frappe.db.commit()
            

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
def enqueue_mark_att(from_date,to_date):
    enqueue(mark_incentive_amount_staff_categories, queue='default',timeout=6000, event='ot_incentive',from_date=from_date,to_date=to_date)

@frappe.whitelist()
def mark_incentive_amount_staff_categories(from_date,to_date):
    employee = frappe.db.get_all('Employee',{'Status':'Active','incentive_category':'Yes'},['name'])
    for emp in employee:
        attendance = frappe.db.sql(""" select ot_hrs,name from `tabAttendance` where attendance_date between '%s' and '%s' and employee = '%s' and docstatus != '2'  """%(from_date,to_date,emp.name),as_dict=True)
        for att in attendance:
            e_slap_ot_start = frappe.db.get_single_value('Attendance Settings','e_slap_ot_start')
            t_slap_ot_start = frappe.db.get_single_value('Attendance Settings','t_slap_ot_start')
            m_slap_ot_start = frappe.db.get_single_value('Attendance Settings','m_slap_ot_start')
            e_slap_ot_end = frappe.db.get_single_value('Attendance Settings','e_slap_ot_end')
            t_slap_ot_end = frappe.db.get_single_value('Attendance Settings','t_slap_ot_end')
            m_slap_ot_end = frappe.db.get_single_value('Attendance Settings','m_slap_ot_end')

            if att.ot_hrs >= e_slap_ot_start and att.ot_hrs < e_slap_ot_end:
                frappe.db.set_value('Attendance',att.name,'e_slap_ot_hrs',att.ot_hrs)
                e_slap_amount = frappe.db.get_single_value('Attendance Settings','e_slap_ot_incentive_amount')
                frappe.db.set_value('Attendance',att.name,'e_slap_incentive_amount',e_slap_amount)
            elif att.ot_hrs >= t_slap_ot_start and att.ot_hrs < t_slap_ot_end:
                frappe.db.set_value('Attendance',att.name,'t_slap_ot_hrs',att.ot_hrs)
                t_slap_amount = frappe.db.get_single_value('Attendance Settings','t_slap_ot_incentive_amount')
                frappe.db.set_value('Attendance',att.name,'t_slap_incentive_amount',t_slap_amount)
            elif att.ot_hrs > m_slap_ot_start:   
                frappe.db.set_value('Attendance',att.name,'m_slap_ot_hrs',att.ot_hrs)
                m_slap_amount = frappe.db.get_single_value('Attendance Settings','m_slap_ot_incentive_amount')
                frappe.db.set_value('Attendance',att.name,'m_slap_incentive_amount',m_slap_amount)
    return "OT Updated"        
                
def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time >= time_range[0] or time <= time_range[1]
    return time_range[0] <= time <= time_range[1]

def get_actual_shift(get_shift_time):
    from datetime import datetime
    from datetime import date, timedelta,time
    nowtime = datetime.now()
    shift_A_time = [time(hour=5, minute=0, second=0),time(hour=7, minute=30, second=0)]
    shift_G_time = [time(hour=7, minute=31, second=0),time(hour=12, minute=00, second=0)]
    shift_B_time = [time(hour=13, minute=00, second=0),time(hour=18, minute=30, second=0)]
    shift_C_time = [time(hour=20, minute=0, second=1),time(hour=23, minute=59, second=0)]
    shift = ''
    if is_between(get_shift_time,shift_A_time):
        shift = 'A'
    if is_between(get_shift_time,shift_G_time):
        shift = 'G'
    if is_between(get_shift_time,shift_B_time):
        shift = 'B'
    if is_between(get_shift_time,shift_C_time):
        shift = 'C'
    return shift    

def get_employees_attendance(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    return attendance

def mark_assigned_shift(from_date,to_date):
    get_attendance = get_employees_attendance(from_date,to_date)
    for att in get_attendance:
        if not att.attendance_regularize:
            shift = frappe.db.exists('Shift Assignment',{'start_date':att.attendance_date,'employee':att.employee,'docstatus':('!=','2')})
            if shift:
                get_shift = frappe.db.get_value('Shift Assignment',{'start_date':att.attendance_date,'employee':att.employee,'docstatus':('!=','2')},['shift_type'])
                get_shift_start_time = frappe.db.get_value('Shift Type',{'name':get_shift},['start_time'])
                get_shift_end_time = frappe.db.get_value('Shift Type',{'name':get_shift},['end_time'])
                frappe.db.set_value('Attendance',att.name,'shift_type',get_shift)
                frappe.db.set_value('Attendance',att.name,'shift_in_time',get_shift_start_time)
                frappe.db.set_value('Attendance',att.name,'shift_out_time',get_shift_end_time)
            else:
                get_shift_start_time = frappe.db.get_value('Shift Type',{'name':"G"},['start_time'])
                get_shift_end_time = frappe.db.get_value('Shift Type',{'name':"G"},['end_time'])
                frappe.db.set_value('Attendance',att.name,'shift_type',"G")
                frappe.db.set_value('Attendance',att.name,'shift_in_time',get_shift_start_time)
                frappe.db.set_value('Attendance',att.name,'shift_out_time',get_shift_end_time)


def mark_status_as_absent(from_date,to_date):
    get_attendance = get_employees_attendance(from_date,to_date)
    for att in get_attendance:
        if not att.leave_application:
            if not att.attendance_regularize:
                if att.actual_shift:
                    if att.shift_type == att.actual_shift:
                        frappe.db.set_value('Attendance',att.name,'matched_status','Matched')
                    else:
                        frappe.db.set_value('Attendance',att.name,'matched_status','Unmatched')
                else:
                    frappe.db.set_value('Attendance',att.name,'matched_status','Unmatched')
    return "Completed"            

def mark_single_punch_as_absent(from_date,to_date):
    get_attendance = get_employees_attendance(from_date,to_date)
    for att in get_attendance:
        if not att.leave_application:
            if not att.attendance_regularize:
                if att.matched_status == 'Matched':
                    if att.in_time and not att.out_time:
                        frappe.db.set_value('Attendance',att.name,'status','Absent') 
                    else:
                        frappe.db.set_value('Attendance',att.name,'status','Present') 
                else:
                    frappe.db.set_value('Attendance',att.name,'status','Absent')      

@frappe.whitelist()
def check_holiday_moved_to_holiday_attendance(from_date,to_date):
    # attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['name'])
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    for a in attendance:
        att=frappe.get_doc('Attendance',a.name)
        if att.in_time and att.out_time:
            hh = check_holiday(att.attendance_date,att.employee)
            if hh:
                hd_att = frappe.db.exists('Holiday Attendance',{'attendance_date':att.attendance_date,'employee':att.employee,'docstatus':('!=','2')})
                if not hd_att:
                    doc = frappe.new_doc('Holiday Attendance')
                    doc.employee = att.employee
                    doc.attendance_date = att.attendance_date
                    doc.status = att.status
                    doc.shift = att.shift
                    doc.in_time = att.in_time
                    doc.out_time = att.out_time
                    doc.total_wh = att.total_wh
                    doc.late_hours = att.late_hours
                    doc.leave_type = att.leave_type
                    doc.leave_application = att.leave_application
                    doc.employee_name = att.employee_name
                    doc.attendance_request = att.attendance_request
                    doc.extra_hours = att.extra_hours
                    doc.ot_hrs = att.ot_hrs
                    doc.late_hrs = att.late_hrs
                    doc.late_deduct = att.late_deduct
                    doc.miss_punch_marked = att.miss_punch_marked
                    doc.on_duty_marked = doc.on_duty_marked 
                    doc.permission_request = att.permission_request
                    doc.single_punch_regularization = att.single_punch_regularization
                    doc.shift_type = att.shift_type
                    doc.shift_in_time = att.shift_in_time
                    doc.shift_out_time = att.shift_out_time
                    doc.actual_shift = att.actual_shift
                    doc.actual_in_time = att.actual_in_time
                    doc.actual_out_time = att.actual_out_time
                    doc.matched_status = att.matched_status
                    doc.attendance_regularize = att.attendance_regularize
                    doc.attendance_name = att.name
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
                frappe.db.sql(""" delete from `tabAttendance` where name = '%s' """%(att.name))    
    return "Holiday Attendance"                

def make_late_hours_empty(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['name','status'])
    for att in attendance:
        if att.status == 'Half Day':
            frappe.db.set_value('Attendance',att.name,'late_hours','00:00')
            frappe.db.set_value('Attendance',att.name,'late_hrs','')
            frappe.db.set_value('Attendance',att.name,'late_deduct','')

def mark_attendance_as_present_mark_holiday(from_date,to_date):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['in_time','attendance_date','out_time','employee','name'])
    if attendance:
        for att in attendance:
            if att.in_time and att.out_time:
                hh = check_holiday(att.attendance_date,att.employee)
                if hh:
                    holiday_att = frappe.get_doc('Attendance',att.name)
                    holiday_att.status = 'Present'
                    holiday_att.shift_type = ''
                    holiday_att.shift_in_time = ''
                    holiday_att.shift_out_time = ''
                    holiday_att.actual_shift = ''
                    holiday_att.actual_in_time = ''
                    holiday_att.actual_out_time = ''
                    holiday_att.matched_status = ''
                    holiday_att.save(ignore_permissions=True)
                    frappe.db.commit()
    else:
        holiday_attendance = frappe.db.get_all('Holiday Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['in_time','attendance_date','out_time','employee','name']) 
        if holiday_attendance:
            for att in holiday_attendance:
                if att.in_time and att.out_time:
                    hh = check_holiday(att.attendance_date,att.employee)
                    if hh:
                        holiday_att = frappe.get_doc('Holiday Attendance',att.name)
                        holiday_att.status = 'Present'
                        holiday_att.shift_type = ''
                        holiday_att.shift_in_time = ''
                        holiday_att.shift_out_time = ''
                        holiday_att.actual_shift = ''
                        holiday_att.actual_in_time = ''
                        holiday_att.actual_out_time = ''
                        holiday_att.matched_status = ''
                        holiday_att.save(ignore_permissions=True)
                        frappe.db.commit()


@frappe.whitelist()
def get_actual_shift_start(get_shift_time):
    shift1 = frappe.db.get_value('Shift Type',{'name':'A'},['checkin_start_time','checkin_end_time'])
    shift2 = frappe.db.get_value('Shift Type',{'name':'B'},['checkin_start_time','checkin_end_time'])
    shift3 = frappe.db.get_value('Shift Type',{'name':'C'},['checkin_start_time','checkin_end_time'])
    shift4 = frappe.db.get_value('Shift Type',{'name':'G'},['checkin_start_time','checkin_end_time'])
    att_time_seconds = get_shift_time.hour * 3600 + get_shift_time.minute * 60 + get_shift_time.second
    shift = ''
    if shift4[0].total_seconds() < att_time_seconds < shift4[1].total_seconds():
        shift = 'G'
    elif (shift1[0].total_seconds() < att_time_seconds < shift1[1].total_seconds()):
        shift = 'A'
    elif shift2[0].total_seconds() < att_time_seconds < shift2[1].total_seconds():
        shift = 'B'
    elif shift3[0].total_seconds() < att_time_seconds < shift3[1].total_seconds():
        shift = 'C'
    
    return shift

@frappe.whitelist()
def get_actual_shift(get_shift_time):
    shift4 = frappe.db.get_value('Shift Type',{'name':'G'},['check_out_start_time','check_out_end_time'])
    shift1 = frappe.db.get_value('Shift Type',{'name':'A'},['check_out_start_time','check_out_end_time'])
    shift2 = frappe.db.get_value('Shift Type',{'name':'B'},['check_out_start_time','check_out_end_time'])
    shift3 = frappe.db.get_value('Shift Type',{'name':'C'},['check_out_start_time','check_out_end_time'])
    
    att_time_seconds = get_shift_time.hour * 3600 + get_shift_time.minute * 60 + get_shift_time.second
    shift = ''
    if shift4[0].total_seconds() < att_time_seconds < shift4[1].total_seconds():
        shift = 'G'
    elif shift1[0].total_seconds() < att_time_seconds < shift1[1].total_seconds():
        shift = 'A'
    elif shift2[0].total_seconds() < att_time_seconds < shift2[1].total_seconds():
        shift = 'B'
    elif shift3[0].total_seconds() < att_time_seconds < shift3[1].total_seconds():
        shift = 'C'
    
    return shift


def get_employees_attendance_settings(from_date,to_date,employee=None):
    if employee:
        attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2'),'employee':employee},['*'])
    else:
        attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['*'])
    return attendance

@frappe.whitelist()    
def mark_absent_with_emp(from_date,to_date,employee):
    no_of_days = date_diff(add_days(to_date, 1),from_date )
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    for date in dates:
        hh = check_holiday(date,employee)
        if not hh:
            on_duty = frappe.db.get_value('Attendance',{'attendance_date':date,'employee':employee,'docstatus':('!=','2')},['on_duty_marked'])
            if not on_duty:
                if not frappe.db.exists('Attendance',{'attendance_date':date,'employee':employee,'docstatus':('!=','2')}):
                    att = frappe.new_doc('Attendance')
                    att.employee = employee
                    att.status = 'Absent'
                    att.attendance_date = date
                    att.total_wh = '00:00:00'
                    att.extra_hours = '00:00:00'
                    att.late_hours ='00:00:00'
                    att.save(ignore_permissions=True)
                    frappe.db.commit()


@frappe.whitelist()                    
def mark_wh_ot_with_emp(from_date,to_date,employee):
    from_date=add_days(from_date,-1)
    frappe.errprint(from_date)
    frappe.errprint(to_date)
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2'),'employee':employee},['name'])
    for a in attendance:
        att=frappe.get_doc('Attendance',a.name)        
        att_status =''
        total_wh = '00:00'
        wh ='00:00'
        late_hr = ''
        late_hour ='00:00'
        late_deduct = ''
        late_entry = 0
        ot_hr = '0'
        extra_hrs = '00:00'

        doj=frappe.db.get_value('Employee',{'name':att.employee},['date_of_joining'])
        if att.attendance_date >= getdate(doj):
            frappe.errprint('Hello')
            in_time=''
            out_time=''
            shift=''
            if att.on_duty_marked:
                frappe.errprint('OD')
                od_doc=frappe.get_doc('On Duty Application',att.on_duty_marked)
                shift=od_doc.shift
                if not att.shift:
                    frappe.db.set_value('Attendance',att.name,'shift',od_doc.shift)
                
                    
                if od_doc.session in ['Full Day', 'First Half']:
                    if od_doc.shift:
                        start = frappe.db.get_value('Shift Type', od_doc.shift, 'start_time')
                        in_time_val = to_time(start)
                        in_time_od = datetime.combine(att.attendance_date, in_time_val)
                        in_time = in_time_od
                        if att.in_time:
                            if att.in_time < in_time:
                                in_time=att.in_time
                        frappe.db.set_value('Attendance',att.name,'in_time',in_time)
                else:
                    if od_doc.shift:
                        start = frappe.db.get_value('Shift Type', od_doc.shift, 'start_time')
                        end = frappe.db.get_value('Shift Type', od_doc.shift, 'end_time')
                        start_time = to_time(start)
                        end_time = to_time(end)
                        start_dt = datetime.combine(att.attendance_date, start_time)
                        if od_doc.shift=='C': 
                            end_dt = datetime.combine(add_days(att.attendance_date,1), end_time)
                        else:
                            end_dt = datetime.combine(att.attendance_date, end_time)
                        if end_dt <= start_dt:
                            end_dt += timedelta(days=1)
                        mid_dt = start_dt + (end_dt - start_dt) / 2
                        in_time = mid_dt
                        if att.in_time:
                            if att.in_time < in_time:
                                in_time=att.in_time
                        frappe.db.set_value('Attendance',att.name,'in_time',in_time)
                if od_doc.session in ['Full Day', 'Second Half']:
                    if od_doc.shift:
                        end = frappe.db.get_value('Shift Type', od_doc.shift, 'end_time')
                        out_time_val = to_time(end)
                        if od_doc.shift=='C': 
                            out_time = datetime.combine(add_days(att.attendance_date,1), out_time_val)
                        else:
                            out_time = datetime.combine((att.attendance_date), out_time_val)
                        if att.out_time:
                            if att.out_time > out_time:
                                out_time=att.out_time
                        frappe.db.set_value('Attendance',att.name,'out_time',out_time)
                else:
                    if od_doc.shift:
                        start = frappe.db.get_value('Shift Type', od_doc.shift, 'start_time')
                        end = frappe.db.get_value('Shift Type', od_doc.shift, 'end_time')
                        start_time = to_time(start)
                        end_time = to_time(end)
                        start_dt = datetime.combine(att.attendance_date, start_time)
                        if od_doc.shift=='C': 
                            end_dt = datetime.combine(add_days(att.attendance_date,1), end_time)
                        else:
                            end_dt = datetime.combine(att.attendance_date, end_time)
                        if end_dt <= start_dt:
                            end_dt += timedelta(days=1)
                        mid_dt = start_dt + (end_dt - start_dt) / 2
                        out_time = mid_dt
                        if att.out_time:
                            if att.out_time > out_time:
                                out_time=att.out_time
                        frappe.db.set_value('Attendance',att.name,'out_time',out_time)
                        
                    
          
            else:
                if att.in_time:
                    in_time=att.in_time
                if att.out_time:
                    out_time=att.out_time
                if att.shift:
                    shift=att.shift
            
            if att.miss_punch_marked:
                miss_p=frappe.get_doc('Miss Punch Application',att.miss_punch_marked)
                frappe.db.set_value('Attendance',att.name,'in_time',miss_p.in_time)
                frappe.db.set_value('Attendance',att.name,'out_time',miss_p.out_time)
                in_time=miss_p.in_time
                out_time=miss_p.out_time
            if att.attendance_regularize:
                att_reg=frappe.get_doc('Attendance Regularize',att.attendance_regularize)
                frappe.db.set_value('Attendance',att.name,'in_time',att_reg.corrected_in)
                frappe.db.set_value('Attendance',att.name,'out_time',att_reg.corrected_out)
                frappe.db.set_value('Attendance',att.name,'shift',att_reg.corrected_shift)
                in_time=att_reg.corrected_in
                out_time=att_reg.corrected_out
                shift=att_reg.corrected_shift
            
    
            if att:
                if in_time and out_time and shift:

                    if out_time < in_time:
                        frappe.log_error(
                            title="Invalid Attendance Time",
                            message=f"OUT time is less than IN time for Attendance {att.name}\nIN: {in_time}\nOUT: {out_time}"
                        )
                        continue
                    # in_time = att.in_time
                    # out_time = att.out_time
                    frappe.errprint("IN/OUT")
                    frappe.errprint(att.attendance_date)
                    if att.permission_request:
                        perm=frappe.get_doc('Permission Request',att.permission_request)
                        in_time_val = to_time(perm.from_time)
                        out_time_val = to_time(perm.to_time)
                        if not att.shift:
                            frappe.db.set_value('Attendance',att.name,'shift',perm.shift)
                        if perm.session=='First Half':
                            perm_in=datetime.combine(perm.permission_date,in_time_val)
                            if perm_in < in_time:
                                in_time=perm_in
                        else:
                            if perm.shift=='C':
                                perm_out=datetime.combine(add_days(perm.permission_date,1),out_time_val)
                            else:
                                perm_out=datetime.combine(perm.permission_date,out_time_val)
                            if perm_out > out_time:
                                out_time=perm_out
                    hh = check_holiday(att.attendance_date, att.employee)
                    if not hh:
                        total_wh = out_time - in_time
                        wh = time_diff_in_hours(out_time, in_time)

                        att_status='Absent'
                        if wh < 4.0:
                            if att.leave_application:
                                leave_appl=frappe.get_doc("Leave Application",att.leave_application)
                                if leave_appl.half_day==1:
                                    if leave_appl.from_date==leave_appl.to_date and leave_appl.from_date==att.attendance_date:
                                        att_status='Half Day'
                                    elif leave_appl.half_day_date==att.attendance_date:
                                        att_status='Half Day'
                                    else:
                                        att_status='On Leave'
                                else:
                                    att_status='On Leave'
                            att_status='Absent'
                        elif 4.0 <= wh < 6.0:
                            if att.leave_application:
                                leave_appl=frappe.get_doc("Leave Application",att.leave_application)
                                if leave_appl.half_day==1:
                                    if leave_appl.from_date==leave_appl.to_date and leave_appl.from_date==att.attendance_date:
                                        att_status='Half Day'
                                    elif leave_appl.half_day_date==att.attendance_date:
                                        att_status='Half Day'
                                    else:
                                        att_status='On Leave'
                                else:
                                    att_status='On Leave'
                            else:
                                att_status='Half Day'
                        elif wh >= 6.0:
                            if att.leave_application:
                                leave_appl=frappe.get_doc("Leave Application",att.leave_application)
                                if leave_appl.half_day==1:
                                    if leave_appl.from_date==leave_appl.to_date and leave_appl.from_date==att.attendance_date:
                                        att_status='Half Day'
                                    elif leave_appl.half_day_date==att.attendance_date:
                                        att_status='Half Day'
                                    else:
                                        att_status='On Leave'
                                else:
                                    att_status='On Leave'
                            else:
                                att_status='Present'
                        
                        shift_end_time = frappe.db.get_value('Shift Type', shift, 'end_time')
                        shift_end_time = pd.to_datetime(str(shift_end_time)).time()
                        shift_start_time = frappe.db.get_value('Shift Type', shift, 'start_time')
                        shift_start_time = pd.to_datetime(str(shift_start_time)).time()
                        total_shift_hours = frappe.db.get_value('Shift Type', shift, 'total_hours')
                        in_date = in_time.date()
                        out_date = out_time.date()

                        if shift == 'C':
                            shift_end_datetime = datetime.combine(add_days(in_date,1),shift_end_time)
                        else:
                            shift_end_datetime = datetime.combine(in_date,shift_end_time)
                        shift_start_datetime = datetime.combine(in_date, shift_start_time)

                        if shift_start_datetime:
                            late_hour = pd.to_datetime('00:00:00').time()
                            late_hr = 0
                            if in_time > shift_start_datetime and att_status== "Present":
                                late_hour = in_time - shift_start_datetime
                                late_hr = time_diff_in_hours(in_time, shift_start_datetime)
                                
                            else:
                                late_hr='0.0'
                                late_hour='00:00'
                               
                            actual_late_hour = frappe.db.get_value('Attendance', att.name, 'late_hours')
                            if actual_late_hour:
                                late_deduct_hour = actual_late_hour.seconds // 3600
                                late_deduct_minute = ((actual_late_hour.seconds // 60) % 60)
                                deducted_minute = late_deduct_minute
                                deducted_hour = late_deduct_hour

                                if 1 <= late_deduct_minute <= 5:
                                    deducted_minute = 5
                                elif 6 <= late_deduct_minute <= 10:
                                    deducted_minute = 10
                                elif 11 <= late_deduct_minute <= 15:
                                    deducted_minute = 15
                                elif 16 <= late_deduct_minute <= 20:
                                    deducted_minute = 20
                                elif 21 <= late_deduct_minute <= 25:
                                    deducted_minute = 25
                                elif 26 <= late_deduct_minute <= 30:
                                    deducted_minute = 30
                                elif 31 <= late_deduct_minute <= 35:
                                    deducted_minute = 35
                                elif 36 <= late_deduct_minute <= 40:
                                    deducted_minute = 40
                                elif 41 <= late_deduct_minute <= 45:
                                    deducted_minute = 45
                                elif 46 <= late_deduct_minute <= 50:
                                    deducted_minute = 50 
                                elif 51 <= late_deduct_minute <= 55:
                                    deducted_minute = 55    
                                elif 56 <= late_deduct_minute <= 60:
                                    deducted_hour = late_deduct_hour + 1
                                    deducted_minute = 0

                                late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute) + ':00'
                                get_late_time = datetime.strptime(str(late_deducted_time), '%H:%M:%S')
                                late_deduct = get_late_time.strftime('%H:%M')
                                late_deduct=late_deduct
                                late_entry=1
                                att_status='Present'
                        if shift_end_datetime:
                            if out_time > shift_end_datetime:
                                extra_hrs = out_time - shift_end_datetime
                                extras = time_diff_in_hours(out_time, shift_end_datetime)
                                if extras > 1.0:
                                    ot_hr = math.floor(extras * 2) / 2
                                else:
                                    ot_hr=0                                   
                            else:
                                ot_hr=0
                                extra_hrs='00:00'                          
                    else:
                        total_wh = out_time - in_time
                        wh = time_diff_in_hours(out_time, in_time)
                        frappe.db.set_value('Attendance', att.name, 'status', 'Present')
                        if wh > 0:
                            ot_hr = (math.floor(wh * 2) / 2) - 0.5  
                            extra_hrs=total_wh
                            total_wh=total_wh
                        else:
                            ot_hr=0
                            extra_hrs='00:00'
                            total_wh='00:00'
                            wh=0
                else:
                    frappe.errprint("IN/OUT/...ELSE...")
                    ot_hr=0
                    extra_hrs='00:00'
                    total_wh='00:00'
                    wh=0
                    att_status='Absent'
                    if att.leave_application:
                        leave_appl=frappe.get_doc("Leave Application",att.leave_application)
                        if leave_appl.half_day==1:
                            if leave_appl.from_date==leave_appl.to_date and leave_appl.from_date==att.attendance_date:
                                att_status='Half Day'
                            elif leave_appl.half_day_date==att.attendance_date:
                                att_status='Half Day'
                            else:
                                att_status='On Leave'
                        else:
                            att_status='On Leave'
                if att.permission_request:
                    perm = frappe.get_doc("Permission Request", att.permission_request)
                    perm_from = datetime.combine( perm.permission_date,to_time(perm.from_time))
                    perm_to = datetime.combine(add_days(perm.permission_date, 1) if perm.shift == 'C' else perm.permission_date,to_time(perm.to_time))
                    if not att.shift:
                            frappe.db.set_value('Attendance',att.name,'shift',perm.shift)
                    perm_duration = perm_to - perm_from
                    wh -= time_diff_in_hours(perm_to, perm_from)
                    total_wh = get_timedelta(total_wh)
                    frappe.errprint(total_wh)
                    total_wh -= perm_duration
                    frappe.db.set_value("Attendance",att.name, "total_wh", total_wh)
                    # frappe.db.set_value("Attendance",att.name, "working_hours", wh)
                    frappe.db.set_value("Attendance",att.name, "status", att_status)
                    frappe.db.set_value("Attendance",att.name, "late_hrs", late_hr)
                    frappe.db.set_value("Attendance",att.name, "late_hours", late_hour)
                    frappe.db.set_value("Attendance",att.name, "late_deduct", late_deduct)
                    frappe.db.set_value("Attendance",att.name, "late_entry", late_entry)
                    frappe.db.set_value("Attendance",att.name, "ot_hrs", ot_hr)
                    frappe.db.set_value("Attendance",att.name, "extra_hours", extra_hrs)
                else:
                    frappe.db.set_value("Attendance",att.name, "total_wh", total_wh)
                    # frappe.db.set_value("Attendance",att.name, "working_hours", wh)
                    frappe.db.set_value("Attendance",att.name, "status", att_status)
                    frappe.db.set_value("Attendance",att.name, "late_hrs", late_hr)
                    frappe.db.set_value("Attendance",att.name, "late_hours", late_hour)
                    frappe.db.set_value("Attendance",att.name, "late_deduct", late_deduct)
                    frappe.db.set_value("Attendance",att.name, "late_entry", late_entry)
                    frappe.db.set_value("Attendance",att.name, "ot_hrs", ot_hr)
                    frappe.db.set_value("Attendance",att.name, "extra_hours", extra_hrs)
   

@frappe.whitelist()
def mark_incentive_amount_staff_categories_emp(from_date,to_date,employee):
    employee = frappe.db.get_all('Employee',{'Status':'Active','incentive_category':'Yes','name':employee},['name'])
    for emp in employee:
        attendance = frappe.db.sql(""" select ot_hrs,name from `tabAttendance` where attendance_date between '%s' and '%s' and employee = '%s' and docstatus != '2'  """%(from_date,to_date,emp.name),as_dict=True)
        for att in attendance:
            e_slap_ot_start = frappe.db.get_single_value('Attendance Settings','e_slap_ot_start')
            t_slap_ot_start = frappe.db.get_single_value('Attendance Settings','t_slap_ot_start')
            m_slap_ot_start = frappe.db.get_single_value('Attendance Settings','m_slap_ot_start')
            e_slap_ot_end = frappe.db.get_single_value('Attendance Settings','e_slap_ot_end')
            t_slap_ot_end = frappe.db.get_single_value('Attendance Settings','t_slap_ot_end')
            m_slap_ot_end = frappe.db.get_single_value('Attendance Settings','m_slap_ot_end')

            if att.ot_hrs >= e_slap_ot_start and att.ot_hrs < e_slap_ot_end:
                frappe.db.set_value('Attendance',att.name,'e_slap_ot_hrs',att.ot_hrs)
                e_slap_amount = frappe.db.get_single_value('Attendance Settings','e_slap_ot_incentive_amount')
                frappe.db.set_value('Attendance',att.name,'e_slap_incentive_amount',e_slap_amount)
            elif att.ot_hrs >= t_slap_ot_start and att.ot_hrs < t_slap_ot_end:
                frappe.db.set_value('Attendance',att.name,'t_slap_ot_hrs',att.ot_hrs)
                t_slap_amount = frappe.db.get_single_value('Attendance Settings','t_slap_ot_incentive_amount')
                frappe.db.set_value('Attendance',att.name,'t_slap_incentive_amount',t_slap_amount)
            elif att.ot_hrs > m_slap_ot_start:   
                frappe.db.set_value('Attendance',att.name,'m_slap_ot_hrs',att.ot_hrs)
                m_slap_amount = frappe.db.get_single_value('Attendance Settings','m_slap_ot_incentive_amount')
                frappe.db.set_value('Attendance',att.name,'m_slap_incentive_amount',m_slap_amount)
    return "OT Updated"        

@frappe.whitelist() 
def mark_assigned_shift_emp(from_date,to_date,employee):
    get_attendance = get_employees_attendance_settings(from_date,to_date,employee)
    for att in get_attendance:
        if not att.attendance_regularize:
            shift = frappe.db.exists('Shift Assignment',{'start_date':att.attendance_date,'employee':att.employee,'docstatus':('!=','2')})
            if shift:
                get_shift = frappe.db.get_value('Shift Assignment',{'start_date':att.attendance_date,'employee':att.employee,'docstatus':('!=','2')},['shift_type'])
                get_shift_start_time = frappe.db.get_value('Shift Type',{'name':get_shift},['start_time'])
                get_shift_end_time = frappe.db.get_value('Shift Type',{'name':get_shift},['end_time'])
                frappe.db.set_value('Attendance',att.name,'shift_type',get_shift)
                frappe.db.set_value('Attendance',att.name,'shift_in_time',get_shift_start_time)
                frappe.db.set_value('Attendance',att.name,'shift_out_time',get_shift_end_time)
            else:
                get_shift_start_time = frappe.db.get_value('Shift Type',{'name':"G"},['start_time'])
                get_shift_end_time = frappe.db.get_value('Shift Type',{'name':"G"},['end_time'])
                frappe.db.set_value('Attendance',att.name,'shift_type',"G")
                frappe.db.set_value('Attendance',att.name,'shift_in_time',get_shift_start_time)
                frappe.db.set_value('Attendance',att.name,'shift_out_time',get_shift_end_time)


@frappe.whitelist()
def mark_attended_shift_emp(from_date,to_date,employee):
    get_attendance = get_employees_attendance_settings(from_date,to_date,employee)
    for att in get_attendance:
        if not att.attendance_regularize:
            if att.in_time:
                frappe.db.set_value('Attendance',att.name,'actual_in_time',format_datetime(att.in_time))
                if att.out_time:
                    frappe.db.set_value('Attendance',att.name,'actual_out_time',format_datetime(att.out_time))
                else:
                    frappe.db.set_value('Attendance',att.name,'actual_out_time','-')
            else:
                frappe.db.set_value('Attendance',att.name,'actual_shift','')
                frappe.db.set_value('Attendance',att.name,'actual_in_time','')
                frappe.db.set_value('Attendance',att.name,'actual_out_time','')

@frappe.whitelist()
def mark_attended_shift(from_date,to_date):
    get_attendance = get_employees_attendance_settings(from_date,to_date)
    for att in get_attendance:
        if not att.attendance_regularize:
            if att.in_time:
                frappe.db.set_value('Attendance',att.name,'actual_in_time',format_datetime(att.in_time))
                if att.out_time:
                    frappe.db.set_value('Attendance',att.name,'actual_out_time',format_datetime(att.out_time))
                else:
                    frappe.db.set_value('Attendance',att.name,'actual_out_time','-')
            else:
                frappe.db.set_value('Attendance',att.name,'actual_shift','')
                frappe.db.set_value('Attendance',att.name,'actual_in_time','')
                frappe.db.set_value('Attendance',att.name,'actual_out_time','')



@frappe.whitelist()
def mark_status_as_absent_emp(from_date,to_date,employee):
    get_attendance = get_employees_attendance_settings(from_date,to_date,employee)
    for att in get_attendance:
        if not att.leave_application:
            if not att.attendance_regularize:
                if att.actual_shift:
                    if att.shift_type == att.actual_shift:
                        frappe.db.set_value('Attendance',att.name,'matched_status','Matched')
                    else:
                        frappe.db.set_value('Attendance',att.name,'matched_status','Unmatched')
                else:
                    frappe.db.set_value('Attendance',att.name,'matched_status','Unmatched')
    return "Completed"            

@frappe.whitelist()
def mark_attendance_as_present_mark_holiday_emp(from_date,to_date,employee):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2'),'employee':employee},['in_time','out_time','attendance_date','employee','name'])
    if attendance:
        for att in attendance:
            if att.in_time and att.out_time:
                hh = check_holiday(att.attendance_date,att.employee)
                if hh:
                    holiday_att = frappe.get_doc('Attendance',att.name)
                    holiday_att.status = 'Present'
                    holiday_att.shift_type = ''
                    holiday_att.shift_in_time = ''
                    holiday_att.shift_out_time = ''
                    holiday_att.actual_shift = ''
                    holiday_att.actual_in_time = ''
                    holiday_att.actual_out_time = ''
                    holiday_att.matched_status = ''
                    holiday_att.save(ignore_permissions=True)
                    frappe.db.commit()
    else:
        holiday_attendance = frappe.db.get_all('Holiday Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2')},['in_time','out_time','attendance_date','employee','name']) 
        if holiday_attendance:
            for att in holiday_attendance:
                if att.in_time and att.out_time:
                    hh = check_holiday(att.attendance_date,att.employee)
                    if hh:
                        holiday_att = frappe.get_doc('Holiday Attendance',att.name)
                        holiday_att.status = 'Present'
                        holiday_att.shift_type = ''
                        holiday_att.shift_in_time = ''
                        holiday_att.shift_out_time = ''
                        holiday_att.actual_shift = ''
                        holiday_att.actual_in_time = ''
                        holiday_att.actual_out_time = ''
                        holiday_att.matched_status = ''
                        holiday_att.save(ignore_permissions=True)
                        frappe.db.commit()

@frappe.whitelist()
def check_holiday_moved_to_holiday_attendance_emp(from_date,to_date,employee):
    # attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2'),'employee':employee},['in_time','out_time','attendance_date','employee','name'])
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2'),'employee':employee},['*'])
    print(attendance , "Attendance")
    
    for att in attendance:
        if att.in_time and att.out_time:
            hh = check_holiday(att.attendance_date,att.employee)
            if hh:
                hd_att = frappe.db.exists('Holiday Attendance',{'attendance_date':att.attendance_date,'employee':att.employee,'docstatus':('!=','2')})
                if not hd_att:
                    print(att.shift , "Attendance")
                    doc = frappe.new_doc('Holiday Attendance')
                    doc.employee = att.employee
                    doc.attendance_date = att.attendance_date
                    doc.status = att.status
                    doc.shift = att.shift
                    doc.in_time = att.in_time
                    doc.out_time = att.out_time
                    doc.total_wh = att.total_wh
                    doc.late_hours = att.late_hours
                    doc.leave_type = att.leave_type
                    doc.leave_application = att.leave_application
                    doc.employee_name = att.employee_name
                    doc.attendance_request = att.attendance_request
                    doc.extra_hours = att.extra_hours
                    doc.ot_hrs = att.ot_hrs
                    doc.late_hrs = att.late_hrs
                    doc.late_deduct = att.late_deduct
                    doc.miss_punch_marked = att.miss_punch_marked
                    doc.on_duty_marked = doc.on_duty_marked 
                    doc.permission_request = att.permission_request
                    doc.single_punch_regularization = att.single_punch_regularization
                    doc.shift_type = att.shift_type
                    doc.shift_in_time = att.shift_in_time
                    doc.shift_out_time = att.shift_out_time
                    doc.actual_shift = att.actual_shift
                    doc.actual_in_time = att.actual_in_time
                    doc.actual_out_time = att.actual_out_time
                    doc.matched_status = att.matched_status
                    doc.attendance_regularize = att.attendance_regularize
                    doc.attendance_name = att.name
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
                frappe.db.sql(""" delete from `tabAttendance` where name = '%s' """%(att.name))    
    return "Holiday Attendance"                

@frappe.whitelist()
def make_late_hours_empty_emp(from_date,to_date,employee):
    attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(from_date,to_date)),'docstatus':('!=','2'),'employee':employee},['name','status'])
    for att in attendance:
        if att.status == 'Half Day':
            frappe.db.set_value('Attendance',att.name,'late_hours','00:00')
            frappe.db.set_value('Attendance',att.name,'late_hrs','')
            frappe.db.set_value('Attendance',att.name,'late_deduct','')


@frappe.whitelist() 
def mark_wh_ot_new(from_date, to_date):
    from_date=add_days(from_date,-2)
    attendance = frappe.db.get_all('Attendance',{'attendance_date': ('between', (from_date, to_date)),'docstatus': ('!=', '2')},['name'])
    for a in attendance:
        att=frappe.get_doc('Attendance',a.name)        
        att_status =''
        total_wh = '00:00'
        wh ='00:00'
        late_hr = ''
        late_hour ='00:00'
        late_deduct = ''
        late_entry = 0
        ot_hr = '0'
        extra_hrs = '00:00'

        doj=frappe.db.get_value('Employee',{'name':att.employee},['date_of_joining'])
        if att.attendance_date >= getdate(doj):
            in_time=''
            out_time=''
            shift=''
            if att.on_duty_marked:
                frappe.errprint('OD')
                od_doc=frappe.get_doc('On Duty Application',att.on_duty_marked)
                shift=od_doc.shift
                if not att.shift:
                    frappe.db.set_value('Attendance',att.name,'shift',od_doc.shift)
                
                    
                if od_doc.session in ['Full Day', 'First Half']:
                    if od_doc.shift:
                        start = frappe.db.get_value('Shift Type', od_doc.shift, 'start_time')
                        in_time_val = to_time(start)
                        in_time_od = datetime.combine(att.attendance_date, in_time_val)
                        in_time = in_time_od
                        if att.in_time:
                            if att.in_time < in_time:
                                in_time=att.in_time
                        frappe.db.set_value('Attendance',att.name,'in_time',in_time)
                else:
                    if od_doc.shift:
                        start = frappe.db.get_value('Shift Type', od_doc.shift, 'start_time')
                        end = frappe.db.get_value('Shift Type', od_doc.shift, 'end_time')
                        start_time = to_time(start)
                        end_time = to_time(end)
                        start_dt = datetime.combine(att.attendance_date, start_time)
                        if od_doc.shift=='C': 
                            end_dt = datetime.combine(add_days(att.attendance_date,1), end_time)
                        else:
                            end_dt = datetime.combine(att.attendance_date, end_time)
                        if end_dt <= start_dt:
                            end_dt += timedelta(days=1)
                        mid_dt = start_dt + (end_dt - start_dt) / 2
                        in_time = mid_dt
                        if att.in_time:
                            if att.in_time < in_time:
                                in_time=att.in_time
                        frappe.db.set_value('Attendance',att.name,'in_time',in_time)
                if od_doc.session in ['Full Day', 'Second Half']:
                    if od_doc.shift:
                        end = frappe.db.get_value('Shift Type', od_doc.shift, 'end_time')
                        out_time_val = to_time(end)
                        if od_doc.shift=='C': 
                            out_time = datetime.combine(add_days(att.attendance_date,1), out_time_val)
                        else:
                            out_time = datetime.combine((att.attendance_date), out_time_val)
                        if att.out_time:
                            if att.out_time > out_time:
                                out_time=att.out_time
                        frappe.db.set_value('Attendance',att.name,'out_time',out_time)
                else:
                    if od_doc.shift:
                        start = frappe.db.get_value('Shift Type', od_doc.shift, 'start_time')
                        end = frappe.db.get_value('Shift Type', od_doc.shift, 'end_time')
                        start_time = to_time(start)
                        end_time = to_time(end)
                        start_dt = datetime.combine(att.attendance_date, start_time)
                        if od_doc.shift=='C': 
                            end_dt = datetime.combine(add_days(att.attendance_date,1), end_time)
                        else:
                            end_dt = datetime.combine(att.attendance_date, end_time)
                        if end_dt <= start_dt:
                            end_dt += timedelta(days=1)
                        mid_dt = start_dt + (end_dt - start_dt) / 2
                        out_time = mid_dt
                        if att.out_time:
                            if att.out_time > out_time:
                                out_time=att.out_time
                        frappe.db.set_value('Attendance',att.name,'out_time',out_time)
                        
                    
            
            else:
                if att.in_time:
                    in_time=att.in_time
                if att.out_time:
                    out_time=att.out_time
                if att.shift:
                    shift=att.shift
            
            if att.miss_punch_marked:
                miss_p=frappe.get_doc('Miss Punch Application',att.miss_punch_marked)
                frappe.db.set_value('Attendance',att.name,'in_time',miss_p.in_time)
                frappe.db.set_value('Attendance',att.name,'out_time',miss_p.out_time)
                in_time=miss_p.in_time
                out_time=miss_p.out_time
            if att.attendance_regularize:
                att_reg=frappe.get_doc('Attendance Regularize',att.attendance_regularize)
                frappe.db.set_value('Attendance',att.name,'in_time',att_reg.corrected_in)
                frappe.db.set_value('Attendance',att.name,'out_time',att_reg.corrected_out)
                frappe.db.set_value('Attendance',att.name,'shift',att_reg.corrected_shift)
                in_time=att_reg.corrected_in
                out_time=att_reg.corrected_out
                shift=att_reg.corrected_shift
            if att:               
                if in_time and out_time and shift:
                    # in_time = att.in_time
                    # out_time = att.out_time
                    if out_time < in_time:
                        frappe.log_error(
                            title="Invalid Attendance Time",
                            message=f"OUT time is less than IN time for Attendance {att.name}\nIN: {in_time}\nOUT: {out_time}"
                        )
                        continue
                    if att.permission_request:
                        perm=frappe.get_doc('Permission Request',att.permission_request)
                        in_time_val = to_time(perm.from_time)
                        out_time_val = to_time(perm.to_time)
                        if perm.session=='First Half':
                            perm_in=datetime.combine(perm.permission_date,in_time_val)
                            if perm_in < in_time:
                                in_time=perm_in
                        else:
                            if perm.shift=='C':
                                perm_out=datetime.combine(add_days(perm.permission_date,1),out_time_val)
                            else:
                                perm_out=datetime.combine(perm.permission_date,out_time_val)
                            if perm_out > out_time:
                                out_time=perm_out
                    hh = check_holiday(att.attendance_date, att.employee)
                    if not hh:
                        total_wh = out_time - in_time
                        wh = time_diff_in_hours(out_time, in_time)

                        att_status='Absent'
                        if wh < 4.0:
                            if att.leave_application:
                                leave_appl=frappe.get_doc("Leave Application",att.leave_application)
                                if leave_appl.half_day==1:
                                    if leave_appl.from_date==leave_appl.to_date and leave_appl.from_date==att.attendance_date:
                                        att_status='Half Day'
                                    elif leave_appl.half_day_date==att.attendance_date:
                                        att_status='Half Day'
                                    else:
                                        att_status='On Leave'
                                else:
                                    att_status='On Leave'
                            else:
                                att_status='Absent'
                        elif 4.0 <= wh < 6.0:
                            if att.leave_application:
                                leave_appl=frappe.get_doc("Leave Application",att.leave_application)
                                if leave_appl.half_day==1:
                                    if leave_appl.from_date==leave_appl.to_date and leave_appl.from_date==att.attendance_date:
                                        att_status='Half Day'
                                    elif leave_appl.half_day_date==att.attendance_date:
                                        att_status='Half Day'
                                    else:
                                        att_status='On Leave'
                                else:
                                    att_status='On Leave'
                            else:
                                att_status='Half Day'
                        elif wh >= 6.0:
                            if att.leave_application:
                                leave_appl=frappe.get_doc("Leave Application",att.leave_application)
                                if leave_appl.half_day==1:
                                    if leave_appl.from_date==leave_appl.to_date and leave_appl.from_date==att.attendance_date:
                                        att_status='Half Day'
                                    elif leave_appl.half_day_date==att.attendance_date:
                                        att_status='Half Day'
                                    else:
                                        att_status='On Leave'
                                else:
                                    att_status='On Leave'
                            else:
                                att_status='Present'
                        
                        shift_end_time = frappe.db.get_value('Shift Type', shift, 'end_time')
                        shift_end_time = pd.to_datetime(str(shift_end_time)).time()
                        shift_start_time = frappe.db.get_value('Shift Type', shift, 'start_time')
                        shift_start_time = pd.to_datetime(str(shift_start_time)).time()
                        total_shift_hours = frappe.db.get_value('Shift Type', shift, 'total_hours')
                        in_date = in_time.date()
                        out_date = out_time.date()

                        if shift == 'C':
                            shift_end_datetime = datetime.combine(add_days(in_date,1),shift_end_time)
                        else:
                            shift_end_datetime = datetime.combine(in_date,shift_end_time)
                        shift_start_datetime = datetime.combine(in_date, shift_start_time)

                        if shift_start_datetime:
                            late_hour = pd.to_datetime('00:00:00').time()
                            late_hr = 0
                            if in_time > shift_start_datetime and att_status== "Present":
                                late_hour = in_time - shift_start_datetime
                                late_hr = time_diff_in_hours(in_time, shift_start_datetime)
                                
                            else:
                                late_hr='0.0'
                                late_hour='00:00'
                               
                            actual_late_hour = frappe.db.get_value('Attendance', att.name, 'late_hours')
                            if actual_late_hour:
                                late_deduct_hour = actual_late_hour.seconds // 3600
                                late_deduct_minute = ((actual_late_hour.seconds // 60) % 60)
                                deducted_minute = late_deduct_minute
                                deducted_hour = late_deduct_hour

                                if 1 <= late_deduct_minute <= 5:
                                    deducted_minute = 5
                                elif 6 <= late_deduct_minute <= 10:
                                    deducted_minute = 10
                                elif 11 <= late_deduct_minute <= 15:
                                    deducted_minute = 15
                                elif 16 <= late_deduct_minute <= 20:
                                    deducted_minute = 20
                                elif 21 <= late_deduct_minute <= 25:
                                    deducted_minute = 25
                                elif 26 <= late_deduct_minute <= 30:
                                    deducted_minute = 30
                                elif 31 <= late_deduct_minute <= 35:
                                    deducted_minute = 35
                                elif 36 <= late_deduct_minute <= 40:
                                    deducted_minute = 40
                                elif 41 <= late_deduct_minute <= 45:
                                    deducted_minute = 45
                                elif 46 <= late_deduct_minute <= 50:
                                    deducted_minute = 50 
                                elif 51 <= late_deduct_minute <= 55:
                                    deducted_minute = 55    
                                elif 56 <= late_deduct_minute <= 60:
                                    deducted_hour = late_deduct_hour + 1
                                    deducted_minute = 0

                                late_deducted_time = str(deducted_hour) + ":" + str(deducted_minute) + ':00'
                                get_late_time = datetime.strptime(str(late_deducted_time), '%H:%M:%S')
                                late_deduct = get_late_time.strftime('%H:%M')
                                late_deduct=late_deduct
                                late_entry=1
                                att_status='Present'
                        if shift_end_datetime:
                            if out_time > shift_end_datetime:
                                extra_hrs = out_time - shift_end_datetime
                                extras = time_diff_in_hours(out_time, shift_end_datetime)
                                if extras > 1.0:
                                    ot_hr = math.floor(extras * 2) / 2
                                else:
                                    ot_hr=0                                   
                            else:
                                ot_hr=0
                                extra_hrs='00:00'                          
                    else:
                        total_wh = out_time - in_time
                        wh = time_diff_in_hours(out_time, in_time)
                        frappe.db.set_value('Attendance', att.name, 'status', 'Present')
                        if wh > 0:
                            ot_hr = (math.floor(wh * 2) / 2) - 0.5  
                            extra_hrs=total_wh
                            total_wh=total_wh
                        else:
                            ot_hr=0
                            extra_hrs='00:00'
                            total_wh='00:00'
                            wh=0
                else:
                    ot_hr=0
                    extra_hrs='00:00'
                    total_wh='00:00'
                    wh=0
                    att_status='Absent'
                    if att.leave_application:
                        leave_appl=frappe.get_doc("Leave Application",att.leave_application)
                        if leave_appl.half_day==1:
                            if leave_appl.from_date==leave_appl.to_date and leave_appl.from_date==att.attendance_date:
                                att_status='Half Day'
                            elif leave_appl.half_day_date==att.attendance_date:
                                att_status='Half Day'
                            else:
                                att_status='On Leave'
                        else:
                            att_status='On Leave'
                if att.permission_request:
                    perm = frappe.get_doc("Permission Request", att.permission_request)
                    perm_from = datetime.combine( perm.permission_date,to_time(perm.from_time))
                    perm_to = datetime.combine(add_days(perm.permission_date, 1) if perm.shift == 'C' else perm.permission_date,to_time(perm.to_time))
                    perm_duration = perm_to - perm_from
                    if wh - time_diff_in_hours(perm_to, perm_from) > 0:
                        wh -= time_diff_in_hours(perm_to, perm_from)
                        total_wh -= perm_duration
                    frappe.db.set_value("Attendance",att.name, "total_wh", total_wh)
                    # frappe.db.set_value("Attendance",att.name, "working_hours", wh)
                    frappe.db.set_value("Attendance",att.name, "status", att_status)
                    frappe.db.set_value("Attendance",att.name, "late_hrs", late_hr)
                    frappe.db.set_value("Attendance",att.name, "late_hours", late_hour)
                    frappe.db.set_value("Attendance",att.name, "late_deduct", late_deduct)
                    frappe.db.set_value("Attendance",att.name, "late_entry", late_entry)
                    frappe.db.set_value("Attendance",att.name, "ot_hrs", ot_hr)
                    frappe.db.set_value("Attendance",att.name, "extra_hours", extra_hrs)
                else:
                    frappe.db.set_value("Attendance",att.name, "total_wh", total_wh)
                    # frappe.db.set_value("Attendance",att.name, "working_hours", wh)
                    frappe.db.set_value("Attendance",att.name, "status", att_status)
                    frappe.db.set_value("Attendance",att.name, "late_hrs", late_hr)
                    frappe.db.set_value("Attendance",att.name, "late_hours", late_hour)
                    frappe.db.set_value("Attendance",att.name, "late_deduct", late_deduct)
                    frappe.db.set_value("Attendance",att.name, "late_entry", late_entry)
                    frappe.db.set_value("Attendance",att.name, "ot_hrs", ot_hr)
                    frappe.db.set_value("Attendance",att.name, "extra_hours", extra_hrs)
   

from datetime import datetime, time, timedelta
@frappe.whitelist()
def to_time(value):
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        hours = (total_seconds // 3600) % 24
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return time(hour=hours, minute=minutes, second=seconds)
    elif isinstance(value, time):
        return value
    else:
        raise TypeError(f"Expected time or timedelta, got {type(value)}")



@frappe.whitelist()
def mark_late_entry(from_date, to_date):
    attendance_list = frappe.db.get_all(
        "Attendance",
        filters={
            "attendance_date": ["between", [from_date, to_date]],
            "docstatus": 0
        },
        fields=["name", "employee", "in_time", "shift", "on_duty_marked", "permission_request"]
    )

    for att in attendance_list:
        # Skip if no in_time or no shift
        if not att.in_time or not att.shift:
            continue

        # Skip if OD or permission_request in first half
        first_half_od = frappe.db.exists("On Duty Application", {
            "name": att.on_duty_marked,
            "session": "First Half",
            "docstatus": 1
        }) if att.on_duty_marked else False

        first_half_perm = frappe.db.exists("Permission Request", {
            "name": att.permission_request,
            "session": "First Half",
            "docstatus": 1
        }) if att.permission_request else False

        if first_half_od or first_half_perm:
            continue

         # Get Shift Start Time
        shift_start = frappe.db.get_value("Shift Type", att.shift, "start_time")
        if not shift_start:
            continue

        # Convert timedelta to time if needed
        if isinstance(shift_start, timedelta):
            shift_start_time = (datetime.min + shift_start).time()
        else:
            shift_start_time = shift_start

        # Add 1-minute grace
        grace_time = (datetime.combine(att.in_time.date(), shift_start_time) + timedelta(minutes=1)).time()

        # Mark Late Entry
        if att.in_time.time() >= grace_time:
            frappe.db.set_value("Attendance", att.name, "late_entry", 1)
        else:
            frappe.db.set_value("Attendance", att.name, "late_entry", 0)


@frappe.whitelist()
def mark_late_entry_emp(from_date, to_date, employee):
    attendance_list = frappe.db.get_all(
        "Attendance",
        filters={
            "attendance_date": ["between", [from_date, to_date]],
            "employee": employee,
            "docstatus": 0
        },
        fields=["name", "employee", "in_time", "shift", "on_duty_marked", "permission_request"]
    )

    for att in attendance_list:
        if not att.in_time or not att.shift:
            continue

        # Skip if OD or permission_request in first half
        first_half_od = frappe.db.exists("On Duty Application", {
            "name": att.on_duty_marked,
            "session": "First Half",
            "docstatus": 1
        }) if att.on_duty_marked else False

        first_half_perm = frappe.db.exists("Permission Request", {
            "name": att.permission_request,
            "session": "First Half",
            "docstatus": 1
        }) if att.permission_request else False

        if first_half_od or first_half_perm:
            continue

        # Get Shift Start Time
        shift_start = frappe.db.get_value("Shift Type", att.shift, "start_time")
        if not shift_start:
            continue

        # Convert timedelta to time if needed
        if isinstance(shift_start, timedelta):
            shift_start_time = (datetime.min + shift_start).time()
        else:
            shift_start_time = shift_start

        # Add 1-minute grace
        grace_time = (datetime.combine(att.in_time.date(), shift_start_time) + timedelta(minutes=1)).time()

        # Mark Late Entry
        if att.in_time.time() >= grace_time:
            frappe.db.set_value("Attendance", att.name, "late_entry", 1)
        else:
            frappe.db.set_value("Attendance", att.name, "late_entry", 0)


@frappe.whitelist()
def get_invalid_attendance():
    from_date = "2025-10-21"
    to_date = "2025-11-20"

    res = frappe.db.sql("""
        SELECT name, attendance_date, in_time, out_time
        FROM `tabAttendance`
        WHERE attendance_date BETWEEN %s AND %s
          AND in_time IS NOT NULL
          AND out_time IS NOT NULL
          AND out_time < in_time
          AND docstatus = 0
    """, (from_date, to_date), as_dict=True)

    print("DEBUG RESULT:", res)   # For bench execute output

    return res

