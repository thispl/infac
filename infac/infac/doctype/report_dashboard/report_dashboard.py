# Copyright (c) 2021, teampro and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ReportDashboard(Document):
	pass


# from __future__ import unicode_literals
# from os import name, sched_getaffinity
# from time import time
# import frappe
# from frappe.monitor import start
# from frappe.utils import cstr, add_days, date_diff, getdate, format_date
# from frappe import _, append_hook, bold
# from frappe.utils.csvutils import UnicodeWriter, read_csv_content
# from frappe.utils.data import format_date
# from frappe.utils.file_manager import get_file
# from frappe.model.document import Document
# from frappe.utils.background_jobs import enqueue
# from datetime import date, timedelta, datetime
# import openpyxl
# from openpyxl import Workbook
# import openpyxl
# import xlrd
# import re
# from openpyxl.styles import Font, Alignment, Border, Side
# from openpyxl import load_workbook
# from openpyxl.utils import get_column_letter
# from openpyxl.styles import GradientFill, PatternFill
# from six import BytesIO, string_types

# @frappe.whitelist()
# def download():
#     filename = 'Attendance Log'
#     test = build_xlsx_response(filename)

# def make_xlsx(data, sheet_name=None, wb=None, column_widths=None):
#     args = frappe.local.form_dict
#     column_widths = column_widths or []
#     if wb is None:
#         wb = openpyxl.Workbook()
#     ws = wb.create_sheet(sheet_name, 0)	
#     ws.append(['INFAC ATTEDANCE LOG','','','','','Present-Total Strength = Absent','','','','Present Percentage'])
#     header_1 = ['Production','Quality','Indirect (Expect Quality)','Moved to  Production from Indirect','Customer Representatives','MALE']
#     days = get_dates(args)
#     for d in days:
#         total_male = frappe.db.count('Employee',{'status':'Active','gender':'Male'})
#         present_male = frappe.db.sql('''SELECT  count(*) as count FROM `tabAttendance` LEFT JOIN `tabEmployee` ON `tabAttendance`.employee = `tabEmployee`.name where `tabEmployee`.gender = 'Male' and `tabAttendance`.attendance_date = '%s' and `tabAttendance`.status = 'Present' '''%(d),as_dict=True)[0]
#         absent_male = frappe.db.sql('''SELECT  count(*) as count FROM `tabAttendance` LEFT JOIN `tabEmployee` ON `tabAttendance`.employee = `tabEmployee`.name where `tabEmployee`.gender = 'Male' and `tabAttendance`.attendance_date = '%s' and `tabAttendance`.status = 'Absent' '''%(d),as_dict=True)[0]
#         frappe.errprint(total_male)
#         header_1.append('')
#         header_1.append(str(present_male.count)+'-'+str(total_male)+'='+str(absent_male.count))
#     ws.append(header_1)
#     header_2 = ['','','','','','FEMALE']
#     days = get_dates(args)
#     for d in days:
#         total_female = frappe.db.count('Employee',{'status':'Active','gender':'Female'})
#         present_female = frappe.db.sql('''SELECT  count(*) as count FROM `tabAttendance` LEFT JOIN `tabEmployee` ON `tabAttendance`.employee = `tabEmployee`.name where `tabEmployee`.gender = 'Female' and `tabAttendance`.attendance_date = '%s' and `tabAttendance`.status = 'Present' '''%(d),as_dict=True)[0]
#         absent_female = frappe.db.sql('''SELECT  count(*) as count FROM `tabAttendance` LEFT JOIN `tabEmployee` ON `tabAttendance`.employee = `tabEmployee`.name where `tabEmployee`.gender = 'Female' and `tabAttendance`.attendance_date = '%s' and `tabAttendance`.status = 'Absent' '''%(d),as_dict=True)[0]
#         header_2.append('')
#         header_2.append(str(present_female.count)+'-'+str(total_female)+'='+str(absent_female.count ))
#     ws.append(header_2)
#     header_3 = ['','','','','','Over all Strength']
#     days = get_dates(args)
#     for d in days:
#         total_employees = frappe.db.count('Employee',{'status':'Active'})
#         present_total = frappe.db.count('Attendance',{'status':'Present','attendance_date':d})
#         absent_total_ = frappe.db.count('Attendance',{'status':'Absent','attendance_date':d})
#         header_3.append('')
#         header_3.append(str(present_total)+'-'+str(total_employees)+'='+str(absent_total_))
#     ws.append(header_3)
# #total production strength of attendance
#     production_strength = ['','','','','','Total in Production']
#     days = get_dates(args)
#     for d in days:
#         total_employees = frappe.db.count('Employee',{'status':'Active','department':'Production - INFAC'})
#         present_total = frappe.db.count('Attendance',{'status':'Present','attendance_date':d})
#         present_production_employee = frappe.db.count('Attendance',{'status':'Present','attendance_date':d,'department':'Production - INFAC'})
#         absent_production_employee = frappe.db.count('Attendance',{'status':'Absent','department':'Production - INFAC','attendance_date':d})
#         production_strength.append('')
#         production_strength.append(str(present_production_employee)+'-'+str(total_employees)+'='+str(absent_production_employee))
#         production_strength.append('')
#         production_strength.append(present_production_employee/present_total*100)
#     ws.append(production_strength)   
# #total indirect except quality
#     present_quality_strength = (['','','','','','Total in Indirect (Except Quality)'])
#     days = get_dates(args)
#     for d in days:
#         total_employees = frappe.db.count('Employee',{'status':'Active','department':'Production - INFAC'})
#         present_total = frappe.db.count('Attendance',{'status':'Present','attendance_date':d})
#         present_quality_employee = frappe.db.count('Attendance',{'status':'Present','attendance_date':d,'department':('not in', ('Production - INFAC','Quality - INFAC'))})
#         absent_quality_employee = frappe.db.count('Attendance',{'status':'Absent','department':'Production - INFAC','attendance_date':d})
#         present_quality_strength.append('')
#         present_quality_strength.append(str(present_quality_employee )+'-'+str(total_employees)+'='+str(absent_quality_employee))
#         present_quality_strength.append('')
#         present_quality_strength.append(present_quality_employee/present_total*100)
#     ws.append(present_quality_strength)
# #total quality    
#     quality = ['','','','','','Total in Quality']
#     days = get_dates(args)
#     for d in days:
#         total_employees = frappe.db.count('Employee',{'status':'Active','department':'Quality - INFAC'})
#         present_total = frappe.db.count('Attendance',{'status':'Present','attendance_date':d})
#         present_quality_employee = frappe.db.count('Attendance',{'status':'Present','attendance_date':d,'department':'Quality - INFAC'})
#         absent_quality_employee = frappe.db.count('Attendance',{'status':'Absent','department':'Quality - INFAC'})
#         quality.append('')
#         quality.append(str(present_quality_employee)+'-'+str(total_employees)+'='+str(absent_quality_employee))
#         quality.append('')
#         quality.append(present_quality_employee/present_total*100)
#     ws.append(quality)    
#     ws.append(['','','','','','',''])   
#     ws.append(['','','','','','',''])
#     ws.append(['','','','','','',''])
#     header = ['Departmnet','Category','Department Line','Employee','Name','Gender','Re']
#     dates = get_dates(args) 
#     for d in dates:
#         day = datetime.strptime(str(d),'%Y-%m-%d').strftime('%d/%m')
#         header.append(day)
#         s = ['Shift']
#         header.extend(s)
#         q = [ (day - 1) + 'In',(day - 1)+'Out Time']
#         header.extend(q)
#         r = [day +'In']
#         header.extend(r)
#     ws.append(header)
#     department = frappe.db.get_all('Department')
#     for dept in department:
#         employees = frappe.get_all("Employee",{'department':dept.name,'status':'Active'},['*']) 
#         if employees:
#             ws.append(['','','','','','','','','','','','','','','','','','','','','',''])
#             total_row = ['Total','','','','','','']
#             for date in dates:
#                 present_employee = frappe.db.sql("select count(*) as count from `tabAttendance` where status = 'Present' and attendance_date = '%s' and department = '%s' "%(date,dept.name),as_dict=True)[0].count
#                 total_row.extend([present_employee,'','',''])
#             ws.append(total_row)  
#             for emp in employees:
#                 row = [emp.department,emp.employee_category,emp.department_line,emp.name,emp.employee_name] or 0
#                 if emp.gender == "Male":
#                     row.append("M")
#                 elif emp.gender == "Female":
#                     row.append("F")
#                 if emp.employee_category == "Master Staff":
#                     row.append("사무")
#                 elif emp.employee_category == "Workers Grade 2" or "Master Worker" or "Supporting Staff" or "Operating Staff":
#                     row.append("현장")
#                 else:
#                     row.append("용역")
#                 for date in dates:
#                     att = frappe.db.get_value('Attendance',{'employee':emp.name,'attendance_date':date},['status','shift','in_time','out_time'],as_dict=True)
#                     if att:
#                         if att.status == 'Present':
#                             status = 1
#                         else:
#                             status = 0
#                         row.append(status)
#                         row.append(att.shift)
#                         row.append(att.in_time)
#                         row.append(att.out_time)
#                         row.append("")
#                 ws.append(row)
#     ws['A2'].fill = PatternFill(fgColor="0EC31E", fill_type = "solid")
#     ws['B2'].fill = PatternFill(fgColor="E9D50D", fill_type = "solid")
#     ws['C2'].fill = PatternFill(fgColor="0096FF", fill_type = "solid")
#     ws['D2'].fill = PatternFill(fgColor="FF0000", fill_type = "solid")
#     ws['E2'].fill = PatternFill(fgColor="ff8c00", fill_type = "solid")
#     for header in ws.iter_rows(min_row=5, max_row=5, min_col= 6, max_col = 10):
#         for cell in header:
#             cell.fill = PatternFill(fgColor='0EC31E', fill_type = "solid")
#     for header in ws.iter_rows(min_row=6, max_row=6, min_col= 6, max_col = 10):
#         for cell in header:
#             cell.fill = PatternFill(fgColor='0096FF', fill_type = "solid")
#     for header in ws.iter_rows(min_row=7, max_row=7, min_col= 6, max_col = 10):
#         for cell in header:
#             cell.fill = PatternFill(fgColor='E9D50D', fill_type = "solid")
            
