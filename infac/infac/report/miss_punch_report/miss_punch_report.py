# Copyright (c) 2013, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe import _, msgprint
from frappe.utils import get_first_day, today, get_last_day, format_datetime, add_years, date_diff, add_days, getdate, cint, format_date,get_url_to_form



def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
	columns = [
		_('Employee') +':Data:100',_('Employee Name') +':Data:150',_('Department') +':Data:150',_('Attendance Date') +':Data:150',
		_('Shift') +':Data:100',_('In Time') +':Data:150',_('Out Time') +':Data:150',_('Miss Punch') +':Data:120'
	]
	return columns

def get_data(filters):
	data = []
	if filters.employee:
		attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date)),'employee':filters.employee},['*'])
	else:
		attendance = frappe.db.get_all('Attendance',{'attendance_date':('between',(filters.from_date,filters.to_date))},['*'])
	for att in attendance:
		miss_punch = None
		if att.in_time and not att.out_time:
			miss_punch = 'Out Time'
		elif att.out_time and not att.in_time:
			miss_punch = 'In Time'
		if miss_punch:
			row = [att.employee,att.employee_name,att.department,format_date(att.attendance_date),att.shift,format_datetime(att.in_time) or '-',format_datetime(att.out_time) or '-',miss_punch]
			data.append(row)

	return data					
		




