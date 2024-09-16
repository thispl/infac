# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from datetime import date
import frappe
from frappe.model.document import Document
from frappe.utils.data import add_days, date_diff
from frappe.utils import cstr, cint, getdate,get_first_day, get_last_day, today, time_diff_in_hours   
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



class PayrollProcessSettings(Document):

	def validate(self):
		self.payroll_date_change_automatic()

	def payroll_date_change_automatic(self):	
		current_date = getdate(today())
		next_month = add_months(current_date,1)
		next_mon = next_month.month
		cur_day =  current_date.day
		cur_month = current_date.month
		cur_year = current_date.year
		next_year = add_years(current_date,1)
		next_year_date = next_year.year
		previous_date = getdate(self.payroll_end_date)
		pre_day = previous_date.day
		pre_month= previous_date.month
		pre_year = previous_date.year
		if cur_day > pre_day:
			payroll_start_period = frappe.db.get_single_value('Payroll Settings','payroll_start_period')
			payroll_end_period = frappe.db.get_single_value('Payroll Settings','payroll_end_period')
			if cur_month == int(12):
				start_date = str(payroll_start_period) + '-' + str(cur_month) + '-' + str(cur_year)
				end_date = str(payroll_end_period) + '-' + str(next_mon) + '-' + str(next_year_date)
				self.payroll_start_date = getdate(start_date)
				self.payroll_end_date = getdate(end_date)
			else:
				start_date = str(payroll_start_period) + '-' + str(cur_month) + '-' + str(cur_year)
				end_date = str(payroll_end_period) + '-' + str(next_mon) + '-' + str(cur_year)
				self.payroll_start_date = getdate(start_date)
				self.payroll_end_date = getdate(end_date)


			