#     ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=4)
#     ws.merge_cells(start_row=1, start_column=6, end_row=1, end_column=9)
#     ws.merge_cells(start_row=2, start_column=6, end_row=2, end_column=7)
#     ws.merge_cells(start_row=3, start_column=6, end_row=3, end_column=7)
#     ws.merge_cells(start_row=4, start_column=6, end_row=4, end_column=7)
#     ws.merge_cells(start_row=5, start_column=6, end_row=5, end_column=7)
#     ws.merge_cells(start_row=6, start_column=6, end_row=6, end_column=7)
#     ws.merge_cells(start_row=7, start_column=6, end_row=7, end_column=7)
#     ws.merge_cells(start_row=2, start_column=8, end_row=2, end_column=9)
#     ws.merge_cells(start_row=3, start_column=8, end_row=3, end_column=9)
#     ws.merge_cells(start_row=4, start_column=8, end_row=4, end_column=9)
#     ws.merge_cells(start_row=5, start_column=8, end_row=5, end_column=9)
#     ws.merge_cells(start_row=6, start_column=8, end_row=6, end_column=9)
#     ws.merge_cells(start_row=7, start_column=8, end_row=7, end_column=9)
#     ws.merge_cells(start_row=1, start_column=10, end_row=1, end_column=10)

#     for cell in ws["11:11"]:
#         cell.alignment = Alignment(horizontal='center')

