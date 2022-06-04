# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from warnings import filters
import frappe
import datetime
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from frappe.model.document import Document

class SinglePunchRegularization(Document):
	@frappe.whitelist()
	def get_employees(self):
		attendance = frappe.db.sql(""" select name,employee,attendance_date,permission_request,in_time,out_time from `tabAttendance` where attendance_date between '%s' and '%s' and employee_category = '%s'  """%(self.from_date,self.to_date,self.employee_category),as_dict=1)
		return attendance

@frappe.whitelist()
def single_punch_mark(att,out_time,name):
	frappe.db.set_value('Attendance',att,'out_time',out_time)
	frappe.db.set_value('Attendance',att,'status','Present')
	frappe.db.set_value('Attendance',att,'single_punch_marked',name)

		
