# Copyright (c) 2023, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from email import utils
from frappe import _
from datetime import date, timedelta, datetime,time
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime,today, format_date)

class EvaluationTest(Document):
    pass


@frappe.whitelist()
def validate_phone_number(number):
    pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
    if bool(pattern.match(number)) == False:
        frappe.throw(_('Only Numeric Values Allowed'))
    elif int(number) > 10:
        frappe.throw(_('Numbers not greater than 10'))    

@frappe.whitelist()
def not_entered_past_date(past_date):
    current_date = date.today()
    if current_date > getdate(past_date):
        frappe.throw(_('Past not Selected'))



