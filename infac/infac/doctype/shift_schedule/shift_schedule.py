# Copyright (c) 2021, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from csv import writer
from inspect import getfile
from socket import fromfd
from unicodedata import name
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file, upload
from frappe.model.document import Document
from erpnext.hr.doctype.employee.employee import Employee, get_holiday_list_for_employee
from erpnext.hr.utils import get_holidays_for_employee
from datetime import datetime,timedelta,date,time
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from numpy import unicode_


class ShiftSchedule(Document):

    def on_submit(self): 
        if self.upload:
            self.create_shift_assignment()

    def create_shift_assignment(self):
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])
        dates = self.get_dates(self.from_date,self.to_date)
        for date in dates:
            for pp in pps:
                frappe.errprint(pp[2])
                if pp[2] != 'Shift':
                    if pp[1]:
                        if not frappe.db.exists("Shift Assignment",{'employee':pp[0],'start_date':date,'end_date':date,'docstatus':['in',[0,1]]}):
                            doc = frappe.new_doc('Shift Assignment')
                            doc.employee = pp[0]
                            doc.shift_type = pp[2]
                            doc.start_date = date
                            doc.end_date = date
                            doc.shift_schedule = self.name
                            doc.submit()
                            doc.save(ignore_permissions=True)
                            frappe.db.commit()

    # def validate():
    #     pass                        
    
    def get_dates(self,from_date,to_date):
        """get list of dates in between from date and to date"""
        no_of_days = date_diff(add_days(to_date, 1), from_date)
        dates = [add_days(from_date, i) for i in range(0, no_of_days)]
        return dates 

    # @frappe.whitelist()
    # def show_summary(self):
    #     filepath = get_file(self.upload)
    #     pps = read_csv_content(filepath[1]) 
    #     data = ''
    #     master_staff = 0
    #     master_worker = 0
    #     workers_grade_2 = 0
    #     supporting_staff = 0
    #     operating_staff = 0
    #     management = 0
    #     general_motors = 0
    #     drivers = 0
    #     hmi_trainess = 0
    #     hirco_cook = 0
    #     diploma_trainees = 0
    #     classic_service = 0
    #     classic_hk = 0
    #     be_trainees = 0
    #     naps_get = 0
    #     naps_gat = 0
    #     naps_det = 0
    #     naps_dat = 0
    #     for pp in pps:
    #         if pp[4] == 'Master Staff':






@frappe.whitelist()
def get_template():
    args = frappe.local.form_dict

    if getdate(args.from_date) > getdate(args.to_date):
        frappe.throw(_("To Date should be greater than From Date"))

    w = UnicodeWriter()
    w = add_header(w)
    w = add_data(w, args)
   
    frappe.response['result'] = cstr(w.getvalue())
    frappe.response['type'] = 'csv'
    frappe.response['doctype'] = "Shift Assignment"

def add_header(w):
    w.writerow(["ID",'Employee Name','Shift'])
    return w

def add_data(w, args):
    data = get_data(args)
    writedata(w, data)
    return w

@frappe.whitelist()
def get_data(args):
    employees = frappe.get_all('Employee',{'status':'Active','department':args.department,},['name','employee_name'])
    data = []
    for employee in employees:
        row = [
            employee.name,employee.employee_name
        ]
        data.append(row)    
    return data



@frappe.whitelist()
def writedata(w, data):
    for row in data:
        w.writerow(row)


        
