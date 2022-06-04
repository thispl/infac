import frappe
from frappe.utils.csvutils import read_csv_content
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
        nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime, format_date)

@frappe.whitelist()
def bulk_shift_assignment_from_csv(filename):
    # below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    # Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    # Path in the system
    filepath = get_file(filename)
    # CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    for pp in pps:
        print(pp[0])
        date = '2022-03-09'
        d = 1
        for i in range(9):
            print(date)
            print(pp[d])
            if pp[d] not in ('-',None):
                if not frappe.db.exists('Shift Assignment',{'employee':pp[0],'start_date':date}):
                    doc = frappe.new_doc('Shift Assignment')
                    doc.employee = pp[0]
                    doc.start_date = date,
                    doc.end_date = date
                    doc.shift_type  = pp[d]
                    doc.save(ignore_permissions=True)
            date = add_days(date,1)
            d += 1