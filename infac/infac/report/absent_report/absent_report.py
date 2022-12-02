# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

import frappe
import frappe
from frappe import _, msgprint
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form
from html2text import element_style


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data



def get_columns(filters):
    columns = [
        _('Employee') +':Data:100',_('Employee Name') +':Data:100',
    ]
    pass


def get_data(filters):
    pass
