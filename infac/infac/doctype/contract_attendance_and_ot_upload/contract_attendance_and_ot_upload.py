# -*- coding: utf-8 -*-
# Copyright (c) 2021, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from calendar import monthrange
import frappe
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta
from frappe.utils import cint, flt, nowdate, add_days, getdate, fmt_money, add_to_date, DATE_FORMAT, date_diff, money_in_words
from frappe import _
import functools
from datetime import datetime, timedelta
from frappe.utils.csvutils import read_csv_content

class ContractAttendanceandOTUpload(Document):
    pass

@frappe.whitelist()
def get_end_date(start_date, frequency):
    start_date = getdate(start_date)
    frequency = frequency.lower() if frequency else 'monthly'
    kwargs = get_frequency_kwargs(frequency) if frequency != 'bimonthly' else get_frequency_kwargs('monthly')

    # weekly, fortnightly and daily intervals have fixed days so no problems
    end_date = add_to_date(start_date, **kwargs) - relativedelta(days=1)
    if frequency != 'bimonthly':
        return dict(end_date=end_date.strftime(DATE_FORMAT))

    else:
        return dict(end_date='')

def get_frequency_kwargs(frequency_name):
    frequency_dict = {
        'monthly': {'months': 1},
        'fortnightly': {'days': 14},
        'weekly': {'days': 7},
        'daily': {'days': 1}
    }
    return frequency_dict.get(frequency_name)

@frappe.whitelist()
def mark_attendance(file_url,start_date,end_date):
    #below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    #Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_url": file_url})
    #Path in the system
    filepath = get_file(file_url)
    #CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    for pp in pps:
        frappe.errprint(pp)
        holiday_list = frappe.db.get_value("Employee",{"name":pp[0]},["holiday_list"])
        holiday_map = frappe._dict()

        # for d in holiday_list:
        #     if d:
        holiday_list = frappe.db.sql('''select holiday_date from `tabHoliday`
            where parent=%s and holiday_date between %s and %s''', (holiday_list, start_date, end_date))
        holidays = []
        for holiday in holiday_list:
            holidays.append(holiday[0])
        import pandas as pd
        total_days = pd.date_range(start_date, end_date).tolist()
        day = 1
        for days in total_days:
            date = days.date()
            if date not in holidays:
                frappe.errprint(date)
                if int(pp[1]) >= day:
                    attendance = frappe.new_doc("Attendance")
                    attendance.update({
                        "employee":pp[0],
                        "attendance_date":date,
                        "status":"Absent"
                    }).save(ignore_permissions = True)
                    attendance.submit()
                    frappe.db.commit()
                    day = day+1
        # if int(pp[2])>0:
        ts = frappe.new_doc("Timesheet")
        ts.employee = pp[0]
        ts.append("time_logs",{
            "activity_type":"Overtime",
            "from_time":start_date,
            "hours":int(pp[2])
        })
        ts.save(ignore_permissions=True)
        ts.submit()
        frappe.db.commit()