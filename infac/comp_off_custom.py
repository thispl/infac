import frappe
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

                    
def check_holiday(from_date,to_date,emp):
    holiday_list = frappe.db.get_value('Employee',emp,'holiday_list')
    holiday = frappe.db.sql("""select `tabHoliday`.holiday_date,`tabHoliday`.weekly_off from `tabHoliday List` 
    left join `tabHoliday` on `tabHoliday`.parent = `tabHoliday List`.name where `tabHoliday List`.name = '%s' and holiday_date between '%s' and '%s' """%(holiday_list,from_date,to_date),as_dict=True)
    if holiday:
        if holiday[0].weekly_off == 1:
            return "WW"
        else:
            return "HH"
    

@frappe.whitelist()
def validate_comp_off(doc, method):
        user_roles = frappe.get_roles(frappe.session.user)
        hr = "HR User" in user_roles
        # admin = "Administrator" in user_roles
        if (not hr):
            allowed_days1 = frappe.db.get_value("HR Time Settings", None, "comp_off_validation_dates")
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

            if not doc.work_from_date:
                return

            if isinstance(doc.work_from_date, str):
                miss_date = datetime.strptime(doc.work_from_date, "%Y-%m-%d").date()
            else:
                miss_date = doc.work_from_date

            if miss_date < earliest_allowed:
                frappe.throw(
                    _("Compensatory Leave Request applications are allowed only for up to the previous {0} working days.")
                    .format(allowed_days)
                )

