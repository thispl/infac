from __future__ import print_function
from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from calendar import month_abbr
from decimal import ROUND_UP
from hmac import new
from itertools import count
from lib2to3.pytree import convert
from math import perm
from operator import neg
from pickle import TRUE
from re import A
import time
from frappe.utils.data import month_diff
from frappe.utils.file_manager import get_file
from datetime import timedelta
from time import strftime, strptime
from stat import FILE_ATTRIBUTE_REPARSE_POINT
from traceback import print_tb
from wsgiref.util import shift_path_info
# from tkinter.filedialog import SaveAs
import frappe
from frappe.utils import time_diff_in_hours 
from frappe.utils.background_jobs import enqueue

from frappe.share import add, remove
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,today,get_time, format_date)
import datetime
from datetime import datetime   
from datetime import timezone
from frappe.utils.csvutils import read_csv_content 
from frappe import permissions
from datetime import datetime,timedelta,date,time
from dateutil.relativedelta import relativedelta
from frappe.utils.user import get_user_fullname
import math
import pandas as pd
from frappe.utils import get_first_day, get_last_day, format_datetime, get_url_to_form
import dateutil.relativedelta
from frappe import throw,_
from frappe.model.rename_doc import rename_doc


@frappe.whitelist()
def inactive_employee(doc,method):
    if doc.status=="Active":
        if doc.relieving_date:
            throw(_("Please remove the relieving date for the Active Employee."))


@frappe.whitelist()
def add_salary_history(doc, method):
    """Add a new row to Salary History when any salary component changes.
    Works for manual updates and bulk import."""
    # if not doc.get("__islocal__"):
    #     salary_fields = [
    #         "basic", "hra", "gross_salary", "special_allowance", "conveyance_allowance",
    #         "welfare_allowance_amount", "attendance_bonus", "higher_education_allowance_amount",
    #         "supr_allowance", "other_allowances", "proposed_salary", "performance_allowance",
    #         "medical_allowance", "heat_allowance", "grade_allowance", "fixed_salary", "washing_allowance" ]
    #     updated = False
    #     for f in salary_fields:
    #         if f in doc.changed_values:
    #             updated = True
    #             break
    #     if updated:
    #         row = doc.append("salary_history", {})
    #         row.effective_date = frappe.utils.nowdate()
    #         row.basic = doc.basic or 0
    #         row.hra = doc.hra or 0
    #         row.gross_salary = doc.gross_salary or 0
    #         row.special_allowance = doc.special_allowance or 0
    #         row.conveyance_allowance = doc.conveyance_allowance or 0
    #         row.welfare_allowance = doc.welfare_allowance_amount or 0
    #         row.attendance_bonus = doc.attendance_bonus or 0
    #         row.higher_education_allowance = doc.higher_education_allowance_amount or 0
    #         row.supervisory_allowance = doc.supr_allowance or 0
    #         row.other_allowance = doc.other_allowances or 0
    #         row.proposed_salary = doc.proposed_salary or 0
    #         row.performance_allowance = doc.performance_allowance or 0
    #         row.medical_allowance = doc.medical_allowance or 0
    #         row.heat_allowance = doc.heat_allowance or 0
    #         row.grade_allowance = doc.grade_allowance or 0
    #         row.fixed_salary = doc.fixed_salary or 0
    #         row.washing_allowance = doc.washing_allowance or 0
    # if doc.get("__islocal__"):
    if not doc.name or doc.is_new():
        return
    
    else:
        salary_fields = [
            "basic", "hra", "gross_salary", "special_allowance", "conveyance_allowance",
            "welfare_allowance_amount", "attendance_bonus", "higher_education_allowance_amount",
            "supr_allowance", "other_allowances", "proposed_salary", "performance_allowance",
            "medical_allowance", "heat_allowance", "grade_allowance", "fixed_salary", "washing_allowance"
        ]

        old_doc = frappe.get_doc("Employee", doc.name)
        updated = False
        for f in salary_fields:
            old_value = old_doc.get(f) or 0
            new_value = doc.get(f) or 0
            if old_value != new_value:
                updated = True
                break
        if updated:
            row = doc.append("salary_history", {})
            row.effective_date = nowdate()
            for f in salary_fields:
                row.set(f, old_doc.get(f) or 0)

@frappe.whitelist()
def update_employee_no(name,employee_number):
    emp = frappe.get_doc("Employee",name)
    emps=frappe.get_all("Employee",{"status":"Active"},['*'])
    for i in emps:
        if emp.employee_number == employee_number:
            pass
        elif i.employee_number == employee_number:
            frappe.throw(f"Employee Number already exists for {i.name}")
        else:
            frappe.db.set_value("Employee",name,"employee_number",employee_number)
            frappe.rename_doc("Employee", name, employee_number, force=1)
            return employee_number



import frappe
from frappe.utils import getdate, nowdate, add_days
from datetime import timedelta

