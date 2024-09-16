# Copyright (c) 2023, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.csvutils import read_csv_content
from frappe.utils.background_jobs import enqueue


class BulkAttendanceRegularizeTool(Document):
	pass

  
