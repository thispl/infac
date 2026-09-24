import frappe
import datetime
from frappe.utils import (getdate, cint, add_months, date_diff, add_days)
from frappe.utils.data import ceil, get_time, get_year_start
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours
from infac.shift_attendance import mark_absent,mark_wh_ot,mark_incentive_amount_staff_categories,mark_assigned_shift,make_late_hours_empty,check_holiday_moved_to_holiday_attendance,mark_attendance_as_present_mark_holiday,mark_single_punch_as_absent,mark_attended_shift,mark_status_as_absent

@frappe.whitelist()  
def mark_att():
    from_date = add_days(today(),-3)
    to_date = add_days(today(),-1)
   
    # from_date = '2025-07-30'
    # to_date = '2025-07-31'
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' order by time   """%(from_date,to_date),as_dict=True)
    # frappe.errprint(checkins)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            # frappe.errprint('1')
            #the below mthod to mark the checkin in attendance application for IN and OUT Punches
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    mark_absent(from_date,to_date)
    mark_wh_ot(from_date,to_date)
    # mark_incentive_amount_staff_categories(from_date,to_date)
    # mark_assigned_shift(from_date,to_date)
    # mark_attended_shift(from_date,to_date)
    # mark_status_as_absent(from_date,to_date)
    mark_single_punch_as_absent(from_date,to_date)
    # mark_attendance_as_present_mark_holiday(from_date,to_date)
    # check_holiday_moved_to_holiday_attendance(from_date,to_date)
    make_late_hours_empty(from_date,to_date)

@frappe.whitelist()  
def mark_att_new1():
    from_date = add_days(today(), -3)
    to_date = today()
   
    # from_date = '2025-07-30'
    # to_date = '2025-07-31'
    checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where date(time) between '%s' and '%s' order by time   """%(from_date,to_date),as_dict=True)
    # frappe.errprint(checkins)
    for c in checkins:
        employee = frappe.db.exists('Employee',{'status':'Active','date_of_joining':['<=',from_date],'name':c.employee})
        if employee:
            # frappe.errprint('1')
            #the below mthod to mark the checkin in attendance application for IN and OUT Punches
            mark_attendance_from_checkin(c.name,c.employee,c.time,c.log_type)
    mark_absent(from_date,to_date)
    mark_wh_ot(from_date,to_date)
    # mark_incentive_amount_staff_categories(from_date,to_date)
    # mark_assigned_shift(from_date,to_date)
    # mark_attended_shift(from_date,to_date)
    # mark_status_as_absent(from_date,to_date)
    mark_single_punch_as_absent(from_date,to_date)
    # mark_attendance_as_present_mark_holiday(from_date,to_date)
    # check_holiday_moved_to_holiday_attendance(from_date,to_date)
    make_late_hours_empty(from_date,to_date)
    
@frappe.whitelist()  
def mark_attendance_from_checkin(checkin,employee,time,log_type):
    att_time = time.time()
    att_date = time.date()
    # frappe.errprint('2')
    if log_type=='IN':
        checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where employee = '%s' and log_type = 'IN' and date(time) = '%s'  order by time ASC """%(employee,att_date),as_dict=True)
        if checkins:
            # frappe.errprint('if')
            att = frappe.db.exists('Attendance',{"employee":employee,'attendance_date':att_date,'docstatus':['!=','2']})   
            if not att:
                
                att = frappe.new_doc("Attendance")
                
                att.employee = employee
                att.attendance_date = att_date
                att.shift = get_actual_shift_start(get_time(checkins[0].time))
                att.status = 'Absent'
                att.in_time = checkins[0].time
                att.total_wh = '00:00'
                att.late_hours = '00:00'
                att.extra_hours = '00:00'
                att.save(ignore_permissions=True)
                frappe.db.commit()
                for c in checkins:
                    frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
                    frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
                return att  
            else:
                # frappe.errprint('else')
                att = frappe.get_doc("Attendance",att)
                print(att.name)
                if att.docstatus == 0:
                    att.in_time =checkins[0]['time']
                    # frappe.errprint('HI@')
                    # frappe.errprint(get_actual_shift_start(get_time(checkins[0]['time'])))
                    if not att.shift:
                        att.shift = get_actual_shift_start(get_time(checkins[0]['time']))
                    att.save(ignore_permissions=True)
                    frappe.db.commit()
                    for c in checkins:
                        frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
                        frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
                    return att 
    if log_type == 'OUT':
        # frappe.errprint('out1')
        if get_time(att_time) < datetime.datetime.strptime('12:00', '%H:%M').time():
            # frappe.errprint('out2')
            max_out = datetime.datetime.strptime('12:00', '%H:%M').time()

            checkins = frappe.db.sql("""
                SELECT * FROM `tabEmployee Checkin`
                WHERE employee = %s
                AND log_type = 'OUT'
                AND DATE(time) = %s
                AND TIME(time) < %s
                ORDER BY time ASC
            """, (employee, att_date, max_out), as_dict=True)

            if checkins:
                current_day_in = frappe.db.sql("""SELECT * FROM `tabEmployee Checkin` WHERE employee = %s AND log_type = 'IN' AND DATE(time) = %s AND TIME(time) < %s ORDER BY time ASC """, (employee, att_date, checkins[-1]['time']), as_dict=True)
                if current_day_in:
                    if frappe.db.exists('Attendance', {'employee': employee, 'attendance_date': att_date, 'docstatus': ('!=', 2)}):
                        att = frappe.get_doc('Attendance', {'employee': employee, 'attendance_date': att_date, 'docstatus': ('!=', 2)})
                        print(att.name)
                        if att.in_time:
                            if att.in_time < checkins[-1]['time']:
                                att.out_time = checkins[-1]['time']
                                if not att.shift:
                                    att.shift = get_actual_shift(get_time(checkins[-1].time))
                        else:
                            att.out_time = checkins[-1]['time']
                            if not att.shift:
                                att.shift = get_actual_shift(get_time(checkins[-1].time))
                        att.save(ignore_permissions=True)
                        frappe.db.commit()
                    else:
                        att = frappe.new_doc("Attendance")
                        
                        att.employee = employee
                        att.attendance_date = att_date
                        if not att.shift:
                            att.shift = get_actual_shift(get_time(checkins[0].time))
                        att.status = 'Absent'
                        att.out_time = checkins[-1].time
                        att.total_wh = '00:00'
                        att.late_hours = '00:00'
                        att.extra_hours = '00:00'
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
                                    att.save(ignore_permissions=True)
                                    frappe.db.commit()
        
        else:
            # frappe.errprint('out3')
            checkins = frappe.db.sql("""select * from `tabEmployee Checkin` where employee = '%s' and log_type = 'OUT' and date(time) = '%s'  order by time ASC """%(employee,att_date),as_dict=True)
            if checkins:
                att = frappe.db.exists('Attendance',{"employee":employee,'attendance_date':att_date,'docstatus':['!=','2']})   
                if not att:
                    att = frappe.new_doc("Attendance")
                    
                    att.employee = employee
                    att.attendance_date = att_date
                    if not att.shift:
                        att.shift = get_actual_shift(get_time(checkins[-1].time))
                    att.status = 'Absent'
                    att.out_time = checkins[-1].time
                    att.total_wh = '00:00'
                    att.late_hours = '00:00'
                    att.extra_hours = '00:00'
                    att.save(ignore_permissions=True)
                    frappe.db.commit()
                    for c in checkins:
                        frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
                        frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
                    return att  
                else:
                    att = frappe.get_doc("Attendance",att)
                    print(att.name)
                    if att.docstatus == 0:
                        if att.in_time and att.in_time < checkins[-1]['time']:
                            att.out_time =checkins[-1]['time']
                            if not att.shift:
                                att.shift = get_actual_shift(get_time(checkins[-1]['time']))
                        att.save(ignore_permissions=True)
                        frappe.db.commit()
                        for c in checkins:
                            frappe.db.set_value('Employee Checkin', c.name, 'skip_auto_attendance', 1)
                            frappe.db.set_value("Employee Checkin",c.name, "attendance", att.name)
                        return att 



