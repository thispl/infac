import frappe
from frappe.utils import time_diff_in_hours 
from frappe.utils.background_jobs import enqueue

from frappe.share import add, remove
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,today,get_time, format_date)
import datetime
from datetime import datetime   


@frappe.whitelist()
def additional_salary_validation(doc, method):
    add_sal = frappe.db.exists("Additional Salary",{"employee":doc.employee,"payroll_date":doc.payroll_date,"salary_component":doc.salary_component,"docstatus":1,"name":["!=",doc.name]})
    if add_sal:
        frappe.throw(frappe._(f"Additional Salary already exists for this Employee "
                f"{doc.employee}, Payroll Date {doc.payroll_date}"
                f" and Salary Component {doc.salary_component}."
            ))
        