# Copyright (c) 2013, TEAMPRO and contributors
# For license information, please see license.txt

from logging import basicConfig
import frappe
from datetime import date, timedelta
from frappe import get_request_header, msgprint, _
from frappe.utils import cstr, cint, getdate
from frappe.utils import cstr, add_days, date_diff, getdate, get_last_day,get_first_day
from datetime import date, timedelta, datetime

def execute(filters=None):
    columns,data = [],[]
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    columns =[
        _('Employee') +":Data:100",_('Employee Name') +":Data:100",_('Employee Category') +':Data:100',_('Department') +'Data:100',
        _('Designation') +':Data:100',_('DOJ') +':Data:100',_('DOB') +':Data:100',_('Start Date') +':Data:100',_('End Date') +':Data:100',
        _('Fixed ') +':Data:100',_('Basic') +':Data:100',_('HRA') +':Data:100',_('SPL') +':Data:100',_('Conveyance') +':Data:100',_('Medical') +':Data:100',
        _('Performance Allowancce') +':Data:100',_('Performance Incentive') +':Data:100',_('Supervisior Allowance') +':Data:100',_('Welfare Allowance') +':Data:100',
        _('Washing Allowance') +':Data:100',_('Grade Allowance') +':Data:100',_("Higher Education Allowance"),_('Heat Allowance') +':Data:100',_('Attendance Bonus'),
        _('Employer PF') +':Data:100',_('Employer ESI') +':Data:100',
        _('OT Amount') +':Data:100',_('Night Shift Allowance'),_('Late Penality') +':Data:100',_('Gross') +':Data:100',_('Canteen') +':Data:100',_('EPF') +':Data:100',_('ESI') +':Data:100',
        _('LWF') +':Data:100',_('TDS') +':Data:100',_('Advance Contribution') +':Data:100',
        _('Total Deduction') +':Data:100',_('Net Salary') +':Data:100',_('Working Days') +':Data:100',_('Payment Days') +':Data:100',_('Absent Days') +':Data:100',
        _('LOP Days') +':Data:100',_('Leave Days') +':Data:100'
    ]
    return columns

def get_data(filters):
    data=[]
    if filters.employee and filters.employee_category:
        salary_slip = frappe.get_all("Salary Slip",{'employee':filters.employee,'start_date':filters.from_date,'employee_category':filters.employee_category},['*'])

    elif filters.employee:
        salary_slip = frappe.get_all("Salary Slip",{'employee':filters.employee,'start_date':filters.from_date,},['*'])

    elif filters.department:
        salary_slip = frappe.get_all("Salary Slip",{'department':filters.department,'start_date':filters.from_date,},['*']) 

    elif filters.employee_category:
        salary_slip = frappe.get_all('Salary Slip',{'employee_category':filters.employee_category,'start_date':filters.from_date},['*'])    

    else:
        salary_slip = frappe.get_all('Salary Slip',{'start_date':filters.from_date,},['*'])    


    for ss in salary_slip:
        emp = frappe.get_doc('Employee',ss.employee,['*'])
        fixed = frappe.db.get_value('Salary Detail',{'abbr':'FS','parent':ss.name},'amount')
        basic = frappe.db.get_value('Salary Detail',{'abbr':'B','parent':ss.name},'amount')
        hra = frappe.db.get_value('Salary Detail',{'abbr':'HRA','parent':ss.name},'amount')
        spl_all = frappe.db.get_value('Salary Detail',{'abbr':'SA','parent':ss.name},'amount')
        convey = frappe.db.get_value('Salary Detail',{'abbr':'C','parent':ss.name},'amount')
        ma = frappe.db.get_value('Salary Detail',{'abbr':'MA','parent':ss.name},'amount')
        pa = frappe.db.get_value('Salary Detail',{'abbr':'PA','parent':ss.name},'amount')
        pi = frappe.db.get_value('Salary Detail',{'abbr':'PI','parent':ss.name},'amount')
        sa = frappe.db.get_value('Salary Detail',{'abbr':'SPA','parent':ss.name},'amount')
        wla = frappe.db.get_value('Salary Detail',{'abbr':'WLA','parent':ss.name},'amount')
        wa = frappe.db.get_value('Salary Detail',{'abbr':'WA','parent':ss.name},'amount')
        late_penality = frappe.db.get_value('Salary Detail',{'abbr':'LP','parent':ss.name},'amount')
        ga = frappe.db.get_value('Salary Detail',{'abbr':'GA','parent':ss.name},'amount')
        hea = frappe.db.get_value('Salary Detail',{'abbr':'HEA','parent':ss.name},'amount')
        ea = frappe.db.get_value('Salary Detail',{'abbr':'HA','parent':ss.name},'amount')
        ab = frappe.db.get_value('Salary Detail',{'abbr':'AB','parent':ss.name},'amount')
        pf = frappe.db.get_value('Salary Detail',{'abbr':'EEPF','parent':ss.name},'amount')
        eesi = frappe.db.get_value('Salary Detail',{'abbr':'EESI','parent':ss.name},'amount')
        ot = frappe.db.get_value('Salary Detail',{'abbr':'OT','parent':ss.name},'amount')
        nsa = frappe.db.get_value('Salary Detail',{'abbr':'NSA','parent':ss.name},'amount')
        cat = frappe.db.get_value('Salary Detail',{'abbr':'CAT','parent':ss.name},'amount')
        epf = frappe.db.get_value('Salary Detail',{'abbr':'EPF','parent':ss.name},'amount')
        esi = frappe.db.get_value('Salary Detail',{'abbr':'ESI','parent':ss.name},'amount')
        lwf = frappe.db.get_value('Salary Detail',{'abbr':'LWF','parent':ss.name},'amount')
        tds = frappe.db.get_value('Salary Detail',{'abbr':'TDS','parent':ss.name},'amount')
        ac = frappe.db.get_value('Salary Detail',{'abbr':'AC','parent':ss.name},'amount')
    
        row = [
        ss.employee,ss.employee_name,ss.employee_category,ss.department,ss.designation,emp.date_of_joining,emp.date_of_birth,
        ss.start_date,ss.end_date,fixed,basic,hra,spl_all,convey,ma,pa,pi,sa,wla,wa,ga,hea,ea,ab,pf,eesi,ot,nsa,late_penality,ss.gross_pay,cat,epf,esi,lwf,tds,ac,
        ss.total_deduction,ss.net_pay,ss.total_working_days,ss.payment_days,ss.absent_days,ss.leave_without_pay,ss.leave_days
        ]
        data.append(row)
    return data



   
