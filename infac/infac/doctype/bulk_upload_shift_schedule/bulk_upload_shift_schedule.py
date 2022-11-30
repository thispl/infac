# Copyright (c) 2022, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from csv import writer
from inspect import getfile
from unicodedata import name
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file, upload
from frappe.model.document import Document
from datetime import datetime,timedelta,date,time
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from numpy import unicode_
from frappe.utils.background_jobs import enqueue



class BulkUploadShiftSchedule(Document):

    def on_submit(self): 
        shift = self.name
        frappe.log_error('Shift scheduele')
        enqueue(self.create_shift_assignment, queue='default', timeout=6000, event='create_shift_assignment',shift=shift) 

    
    # def enqueue_submit_schedule(self,docstatus,shift):
    #     if docstatus == "Approved":
    #         shift_assigned = frappe.get_all("Shift Assignment",{'shift_schedule':self.name,'docstatus':'0'})
    #         for shift in shift_assigned:
    #             doc = frappe.get_doc('Shift Assignment',shift.name)
    #             doc.submit()
    #             frappe.db.commit()
    #         frappe.msgprint('Shift Schedule Approved Successfully')

    #     elif docstatus == 'Rejected':
    #         shift_reject = frappe.db.get_all('Shift Assignment',{'shift_schedule':self.name,'docstatus':'0'})
    #         for shift in shift_reject:
    #             frappe.errprint(shift.name)
    #             frappe.delete_doc('Shift Assignment',shift.name)
    #         frappe.msgprint('Shift Schedule Rejected Successfully')  

    # def validate(self):
    #     enqueue(self.create_shift_assignment, queue='default', timeout=6000, event='create_shift_assignment')    

    def create_shift_assignment(self,shift):
        filepath = get_file(self.attach)
        pps = read_csv_content(filepath[1])
        dates = self.get_dates()
        for date in dates:
            for pp in pps:
                if pp[2] != 'Shift':
                    if pp[1]:
                        get_shift = frappe.db.exists("Shift Assignment",{'employee':pp[0],'start_date':date,'end_date':date,'docstatus':['in',[0,1]]})
                        if not get_shift:
                            doc = frappe.new_doc('Shift Assignment')
                            doc.employee = pp[0]
                            doc.shift_type = pp[2]
                            doc.department = pp[3]
                            doc.start_date = date
                            doc.end_date = date
                            doc.bulk_upload_shift = self.name
                            doc.save(ignore_permissions=True)
                            doc.submit()
                            frappe.db.commit()
                        else:
                            frappe.db.set_value('Shift Assignment',get_shift,'shift_type',pp[2])    

    def get_dates(self):
        no_of_days = date_diff(add_days(self.to_date, 1), self.from_date)
        dates = [add_days(self.from_date, i) for i in range(0, no_of_days)]
        return dates
    



@frappe.whitelist()
def get_template(from_date):
    args = frappe.local.form_dict

    if getdate(args.from_date) > getdate(args.to_date):
        frappe.throw(_("To Date should be greater than From Date"))

    w = UnicodeWriter()
    w = add_header(w)
    w = add_data(w, args,from_date)

    frappe.response['result'] = cstr(w.getvalue())
    frappe.response['type'] = 'csv'
    frappe.response['doctype'] = "Shift Assignment"

def add_header(w):
    w.writerow(['Employee ID','Employee Name','Shift','Department','Department Line'])
    return w

def add_data(w, args,from_date):
    data = get_data(args,from_date)
    writedata(w, data)
    return w

@frappe.whitelist()
def get_data(args,from_date):
    employees = frappe.get_all('Employee',{'status':'Active','department':args.department},['*'])
    data = []
    for emp in employees:
        previous_day = add_days(from_date,-2)
        shift = frappe.db.get_value('Shift Assignment',{'employee':emp.employee_number,'start_date':previous_day},['shift_type'])
        if shift:
            row = [emp.name,emp.employee_name,shift,emp.department,emp.department_line]
            data.append(row)    
        else:
            row = [emp.name,emp.employee_name,'G',emp.department,emp.department_line]
            data.append(row)  
    return data

@frappe.whitelist()
def writedata(w, data):
    for row in data:
        w.writerow(row)


