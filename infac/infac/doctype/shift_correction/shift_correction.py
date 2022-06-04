# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from warnings import filters
import frappe
import datetime
from frappe.utils import cstr, add_days, date_diff, getdate, format_date
from frappe.model.document import Document


class ShiftCorrection(Document):

	@frappe.whitelist()
	def get_employees(self):
		# attendance = frappe.db.sql(""" select name,employee,attendance_date,shift from  `tabAttendance`  where attendance_date between '%s' and '%s' and employee_category = '%s'  """%(self.from_date,self.to_date,self.employee_category),as_dict=1)
		shift = frappe.db.sql("""select name,employee from `tabShift Assignment` where start_date between  %s   and employee_category = '%s' """%(self.from_date,self.employee_category),as_dict=1)
		# return attendance,shift
		return shift