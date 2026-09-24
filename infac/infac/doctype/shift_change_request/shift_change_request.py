# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from copy import copy
from datetime import datetime
import frappe
from frappe.model.document import Document
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from frappe import _
from frappe.utils import getdate, today


class ShiftChangeRequest(Document):

    def validate(self):
        self.validate_past_dates()

    def validate_past_dates(self):
        if self.from_date and getdate(self.from_date) < getdate(today()):
            frappe.throw(_("From Date cannot be a past date."))

        if self.to_date and getdate(self.to_date) < getdate(today()):
            frappe.throw(_("To Date cannot be a past date."))

        if self.from_date and self.to_date and getdate(self.to_date) < getdate(self.from_date):
            frappe.throw(_("To Date cannot be before From Date."))

        if not self.has_value_changed("workflow_state"):
            return

        if self.has_value_changed("workflow_state") and self.workflow_state == "Approved":
            self.level_1_timing=now_datetime()
            self.level_1_approved_by=frappe.session.user

    def on_submit(self):
        get_shift = frappe.db.get_all('Shift Assignment',{'start_date':('between',(self.from_date,self.to_date)),'employee':self.employee},['name','shift_type'])
        for shift in get_shift:
            frappe.db.set_value('Shift Assignment',shift.name,'shift_type',self.shift_change)
        frappe.msgprint('Shift Changed successfully')

    def before_insert(self):
            current_user = frappe.session.user
            current_time = now_datetime()
            self.created_by = current_user  
            self.created_on= current_time 

@frappe.whitelist()
def get_shift_assignment(emp,from_date,to_date,name):
    datalist = []
    shift_assignment = frappe.db.get_all('Shift Assignment',{'start_date':('between',(from_date,to_date)),'employee':emp},['shift_type','name'])
    if shift_assignment:
        for shift in shift_assignment:
            datalist.append(shift.shift_type)
    else:
        message = 'Employee Have No Shift Assignment'
        datalist.append(frappe.throw(_(message)))  
    return datalist     