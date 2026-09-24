# Copyright (c) 2021, teampro and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from csv import writer
from inspect import getfile
from pickle import EMPTY_DICT
from socket import fromfd, timeout
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
    
    # def on_submit(self):
    #     shift = self.name
    #     workflow_state = self.workflow_state
    #     enqueue(self.enqueue_submit_schedule, queue='default', timeout=6000, event='enqueue_submit_schedule',shift=shift,workflow_state=workflow_state)


    # def enqueue_submit_schedule(self,workflow_state,shift):
    #     frappe.log_error('Shift Schedule')
    #     if workflow_state == "Approved":
    #         shift_assigned = frappe.get_all("Shift Assignment",{'shift_schedule':self.name,'docstatus':'0'})
    #         for shift in shift_assigned:
    #             doc = frappe.get_doc('Shift Assignment',shift.name)
    #             doc.submit()
    #             frappe.db.commit()
    #         frappe.msgprint('Shift Schedule Approved Successfully')

    #     elif workflow_state == 'Rejected':
    #         shift_reject = frappe.db.get_all('Shift Assignment',{'shift_schedule':self.name,'docstatus':'0'})
    #         for shift in shift_reject:
    #             frappe.errprint(shift.name)
    #             frappe.delete_doc('Shift Assignment',shift.name)
    #         frappe.msgprint('Shift Schedule Rejected Successfully')    

    def on_submit(self):
        ss = self.name
        fd = self.from_date
        td = self.to_date
        file = self.upload
        workflow_state = self.workflow_state
        enqueue(
            self.enqueue_submit_schedule,
            queue='default',
            timeout=6000,
            event='enqueue_submit_schedule',
            ss=ss, fd=fd, td=td, file=file, workflow_state=workflow_state
        )

    def enqueue_submit_schedule(self, ss, workflow_state, fd, td, file):
        if workflow_state == "Approved":
            filepath = get_file(file)
            pps = read_csv_content(filepath[1])
            no_of_days = date_diff(add_days(td, 1), fd)
            dates = [add_days(fd, i) for i in range(0, no_of_days)]

            for pp in pps:
                if pp[4] and pp[4] != 'Shift':
                    for date in dates:
                        if not frappe.db.exists(
                            "Shift Assignment",
                            {
                                'employee': pp[0],
                                'start_date': date,
                                'end_date': date,
                                'docstatus': ['in', [0, 1]]
                            }
                        ):
                            doc = frappe.new_doc("Shift Assignment")
                            doc.employee = pp[0]
                            doc.department = pp[2]
                            doc.employment_type = pp[3]
                            doc.shift_type = pp[4]
                            doc.start_date = date
                            doc.end_date = date
                            doc.shift_schedule = ss
                            doc.save(ignore_permissions=True)
                            doc.submit()
                            frappe.db.commit()

  
    def validate(self):
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])
        dates = self.get_dates(self.from_date, self.to_date)
        emp_list = []
        error_messages = []

        if self.is_new():
            for date in dates:
                if frappe.db.exists("Shift Schedule", {
                    "from_date": ["<=", date],
                    "to_date": [">=", date],
                    "department": self.department,
                    "docstatus": ["!=", 2]
                }):
                    frappe.throw(_(f"Shift Schedule already exists for {self.department} on {date}"))
        for pp in pps:
            if pp[0] == "ID":
                continue

            emp_list.append(pp[0])
            emp_id, emp_name, department, employment_type, shift = pp[0], pp[1], pp[2], pp[3], pp[4]

            if emp_list.count(emp_id) > 1:
                error_messages.append(f"<li>Employee ID <b>{emp_id}</b> appears multiple times in the sheet.</li>")

            if not frappe.db.exists("Employee", {"name": emp_id, "status": "Active"}):
                error_messages.append(f"<li><b>{emp_id}</b> is not an Active Employee.</li>")
                continue

            emp_department = frappe.db.get_value("Employee", emp_id, "department")
            emp_employment_type = frappe.db.get_value("Employee", emp_id, "employment_type")

            if employment_type != emp_employment_type:
                error_messages.append(f"<li>{emp_id}-{emp_name} is not assigned to {employment_type} Employment Type</li>")
            if department != emp_department:
                error_messages.append(f"<li>{emp_id}-{emp_name} is not assigned to {department} Department</li>")

            if not shift:
                error_messages.append(f"<li>Shift value missing for <b>{emp_id}</b> in the upload sheet.</li>")
            else:
                for date in dates:
                    sa = frappe.db.exists( "Shift Assignment", {"employee": emp_id, "start_date": ["between", [self.from_date, self.to_date]],"docstatus": ["!=", 2] })
                    if sa:
                        sa_dept = frappe.db.get_value("Shift Assignment", sa, "department")
                        error_messages.append(
                            f"<li>{sa_dept} department already allocated shift for <b>{emp_id}</b> between {self.from_date} and {self.to_date}</li>"
                        )
                    # sa = frappe.db.exists("Shift Assignment", {"employee": emp_id, "start_date": date, "docstatus": ["!=", 2]})
                    # if sa:
                    #     sa_dept = frappe.db.get_value("Shift Assignment", sa, "department")
                    #     error_messages.append(f"<li>{sa_dept} department already allocated shift for <b>{emp_id}</b> on {date}</li>")

        if error_messages:
            frappe.throw("<br>".join(error_messages))

        if self.upload:
            self.number_of_employees = self.calculate_total_employees()
    
    def on_cancel(self):
        """
        Cancel all Shift Assignments linked to this Shift Schedule.
        """
        assignments = frappe.get_all(
            "Shift Assignment",
            filters={"shift_schedule": self.name, "docstatus": 1},
            fields=["name"]
        )

        for assignment in assignments:
            try:
                doc = frappe.get_doc("Shift Assignment", assignment.name)
                doc.cancel()
                frappe.db.commit()
            except Exception as e:
                frappe.log_error(f"Failed to cancel Shift Assignment {assignment.name}: {str(e)}")

        frappe.msgprint(f"All Shift Assignments linked to {self.name} have been cancelled.")



    # def on_cancel(self):
    #     shift_cancel = frappe.db.get_all('Shift Assignment',{'shift_schedule':self.name,'docstatus':'1'})
    #     for shift in shift_cancel:
    #         frappe.delete_doc('Shift Assignment',shift.name)
    #     frappe.msgprint('Shift Schedule Rejected Successfully')
    def on_update(self):
        enqueue(self.enqueue_draft_schedule, queue='default', timeout=6000, event='enqueue_draft_schedule')

    def enqueue_draft_schedule(self):
        # self.number_of_employees = len(self.employee_details) 
        # emp_count = len(self.employee_details)
        # self.db_set("number_of_employees", emp_count)

        if(self.workflow_state == 'Pending For HOD'):
            self.upload_shift()
            frappe.msgprint('Shift Schedule Created')
    
    def upload_shift(self):
        dates = self.get_dates(self.from_date, self.to_date)
        for date in dates:
            for row in self.employee_details:
                get_shift =  frappe.db.exists('Shift Assignment',{'employee':row.employee,'start_date':date,'end_date':date,'docstatus':['in',[0,1]]})
                if not get_shift:
                    doc = frappe.new_doc('Shift Assignment')
                    doc.employee = row.employee
                    doc.shift_type = row.shift
                    doc.start_date = date
                    doc.end_date = date
                    doc.shift_schedule = self.name
                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
                else:
                    frappe.db.set_value('Shift Assignment',get_shift,'shift_type',row.shift)
        
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



    def get_dates(self,from_date, to_date):
        """get list of dates in between from date and to date"""
        no_of_days = date_diff(add_days(self.to_date, 1), self.from_date)
        dates = [add_days(self.from_date, i) for i in range(0, no_of_days)]
        return dates   
    
    # @frappe.whitelist()
    # def show_csv_data(self):
    #     filepath = get_file(self.upload)
    #     pps = read_csv_content(filepath[1])
    #     data_list = ''
    #     for pp in pps:
    #         if pp[0] == 'ID':
    #             data_list += "<tr><td style='background-color:#b54a6a; border: 1px solid black'>%s</td><td style='background-color:#b54a6a; border: 1px solid black'>%s</td><td style='background-color:#b54a6a; border: 1px solid black'>%s</td><td style='background-color:#b54a6a; border: 1px solid black'>%s</td><td style='background-color:#b54a6a; border: 1px solid black'>%s</td></tr>"%(pp[0],pp[1],pp[2],pp[3],pp[4])
    #         else:
    #             # boarding_point = frappe.db.get_value('Employee',{'employee':pp[0]},['boarding_point'])
    #             data_list += "<tr><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td><td style = 'border: 1px solid black'>%s</td></tr>"%(pp[0],pp[1],pp[2],pp[3],pp[4])
    #     return data_list

    @frappe.whitelist()
    def show_csv_data(self):
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])
        data_list = ''
        
        for pp in pps:
            if pp[0] == 'ID':
                # Header row with white font
                data_list += "<tr><td style='background-color:#b54a6a; color:white; border: 1px solid black'>%s</td>" \
                            "<td style='background-color:#b54a6a; color:white; border: 1px solid black'>%s</td>" \
                            "<td style='background-color:#b54a6a; color:white; border: 1px solid black'>%s</td>" \
                            "<td style='background-color:#b54a6a; color:white; border: 1px solid black'>%s</td>" \
                            "<td style='background-color:#b54a6a; color:white; border: 1px solid black'>%s</td></tr>" \
                            % (pp[0], pp[1], pp[2], pp[3], pp[4])
            else:
                # Data rows remain default
                data_list += "<tr><td style='border: 1px solid black'>%s</td>" \
                            "<td style='border: 1px solid black'>%s</td>" \
                            "<td style='border: 1px solid black'>%s</td>" \
                            "<td style='border: 1px solid black'>%s</td>" \
                            "<td style='border: 1px solid black'>%s</td></tr>" \
                            % (pp[0], pp[1], pp[2], pp[3], pp[4])
        
        return data_list


    @frappe.whitelist()
    def show_summary(self):
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])
        data = ''

        # Staff
        wc1 = wc2 = wc3 = wcpp1 = 0
        # Worker
        bc1 = bc2 = bc3 = bcpp1 = 0
        # NAPS
        naps1 = naps2 = naps3 = napsg = 0
        # Trainee
        trainee1 = trainee2 = trainee3 = traineeg = 0
        # Contract
        contract1 = contract2 = contract3 = contractg = 0

        for pp in pps:
            emp_type, shift = pp[3], pp[4]

            if emp_type == 'STAFF':
                if shift == "A": wc1 += 1
                elif shift == "B": wc2 += 1
                elif shift == "C": wc3 += 1
                elif shift == "G": wcpp1 += 1

            elif emp_type == 'WORKER':
                if shift == "A": bc1 += 1
                elif shift == "B": bc2 += 1
                elif shift == "C": bc3 += 1
                elif shift == "G": bcpp1 += 1

            elif emp_type == 'NAPS':
                if shift == "A": naps1 += 1
                elif shift == "B": naps2 += 1
                elif shift == "C": naps3 += 1
                elif shift == "G": napsg += 1

            elif emp_type == 'TRAINEE':
                if shift == "A": trainee1 += 1
                elif shift == "B": trainee2 += 1
                elif shift == "C": trainee3 += 1
                elif shift == "G": traineeg += 1

            elif emp_type == 'Contract':
                if shift == "A": contract1 += 1
                elif shift == "B": contract2 += 1
                elif shift == "C": contract3 += 1
                elif shift == "G": contractg += 1

        # Row totals
        staff_total = wc1 + wc2 + wc3 + wcpp1
        worker_total = bc1 + bc2 + bc3 + bcpp1
        naps_total = naps1 + naps2 + naps3 + napsg
        trainee_total = trainee1 + trainee2 + trainee3 + traineeg
        contract_total = contract1 + contract2 + contract3 + contractg

        # Column totals
        total_a = wc1 + bc1 + naps1 + trainee1 + contract1
        total_b = wc2 + bc2 + naps2 + trainee2 + contract2
        total_c = wc3 + bc3 + naps3 + trainee3 + contract3
        total_g = wcpp1 + bcpp1 + napsg + traineeg + contractg
        grand_total = staff_total + worker_total + naps_total + trainee_total + contract_total
        
        data += """
                <table style="border-collapse: collapse; width: 50%; border: 1px solid black;">
                    <tr>
                        <td style="background-color:#b54a6a; color:white; border: 1px solid black">Shift</td>
                        <td style="background-color:#b54a6a; color:white; border: 1px solid black">A</td>
                        <td style="background-color:#b54a6a; color:white; border: 1px solid black">B</td>
                        <td style="background-color:#b54a6a; color:white; border: 1px solid black">C</td>
                        <td style="background-color:#b54a6a; color:white; border: 1px solid black">G</td>
                        <td style="background-color:#b54a6a; color:white; border: 1px solid black">Total</td>
                    </tr>
                    <tr>
                        <th style="border: 1px solid black">Staff</th>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="background-color:#9da3a3; border: 1px solid black">{}</td>
                    </tr>
                    <tr>
                        <th style="border: 1px solid black">Worker</th>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="background-color:#9da3a3; border: 1px solid black">{}</td>
                    </tr>
                    <tr>
                        <th style="border: 1px solid black">NAPS</th>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="background-color:#9da3a3; border: 1px solid black">{}</td>
                    </tr>
                    <tr>
                        <th style="border: 1px solid black">Trainee</th>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="background-color:#9da3a3; border: 1px solid black">{}</td>
                    </tr>
                    <tr>
                        <th style="border: 1px solid black">Contract</th>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="border: 1px solid black">{}</td>
                        <td style="background-color:#9da3a3; border: 1px solid black">{}</td>
                    </tr>
                    <tr>
                        <td style="background-color:#9da3a3; border: 1px solid black">Total</td>
                        <td style="background-color:#9da3a3; border: 1px solid black">{}</td>
                        <td style="background-color:#9da3a3; border: 1px solid black">{}</td>
                        <td style="background-color:#9da3a3; border: 1px solid black">{}</td>
                        <td style="background-color:#9da3a3; border: 1px solid black">{}</td>
                        <td style="background-color:#9da3a3; border: 1px solid black">{}</td>
                    </tr>
                </table>
            """.format(
                wc1, wc2, wc3, wcpp1, staff_total,
                bc1, bc2, bc3, bcpp1, worker_total,
                naps1, naps2, naps3, napsg, naps_total,
                trainee1, trainee2, trainee3, traineeg, trainee_total,
                contract1, contract2, contract3, contractg, contract_total,
                total_a, total_b, total_c, total_g, grand_total
            )

        return data

    def calculate_total_employees(self):
        filepath = get_file(self.upload)
        pps = read_csv_content(filepath[1])

        staff = worker = naps = trainee = contract = 0

        for pp in pps:
            emp_type = pp[3]
            if emp_type == "STAFF":
                staff += 1
            elif emp_type == "WORKER":
                worker += 1
            elif emp_type == "NAPS":
                naps += 1
            elif emp_type == "TRAINEE":
                trainee += 1
            elif emp_type == "Contract":
                contract += 1

        return staff + worker + naps + trainee + contract

