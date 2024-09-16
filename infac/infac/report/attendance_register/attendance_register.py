from __future__ import unicode_literals
from functools import total_ordering
from itertools import count
import frappe
from frappe import permissions
from frappe.utils import cstr, cint, getdate, get_last_day, get_first_day, add_days,date_diff
from math import floor
from frappe import msgprint, _
from calendar import month, monthrange
from datetime import date, timedelta, datetime,time
from numpy import true_divide

import pandas as pd

status_map = {
    'Permission Request' :'PR',
    'On Duty':'OD',
    'Half Day':'HD',
    "Absent": "A",
	"Half Day": "HD",
	"Holiday": "HH",
	"Weekly Off": "WW",
    "Present": "P",
    "None" : "",
    "Leave Without Pay": "LOP",
    "Casual Leave": "CL",
    "Earned Leave": "EL",
    "Sick Leave": "SL",
    "Emergency -1": 'EML-1',
    "Emergency -2": 'EML-2',
    "Paternal Leave": 'PL',
    "Marriage Leave":'ML',
    "Medical Leave" : 'MDL',
    "Paternity Leave":'PTL',
    "Education Leave":'EL',
    "Maternity Leave":'MTL',
    "Covid -19": "COV-19",
    "Privilege Leave": "PVL",
    "Compensatory Off": "C-OFF",
    "BEREAVEMENT LEAVE":'BL'
}
def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data

def get_columns(filters):
    columns = []
    columns += [
        _("Employee ID") + ":Data/:150",_("Employee Name") + ":Data/:200",_('Employee Category') +':Data:100',_("Department") + ":Data/:150",_("DOJ") + ":Date/:100",_("Status") + ":Data/:150",
    ]
    dates = get_dates(filters.from_date,filters.to_date)
    for date in dates:
        date = datetime.strptime(date,'%Y-%m-%d')
        day = datetime.date(date).strftime('%d')
        month = datetime.date(date).strftime('%b')
        columns.append(_(day + '/' + month) + ":Data/:70")
    columns.append(_("Present") + ":Data/:100")
    columns.append(_('Half Day') +':Data/:100')
    columns.append(_('On Duty') + ':Data/:100')
    columns.append(_('Permission') + ':Data/:100')
    columns.append(_("Absent") + ":Data/:100")
    columns.append(_('Weekoff')+ ':Data/:100')
    columns.append(_('Holiday')+ ':Data/:100')
    columns.append(_('Paid Leave')+ ':Data/:150')
    columns.append(_('LOP')+ ':Data/:100')
    columns.append(_('COFF')+ ':Data/:100')
    columns.append(_('OT')+ ':Data/:100')
    columns.append(_('Actual Late')+ ':Data/:100')
    columns.append(_('Late Deduct')+ ':Data/:150')
    columns.append(_('Permission Hours')+ ':Data/:150')
    columns.append(_('Night Shift')+ ':Data/:150')
    
    return columns

