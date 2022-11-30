# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from copy import copy
from datetime import datetime
import frappe
from frappe.model.document import Document
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from frappe import _


class ShiftChangeRequest(Document):

    

    def on_submit(self):
        get_shift = frappe.db.get_all('Shift Assignment',{'start_date':('between',(self.from_date,self.to_date)),'employee':self.employee},['name','shift_type'])
        for shift in get_shift:
            frappe.db.set_value('Shift Assignment',shift.name,'shift_type',self.shift_change)
        frappe.msgprint('Shift Changed successfully')

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