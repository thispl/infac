# Copyright (c) 2025, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint
import calendar
from datetime import datetime, timedelta
from frappe.utils import flt


class IncentiveRequest(Document):
	pass

@frappe.whitelist()  
def check_attendance(date, emp, desig):
	if frappe.db.exists('Attendance', {"employee": emp, 'attendance_date': date, 'docstatus': ['!=', 2]}):
		att = frappe.db.get_value(
			'Attendance', 
			{"employee": emp, 'attendance_date': date, 'docstatus': ['!=', 2]}, 
			['in_time', 'out_time', 'ot_hrs'], 
			as_dict=True
		)
		incentive_amount = check_shift_incentive(desig, att['ot_hrs'])
		return att['in_time'], att['out_time'], att['ot_hrs'], incentive_amount
	else:
		return 'NO'

# @frappe.whitelist()
# def check_shift_incentive(desig, ot_hours):
# 	shift_incentive = frappe.db.get_value("Designation", desig, "shift_incentive_applicable")	
# 	if shift_incentive == 1:
# 		slab_doc = frappe.get_single("Incentive Slab")
# 		result = []
# 		for row in slab_doc.slab:
# 			result.append({
# 				"hours": row.hours,
# 				"amount": row.amount
# 			})
# 		result = sorted(result, key=lambda x: x["hours"], reverse=True)
# 		for slab in result:
# 			if cint(ot_hours) == cint(slab["hours"]):
# 				return slab["amount"]
# 		return 0
# 	else:
# 		return 0
	
@frappe.whitelist()
def check_shift_incentive(desig, ot_hours):
    shift_incentive = frappe.db.get_value("Designation", desig, "shift_incentive_applicable")	
    if shift_incentive == 1:
        slab_doc = frappe.get_single("Incentive Slab")
        result = []
        for row in slab_doc.slab:
            result.append({
                "hours": row.hours,
                "amount": row.amount
            })
        result = sorted(result, key=lambda x: x["hours"], reverse=True)

        nearest_amount = 0
        for slab in result:
            if flt(ot_hours) >= flt(slab["hours"]):
                nearest_amount = slab["amount"]
                break
        return nearest_amount
    else:
        return 0


from datetime import datetime
import frappe

@frappe.whitelist()
def check_ot_incentive(desig, ot_hours, employee, ot_date):
	ot_incentive = frappe.db.get_value("Designation", desig, "ot_incentive_applicable")
	salary_assignment = None  

	if ot_incentive == 1: 
		salary_assignment = frappe.db.sql("""
			SELECT name, base, from_date
			FROM `tabSalary Structure Assignment`
			WHERE employee = %s AND from_date <= %s
			ORDER BY from_date DESC
			LIMIT 1
		""", (employee, ot_date), as_dict=True)

	if salary_assignment:
		salary_assignment = salary_assignment[0]
		base_salary = salary_assignment.base
		fixed_salary = base_salary - (base_salary * 0.05)
		frappe.errprint(fixed_salary)

		ot_date = datetime.strptime(ot_date, "%Y-%m-%d").date()
		month = ot_date.month
		year = ot_date.year

		if month == 1:
			start_date = datetime(year-1, 12, 21).date()
		else:
			start_date = datetime(year, month-1, 21).date()

		end_date = datetime(year, month, 20).date()

		holiday_list = frappe.db.get_value("Employee", employee, "holiday_list")
		if holiday_list:
			holidays = frappe.get_all(
				"Holiday",
				filters={
					"parent": holiday_list,
					"holiday_date": ["between", [start_date, end_date]],
					"weekly_off": 1
				},
				fields=["holiday_date"]
			)
			week_off_count = len(holidays)
		else:
			week_off_count = 0

		try:
			ot_hours = float(ot_hours) if ot_hours not in (None, "", " ") else 0.0
		except ValueError:
			ot_hours = 0.0

		working_days = 31 - week_off_count
		frappe.errprint(working_days)
		ot_amount = (fixed_salary / working_days / 8 * 1.5) * ot_hours
		return ot_amount
	
	return 0.0


# from datetime import datetime

# @frappe.whitelist()
# def check_ot_incentive(desig, ot_hours, employee, ot_date):
# 	ot_incentive = frappe.db.get_value("Designation", desig, "ot_incentive_applicable")
# 	if ot_incentive == 1: 
# 		salary_assignment = frappe.db.sql("""
# 			SELECT name, base, from_date
# 			FROM `tabSalary Structure Assignment`
# 			WHERE employee = %s AND from_date <= %s
# 			ORDER BY from_date DESC
# 			LIMIT 1
# 		""", (employee, ot_date), as_dict=True)

# 	if salary_assignment:
# 		salary_assignment = salary_assignment[0]
# 		base_salary = salary_assignment.base
# 		fixed_salary = base_salary - (base_salary * 0.05)

# 		ot_date = datetime.strptime(ot_date, "%Y-%m-%d").date()

# 		month = ot_date.month
# 		year = ot_date.year

# 		if month == 1:
# 			start_date = datetime(year-1, 12, 21).date()
# 		else:
# 			start_date = datetime(year, month-1, 21).date()

# 		end_date = datetime(year, month, 20).date()

# 		holiday_list = frappe.db.get_value("Employee", employee, "holiday_list")
# 		if holiday_list:
# 			holidays = frappe.get_all(
# 				"Holiday",
# 				filters={
# 					"parent": holiday_list,
# 					"holiday_date": ["between", [start_date, end_date]],
# 					"weekly_off": 1 
# 				},
# 				fields=["holiday_date"]
# 			)
# 			week_off_count = len(holidays)
# 		else:
# 			week_off_count = 0

# 		try:
# 			ot_hours = float(ot_hours) if ot_hours not in (None, "", " ") else 0.0
# 		except ValueError:
# 			ot_hours = 0.0

# 		working_days = 31 - week_off_count
# 		ot_amount = (fixed_salary / working_days / 8 * 1.5) * ot_hours
# 		return ot_amount


