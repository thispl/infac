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
def validate_leave(doc, method):
    user_roles = frappe.get_roles(frappe.session.user)
    hr = "HR User" in user_roles
    # admin = "Administrator" in user_roles
    if (not hr):
        allowed_days1 = frappe.db.get_value("HR Time Settings", None, "leave_validation_dates")
        allowed_days = int(allowed_days1 or 0)
        current_date = today()
        if isinstance(current_date, str):
            current_date = datetime.strptime(current_date, "%Y-%m-%d").date()

        def is_working_day(check_date):
            return not check_holiday(check_date,check_date, doc.employee)

        days_count = 0
        earliest_allowed = current_date
        while days_count < allowed_days:
            earliest_allowed = add_days(earliest_allowed, -1)
            if is_working_day(earliest_allowed):
                days_count += 1

        if not doc.to_date:
            return

        if isinstance(doc.to_date, str):
            miss_date = datetime.strptime(doc.to_date, "%Y-%m-%d").date()
        else:
            miss_date = doc.to_date

        if miss_date < earliest_allowed:
            frappe.throw(
                _("Leave applications are allowed only for up to the previous {0} working days.")
                .format(allowed_days)
            )

def check_holiday(from_date,to_date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date between '%s' and '%s' """%(holiday_list,from_date,to_date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"
    


def update_status_on_workflow(doc, method):

    if doc.workflow_state == "Approved":
        doc.status = "Approved"
    elif doc.workflow_state == "Rejected":
        doc.status = "Rejected"

def while_cancel(doc, method):
    doc.status = "Cancelled"
    doc.db_update()

@frappe.whitelist()
def validate_halfday_leave(doc, method):
    if doc.half_day:
        existing_leave = frappe.db.exists("Leave Application", {"employee": doc.employee,"from_date": doc.from_date,"to_date": doc.to_date,"leave_type": doc.leave_type,"half_day": 1,"docstatus": ["!=", 2],"name": ["!=", doc.name] })
        if existing_leave:
            frappe.throw(_("You have already applied a Half-Day leave for this date with the same Leave Type."),
                frappe.ValidationError
            )

@frappe.whitelist()
def leave_approval_tracking(doc, method):
    # Run only if workflow_state changed
    if not doc.has_value_changed("workflow_state"):
        return

    current_user = frappe.session.user
    current_time = now_datetime()

    # Level 1 Approval
    if doc.workflow_state == "Superior Pending":
        doc.level_1_timing = current_time
        doc.level_1_approved_by = current_user

    # Level 2 Approval (Final Approval)
    elif doc.workflow_state == "Approved":
        doc.level_2_timing = current_time
        doc.level_2_approved_by = current_user

    # Rejected حالة
    elif doc.workflow_state == "Rejected":
        doc.rejected_timing = current_time
        doc.rejected_by = current_user

@frappe.whitelist()  
def creation_update(doc, method):
        current_user = frappe.session.user
        current_time = now_datetime()
        doc.created_by = current_user  
        doc.created_on= current_time 

@frappe.whitelist()
def show_html(from_date=None, to_date=None):
    html = "<h2><center>Leave Application</center></h2><table class='table table-bordered'><tr><th style=font-size:16px;>From Date</th><th style=font-size:16px;>To Date</th></tr><tr><td><h3>%s</h3></td><td><h3>%s</h3></td></tr></table>" % (
        frappe.utils.format_date(from_date),
        frappe.utils.format_date(to_date)
    )
    return html

def on_update(doc, method):
    pass 
import frappe
from frappe import _
from frappe.model.workflow import apply_workflow

@frappe.whitelist()
def incharge_approve(docname, approved_through):
    doc = frappe.get_doc("Leave Application", docname)
    doc.db_set("approved_through", approved_through, update_modified=True)
    apply_workflow(doc, "Approve")
    frappe.db.commit()
    return {"status": "success"}