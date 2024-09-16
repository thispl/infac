# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
from frappe.utils import (
    add_days,
    add_months,
    add_years,
    cint,
    cstr,
    date_diff,
    flt,
    formatdate,
    get_last_day,
    get_timestamp,
    getdate,
    nowdate,
    today,
)


class AttendanceSettings(Document):
    

    def on_update(self):
        if self.employee and self.attendance_date:
            att = frappe.db.exists('Attendance',{'employee':self.employee,'attendance_date':self.attendance_date})
            if att:
                 frappe.db.sql(""" delete from `tabAttendance` where name = '%s' """%(att)) 

  