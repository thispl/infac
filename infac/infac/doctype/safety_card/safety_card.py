# Copyright (c) 2026, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class SafetyCard(Document):
    def validate(self):
        today = getdate(nowdate())
        if self.return_date:
            self.status = "Closed"
        elif self.end_date and getdate(self.end_date) < today:
            self.status = "Overdue"
        else:
            self.status = "Active"
