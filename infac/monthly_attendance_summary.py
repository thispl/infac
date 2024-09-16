import frappe
from frappe.utils import cstr, add_days, date_diff,format_datetime,format_date,getdate





@frappe.whitelist()
def get_attendance(user):
    data = {}
    # datalist = []
    emp_id = frappe.db.get_value('Employee',{'Status':'Active','user_id':user},['name'])
    emp_name = frappe.db.get_value('Employee',{'Status':'Active','user_id':user},['employee_name'])
    dept = frappe.db.get_value('Employee',{'Status':'Active','user_id':user},['department'])
    start_date = frappe.db.get_value('Payroll Dates Automatic',{'name':'PAYDATE0001'},['payroll_start_date'])
    end_date = frappe.db.get_value('Payroll Dates Automatic',{'name':'PAYDATE0001'},['payroll_end_date'])
    no_of_days = date_diff(add_days(end_date, 1), start_date)
    dates = [add_days(start_date, i) for i in range(0, no_of_days)]
    for date in dates:
        att = frappe.db.get_all('Attendance',{'employee':emp_id,'attendance_date':('between',(start_date,end_date))},['attendance_date','in_time','out_time','shift','status','total_wh','ot_hrs','late_deduct'])
    # data.update({
    #     'emp_id':emp_id,
    #     'emp_name':emp_name,
    #     'dept':dept,
    #     'attendance':attendance
    # })    
    # datalist.append(data.copy())
        data['emp_id'] = emp_id
        data['emp_name'] = emp_name
        data['dept'] = dept
        data['att'] = [{ 'attendance_date':'2023-03-28','shift':'G'}]
    return data
    