def get_data(filters):
    # week_off_count = frappe.db.get_value('Holiday Count List',{'from_date':('between',(filters.from_date,filters.to_date))},['total_week_off'])
    # holiday_count = frappe.db.get_value('Holiday Count List',{'from_date':('between',(filters.from_date,filters.to_date))},['total_holiday'])
    data = []
    emp_status_map = []
    employees = get_employees(filters)
    for emp in employees:
        dates = get_dates(filters.from_date,filters.to_date)
        row1 = [emp.name,emp.employee_name,emp.employee_category,emp.department,emp.date_of_joining,""]
        row2 = ["","","","","","In Time"]
        row3 = ["","","","","","Out Time"]
        row4 = ["","","","","","Shift"]
        row5 = ["","","","","","Late"]
        row6 = ["","","","","","Late Deduct"]
        row7 = ["","","","","","TWH"]
        row8 = ["","","","","","OT"]
        total_present = 0
        total_half_day = 0
        total_absent = 0
        total_holiday = 0
        total_weekoff = 0
        total_ot = 0
        total_od = 0
        total_permission = 0
        total_lop = 0
        total_paid_leave = 0
        total_combo_off = 0
        c_shift = 0
        # total_late = pd.to_datetime('00:00:00').time()
        total_late = timedelta(0,0,0)
        total_late_deduct = timedelta(0,0)
        ww = 0
        twh = 0
        ot = 0
        for date in dates:
            att = frappe.db.get_value("Attendance",{'attendance_date':date,'employee':emp.name,'docstatus':('!=','2')},['status','in_time','out_time','shift','total_wh','ot_hrs','late_hrs','leave_type','employee_category','on_duty_marked','permission_request','leave_type','late_hours','employee','attendance_date','name','late_deduct','name']) or ''
            if att:
                status = status_map.get(att[0], "")
                if att[9]:
                    hh = check_holiday(date,emp.name)
                    if hh:
                        frappe.errprint("on Duty")
                        if hh == 'WW':
                            row1.append(hh)
                            total_weekoff +=1
                        elif hh == 'HH':
                            row1.append(hh)
                            total_holiday +=1   
                        # row1.append(hh)
                    else:    
                        row1.append('OD')
                        total_od = total_od + 1  
                elif att[10]:
                    hh = check_holiday(date,emp.name)
                    if hh:
                        frappe.errprint("Permission Request")
                        if hh == 'WW':
                            row1.append(hh)
                            total_weekoff +=1
                        elif hh == 'HH':
                            row1.append(hh)
                            total_holiday +=1   
                        # row1.append(hh)
                    else:      
                        row1.append('P/P')
                        total_present +=  1
                        total_permission += 1    
                elif att[0] == 'Present':
                    hh = check_holiday(date,emp.name)
                    if hh:
                        frappe.errprint("Present")
                        if hh == 'WW':
                            row1.append(hh)
                            total_weekoff +=1
                        if hh == 'HH':
                            row1.append(hh)
                            total_holiday +=1   
                        # row1.append(hh)   
                    else:  
                        row1.append(status)
                        total_present = total_present + 1 

                elif att[0] == 'Half Day':
                    hh = check_holiday(date,emp.name)
                    if hh:
                        frappe.errprint("Half Day")
                        if hh == 'WW':
                            row1.append(hh)
                            total_weekoff += 1
                        elif hh == 'HH':
                            row1.append(hh)
                            total_holiday += 1
                        # row1.append(hh)
                    else:
                        if att[11]:
                            row1.append('P/L')
                            total_present = total_present + 0.5
                            total_paid_leave = total_paid_leave + 0.5
                        else:
                            row1.append('P/A')
                            total_present = total_present + 0.5
                            total_half_day = total_half_day + 0.5
                elif att[0] == 'Absent':
                    hh = check_holiday(date,emp.name)
                    if hh:
                        frappe.errprint("Absent")
                        if hh == 'WW':
                            row1.append(hh)
                            total_weekoff += 1
                        elif hh == 'HH':
                            row1.append(hh)
                            total_holiday += 1
                        # row1.append(hh)
                    else: 
                        row1.append(status)
                        total_absent = total_absent + 1                         
                elif att[7]:
                    hh = check_holiday(date,emp.name)
                    if hh:
                        frappe.errprint("Leave Type")
                        if hh == 'WW':
                            total_weekoff += 1
                        elif hh == 'HH':
                            total_holiday += 1
                        row1.append(hh)
                    else:    
                        status = status_map.get(att[7], "")
                        if status != 'LOP':
                            if status == 'C-OFF':
                                total_combo_off += 1
                            else:
                                total_paid_leave += 1
                        else:                        
                            total_lop += 1
                        row1.append(status)
                else:
                    row1.append('-')
                if att[1] is not None :
                    if att[1] != '0':
                        row2.append(att[1].strftime('%H:%M'))
                    else:
                        row2.append('-')

                else:
                    row2.append('-')
                if att[2] is not None :
                    if att[2] != '0':
                        row3.append(att[2].strftime('%H:%M'))
                    else:
                        row3.append('-')

                else:
                    row3.append('-')
                
                if att[3]:
                    if att[0] == 'Absent':
                        row4.append('')
                    else:
                        row4.append(att[3])    
                else:
                    row4.append('-')

                if att[3] == 'C':
                    c_shift += 1   

                #This is the Late Hours Condition    
                if att[12]:
                    # hh = check_holiday(date,emp.name)
                    # if hh:
                    #     frappe.errprint("Late Hours")
                    #     if hh == 'WW':
                    #         total_weekoff += 1
                    #     elif hh == 'HH':
                    #         total_holiday += 1
                    #     row5.append('-')    
                    # else:  
                    if att[0] == 'Absent':
                        row5.append('-')
                    else:   
                        frappe.errprint(att[15])
                        if str(att[12]) !='0':  
                            # frappe.errprint(att[13]) 
                            # if datetime.strptime(str(att[12]),'%H:%M:%S'):
                            #     late = datetime.strptime(str(att[12]),'%H:%M:%S').strftime('%H:%M')
                            # else:
                            #     if datetime.strptime(str(att[12]),'%H:%M:%S.%f'):
                            #         late = datetime.strptime(str(att[12]),'%H:%M:%S.%f').strftime('%H:%M')
                            row5.append(str(att[12]))
                            total_late = total_late + att[12]
                        else:
                            row5.append('-')
                            total_late = total_late + att[12]

                else:
                    row5.append('-')

                #This is the Late Deduct condition        
                if att[16]: 
                    # hh = check_holiday(date,emp.name)
                    # if not hh:
                    #     # frappe.errprint("Late Deduct")
                    #     # if hh == 'WW':
                    #     #     total_weekoff += 1
                    #     # elif hh == 'HH':
                    #     #     total_holiday += 1
                    #     # row6.append('-')
                    # else:
                    if att[0] == "Absent":
                        row6.append('-')
                    else:
                        if att[16] != '0':  
                            str_time = datetime.strptime(att[16],'%H:%M').time()
                            time_time_delta = timedelta(hours=str_time.hour,minutes=str_time.minute,seconds=0)
                            row6.append(att[16]) 
                            #late_deduct column to add_time
                            total_late_deduct = total_late_deduct + time_time_delta
                        else:
                            row6.append('-')
                            total_late_deduct = total_late_deduct



                else:
                    row6.append('-')      

                if att[4] is not None and att[0] != 'Absent':
                    hh = att[4].seconds//3600
                    mm = (att[4].seconds//60)%60
                    twh = str(hh) + ":" + str(mm)
                    row7.append(twh) 
                else:
                    row7.append('-')    

                if att[5]: 
                    if att[0] == "Absent":
                        row8.append('')  
                    else:     
                        row8.append(att[5])
                        total_ot += att[5]
                else:
                    row8.append('-')
                                 
            else:
                hh = check_holiday(date,emp.name)
                if hh:
                    frappe.errprint("Attendance is not created")
                    if hh == 'WW': 
                        total_weekoff += 1
                    elif hh == 'HH':
                        total_holiday += 1
                    row1.append(hh)
                    holiday = frappe.db.get_value('Holiday Attendance',{'employee':emp.name,'attendance_date':date,'docstatus':('!=','2')},['in_time','out_time','shift','late_hours','late_deduct','total_wh','ot_hrs'])
                    if holiday:
                        if holiday[0]:
                            row2.append(holiday[0].strftime('%H:%M'))
                        else:
                            row2.append('-')  
                        if holiday[1]:
                            row3.append(holiday[1].strftime('%H:%M'))
                        else:
                            row3.append('-')  
                        if holiday[2]:
                            row4.append(holiday[2])   
                        else:
                            row4.append('-')   
                        if holiday[3]:
                            row5.append(holiday[3]) 
                            # total_late = total_late + holiday[3]
                        else:
                            row5.append('-') 
                        if holiday[4]:
                            row6.append(holiday[4]) 
                            # str_time = datetime.strptime(holiday[4],'%H:%M').time()
                            # time_time_delta = timedelta(hours=str_time.hour,minutes=str_time.minute,seconds=0)
                            # total_late_deduct = total_late_deduct + time_time_delta 
                        else:
                            row6.append('-') 
                        if holiday[5]:
                            row7.append(holiday[5]) 
                        else:
                            row7.append('-')
                        if holiday[6]:
                            row8.append(holiday[6])
                            total_ot += holiday[6] 
                        else:
                            row8.append('-')                        
                    else:
                        row2.append('-')
                        row3.append('-') 
                        row4.append('-') 
                        row5.append('-')
                        row6.append('-')
                        row7.append('-')
                        row8.append('-')
                
                else:
                    row1.append('-')
                    row2.append('-')
                    row3.append('-')
                    row4.append('-')
                    row5.append('-')
                    row6.append('-')
                    row7.append('-')
                    row8.append('-')

        

        permission_hours = frappe.db.sql("""select sum(hours) as sum from `tabPermission Request` where permission_date between '%s' and '%s' and employee_id = '%s' and docstatus = '1' """%(filters.from_date,filters.to_date,emp.name),as_dict=True)[0].sum or 0
        row1.extend([total_present,total_half_day,total_od,total_permission,total_absent,total_weekoff,total_holiday,total_paid_leave,total_lop,total_combo_off,total_ot,total_late,total_late_deduct,permission_hours or '-',c_shift or 0.0])
        row2.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row3.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row4.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row5.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row6.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row7.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
        row8.extend(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])



        data.append(row1)
        data.append(row2)
        data.append(row3)
        data.append(row4)
        data.append(row5)
        data.append(row6)
        data.append(row7)
        data.append(row8)
    return data

