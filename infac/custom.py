from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils.data import today, add_days
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
    nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime
from frappe.utils.csvutils import read_csv_content
from six.moves import range
from six import string_types
import frappe
import json
from datetime import datetime
from calendar import monthrange
from frappe import _, msgprint
from frappe.utils import flt
from frappe.utils import cstr, cint, getdate
from datetime import date

@frappe.whitelist()
def el_leave_policy():
    employees =frappe.get_all("Employee",{"employee_group":"WC"},["name","employee_name","personal_email"])
    for emp in employees:
        print(emp.name)
        count = 0
        el = 0
        today = nowdate.month
        # start_date = add_months(today, -12)
        # end_date = add_days(today, -1)
        # print(end_date)
        # print(start_date)
        for att in (frappe.db.sql("""select status,attendance_date from `tabAttendance` where month(attendance_date) = %s and year(attendance_date) = %s'  """ %(month(today),year(today)),as_dict=True)):
            print(att)
            if (att.status == "Present"):
                count += 1
            else:
                count = 0
            # print(count)
            if count >= 20:
                el = count // 20 + el
                count = 0
                break  
        print(el)
        print(datetime.today().date())
        get_la = frappe.new_doc("Leave Allocation")
        get_la.employee = emp.name
        get_la.leave_type = "Earned Leave"
        get_la.from_date = datetime.today().date()
        get_la.to_date = add_months(datetime.today().date(), 12)
        get_la.new_leaves_allocated = (int(el))
        get_la.save(ignore_permissions = True)
        frappe.db.commit()