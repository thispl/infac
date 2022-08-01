# Copyright (c) 2021, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from csv import writer
from inspect import getfile
from pickle import EMPTY_DICT
from socket import fromfd
from tracemalloc import start
from unicodedata import name
from wsgiref.util import shift_path_info
import frappe
from frappe.utils import cstr, add_days, date_diff, getdate
from frappe import _
from frappe.utils.csvutils import UnicodeWriter, read_csv_content
from frappe.utils.file_manager import get_file, upload
from frappe.model.document import Document
from datetime import datetime,timedelta,date,time
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr
from frappe.utils.background_jobs import enqueue




class ShiftSchedule(Document):
    
    @frappe.whitelist()
    def on_submit(self):
        shift = self.name
        workflow_state = self.workflow_state
        enqueue(self.enqueue_submit_schedule, queue='default', timeout=6000, event='enqueue_submit_schedule',shift=shift,workflow_state=workflow_state)


    @frappe.whitelist()
    def enqueue_submit_schedule(self,workflow_state):
        if workflow_state == "Approved":
            shift_assigned = frappe.get_all("Shift Assignment",{'shift_schedule':self.name,'docstatus':'0'})
            for shift in shift_assigned:
                doc = frappe.get_doc('Shift Assignment',shift.name)
                doc.submit()
                frappe.db.commit()
            frappe.msgprint('Shift Schedule Approved Successfully')

        elif workflow_state == 'Rejected':
            shift_reject = frappe.db.get_all('Shift Assignment',{'shift_schedule':self.name,'docstatus':'0'})
            for shift in shift_reject:
                frappe.errprint(shift.name)
                frappe.delete_doc('Shift Assignment',shift.name)
            frappe.msgprint('Shift Schedule Rejected Successfully')    


    # def on_cancel(self):
    #     shift_cancel = frappe.db.get_all('Shift Assignment',{'shift_schedule':self.name,'docstatus':'1'})
    #     for shift in shift_cancel:
    #         frappe.delete_doc('Shift Assignment',shift.name)
    #     frappe.msgprint('Shift Schedule Rejected Successfully')


    def after_insert(self):
        self.number_of_employees = len(self.employee_details) 
        if(self.workflow_state == 'Pending For HR'):
            shift = self.upload_shift()
            frappe.msgprint('Shift Schedule Created')

    def upload_shift(self):
        dates = self.get_dates(self.from_date,self.to_date)
        for date in dates:
            for row in self.employee_details:
                if not frappe.db.exists('Shift Assignment',{'employee':row.employee,'start_date':date,'end_date':date,'docstatus':['in',[0,1]]}):
                    doc = frappe.new_doc('Shift Assignment')
                    doc.employee = row.employee
                    doc.shift_type = row.shift
                    doc.start_date = date
                    doc.end_date = date
                    doc.shift_schedule = self.name
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()  

     
               
    @frappe.whitelist()
    def get_employees(self):
        datalist = []
        data = {}
        previous_day_shift = add_days(self.from_date,-2)
        conditions = ''
        if self.department_line:
            conditions = "and department_line = '%s' " % self.department_line
        employees = frappe.db.sql("""select name,employee_name,department,department_line from `tabEmployee` where department = '%s' and status = 'Active' %s """%(self.department,conditions),as_dict=1)
        for emp in employees:
            shift = frappe.db.get_value('Shift Assignment',{'start_date':previous_day_shift,'department_line':emp['department_line'],'employee':emp['name']},['shift_type'])    
            if shift:
                data.update({
                    'employee':emp['name'],
                    'employee_name':emp['employee_name'],
                    'shift':shift
                })
                datalist.append(data.copy())
            else:
                data.update({
                    'employee':emp['name'],
                    'employee_name':emp['employee_name'],
                    'shift':"G"
                })
                datalist.append(data.copy())
        return datalist



    def get_dates(self,from_date,to_date):
        """get list of dates in between from date and to date"""
        no_of_days = date_diff(add_days(to_date, 1), from_date)
        dates = [add_days(from_date, i) for i in range(0, no_of_days)]
        return dates     