def get_dates(from_date,to_date):
    no_of_days = date_diff(add_days(to_date, 1), from_date)
    dates = [add_days(from_date, i) for i in range(0, no_of_days)]
    return dates

def get_employees(filters):
    conditions = ''
    left_employees = []
    if filters.employee:
        conditions += "and employee = '%s' " % (filters.employee)
    if filters.employee_category:
        conditions += "and employee_category = '%s' " % (filters.employee_category)

    employees = frappe.db.sql("""select name, employee_name, department,employee_category,date_of_joining from `tabEmployee` where status = 'Active' %s """ % (conditions), as_dict=True)
    left_employees = frappe.db.sql("""select name, employee_name, department,employee_category, date_of_joining from `tabEmployee` where status = 'Left' and relieving_date >= '%s' %s """ %(filters.from_date,conditions),as_dict=True)
    employees.extend(left_employees)
    return employees
  
@frappe.whitelist()
def get_to_date(from_date):
    day = from_date[-2:]
    if int(day) > 21:
        d = add_days(get_last_day(from_date),21)
        return d
    if int(day) <= 21:
        d = add_days(get_first_day(from_date),21)
        return d

def check_holiday(date,emp):
    holiday_list = frappe.db.get_value('Company','Infac India Private Limited','default_holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date = '%s' """%(holiday_list,date),as_dict=True)
    frappe.errprint(holiday)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"