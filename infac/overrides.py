from email import message
from email.errors import MessageError
from pickle import TRUE
from symbol import pass_stmt
import frappe
from frappe import _
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
from erpnext.hr.doctype.leave_application.leave_application import LeaveApplication
from erpnext.hr.doctype.leave_allocation.leave_allocation import LeaveAllocation
from erpnext.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry
from erpnext.hr.doctype.employee.employee import Employee
from frappe.frappeclient import FrappeException
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day
from erpnext.hr.utils import validate_dates, validate_overlap, get_leave_period, \
    get_holidays_for_employee, create_additional_leave_ledger_entry

class CustomEmployee(Employee):
    def before_save(self):
        if self.employee_category == 'Master Staff':
            self.proposed_salary = self.gross_salary - (self.welfare_allowance_amount + self.attendance_bonus + self.higher_education_allowance_amount + self.supr_allowance + self.other_allowances)
            perf_percent = frappe.db.get_single_value('Payroll Process Settings','performance_allowance_calculation')
            self.performance_allowance = round(self.proposed_salary * perf_percent)
            self.fixed_salary = round(self.proposed_salary - self.performance_allowance)

        elif self.employee_category == 'Master Worker' or self.employee_category == 'Workers Grade 2':
            self.fixed_salary = round(self.gross_salary -(self.medical_allowance + self.special_allowance + self.washing_allowance + self.heat_allowance + self.welfare_allowance_amount + self.grade_allowance + self.attendance_bonus + self.higher_education_allowance_amount + self.other_allowances))

        elif self.employee_category == 'Operating Staff' or self.employee_category == 'Supporting Staff':
            self.proposed_salary = self.gross_salary - (self.attendance_bonus + self.welfare_allowance_amount + self.heat_allowance)
            perf_percent = frappe.db.get_single_value('Payroll Process Settings','performance_allowance_calculation')
            self.performance_allowance = round(self.proposed_salary * perf_percent)
            self.fixed_salary = round(self.proposed_salary - self.performance_allowance)
                                                 
class CustomSalarySlip(SalarySlip):
    def before_save(self):
        absent_days = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status = 'Absent' and attendance_date between '%s' and '%s' and docstatus = '1'""" % (self.employee,self.start_date,self.end_date),as_dict=True)[0]
        paid_leave = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status = 'On Leave'  and leave_type in ('Casual Leave','Earned Leave','Sick Leave','Compensatory Off','Marriage Leave','Maternity Leave','Medical Leave','Paternity Leave') and  attendance_date between '%s' and '%s' and docstatus = '1'""" % (self.employee,self.start_date,self.end_date),as_dict=True)[0]
        # lop_leave = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status = 'On Leave'  and leave_type = 'Leave Without Pay' and  attendance_date between '%s' and '%s' and docstatus = '1'""" % (self.employee,self.start_date,self.end_date),as_dict=True)[0]
        paid_half_day_leave = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status = 'Half Day'  and leave_type in ('Casual Leave','Earned Leave','Sick Leave','Compensatory Off','Marriage Leave','Maternity Leave','Medical Leave','Paternity Leave') and  attendance_date between '%s' and '%s' and docstatus = '1'""" % (self.employee,self.start_date,self.end_date),as_dict=True)[0]
        # lop_half_day = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status = 'Half Day'  and leave_type = 'Leave Without Pay' and  attendance_date between '%s' and '%s' and docstatus = '1'""" % (self.employee,self.start_date,self.end_date),as_dict=True)[0]
        self.absent_days = absent_days['count']
        self.paid_leaves = paid_leave['count'] + (paid_half_day_leave['count']/2)
        self.leave_days = paid_leave['count'] + (paid_half_day_leave['count']/2) + absent_days['count'] + self.leave_without_pay 
        frappe.db.set_value("Employee",self.employee,"non_present_days",self.leave_days)
          
class CustomPayrollEntry(PayrollEntry):
    def before_save(self):
        self.number_of_employees = len(self.employees)
        for emp in self.employees:
            empid = frappe.get_doc('Employee',emp.employee)
            absent_days = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status = 'Absent' and attendance_date between '%s' and '%s' and docstatus = '1'""" % (empid.employee,self.start_date,self.end_date),as_dict=True)[0]
            leave_days = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status = 'On Leave' and attendance_date between '%s' and '%s' and docstatus = '1'""" % (empid.employee,self.start_date,self.end_date),as_dict=True)[0]
            absent_half_days = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status in ('Half Day') and attendance_date between '%s' and '%s' and docstatus = '1' """ % (emp.employee,self.start_date,self.end_date),as_dict=True)[0]
            frappe.db.set_value("Employee",empid.employee,"non_present_days",absent_days['count'] + leave_days['count'] + (absent_half_days['count']/2))
            

class CustomLeaveApplication(LeaveApplication):
    def before_save(self):
        # self.attendance_hours_empty()
        self.validation_leave_application()
        self.attendance_validation() 
        attendance = frappe.db.get_value('Attendance',{'employee':self.employee,'attendance_date':self.from_date},['permission_request'])
        if attendance:
            frappe.throw(_("Employee Permission and Leave can not Applied same Time"))
            frappe.validated = False
          
    def attendance_hours_empty(self):
        attendance = frappe.db.sql(""" select name,employee,attendance_date,in_time,out_time from `tabAttendance` where employee = '%s' and attendance_date between '%s' and '%s' and status = 'Absent' and docstatus != '2' """%(self.employee,self.from_date,self.to_date),as_dict=1) 
        for att in attendance:  
            if att.in_time == None and att.out_time == None:
                get_att = frappe.get_doc('Attendance',{'name':att.name})
                get_att.total_wh = '00:00'
                get_att.extra_hours = '00:00'
                get_att.late_hours = '00:00'
                get_att.save(ignore_permissions=TRUE) 
                frappe.db.commit()  
            else:
                frappe.log_error('Attendance not Absent',att.attendance_date)   

    def validation_leave_application(self):
        if self.leave_type == 'Maternity Leave' or self.leave_type == 'Paternity Leave':
            employee = frappe.db.get_value('Employee',{'status':'Active'},['no_of_kids'])
            if employee:
                if employee >= 2:
                    frappe.throw(_("Materity or Paternity Leave allowed for Less than 2 Kids"))
                    frappe.validated = False
            else:
                frappe.log_error('Employee has no Kids')  

    def attendance_validation(self):
        attendance = frappe.db.sql(""" select name from `tabAttendance` where attendance_date between '%s' and '%s' and employee = '%s'   """%(self.from_date,self.to_date,self.employee),as_dict=1)
        if attendance:
            att = frappe.db.get_value('Attendance',{'name':attendance[0]['name']},['status','on_duty_marked'])  
            if att[0] == 'Present' and att[1]:
                frappe.throw(_('Employee %s is already between %s and %s marked attendance as Present with On Duty'%(self.employee,self.from_date,self.to_date)))    
            elif att[0] == 'Present':
                frappe.throw(_('Employee %s is already between %s and %s marked attendance as Present'%(self.employee,self.from_date,self.to_date)))    

   
            
class CustomLeaveAllocation(LeaveAllocation):
    def before_save(self):
        self.validation_leave_allocation()

    def validation_leave_allocation(self):
        if self.leave_type == 'Maternity Leave' or self.leave_type == 'Paternity Leave':
            employee = frappe.db.get_value('Employee',{'status':'Active'},['no_of_kids'])
            if employee:
                if employee >= 2:
                    frappe.throw(_("Materity or Paternity Leave allowed for Less than 2 Kids"))
                    frappe.validated = False
            else:
                frappe.log_error('Employee has no Kids')      