# @frappe.whitelist()
# def department_line(dept):
#     data = []
#     user = frappe.db.get_value('User',{'name':frappe.session.user},['email'])
#     if user == 'arunpandiyan@infacindia.com':
#         if dept == 'IQC':
#             frappe.throw(_('You will allow to Schedule the IQC Department Line'))
#             data.append('IQC')
#     return data      
        


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

@frappe.whitelist()
def add_header(w):
    w.writerow(["ID", "Name", "Department", "Employment Type", "Shift"])
    return w

@frappe.whitelist()
def add_data(w, args):
    data = get_data(args)
    writedata(w, data)
    return w

@frappe.whitelist()
def writedata(w, data):
    for row in data:
        w.writerow(row)

@frappe.whitelist()
def get_data(args):
    employees = get_active_employees(args)
    data = []
    for employee in employees:
        row = [
            employee.get("name"),
            employee.get("employee_name"),
            employee.get("department"),
            employee.get("employment_type"),
            employee.get("shift"),
        ]
        data.append(row)
    return data

@frappe.whitelist()
def get_active_employees(args):
    datalist = []
    previous_day_shift = add_days(args.from_date, -2)

    conditions = ""
    if args.get("department_line"):
        conditions = "and department_line = '%s' " % args.get("department_line")

    employees = frappe.db.sql("""
        select 
            name, employee_name, department, department_line, 
            employment_type, default_shift
        from `tabEmployee`
        where department = %s and status = 'Active' {conditions}
    """.format(conditions=conditions), args.get("department"), as_dict=1)

    for emp in employees:
        shift = frappe.db.get_value(
            "Shift Assignment",
            {
                "start_date": previous_day_shift,
                # "department_line": emp.get("department_line"),
                "employee": emp.get("name"),
            },
            ["shift_type"]
        ) or emp.get("default_shift") or "G"

        datalist.append({
            "name": emp.get("name"),
            "employee_name": emp.get("employee_name"),
            "department": emp.get("department"),
            "employment_type": emp.get("employment_type"),
            "shift": shift
        })

    return datalist


