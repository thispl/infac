# # Copyright (c) 2025, teampro and contributors
# # For license information, please see license.txt

# from calendar import month
# import frappe
# from frappe.model.document import Document
# from frappe.monitor import start

# class DownloadSalarySlip(Document):
# 	@frappe.whitelist()
# 	def get_salary_slip(self):
# 		if self.month:
# 			# start_date = str(self.year) + '-' + str(month.get(self.month)) + '-21'
# 			end_date = str(self.year) + '-' + str(month.get(self.month)) + '-20'

# 		slips = frappe.db.sql("""select name from `tabSalary Slip` where end_date = '%s' and employee = '%s' and docstatus != 2 """%(end_date,self.employee_id),as_dict=True)
# 		return slips

# month = {
# 	'Jan':1,
# 	'Feb':2,
# 	'Mar':3,
# 	'Apr':4,
# 	'May':5,
# 	'Jun':6,
# 	'Jul':7,
# 	'Aug':8,
# 	'Sep':9,
# 	'Oct':10,
# 	'Nov':11,
# 	'Dec':12
# }



from calendar import month
import frappe
from frappe.model.document import Document

class DownloadSalarySlip(Document):

    @frappe.whitelist()
    def get_salary_slip(self):
        if self.month:
            end_date = str(self.year) + "-" + str(month.get(self.month)) + "-20"

        slips = frappe.db.sql("""
            SELECT name
            FROM `tabSalary Slip`
            WHERE end_date = %s
            AND employee = %s
            AND docstatus = 1
        """, (end_date, self.employee_id), as_dict=True)

        if not slips:
            frappe.throw("Salary Slip is not submitted for the selected month.")

        return slips


month = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}