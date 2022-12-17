# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file
from frappe.model.document import Document
from datetime import datetime,timedelta,date,time
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr



class MonthlyAllowanceBulkupload(Document):

	# @frappe.whitelist()
	# def get_template():
	# 	args = frappe.local.form_dict

	# 	w = UnicodeWriter()
    # 	w = add_header(w)
    # 	w = add_data(w, args)

	# 	frappe.response['result'] = cstr(w.getvalue())
    # 	frappe.response['type'] = 'csv'
    # 	frappe.response['doctype'] = "Monthly Allowance Application "

	# def add_header(w):
	# 	w.write_row['ID','Payroll Date','Salary Component','Amount']
	# 	return w

	# def add_data(w,args):
	# 	data = get_data(w)
	# 	writedata(w,data)
	# 	return w
	# 	pass

	# def get_data(w):
		pass


		