@frappe.whitelist()
def get_actual_shift_start(get_shift_time):
    shift1 = frappe.db.get_value('Shift Type',{'name':'A'},['checkin_start_time','checkin_end_time'])
    shift2 = frappe.db.get_value('Shift Type',{'name':'B'},['checkin_start_time','checkin_end_time'])
    shift3 = frappe.db.get_value('Shift Type',{'name':'C'},['checkin_start_time','checkin_end_time'])
    shift4 = frappe.db.get_value('Shift Type',{'name':'G'},['checkin_start_time','checkin_end_time'])
    att_time_seconds = get_shift_time.hour * 3600 + get_shift_time.minute * 60 + get_shift_time.second
    shift = ''
    if (shift1[0].total_seconds() < att_time_seconds < shift1[1].total_seconds()):
        shift = 'A'
    elif shift2[0].total_seconds() < att_time_seconds < shift2[1].total_seconds():
        shift = 'B'
    elif shift3[0].total_seconds() < att_time_seconds < shift3[1].total_seconds():
        shift = 'C'
    elif shift4[0].total_seconds() < att_time_seconds < shift4[1].total_seconds():
        shift = 'G'
    return shift

@frappe.whitelist()
def get_actual_shift(get_shift_time):
    shift1 = frappe.db.get_value('Shift Type',{'name':'A'},['check_out_start_time','check_out_end_time'])
    shift2 = frappe.db.get_value('Shift Type',{'name':'B'},['check_out_start_time','check_out_end_time'])
    shift3 = frappe.db.get_value('Shift Type',{'name':'C'},['check_out_start_time','check_out_end_time'])
    shift4 = frappe.db.get_value('Shift Type',{'name':'G'},['check_out_start_time','check_out_end_time'])
    att_time_seconds = get_shift_time.hour * 3600 + get_shift_time.minute * 60 + get_shift_time.second
    shift = ''
    if shift1[0].total_seconds() < att_time_seconds < shift1[1].total_seconds():
        shift = 'A'
    elif shift2[0].total_seconds() < att_time_seconds < shift2[1].total_seconds():
        shift = 'B'
    elif shift3[0].total_seconds() < att_time_seconds < shift3[1].total_seconds():
        shift = 'C'
    elif shift4[0].total_seconds() < att_time_seconds < shift4[1].total_seconds():
        shift = 'G'
    return shift


@frappe.whitelist()
def create_hooks_event():
    job = frappe.db.exists('Scheduled Job Type', 'mark_attendance')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'infac.create_attendance.mark_att',
            "frequency": 'Cron',
            "cron_format": '*/20 * * * *'
        })
        sjt.save(ignore_permissions=True)

@frappe.whitelist()
def att_mark():
    job = frappe.db.exists('Scheduled Job Type', 'mark_attendance')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")
        sjt.update({
            "method": 'infac.create_attendance.mark_att_new1',
            "frequency": 'Cron',
            "cron_format": '0 8 * * *'
        })
        sjt.save(ignore_permissions=True)        