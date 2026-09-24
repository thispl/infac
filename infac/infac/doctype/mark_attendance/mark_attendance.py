# Copyright (c) 2026, abdulla.pi@groupteampro.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from infac.shift_attendance import mark_att_for_emp

class MarkAttendance(Document):
	def on_submit(self):
		if self.in_time:
			if not frappe.db.exists("Employee Checkin",{"employee":self.employee, "time":self.in_time}):
				checkin = frappe.new_doc("Employee Checkin")
				checkin.employee = self.employee
				checkin.time = self.in_time
				checkin.log_type = "IN"
				checkin.insert(ignore_permissions=True)
		if self.out_time:
			if not frappe.db.exists("Employee Checkin",{"employee":self.employee, "time":self.out_time}):
				checkin = frappe.new_doc("Employee Checkin")
				checkin.employee = self.employee
				checkin.time = self.out_time
				checkin.log_type = "OUT"
				checkin.insert(ignore_permissions=True)
		if self.in_time or self.out_time:
			mark_att_for_emp(self.date,self.date,self.employee)
		