#     department = frappe.db.get_all('Department')
#     minrow = 13
#     for dept in department:
#         if dept.name == "Production - INFAC":
#             employee = frappe.get_all("Employee",{'department':dept.name,'status':'Active'},['*'])
#             if employee:
#                 maxrow = minrow + len(employee)
#                 for header in ws.iter_rows(min_row= minrow, max_row=maxrow, min_col= 8, max_col = 8):
#                     for cell in header:
#                         cell.fill = PatternFill(fgColor='0EC31E', fill_type = "solid")
#                         minrow = maxrow + 2

#         elif dept.name == "Quality - INFAC":
#             employee = frappe.get_all("Employee",{'department':dept.name,'status':'Active'},['*'])
#             if employee:
#                 maxrow = minrow + len(employee)
#                 for header in ws.iter_rows(min_row= minrow, max_row=maxrow, min_col= 8, max_col = 8):
#                     for cell in header:
#                         cell.fill = PatternFill(fgColor='E9D50D', fill_type = "solid")
#                         minrow = maxrow + 2
                
#         elif dept.name == "CUSTOMER REPRESENTATIVE MOBIS - INFAC":
#             employee = frappe.get_all("Employee",{'department':dept.name,'status':'Active'},['*'])
#             if employee:
#                 maxrow = minrow + len(employee)
#                 for header in ws.iter_rows(min_row= minrow, max_row=maxrow, min_col= 8, max_col = 8):
#                     for cell in header:
#                         cell.fill = PatternFill(fgColor='ff8c00', fill_type = "solid")
#                         minrow = maxrow + 2
            
#         else:
#             employee = frappe.get_all("Employee",{'department':dept.name,'status':'Active'},['*'])
#             if employee:
#                 maxrow = minrow + len(employee)
#                 for header in ws.iter_rows(min_row= minrow, max_row=maxrow, min_col= 8, max_col = 8):
#                     for cell in header:
#                         cell.fill = PatternFill(fgColor='0096FF', fill_type = "solid")
#                         minrow = maxrow + 2
        
#     border = Border(left=Side(border_style='thin', color='000000'),
#         right=Side(border_style='thin', color='000000'),
#         top=Side(border_style='thin', color='000000'),
#         bottom=Side(border_style='thin', color='000000'))

#     for rows in ws.iter_rows(min_row=1, max_row=7, min_col=6, max_col=10):
#         for cell in rows:
#             cell.border = border

#     department = frappe.db.get_all('Department')
#     dept_color = []
#     for dept in department:
#         employee = frappe.get_all("Employee",{'department':dept.name,'status':'Active'},['*'])
#         i = 11
#         j = len(employee)
#         for rows in ws.iter_rows(min_row=i, max_row=j, min_col=1, max_col=7+((len(dates)*4))):
#             for cell in rows:
#                 cell.border = border

#     xlsx_file = BytesIO()
#     wb.save(xlsx_file)
#     return xlsx_file

# def build_xlsx_response(filename):
#     xlsx_file = make_xlsx(filename)
#     frappe.response['filename'] = filename + '.xlsx'
#     frappe.response['filecontent'] = xlsx_file.getvalue()
#     frappe.response['type'] = 'binary'	

# def get_dates(args):
#     no_of_days = date_diff(add_days(args.to_date, 1), args.from_date)
#     dates = [add_days(args.from_date, i) for i in range(0, no_of_days)]
#     return dates



