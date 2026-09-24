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
def permission_approval_12_25():
    permissions = frappe.get_all(
        "Permission Request",
        filters={
            "workflow_state": "Superior Pending",
            "docstatus": 0
        },
        pluck="name"
    )
    for name in permissions:
        doc = frappe.get_doc("Permission Request", name)
        doc.workflow_state = "Approved"
        doc.save(ignore_permissions=True)
        doc.submit()
        frappe.db.commit()

@frappe.whitelist()
def permission_approval_20_55():
    permissions = frappe.get_all(
        "Permission Request",
        filters={
            "workflow_state": "Superior Pending",
            "docstatus": 0
        },
        pluck="name"
    )
    for name in permissions:
        doc = frappe.get_doc("Permission Request", name)
        doc.workflow_state = "Approved"
        doc.save(ignore_permissions=True)
        doc.submit()
        frappe.db.commit()

@frappe.whitelist()
def permission_approval_03_15():
    permissions = frappe.get_all(
        "Permission Request",
        filters={
            "workflow_state": "Superior Pending",
            "docstatus": 0
        },
        pluck="name"
    )
    for name in permissions:
        doc = frappe.get_doc("Permission Request", name)
        doc.workflow_state = "Approved"
        doc.save(ignore_permissions=True)
        doc.submit()
        frappe.db.commit()

from frappe.model.workflow import apply_workflow

@frappe.whitelist()
def auto_approve_permission():
    permissions = frappe.get_all(
        "Permission Request",
        filters={
            "workflow_state": "Superior Pending",
            "docstatus": 0
        },
        pluck="name"
    )
    for name in permissions:
        doc = frappe.get_doc("Permission Request", name)
        doc.workflow_state = "Approved"
        doc.save(ignore_permissions=True)
        doc.submit()
        frappe.db.commit()



@frappe.whitelist()
def cron_failed_method():
    cutoff_time = datetime.now() - timedelta(minutes=5)
    failed_jobs = frappe.get_all(
        "Scheduled Job Log",
        filters={
            "status": "Failed",
            "creation": [">=", cutoff_time],
            "scheduled_job_type": ["!=", "video.update_youtube_data"]
        },
        fields=["scheduled_job_type"]
    )
    unique_job_types = set()
    for job in failed_jobs:
        unique_job_types.add(job['scheduled_job_type'])

    for job_type in unique_job_types:
        frappe.sendmail(
            recipients = ["pavithra.s@groupteampro.com","sivarenisha.m@groupteampro.com"],
            subject = 'Failed Cron List - INFAC',
            message = 'Dear Sir / Mam <br> Kindly find the below failed Scheduled Job  %s'%(job_type)
        )


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
def process_today_checkins_fast():
    from datetime import datetime, timedelta
    from frappe.utils import today, get_datetime

    dt = get_datetime(today())
    start_of_day = datetime.combine(dt.date(), datetime.min.time())
    end_of_day = datetime.combine(dt.date(), datetime.max.time())

    # Efficient SQL query instead of get_all
    records = frappe.db.sql("""
        SELECT name, employee, time, late_entry
        FROM `tabEmployee Checkin`
        WHERE log_type = 'IN'
        AND time BETWEEN %s AND %s
        ORDER BY employee ASC, time ASC
    """, (start_of_day, end_of_day), as_dict=True)

    if not records:
        return "No checkins today"

    current_emp = None
    first_done = False

    for r in records:
        # New employee block
        if r.employee != current_emp:
            current_emp = r.employee
            first_done = False

        # First IN
        if not first_done:
            first_done = True

            f_time = get_datetime(r.time)
            att_time = f_time.time()

            # Get shift
            shift = get_actual_shift_start(att_time)
            ass_shift = frappe.db.get_value("Shift Assignment",{"employee": r.employee, "start_date": ["<=", f_time.date()],"end_date": [">=", f_time.date()],"docstatus": 1 },"shift_type")

            existing_shift = frappe.db.get_value("Employee Checkin", r.name, "shift")

            # Only set if shift is found AND field is empty
            # if shift and not existing_shift:
            frappe.db.set_value("Employee Checkin", r.name, "shift", shift)
                
            frappe.db.set_value("Employee Checkin", r.name, "assigned_shift", ass_shift)

            # Compute late entry
            if shift:
                shift_start = frappe.db.get_value("Shift Type", shift, "start_time")

                if isinstance(shift_start, timedelta):
                    shift_start_time = (datetime.min + shift_start).time()
                else:
                    shift_start_time = shift_start

                grace_time = (
                    datetime.combine(f_time.date(), shift_start_time) +
                    timedelta(minutes=1)
                ).time()

                is_late = 1 if att_time >= grace_time else 0

                frappe.db.set_value("Employee Checkin", r.name, "late_entry", is_late)

        # Remaining INs
        # else:
        #     frappe.db.set_value("Employee Checkin", r.name, {
        #         "late_entry": 0,
        #         "shift": "",
        #         "assigned_shift":""
        #     })

    return "Processed successfully (FAST version)"

