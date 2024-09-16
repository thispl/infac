# Copyright (c) 2023, teampro and contributors
# For license information, please see license.txt


from __future__ import print_function
import frappe
from frappe.model.document import Document
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

class PayrollDatesAutomatic(Document):
	pass

@frappe.whitelist()
def create_hooks():
    job = frappe.db.exists('Scheduled Job Type', 'payroll_date_automatic_upt')
    if not job:
        sjt = frappe.new_doc("Scheduled Job Type")  
        sjt.update({
            "method" : 'infac.infac.doctype.payroll_dates_automatic.payroll_dates_automatic.payroll_date_automatic',
            "frequency" : 'Cron',
            "cron_format" : '0 7 21 * *'
        })
        sjt.save(ignore_permissions=True)


@frappe.whitelist()
def payroll_date_automatic():
    # today = getdate('2023-01-21')
    today = getdate(datetime.now())
    cur_day = today.day
    if cur_day == 21:
        month = today.month
        month_start = datetime.strftime(today, '%B')
        next_month = today.month + 1
        if next_month > 12:
            next_month = 1
            year = today.year + 1
        else:
            year = today.year
        next_month_20th = getdate(datetime(year, next_month, 20))
        month_end = datetime.strftime(next_month_20th, '%B')
        frappe.db.set_value('Payroll Dates Automatic','PAYDATE0001','payroll_start_date',today)
        frappe.db.set_value('Payroll Dates Automatic','PAYDATE0001','payroll_end_date',next_month_20th)
        frappe.db.set_value('Payroll Dates Automatic','PAYDATE0001','month_start',month_start)
        frappe.db.set_value('Payroll Dates Automatic','PAYDATE0001','month_end',month_end)
