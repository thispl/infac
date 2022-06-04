import frappe
from frappe import _
from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip
from erpnext.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry

from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day
from erpnext.hr.utils import validate_dates, validate_overlap, get_leave_period, \
    get_holidays_for_employee, create_additional_leave_ledger_entry

class CustomSalarySlip(SalarySlip):
    def after_save(self):
        absent_days = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status in ('Absent','On Leave') and attendance_date between '%s' and '%s' and docstatus = 1""" % (self.employee,self.start_date,self.end_date),as_dict=True)[0]
        absent_half_days = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status in ('Half Day') and attendance_date between '%s' and '%s' and docstatus = 1""" % (self.employee,self.start_date,self.end_date),as_dict=True)[0]
        self.absent_days = absent_days['count'] + (absent_half_days['count']/2)
        self.payment_days = self.arrear_payment_days + self.payment_days
        



class CustomPayrollEntry(PayrollEntry):
    def validate(self):
        self.number_of_employees = len(self.employees)
        for emp in self.employees:
            empid = frappe.get_doc('Employee',emp.employee)
            absent_days = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status in ('Absent','On Leave') and attendance_date between '%s' and '%s' and docstatus = 1""" % (empid.employee,self.start_date,self.end_date),as_dict=True)[0]
            absent_half_days = frappe.db.sql(""" select count(*) as count from `tabAttendance` where employee='%s' and status in ('Half Day') and attendance_date between '%s' and '%s' and docstatus = 1""" % (emp.employee,self.start_date,self.end_date),as_dict=True)[0]
            frappe.db.set_value("Employee",empid.employee,"non_present_days",absent_days['count'] + (absent_half_days['count']/2))