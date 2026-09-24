# Copyright (c) 2026, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import format_date

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		_('Employee ID') + ":Link/Employee:120",
		_('Employee Name') + ':Data:200',
		_('Department') + ':Link/Department:150',
		_('Department Line') + ':Link/Department Line:150',
		_('Date') + ':Data:100',
		_('Shift') + ':Data:100',
		_('Actual Shift') + ':Data:100',
		_('Status') + ':Data:120',
	]
	return columns

def get_data(filters):
	data = []

	conditions = "att.attendance_date between %(from_date)s and %(to_date)s and att.docstatus < 2 and att.matched_status = 'Unmatched'"

	if filters.employee:
		conditions += " and att.employee = %(employee)s"

	if filters.employment_type:
		conditions += " and emp.employment_type = %(employment_type)s"

	attendance = frappe.db.sql("""
		select att.employee, att.employee_name, emp.department, emp.department_line,
			att.attendance_date, att.shift_type, att.actual_shift, att.matched_status
		from `tabAttendance` att
		left join `tabEmployee` emp on emp.name = att.employee
		where {conditions}
		order by att.attendance_date asc, att.employee asc
	""".format(conditions=conditions), filters, as_dict=True)

	for att in attendance:
		row = [
			att.employee,
			att.employee_name,
			att.department or '',
			att.department_line or '',
			format_date(att.attendance_date),
			att.shift_type or '',
			att.actual_shift or '',
			att.matched_status or '',
		]
		data.append(row)

	return data
