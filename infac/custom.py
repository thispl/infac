from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.data import today, add_days
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
