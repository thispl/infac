# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from datetime import date
from email import message
import queue
from xmlrpc.client import FastParser
import frappe
from frappe.model.document import Document
from frappe.utils.data import add_days, date_diff
from frappe.utils.background_jobs import enqueue


class PayrollProcessSettings(Document):
	pass

