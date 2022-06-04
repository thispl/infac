# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from codecs import ignore_errors
import frappe
from frappe import new_doc, permissions
from frappe.model.document import Document
from frappe import errprint, msgprint, _
from frappe.share import add
from numpy import True_


class MonthlyAllowanceApplication(Document):

	def on_update(self):
		allowance = frappe.db.get_all('Monthly Allowance Application',{'employee':self.employee,'payroll_date':self.payroll_date},['tds','other_allowances_1','other_allowances_2','other_allowances_3','other_allowances_4'])
		if allowance:
			add_salary = frappe.new_doc('Additional Salary')
			add_salary.employee = self.employee
			add_salary.payroll_date = self.payroll_date
			add_salary.salary_component = 'Tax Deducted At Source'
			add_salary.amount = self.tds
			add_salary.monthly_allowance = self.name
			add_salary.save(ignore_permissions = True)
			add_salary.submit()
			frappe.db.commit()
			
		
			
		if allowance:
			add_salary = frappe.new_doc('Additional Salary')
			add_salary.employee = self.employee
			add_salary.payroll_date = self.payroll_date
			add_salary.salary_component = 'Other Allowances 1'
			add_salary.amount = self.other_allowances_1
			add_salary.monthly_allowance = self.name
			add_salary.save(ignore_permissions = True)
			add_salary.submit()
			frappe.db.commit()

		if allowance:
			add_salary = frappe.new_doc('Additional Salary')
			add_salary.employee = self.employee
			add_salary.payroll_date = self.payroll_date
			add_salary.salary_component = 'Other Allowances 2'
			add_salary.amount = self.other_allowances_2
			add_salary.monthly_allowance = self.name
			add_salary.save(ignore_permissions = True)
			add_salary.submit()
			frappe.db.commit()

		if allowance:
			add_salary = frappe.new_doc('Additional Salary')
			add_salary.employee = self.employee
			add_salary.payroll_date = self.payroll_date
			add_salary.salary_component = 'Other Allowances 3'
			add_salary.amount = self.other_allowances_3
			add_salary.monthly_allowance = self.name
			add_salary.save(ignore_permissions = True)
			add_salary.submit()
			frappe.db.commit()

		if allowance:
			add_salary = frappe.new_doc('Additional Salary')
			add_salary.employee = self.employee
			add_salary.payroll_date = self.payroll_date
			add_salary.salary_component = 'Other Allowances 4'
			add_salary.amount = self.other_allowances_4
			add_salary.monthly_allowance = self.name
			add_salary.save(ignore_permissions = True)
			add_salary.submit()
			frappe.db.commit()

		if allowance:
			add_salary = frappe.new_doc('Additional Salary')
			add_salary.employee = self.employee
			add_salary.payroll_date = self.payroll_date
			add_salary.salary_component = 'Night Shift Allowance'
			add_salary.amount = self.three_hour_incentive
			add_salary.monthly_allowance = self.name
			add_salary.save(ignore_permissions = True)
			add_salary.submit()
			frappe.db.commit()		
				

		# if allowance:
		# 	add_salary = frappe.new_doc('Additional Salary')
		# 	add_salary.employee = self.employee
		# 	add_salary.payroll_date = self.payroll_date
		# 	add_salary.salary_component = '3 Hours Incentive'
		# 	add_salary.amount = self.three_hour_incentive
		# 	add_salary.save(ignore_permissions = True)
		# 	frappe.db.commit()		

		# if allowance:
		# 	add_salary = frappe.new_doc('Additional Salary')
		# 	add_salary.employee = self.employee
		# 	add_salary.payroll_date = self.payroll_date
		# 	add_salary.salary_component = '5 Hours Incentive'
		# 	add_salary.amount = self.five_hours_incentive
		# 	add_salary.save(ignore_permissions = True)
		# 	frappe.db.commit()	

		
				
				
		