@frappe.whitelist()
def create_initial_attendance_and_shift(doc, method=None):

    if not doc.date_of_joining:
        return

    doj = getdate(doc.date_of_joining)
    current_date = getdate(nowdate())

    create_attendance_records(doc, doj, current_date)
    create_shift_assignment(doc, doj)

@frappe.whitelist()
def create_attendance_records(employee, from_date, to_date):

    current = from_date

    while current <= to_date:

        # Skip Sunday
        if current.weekday() == 6:
            current = add_days(current, 1)
            continue

        if not frappe.db.exists(
            "Attendance",
            {
                "employee": employee.name,
                "attendance_date": current
            }
        ):

            att = frappe.new_doc("Attendance")
            att.employee = employee.name
            att.employee_name = employee.employee_name
            att.attendance_date = current
            att.status = "Present"
            att.insert(ignore_permissions=True)

        current = add_days(current, 1)

# @frappe.whitelist()
# def create_shift_assignment(employee, doj):

#     # if not employee.default_shift:
#     #     return

#     # Saturday as week end
#     # Monday=0, Tuesday=1, ..., Saturday=5, Sunday=6
#     weekday = doj.weekday()

#     days_to_saturday = 5 - weekday

#     if days_to_saturday < 0:
#         days_to_saturday += 7

#     week_end = add_days(doj, days_to_saturday)

#     if frappe.db.exists(
#         "Shift Assignment",
#         {
#             "employee": employee.name,
#             "start_date": doj
#         }
#     ):
#         return

#     shift = frappe.new_doc("Shift Assignment")
#     shift.employee = employee.name
#     shift.shift_type = "G"
#     shift.start_date = doj
#     shift.end_date = week_end
#     shift.insert(ignore_permissions=True)
#     shift.submit()



import frappe
from frappe.utils import getdate, add_days

@frappe.whitelist()
def create_shift_assignment(doc, doj):

    employee = doc.name

    doj = getdate(doj)

    days_to_saturday = (5 - doj.weekday()) % 7
    end_date = add_days(doj, days_to_saturday)

    current_date = doj

    while current_date <= end_date:

        if not frappe.db.exists(
            "Shift Assignment",
            {
                "employee": employee,
                "start_date": current_date
            }
        ):

            shift = frappe.new_doc("Shift Assignment")
            shift.employee = employee
            shift.shift_type = "G"
            shift.start_date = current_date
            shift.end_date = current_date
            shift.insert(ignore_permissions=True)
            shift.submit()

        current_date = add_days(current_date, 1)

# @frappe.whitelist()
# def create_shift_assignment(employee, doj):

#     current_date = getdate(today())
#     doj = getdate(doj)

#     while doj <= current_date:

#         if not frappe.db.exists(
#             "Shift Assignment",
#             {
#                 "employee": employee.name,
#                 "start_date": doj
#             }
#         ):

#             shift = frappe.new_doc("Shift Assignment")
#             shift.employee = employee.name
#             shift.shift_type = "G"
#             shift.start_date = doj
#             shift.end_date = doj    
#             shift.insert(ignore_permissions=True)
#             shift.submit()

#         doj = add_days(doj, 1)

@frappe.whitelist()
def validate_employee_creation(doc, method=None):
    if not doc.is_new():
        return

    if not doc.date_of_joining:
        return

    doj = getdate(doc.date_of_joining)
    today = getdate(nowdate())

    days_diff = (today - doj).days

    creation_limit = frappe.db.get_single_value(
        "HR Time Settings",
        "employee_creation_limit"
    ) or 1

    if days_diff > int(creation_limit):
        frappe.throw(
            _(
                "Employee record must be created within {0} day(s) from the Date of Joining. "
                "DOJ: {1}, Current Date: {2}"
            ).format(creation_limit, doj, today)
        )

    #         if days_diff > 1:
    #             frappe.throw(
    #                 _("Employee record must be created on the Date of Joining or the next day. "
    #                 "DOJ: {0}, Current Date: {1}").format(doj, today)
    #             )

@frappe.whitelist()
def cancel_shift_assignment_on_left(doc, method=None):
    if doc.status != "Left":
        return

    if not doc.relieving_date:
        return

    relieving_date = getdate(doc.relieving_date)
    cancel_from_date = add_days(relieving_date, 1)

    shift_assignments = frappe.get_all(
        "Shift Assignment",
        filters={
            "employee": doc.name,
            "docstatus": 1,
            "start_date": [">=", cancel_from_date]
        },
        fields=["name", "start_date", "end_date"]
    )

    cancelled_count = 0

    for shift in shift_assignments:
        shift_doc = frappe.get_doc("Shift Assignment", shift.name)
        shift_doc.cancel()
        cancelled_count += 1

    if cancelled_count:
        frappe.msgprint(
            _("{0} Shift Assignment(s) cancelled from {1}.").format(
                cancelled_count,
                frappe.utils.formatdate(cancel_from_date)
            ),
            title=_("Shift Assignment Cancelled"),
            indicator="green"
        )