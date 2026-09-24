# # # import calendar

# # # import frappe
# # # from frappe import _
# # # from frappe.utils import cint, getdate


# # # def _safe_get(doc, fieldname):
# # # 	"""Return a field value if it exists on the doctype, else None.
# # # 	Different HRMS versions/customizations name Aadhaar/PAN/UAN fields
# # # 	differently, so this avoids hard failures."""
# # # 	return doc.get(fieldname) if fieldname in doc.as_dict() else None


# # # @frappe.whitelist()
# # # def get_employee_details(employee):
# # # 	"""Fetch the employee profile card data."""
# # # 	if not frappe.has_permission("Employee", "read", employee):
# # # 		frappe.throw(_("Not permitted"), frappe.PermissionError)

# # # 	doc = frappe.get_doc("Employee", employee)

# # # 	reports_to = None
# # # 	if doc.reports_to:
# # # 		reports_to = frappe.db.get_value("Employee", doc.reports_to, "employee_name")

# # # 	return {
# # # 		"employee": doc.name,
# # # 		"employee_name": doc.employee_name,
# # # 		"designation": doc.designation,
# # # 		"department": doc.department,
# # # 		"status": doc.status,
# # # 		"image": doc.image,
# # # 		"date_of_joining": doc.date_of_joining,
# # # 		"date_of_birth": doc.date_of_birth,
# # # 		"gender": doc.gender,
# # # 		"marital_status": doc.marital_status,
# # # 		"blood_group": doc.blood_group,
# # # 		"reports_to": reports_to,
# # # 		"company_email": doc.user_id or doc.personal_email,
# # # 		"cell_number": doc.cell_number,
# # # 		"current_address": doc.current_address,
# # # 		"pan_number": _safe_get(doc, "pan_number"),
# # # 		"aadhaar_number": _safe_get(doc, "aadhaar_number") or _safe_get(doc, "aadhar_number"),
# # # 		"provident_fund_account": _safe_get(doc, "provident_fund_account"),
# # # 		"uan": _safe_get(doc, "uan_number"),
# # # 		"esic_no": _safe_get(doc, "esic_no") or _safe_get(doc, "esi_number"),
# # # 	}


# # # @frappe.whitelist()
# # # def get_attendance_calendar(employee, year):
# # # 	"""Return day-level attendance records for the given year, plus a
# # # 	month-wise summary of status counts (Present, Absent, Half Day,
# # # 	On Leave, Work From Home, Holiday)."""
# # # 	year = cint(year)

# # # 	records = frappe.get_all(
# # # 		"Attendance",
# # # 		filters={
# # # 			"employee": employee,
# # # 			"docstatus": 1,
# # # 			"attendance_date": ["between", [f"{year}-01-01", f"{year}-12-31"]],
# # # 		},
# # # 		fields=["attendance_date", "status", "leave_type"],
# # # 	)

# # # 	# month (1-12) -> status -> count
# # # 	summary = {m: {} for m in range(1, 13)}
# # # 	days_by_month = {m: [] for m in range(1, 13)}

# # # 	for r in records:
# # # 		d = getdate(r.attendance_date)
# # # 		summary[d.month][r.status] = summary[d.month].get(r.status, 0) + 1
# # # 		days_by_month[d.month].append(
# # # 			{"day": d.day, "status": r.status, "leave_type": r.leave_type}
# # # 		)

# # # 	months = []
# # # 	for m in range(1, 13):
# # # 		months.append(
# # # 			{
# # # 				"month": m,
# # # 				"month_name": calendar.month_name[m],
# # # 				"days_in_month": calendar.monthrange(year, m)[1],
# # # 				"days": days_by_month[m],
# # # 				"summary": summary[m],
# # # 			}
# # # 		)

# # # 	return {"year": year, "months": months}


# # # @frappe.whitelist()
# # # def get_leave_summary(employee, year):
# # # 	"""Return allocated / taken / balance per leave type for the year."""
# # # 	year = cint(year)
# # # 	from_date = f"{year}-01-01"
# # # 	to_date = f"{year}-12-31"

# # # 	leave_types = frappe.get_all("Leave Type", pluck="name")
# # # 	result = []

# # # 	for lt in leave_types:
# # # 		allocation = frappe.db.sql(
# # # 			"""
# # # 			SELECT SUM(total_leaves_allocated) AS allocated
# # # 			FROM `tabLeave Allocation`
# # # 			WHERE employee=%s AND leave_type=%s AND docstatus=1
# # # 			AND from_date <= %s AND to_date >= %s
# # # 			""",
# # # 			(employee, lt, to_date, from_date),
# # # 			as_dict=True,
# # # 		)
# # # 		allocated = (allocation[0].allocated if allocation else 0) or 0

# # # 		taken = frappe.db.sql(
# # # 			"""
# # # 			SELECT SUM(total_leave_days) AS taken
# # # 			FROM `tabLeave Application`
# # # 			WHERE employee=%s AND leave_type=%s AND docstatus=1
# # # 			AND YEAR(from_date)=%s
# # # 			""",
# # # 			(employee, lt, year),
# # # 			as_dict=True,
# # # 		)
# # # 		taken = (taken[0].taken if taken else 0) or 0

# # # 		if allocated or taken:
# # # 			result.append(
# # # 				{
# # # 					"leave_type": lt,
# # # 					"allocated": allocated,
# # # 					"taken": taken,
# # # 					"balance": allocated - taken,
# # # 				}
# # # 			)

# # # 	loss_of_pay = frappe.db.sql(
# # # 		"""
# # # 		SELECT COUNT(*) AS lop
# # # 		FROM `tabAttendance`
# # # 		WHERE employee=%s AND status='Absent' AND docstatus=1
# # # 		AND YEAR(attendance_date)=%s
# # # 		""",
# # # 		(employee, year),
# # # 		as_dict=True,
# # # 	)
# # # 	lop = (loss_of_pay[0].lop if loss_of_pay else 0) or 0

# # # 	return {"leave_types": result, "loss_of_pay": lop}




# # import calendar

# # import frappe
# # from frappe import _
# # from frappe.utils import add_days, cint, getdate


# # def _safe_get(doc, fieldname):
# # 	"""Return a field value if it exists on the doctype, else None.
# # 	Different HRMS versions/customizations name Aadhaar/PAN/UAN fields
# # 	differently, so this avoids hard failures."""
# # 	return doc.get(fieldname) if fieldname in doc.as_dict() else None


# # @frappe.whitelist()
# # def get_employee_details(employee):
# # 	"""Fetch the employee profile card data."""
# # 	if not frappe.has_permission("Employee", "read", employee):
# # 		frappe.throw(_("Not permitted"), frappe.PermissionError)

# # 	doc = frappe.get_doc("Employee", employee)

# # 	reports_to = None
# # 	if doc.reports_to:
# # 		reports_to = frappe.db.get_value("Employee", doc.reports_to, "employee_name")

# # 	return {
# # 		"employee": doc.name,
# # 		"employee_name": doc.employee_name,
# # 		"designation": doc.designation,
# # 		"department": doc.department,
# # 		"status": doc.status,
# # 		"image": doc.image,
# # 		"date_of_joining": doc.date_of_joining,
# # 		"date_of_birth": doc.date_of_birth,
# # 		"gender": doc.gender,
# # 		"marital_status": doc.marital_status,
# # 		"blood_group": doc.blood_group,
# # 		"reports_to": reports_to,
# # 		"company_email": doc.company_email or doc.personal_email,
# # 		"cell_number": doc.cell_number,
# # 		"current_address": doc.current_address,
# # 		"pan_number": _safe_get(doc, "pan_number"),
# # 		"aadhaar_number": _safe_get(doc, "aadhaar_number") or _safe_get(doc, "aadhar_number"),
# # 		"provident_fund_account": _safe_get(doc, "provident_fund_account"),
# # 		"uan": _safe_get(doc, "uan"),
# # 		"esic_no": _safe_get(doc, "esic_no") or _safe_get(doc, "esi_number"),
# # 	}


# # def get_holiday_list_for_employee(employee):
# # 	holiday_list, company = frappe.db.get_value(
# # 		"Employee", employee, ["holiday_list", "company"]
# # 	) or (None, None)

# # 	if not holiday_list and company:
# # 		holiday_list = frappe.get_cached_value("Company", company, "default_holiday_list")

# # 	return holiday_list


# # @frappe.whitelist()
# # def get_attendance_calendar(employee, year):
# # 	"""Return day-level attendance records for the given year (merged with
# # 	the employee's Holiday List), plus a month-wise summary of status
# # 	counts (Present, Absent, Half Day, On Leave, Work From Home, Holiday)."""
# # 	year = cint(year)
# # 	from_date = f"{year}-01-01"
# # 	to_date = f"{year}-12-31"

# # 	records = frappe.get_all(
# # 		"Attendance",
# # 		filters={
# # 			"employee": employee,
# # 			"docstatus": 1,
# # 			"attendance_date": ["between", [from_date, to_date]],
# # 		},
# # 		fields=["attendance_date", "status", "leave_type"],
# # 	)

# # 	# date -> {"status": ..., "leave_type": ...}
# # 	day_info = {}
# # 	for r in records:
# # 		day_info[getdate(r.attendance_date)] = {
# # 			"status": r.status,
# # 			"leave_type": r.leave_type,
# # 		}

# # 	# overlay holidays from the employee's Holiday List, but don't override
# # 	# an actual Attendance record already marked for that day
# # 	holiday_list = get_holiday_list_for_employee(employee)
# # 	if holiday_list:
# # 		holidays = frappe.get_all(
# # 			"Holiday",
# # 			filters={"parent": holiday_list, "holiday_date": ["between", [from_date, to_date]]},
# # 			fields=["holiday_date", "description"],
# # 		)
# # 		for h in holidays:
# # 			d = getdate(h.holiday_date)
# # 			if d not in day_info:
# # 				day_info[d] = {"status": "Holiday", "leave_type": h.description}

# # 	summary = {m: {} for m in range(1, 13)}
# # 	days_by_month = {m: [] for m in range(1, 13)}
# # 	leave_type_summary = {m: {} for m in range(1, 13)}
# # 	leave_types_seen = set()

# # 	for d, info in day_info.items():
# # 		status = info["status"]
# # 		summary[d.month][status] = summary[d.month].get(status, 0) + 1
# # 		days_by_month[d.month].append(
# # 			{"day": d.day, "status": status, "leave_type": info["leave_type"]}
# # 		)
# # 		if info["leave_type"]:
# # 			leave_type_summary[d.month][info["leave_type"]] = (
# # 				leave_type_summary[d.month].get(info["leave_type"], 0) + 1
# # 			)
# # 			leave_types_seen.add(info["leave_type"])

# # 	months = []
# # 	for m in range(1, 13):
# # 		months.append(
# # 			{
# # 				"month": m,
# # 				"month_name": calendar.month_name[m],
# # 				"days_in_month": calendar.monthrange(year, m)[1],
# # 				"days": days_by_month[m],
# # 				"summary": summary[m],
# # 				"leave_type_summary": leave_type_summary[m],
# # 			}
# # 		)

# # 	return {
# # 		"year": year,
# # 		"months": months,
# # 		"holiday_list": holiday_list,
# # 		"leave_types": sorted(leave_types_seen),
# # 	}


# # @frappe.whitelist()
# # def get_leave_summary(employee, year):
# # 	"""Return allocated / taken / balance per leave type for the year."""
# # 	year = cint(year)
# # 	from_date = f"{year}-01-01"
# # 	to_date = f"{year}-12-31"

# # 	leave_types = frappe.get_all("Leave Type", pluck="name")
# # 	result = []

# # 	for lt in leave_types:
# # 		allocation = frappe.db.sql(
# # 			"""
# # 			SELECT SUM(total_leaves_allocated) AS allocated
# # 			FROM `tabLeave Allocation`
# # 			WHERE employee=%s AND leave_type=%s AND docstatus=1
# # 			AND from_date <= %s AND to_date >= %s
# # 			""",
# # 			(employee, lt, to_date, from_date),
# # 			as_dict=True,
# # 		)
# # 		allocated = (allocation[0].allocated if allocation else 0) or 0

# # 		taken = frappe.db.sql(
# # 			"""
# # 			SELECT SUM(total_leave_days) AS taken
# # 			FROM `tabLeave Application`
# # 			WHERE employee=%s AND leave_type=%s AND docstatus=1
# # 			AND YEAR(from_date)=%s
# # 			""",
# # 			(employee, lt, year),
# # 			as_dict=True,
# # 		)
# # 		taken = (taken[0].taken if taken else 0) or 0

# # 		if allocated or taken:
# # 			result.append(
# # 				{
# # 					"leave_type": lt,
# # 					"allocated": allocated,
# # 					"taken": taken,
# # 					"balance": allocated - taken,
# # 				}
# # 			)

# # 	loss_of_pay = frappe.db.sql(
# # 		"""
# # 		SELECT COUNT(*) AS lop
# # 		FROM `tabAttendance`
# # 		WHERE employee=%s AND status='Absent' AND docstatus=1
# # 		AND YEAR(attendance_date)=%s
# # 		""",
# # 		(employee, year),
# # 		as_dict=True,
# # 	)
# # 	lop = (loss_of_pay[0].lop if loss_of_pay else 0) or 0

# # 	return {"leave_types": result, "loss_of_pay": lop}


# # # ---------------------------------------------------------------------------
# # # Payroll-cycle (21st-to-20th) attendance table
# # # ---------------------------------------------------------------------------

# # LEAVE_BUCKET_KEYWORDS = {
# # 	"EE": ["earned"],
# # 	"CC": ["casual"],
# # 	"SS": ["sick"],
# # 	"Spl/ML": ["special", "maternity", "compensatory", "paternity"],
# # }


# # def _bucket_for_leave_type(leave_type):
# # 	"""Map a Leave Type name to one of the 4 fixed summary columns
# # 	(EE / CC / SS / Spl-ML). Anything unrecognised falls into Spl/ML
# # 	so it's still counted somewhere - adjust LEAVE_BUCKET_KEYWORDS above
# # 	if your Leave Type names don't match these keywords."""
# # 	if not leave_type:
# # 		return None
# # 	lt = leave_type.lower()
# # 	for bucket, keywords in LEAVE_BUCKET_KEYWORDS.items():
# # 		for kw in keywords:
# # 			if kw in lt:
# # 				return bucket
# # 	return "Spl/ML"


# # def _leave_abbr(leave_type):
# # 	"""Short 2-3 letter code shown inside a day cell, e.g. 'Casual Leave' -> 'CL'."""
# # 	if not leave_type:
# # 		return ""
# # 	words = [w for w in leave_type.split() if w.lower() != "leave"]
# # 	if not words:
# # 		return leave_type[:2].upper()
# # 	if len(words) == 1:
# # 		return words[0][:2].upper()
# # 	return "".join(w[0] for w in words).upper()


# # @frappe.whitelist()
# # def get_payroll_attendance(employee, year):
# # 	"""Build the 21st-to-20th payroll-cycle attendance table: one row per
# # 	month with day-level status codes, plus calculated totals per row
# # 	(Calendar Days, Working Days, Worked Days, EE/CC/SS/Spl-ML, WW/HH,
# # 	Paid Days, AA)."""
# # 	year = cint(year)
# # 	holiday_list = get_holiday_list_for_employee(employee)

# # 	span_start = f"{year - 1}-12-01"
# # 	span_end = f"{year}-12-31"

# # 	att_records = frappe.get_all(
# # 		"Attendance",
# # 		filters={
# # 			"employee": employee,
# # 			"docstatus": 1,
# # 			"attendance_date": ["between", [span_start, span_end]],
# # 		},
# # 		fields=["attendance_date", "status", "leave_type"],
# # 	)
# # 	day_info = {
# # 		getdate(r.attendance_date): {"status": r.status, "leave_type": r.leave_type}
# # 		for r in att_records
# # 	}

# # 	holiday_info = {}
# # 	if holiday_list:
# # 		holidays = frappe.get_all(
# # 			"Holiday",
# # 			filters={"parent": holiday_list, "holiday_date": ["between", [span_start, span_end]]},
# # 			fields=["holiday_date", "weekly_off"],
# # 		)
# # 		for h in holidays:
# # 			holiday_info[getdate(h.holiday_date)] = bool(h.weekly_off)

# # 	rows = []
# # 	for m in range(1, 13):
# # 		end_date = getdate(f"{year}-{m:02d}-20")
# # 		if m == 1:
# # 			start_date = getdate(f"{year - 1}-12-21")
# # 		else:
# # 			start_date = getdate(f"{year}-{m - 1:02d}-21")

# # 		days = []
# # 		bucket_totals = {"EE": 0, "CC": 0, "SS": 0, "Spl/ML": 0}
# # 		ww_hh = 0
# # 		aa = 0
# # 		present_days = 0

# # 		d = start_date
# # 		while d <= end_date:
# # 			info = day_info.get(d)
# # 			code, css = "", "att-blank"

# # 			if info:
# # 				status = info["status"]
# # 				leave_type = info["leave_type"]
# # 				if status == "Present":
# # 					code, css = "XX", "att-present"
# # 					present_days += 1
# # 				elif status == "Absent":
# # 					code, css = "AA", "att-absent"
# # 					aa += 1
# # 				elif status == "Half Day":
# # 					abbr = _leave_abbr(leave_type)
# # 					code, css = (f"0.5{abbr}" if abbr else "0.5"), "att-halfday"
# # 					bucket = _bucket_for_leave_type(leave_type)
# # 					if bucket:
# # 						bucket_totals[bucket] += 0.5
# # 					present_days += 0.5
# # 				elif status == "On Leave":
# # 					abbr = _leave_abbr(leave_type)
# # 					code, css = (abbr or "LV"), "att-leave"
# # 					bucket = _bucket_for_leave_type(leave_type)
# # 					if bucket:
# # 						bucket_totals[bucket] += 1
# # 				elif status == "Work From Home":
# # 					code, css = "WFH", "att-wfh"
# # 				else:
# # 					code, css = (status[:2].upper() if status else ""), "att-other"
# # 			elif d in holiday_info:
# # 				if holiday_info[d]:
# # 					code, css = "WW", "att-weeklyoff"
# # 				else:
# # 					code, css = "HH", "att-holiday"
# # 				ww_hh += 1

# # 			days.append({"date": str(d), "day": d.day, "code": code, "css": css})
# # 			d = add_days(d, 1)

# # 		# calendar_days = (end_date - start_date).days + 1
# # 		# working_days = calendar_days - ww_hh
# # 		# leave_total = sum(bucket_totals.values())
# # 		# worked_days = working_days - leave_total - aa
# # 		# paid_days = calendar_days - aa

# # 		calendar_days = (end_date - start_date).days + 1
# # 		working_days = calendar_days - ww_hh
# # 		worked_days = present_days
# # 		paid_days = calendar_days - aa

# # 		rows.append(
# # 			{
# # 				"month_name": calendar.month_name[m],
# # 				"start_date": str(start_date),
# # 				"end_date": str(end_date),
# # 				"days": days,
# # 				"totals": {
# # 					"calendar_days": calendar_days,
# # 					"working_days": working_days,
# # 					"worked_days": worked_days,
# # 					"ee": bucket_totals["EE"],
# # 					"cc": bucket_totals["CC"],
# # 					"ss": bucket_totals["SS"],
# # 					"spl_ml": bucket_totals["Spl/ML"],
# # 					"ww_hh": ww_hh,
# # 					"paid_days": paid_days,
# # 					"aa": aa,
# # 				},
# # 			}
# # 		)

# # 	grand = {
# # 		"calendar_days": 0, "working_days": 0, "worked_days": 0,
# # 		"ee": 0, "cc": 0, "ss": 0, "spl_ml": 0,
# # 		"ww_hh": 0, "paid_days": 0, "aa": 0,
# # 	}
# # 	for row in rows:
# # 		for k in grand:
# # 			grand[k] += row["totals"][k]

# # 	return {"year": year, "rows": rows, "grand_totals": grand}

# # #update ---- 07/07

# # # import calendar

# # # import frappe
# # # from frappe import _
# # # from frappe.utils import add_days, cint, getdate


# # # def _safe_get(doc, fieldname):
# # # 	"""Return a field value if it exists on the doctype, else None.
# # # 	Different HRMS versions/customizations name Aadhaar/PAN/UAN fields
# # # 	differently, so this avoids hard failures."""
# # # 	return doc.get(fieldname) if fieldname in doc.as_dict() else None


# # # @frappe.whitelist()
# # # def get_employee_details(employee):
# # # 	"""Fetch the employee profile card data."""
# # # 	if not frappe.has_permission("Employee", "read", employee):
# # # 		frappe.throw(_("Not permitted"), frappe.PermissionError)

# # # 	doc = frappe.get_doc("Employee", employee)

# # # 	reports_to = None
# # # 	if doc.reports_to:
# # # 		reports_to = frappe.db.get_value("Employee", doc.reports_to, "employee_name")

# # # 	return {
# # # 		"employee": doc.name,
# # # 		"employee_name": doc.employee_name,
# # # 		"designation": doc.designation,
# # # 		"department": doc.department,
# # # 		"status": doc.status,
# # # 		"image": doc.image,
# # # 		"date_of_joining": doc.date_of_joining,
# # # 		"date_of_birth": doc.date_of_birth,
# # # 		"gender": doc.gender,
# # # 		"marital_status": doc.marital_status,
# # # 		"blood_group": doc.blood_group,
# # # 		"reports_to": reports_to,
# # # 		"company_email": doc.company_email or doc.personal_email,
# # # 		"cell_number": doc.cell_number,
# # # 		"current_address": doc.current_address,
# # # 		"pan_number": _safe_get(doc, "pan_number"),
# # # 		"aadhaar_number": _safe_get(doc, "aadhaar_number") or _safe_get(doc, "aadhar_number"),
# # # 		"provident_fund_account": _safe_get(doc, "provident_fund_account"),
# # # 		"uan": _safe_get(doc, "uan"),
# # # 		"esic_no": _safe_get(doc, "esic_no") or _safe_get(doc, "esi_number"),
# # # 	}


# # # def get_holiday_list_for_employee(employee):
# # # 	holiday_list, company = frappe.db.get_value(
# # # 		"Employee", employee, ["holiday_list", "company"]
# # # 	) or (None, None)

# # # 	if not holiday_list and company:
# # # 		holiday_list = frappe.get_cached_value("Company", company, "default_holiday_list")

# # # 	return holiday_list


# # # @frappe.whitelist()
# # # def get_attendance_calendar(employee, year):
# # # 	"""Return day-level attendance records for the given year (merged with
# # # 	the employee's Holiday List), plus a month-wise summary of status
# # # 	counts (Present, Absent, Half Day, On Leave, Work From Home, Holiday)."""
# # # 	year = cint(year)
# # # 	from_date = f"{year}-01-01"
# # # 	to_date = f"{year}-12-31"

# # # 	records = frappe.get_all(
# # # 		"Attendance",
# # # 		filters={
# # # 			"employee": employee,
# # # 			"docstatus": 1,
# # # 			"attendance_date": ["between", [from_date, to_date]],
# # # 		},
# # # 		fields=["attendance_date", "status", "leave_type"],
# # # 	)

# # # 	# date -> {"status": ..., "leave_type": ...}
# # # 	day_info = {}
# # # 	for r in records:
# # # 		day_info[getdate(r.attendance_date)] = {
# # # 			"status": r.status,
# # # 			"leave_type": r.leave_type,
# # # 		}

# # # 	# overlay holidays from the employee's Holiday List, but don't override
# # # 	# an actual Attendance record already marked for that day
# # # 	holiday_list = get_holiday_list_for_employee(employee)
# # # 	if holiday_list:
# # # 		holidays = frappe.get_all(
# # # 			"Holiday",
# # # 			filters={"parent": holiday_list, "holiday_date": ["between", [from_date, to_date]]},
# # # 			fields=["holiday_date", "description"],
# # # 		)
# # # 		for h in holidays:
# # # 			d = getdate(h.holiday_date)
# # # 			if d not in day_info:
# # # 				day_info[d] = {"status": "Holiday", "leave_type": h.description}

# # # 	summary = {m: {} for m in range(1, 13)}
# # # 	days_by_month = {m: [] for m in range(1, 13)}
# # # 	leave_type_summary = {m: {} for m in range(1, 13)}
# # # 	leave_types_seen = set()

# # # 	for d, info in day_info.items():
# # # 		status = info["status"]
# # # 		summary[d.month][status] = summary[d.month].get(status, 0) + 1
# # # 		days_by_month[d.month].append(
# # # 			{"day": d.day, "status": status, "leave_type": info["leave_type"]}
# # # 		)
# # # 		if info["leave_type"]:
# # # 			leave_type_summary[d.month][info["leave_type"]] = (
# # # 				leave_type_summary[d.month].get(info["leave_type"], 0) + 1
# # # 			)
# # # 			leave_types_seen.add(info["leave_type"])

# # # 	months = []
# # # 	for m in range(1, 13):
# # # 		months.append(
# # # 			{
# # # 				"month": m,
# # # 				"month_name": calendar.month_name[m],
# # # 				"days_in_month": calendar.monthrange(year, m)[1],
# # # 				"days": days_by_month[m],
# # # 				"summary": summary[m],
# # # 				"leave_type_summary": leave_type_summary[m],
# # # 			}
# # # 		)

# # # 	return {
# # # 		"year": year,
# # # 		"months": months,
# # # 		"holiday_list": holiday_list,
# # # 		"leave_types": sorted(leave_types_seen),
# # # 	}


# # # @frappe.whitelist()
# # # def get_leave_summary(employee, year):
# # # 	"""Return allocated / taken / balance per leave type for the year."""
# # # 	year = cint(year)
# # # 	from_date = f"{year}-01-01"
# # # 	to_date = f"{year}-12-31"

# # # 	leave_types = frappe.get_all("Leave Type", pluck="name")
# # # 	result = []

# # # 	for lt in leave_types:
# # # 		allocation = frappe.db.sql(
# # # 			"""
# # # 			SELECT SUM(total_leaves_allocated) AS allocated
# # # 			FROM `tabLeave Allocation`
# # # 			WHERE employee=%s AND leave_type=%s AND docstatus=1
# # # 			AND from_date <= %s AND to_date >= %s
# # # 			""",
# # # 			(employee, lt, to_date, from_date),
# # # 			as_dict=True,
# # # 		)
# # # 		allocated = (allocation[0].allocated if allocation else 0) or 0

# # # 		taken = frappe.db.sql(
# # # 			"""
# # # 			SELECT SUM(total_leave_days) AS taken
# # # 			FROM `tabLeave Application`
# # # 			WHERE employee=%s AND leave_type=%s AND docstatus=1
# # # 			AND YEAR(from_date)=%s
# # # 			""",
# # # 			(employee, lt, year),
# # # 			as_dict=True,
# # # 		)
# # # 		taken = (taken[0].taken if taken else 0) or 0

# # # 		if allocated or taken:
# # # 			result.append(
# # # 				{
# # # 					"leave_type": lt,
# # # 					"allocated": allocated,
# # # 					"taken": taken,
# # # 					"balance": allocated - taken,
# # # 				}
# # # 			)

# # # 	loss_of_pay = frappe.db.sql(
# # # 		"""
# # # 		SELECT COUNT(*) AS lop
# # # 		FROM `tabAttendance`
# # # 		WHERE employee=%s AND status='Absent' AND docstatus=1
# # # 		AND YEAR(attendance_date)=%s
# # # 		""",
# # # 		(employee, year),
# # # 		as_dict=True,
# # # 	)
# # # 	lop = (loss_of_pay[0].lop if loss_of_pay else 0) or 0

# # # 	return {"leave_types": result, "loss_of_pay": lop}


# # # # ---------------------------------------------------------------------------
# # # # Payroll-cycle (21st-to-20th) attendance table
# # # # ---------------------------------------------------------------------------

# # # LEAVE_BUCKET_KEYWORDS = {
# # # 	"EE": ["earned"],
# # # 	"CC": ["casual"],
# # # 	"SS": ["sick"],
# # # 	"Spl/ML": ["special", "maternity", "compensatory", "paternity"],
# # # }


# # # def _bucket_for_leave_type(leave_type):
# # # 	"""Map a Leave Type name to one of the 4 fixed summary columns
# # # 	(EE / CC / SS / Spl-ML). Anything unrecognised falls into Spl/ML
# # # 	so it's still counted somewhere - adjust LEAVE_BUCKET_KEYWORDS above
# # # 	if your Leave Type names don't match these keywords."""
# # # 	if not leave_type:
# # # 		return None
# # # 	lt = leave_type.lower()
# # # 	for bucket, keywords in LEAVE_BUCKET_KEYWORDS.items():
# # # 		for kw in keywords:
# # # 			if kw in lt:
# # # 				return bucket
# # # 	return "Spl/ML"


# # # def _leave_abbr(leave_type):
# # # 	"""Short 2-3 letter code shown inside a day cell, e.g. 'Casual Leave' -> 'CL'."""
# # # 	if not leave_type:
# # # 		return ""
# # # 	words = [w for w in leave_type.split() if w.lower() != "leave"]
# # # 	if not words:
# # # 		return leave_type[:2].upper()
# # # 	if len(words) == 1:
# # # 		return words[0][:2].upper()
# # # 	return "".join(w[0] for w in words).upper()


# # # @frappe.whitelist()
# # # def get_payroll_attendance(employee, year):
# # # 	"""Build the 21st-to-20th payroll-cycle attendance table: one row per
# # # 	month with day-level status codes, plus calculated totals per row
# # # 	(Calendar Days, Working Days, Worked Days, EE/CC/SS/Spl-ML, WW/HH,
# # # 	Paid Days, AA)."""
# # # 	year = cint(year)
# # # 	holiday_list = get_holiday_list_for_employee(employee)

# # # 	span_start = f"{year - 1}-12-01"
# # # 	span_end = f"{year}-12-31"

# # # 	att_records = frappe.get_all(
# # # 		"Attendance",
# # # 		filters={
# # # 			"employee": employee,
# # # 			"docstatus": 1,
# # # 			"attendance_date": ["between", [span_start, span_end]],
# # # 		},
# # # 		fields=["attendance_date", "status", "leave_type"],
# # # 	)
# # # 	day_info = {
# # # 		getdate(r.attendance_date): {"status": r.status, "leave_type": r.leave_type}
# # # 		for r in att_records
# # # 	}

# # # 	holiday_info = {}
# # # 	if holiday_list:
# # # 		holidays = frappe.get_all(
# # # 			"Holiday",
# # # 			filters={"parent": holiday_list, "holiday_date": ["between", [span_start, span_end]]},
# # # 			fields=["holiday_date", "weekly_off"],
# # # 		)
# # # 		for h in holidays:
# # # 			holiday_info[getdate(h.holiday_date)] = bool(h.weekly_off)

# # # 	rows = []
# # # 	for m in range(1, 13):
# # # 		end_date = getdate(f"{year}-{m:02d}-20")
# # # 		if m == 1:
# # # 			start_date = getdate(f"{year - 1}-12-21")
# # # 		else:
# # # 			start_date = getdate(f"{year}-{m - 1:02d}-21")

# # # 		days = []
# # # 		bucket_totals = {"EE": 0, "CC": 0, "SS": 0, "Spl/ML": 0}
# # # 		ww_hh = 0
# # # 		aa = 0

# # # 		d = start_date
# # # 		while d <= end_date:
# # # 			info = day_info.get(d)
# # # 			code, css = "", "att-blank"

# # # 			if info:
# # # 				status = info["status"]
# # # 				leave_type = info["leave_type"]
# # # 				if status == "Present":
# # # 					code, css = "XX", "att-present"
# # # 				elif status == "Absent":
# # # 					code, css = "AA", "att-absent"
# # # 					aa += 1
# # # 				elif status == "Half Day":
# # # 					abbr = _leave_abbr(leave_type)
# # # 					code, css = (f"0.5{abbr}" if abbr else "0.5"), "att-halfday"
# # # 					bucket = _bucket_for_leave_type(leave_type)
# # # 					if bucket:
# # # 						bucket_totals[bucket] += 0.5
# # # 				elif status == "On Leave":
# # # 					abbr = _leave_abbr(leave_type)
# # # 					code, css = (abbr or "LV"), "att-leave"
# # # 					bucket = _bucket_for_leave_type(leave_type)
# # # 					if bucket:
# # # 						bucket_totals[bucket] += 1
# # # 				elif status == "Work From Home":
# # # 					code, css = "WFH", "att-wfh"
# # # 				else:
# # # 					code, css = (status[:2].upper() if status else ""), "att-other"
# # # 			elif d in holiday_info:
# # # 				if holiday_info[d]:
# # # 					code, css = "WW", "att-weeklyoff"
# # # 				else:
# # # 					code, css = "HH", "att-holiday"
# # # 				ww_hh += 1

# # # 			days.append({"date": str(d), "day": d.day, "code": code, "css": css})
# # # 			d = add_days(d, 1)

# # # 		calendar_days = (end_date - start_date).days + 1
# # # 		working_days = calendar_days - ww_hh
# # # 		leave_total = sum(bucket_totals.values())
# # # 		worked_days = working_days - leave_total - aa
# # # 		paid_days = calendar_days - aa

# # # 		rows.append(
# # # 			{
# # # 				"month_name": calendar.month_name[m],
# # # 				"start_date": str(start_date),
# # # 				"end_date": str(end_date),
# # # 				"days": days,
# # # 				"totals": {
# # # 					"calendar_days": calendar_days,
# # # 					"working_days": working_days,
# # # 					"worked_days": worked_days,
# # # 					"ee": bucket_totals["EE"],
# # # 					"cc": bucket_totals["CC"],
# # # 					"ss": bucket_totals["SS"],
# # # 					"spl_ml": bucket_totals["Spl/ML"],
# # # 					"ww_hh": ww_hh,
# # # 					"paid_days": paid_days,
# # # 					"aa": aa,
# # # 				},
# # # 			}
# # # 		)

# # # 	grand = {
# # # 		"calendar_days": 0, "working_days": 0, "worked_days": 0,
# # # 		"ee": 0, "cc": 0, "ss": 0, "spl_ml": 0,
# # # 		"ww_hh": 0, "paid_days": 0, "aa": 0,
# # # 	}
# # # 	for row in rows:
# # # 		for k in grand:
# # # 			grand[k] += row["totals"][k]

# # # 	return {"year": year, "rows": rows, "grand_totals": grand}


# # # import calendar

# # # import frappe
# # # from frappe import _
# # # from frappe.utils import cint, getdate


# # # def _safe_get(doc, fieldname):
# # # 	"""Return a field value if it exists on the doctype, else None.
# # # 	Different HRMS versions/customizations name Aadhaar/PAN/UAN fields
# # # 	differently, so this avoids hard failures."""
# # # 	return doc.get(fieldname) if fieldname in doc.as_dict() else None


# # # @frappe.whitelist()
# # # def get_employee_details(employee):
# # # 	"""Fetch the employee profile card data."""
# # # 	if not frappe.has_permission("Employee", "read", employee):
# # # 		frappe.throw(_("Not permitted"), frappe.PermissionError)

# # # 	doc = frappe.get_doc("Employee", employee)

# # # 	reports_to = None
# # # 	if doc.reports_to:
# # # 		reports_to = frappe.db.get_value("Employee", doc.reports_to, "employee_name")

# # # 	return {
# # # 		"employee": doc.name,
# # # 		"employee_name": doc.employee_name,
# # # 		"designation": doc.designation,
# # # 		"department": doc.department,
# # # 		"status": doc.status,
# # # 		"image": doc.image,
# # # 		"date_of_joining": doc.date_of_joining,
# # # 		"date_of_birth": doc.date_of_birth,
# # # 		"gender": doc.gender,
# # # 		"marital_status": doc.marital_status,
# # # 		"blood_group": doc.blood_group,
# # # 		"reports_to": reports_to,
# # # 		"company_email": doc.user_id or doc.personal_email,
# # # 		"cell_number": doc.cell_number,
# # # 		"current_address": doc.current_address,
# # # 		"pan_number": _safe_get(doc, "pan_number"),
# # # 		"aadhaar_number": _safe_get(doc, "aadhaar_number") or _safe_get(doc, "aadhar_number"),
# # # 		"provident_fund_account": _safe_get(doc, "provident_fund_account"),
# # # 		"uan": _safe_get(doc, "uan_number"),
# # # 		"esic_no": _safe_get(doc, "esic_no") or _safe_get(doc, "esi_number"),
# # # 	}


# # # # @frappe.whitelist()
# # # # def get_attendance_calendar(employee, year):
# # # # 	"""Return day-level attendance records for the given year, plus a
# # # # 	month-wise summary of status counts (Present, Absent, Half Day,
# # # # 	On Leave, Work From Home, Holiday)."""
# # # # 	year = cint(year)

# # # # 	records = frappe.get_all(
# # # # 		"Attendance",
# # # # 		filters={
# # # # 			"employee": employee,
# # # # 			"docstatus": 1,
# # # # 			"attendance_date": ["between", [f"{year}-01-01", f"{year}-12-31"]],
# # # # 		},
# # # # 		fields=["attendance_date", "status", "leave_type"],
# # # # 	)

# # # # 	# month (1-12) -> status -> count
# # # # 	summary = {m: {} for m in range(1, 13)}
# # # # 	days_by_month = {m: [] for m in range(1, 13)}

# # # # 	for r in records:
# # # # 		d = getdate(r.attendance_date)
# # # # 		summary[d.month][r.status] = summary[d.month].get(r.status, 0) + 1
# # # # 		days_by_month[d.month].append(
# # # # 			{"day": d.day, "status": r.status, "leave_type": r.leave_type}
# # # # 		)

# # # # 	months = []
# # # # 	for m in range(1, 13):
# # # # 		months.append(
# # # # 			{
# # # # 				"month": m,
# # # # 				"month_name": calendar.month_name[m],
# # # # 				"days_in_month": calendar.monthrange(year, m)[1],
# # # # 				"days": days_by_month[m],
# # # # 				"summary": summary[m],
# # # # 			}
# # # # 		)

# # # # 	return {"year": year, "months": months}

# # # def get_holiday_list_for_employee(employee):
# # # 	holiday_list, company = frappe.db.get_value(
# # # 		"Employee", employee, ["holiday_list", "company"]
# # # 	) or (None, None)

# # # 	if not holiday_list and company:
# # # 		holiday_list = frappe.get_cached_value("Company", company, "default_holiday_list")

# # # 	return holiday_list


# # # @frappe.whitelist()
# # # def get_attendance_calendar(employee, year):
# # # 	"""Return day-level attendance records for the given year (merged with
# # # 	the employee's Holiday List), plus a month-wise status summary."""
# # # 	year = cint(year)
# # # 	from_date = f"{year}-01-01"
# # # 	to_date = f"{year}-12-31"

# # # 	records = frappe.get_all(
# # # 		"Attendance",
# # # 		filters={
# # # 			"employee": employee,
# # # 			"docstatus": 1,
# # # 			"attendance_date": ["between", [from_date, to_date]],
# # # 		},
# # # 		fields=["attendance_date", "status", "leave_type"],
# # # 	)

# # # 	# date -> {"status": ..., "leave_type": ...}
# # # 	day_info = {}
# # # 	for r in records:
# # # 		day_info[getdate(r.attendance_date)] = {
# # # 			"status": r.status,
# # # 			"leave_type": r.leave_type,
# # # 		}

# # # 	# overlay holidays from the employee's Holiday List, but don't override
# # # 	# an actual Attendance record already marked for that day
# # # 	holiday_list = get_holiday_list_for_employee(employee)
# # # 	if holiday_list:
# # # 		holidays = frappe.get_all(
# # # 			"Holiday",
# # # 			filters={"parent": holiday_list, "holiday_date": ["between", [from_date, to_date]]},
# # # 			fields=["holiday_date", "description"],
# # # 		)
# # # 		for h in holidays:
# # # 			d = getdate(h.holiday_date)
# # # 			if d not in day_info:
# # # 				day_info[d] = {"status": "Holiday", "leave_type": h.description}

# # # 	summary = {m: {} for m in range(1, 13)}
# # # 	days_by_month = {m: [] for m in range(1, 13)}

# # # 	for d, info in day_info.items():
# # # 		status = info["status"]
# # # 		summary[d.month][status] = summary[d.month].get(status, 0) + 1
# # # 		days_by_month[d.month].append(
# # # 			{"day": d.day, "status": status, "leave_type": info["leave_type"]}
# # # 		)

# # # 	months = []
# # # 	for m in range(1, 13):
# # # 		months.append(
# # # 			{
# # # 				"month": m,
# # # 				"month_name": calendar.month_name[m],
# # # 				"days_in_month": calendar.monthrange(year, m)[1],
# # # 				"days": days_by_month[m],
# # # 				"summary": summary[m],
# # # 			}
# # # 		)

# # # 	return {"year": year, "months": months, "holiday_list": holiday_list}

# # # @frappe.whitelist()
# # # def get_leave_summary(employee, year):
# # # 	"""Return allocated / taken / balance per leave type for the year."""
# # # 	year = cint(year)
# # # 	from_date = f"{year}-01-01"
# # # 	to_date = f"{year}-12-31"

# # # 	leave_types = frappe.get_all("Leave Type", pluck="name")
# # # 	result = []

# # # 	for lt in leave_types:
# # # 		allocation = frappe.db.sql(
# # # 			"""
# # # 			SELECT SUM(total_leaves_allocated) AS allocated
# # # 			FROM `tabLeave Allocation`
# # # 			WHERE employee=%s AND leave_type=%s AND docstatus=1
# # # 			AND from_date <= %s AND to_date >= %s
# # # 			""",
# # # 			(employee, lt, to_date, from_date),
# # # 			as_dict=True,
# # # 		)
# # # 		allocated = (allocation[0].allocated if allocation else 0) or 0

# # # 		taken = frappe.db.sql(
# # # 			"""
# # # 			SELECT SUM(total_leave_days) AS taken
# # # 			FROM `tabLeave Application`
# # # 			WHERE employee=%s AND leave_type=%s AND docstatus=1
# # # 			AND YEAR(from_date)=%s
# # # 			""",
# # # 			(employee, lt, year),
# # # 			as_dict=True,
# # # 		)
# # # 		taken = (taken[0].taken if taken else 0) or 0

# # # 		if allocated or taken:
# # # 			result.append(
# # # 				{
# # # 					"leave_type": lt,
# # # 					"allocated": allocated,
# # # 					"taken": taken,
# # # 					"balance": allocated - taken,
# # # 				}
# # # 			)

# # # 	loss_of_pay = frappe.db.sql(
# # # 		"""
# # # 		SELECT COUNT(*) AS lop
# # # 		FROM `tabAttendance`
# # # 		WHERE employee=%s AND status='Absent' AND docstatus=1
# # # 		AND YEAR(attendance_date)=%s
# # # 		""",
# # # 		(employee, year),
# # # 		as_dict=True,
# # # 	)
# # # 	lop = (loss_of_pay[0].lop if loss_of_pay else 0) or 0

# # # 	return {"leave_types": result, "loss_of_pay": lop}


# import calendar

# import frappe
# from frappe import _
# from frappe.utils import add_days, cint, getdate


# def _safe_get(doc, fieldname):
# 	"""Return a field value if it exists on the doctype, else None.
# 	Different HRMS versions/customizations name Aadhaar/PAN/UAN fields
# 	differently, so this avoids hard failures."""
# 	return doc.get(fieldname) if fieldname in doc.as_dict() else None


# def _get_optional_fieldname(doctype, candidates):
# 	"""Return the first fieldname from `candidates` that actually exists on
# 	`doctype`, else None. Used for fields that may be named differently
# 	across customizations (e.g. the "Permission Request" link field on
# 	Attendance)."""
# 	meta = frappe.get_meta(doctype)
# 	for fieldname in candidates:
# 		if meta.has_field(fieldname):
# 			return fieldname
# 	return None


# @frappe.whitelist()
# def get_employee_details(employee):
# 	"""Fetch the employee profile card data."""
# 	if not frappe.has_permission("Employee", "read", employee):
# 		frappe.throw(_("Not permitted"), frappe.PermissionError)

# 	doc = frappe.get_doc("Employee", employee)

# 	reports_to = None
# 	if doc.reports_to:
# 		reports_to = frappe.db.get_value("Employee", doc.reports_to, "employee_name")

# 	return {
# 		"employee": doc.name,
# 		"employee_name": doc.employee_name,
# 		"designation": doc.designation,
# 		"department": doc.department,
# 		"status": doc.status,
# 		"image": doc.image,
# 		"date_of_joining": doc.date_of_joining,
# 		"date_of_birth": doc.date_of_birth,
# 		"gender": doc.gender,
# 		"marital_status": doc.marital_status,
# 		"blood_group": doc.blood_group,
# 		"reports_to": reports_to,
# 		"company_email": doc.company_email or doc.personal_email,
# 		"cell_number": doc.cell_number,
# 		"current_address": doc.current_address,
# 		"pan_number": _safe_get(doc, "pan_number"),
# 		"aadhaar_number": _safe_get(doc, "aadhaar_number") or _safe_get(doc, "aadhar_number"),
# 		"provident_fund_account": _safe_get(doc, "provident_fund_account"),
# 		"uan": _safe_get(doc, "uan"),
# 		"esic_no": _safe_get(doc, "esic_no") or _safe_get(doc, "esi_number"),
# 	}


# def get_holiday_list_for_employee(employee):
# 	holiday_list, company = frappe.db.get_value(
# 		"Employee", employee, ["holiday_list", "company"]
# 	) or (None, None)

# 	if not holiday_list and company:
# 		holiday_list = frappe.get_cached_value("Company", company, "default_holiday_list")

# 	return holiday_list


# @frappe.whitelist()
# def get_attendance_calendar(employee, year):
# 	"""Return day-level attendance records for the given year (merged with
# 	the employee's Holiday List), plus a month-wise summary of status
# 	counts (Present, Absent, Half Day, On Leave, Work From Home, Holiday)."""
# 	year = cint(year)
# 	from_date = f"{year}-01-01"
# 	to_date = f"{year}-12-31"

# 	records = frappe.get_all(
# 		"Attendance",
# 		filters={
# 			"employee": employee,
# 			"docstatus": 1,
# 			"attendance_date": ["between", [from_date, to_date]],
# 		},
# 		fields=["attendance_date", "status", "leave_type"],
# 	)

# 	# date -> {"status": ..., "leave_type": ...}
# 	day_info = {}
# 	for r in records:
# 		day_info[getdate(r.attendance_date)] = {
# 			"status": r.status,
# 			"leave_type": r.leave_type,
# 		}

# 	# overlay holidays from the employee's Holiday List, but don't override
# 	# an actual Attendance record already marked for that day
# 	holiday_list = get_holiday_list_for_employee(employee)
# 	if holiday_list:
# 		holidays = frappe.get_all(
# 			"Holiday",
# 			filters={"parent": holiday_list, "holiday_date": ["between", [from_date, to_date]]},
# 			fields=["holiday_date", "description"],
# 		)
# 		for h in holidays:
# 			d = getdate(h.holiday_date)
# 			if d not in day_info:
# 				day_info[d] = {"status": "Holiday", "leave_type": h.description}

# 	summary = {m: {} for m in range(1, 13)}
# 	days_by_month = {m: [] for m in range(1, 13)}
# 	leave_type_summary = {m: {} for m in range(1, 13)}
# 	leave_types_seen = set()

# 	for d, info in day_info.items():
# 		status = info["status"]
# 		summary[d.month][status] = summary[d.month].get(status, 0) + 1
# 		days_by_month[d.month].append(
# 			{"day": d.day, "status": status, "leave_type": info["leave_type"]}
# 		)
# 		if info["leave_type"]:
# 			leave_type_summary[d.month][info["leave_type"]] = (
# 				leave_type_summary[d.month].get(info["leave_type"], 0) + 1
# 			)
# 			leave_types_seen.add(info["leave_type"])

# 	months = []
# 	for m in range(1, 13):
# 		months.append(
# 			{
# 				"month": m,
# 				"month_name": calendar.month_name[m],
# 				"days_in_month": calendar.monthrange(year, m)[1],
# 				"days": days_by_month[m],
# 				"summary": summary[m],
# 				"leave_type_summary": leave_type_summary[m],
# 			}
# 		)

# 	return {
# 		"year": year,
# 		"months": months,
# 		"holiday_list": holiday_list,
# 		"leave_types": sorted(leave_types_seen),
# 	}


# @frappe.whitelist()
# def get_leave_summary(employee, year):
# 	"""Return allocated / taken / balance per leave type for the year."""
# 	year = cint(year)
# 	from_date = f"{year}-01-01"
# 	to_date = f"{year}-12-31"

# 	leave_types = frappe.get_all("Leave Type", pluck="name")
# 	result = []

# 	for lt in leave_types:
# 		allocation = frappe.db.sql(
# 			"""
# 			SELECT SUM(total_leaves_allocated) AS allocated
# 			FROM `tabLeave Allocation`
# 			WHERE employee=%s AND leave_type=%s AND docstatus=1
# 			AND from_date <= %s AND to_date >= %s
# 			""",
# 			(employee, lt, to_date, from_date),
# 			as_dict=True,
# 		)
# 		allocated = (allocation[0].allocated if allocation else 0) or 0

# 		taken = frappe.db.sql(
# 			"""
# 			SELECT SUM(total_leave_days) AS taken
# 			FROM `tabLeave Application`
# 			WHERE employee=%s AND leave_type=%s AND docstatus=1
# 			AND YEAR(from_date)=%s
# 			""",
# 			(employee, lt, year),
# 			as_dict=True,
# 		)
# 		taken = (taken[0].taken if taken else 0) or 0

# 		if allocated or taken:
# 			result.append(
# 				{
# 					"leave_type": lt,
# 					"allocated": allocated,
# 					"taken": taken,
# 					"balance": allocated - taken,
# 				}
# 			)

# 	loss_of_pay = frappe.db.sql(
# 		"""
# 		SELECT COUNT(*) AS lop
# 		FROM `tabAttendance`
# 		WHERE employee=%s AND status='Absent' AND docstatus=1
# 		AND YEAR(attendance_date)=%s
# 		""",
# 		(employee, year),
# 		as_dict=True,
# 	)
# 	lop = (loss_of_pay[0].lop if loss_of_pay else 0) or 0

# 	return {"leave_types": result, "loss_of_pay": lop}


# # ---------------------------------------------------------------------------
# # Payroll-cycle (21st-to-20th) attendance table
# # ---------------------------------------------------------------------------

# LEAVE_BUCKET_KEYWORDS = {
# 	"EE": ["earned"],
# 	"CC": ["casual"],
# 	"SS": ["sick"],
# 	"Spl/ML": ["special", "maternity", "compensatory", "paternity"],
# }


# def _bucket_for_leave_type(leave_type):
# 	"""Map a Leave Type name to one of the 4 fixed summary columns
# 	(EE / CC / SS / Spl-ML). Anything unrecognised falls into Spl/ML
# 	so it's still counted somewhere - adjust LEAVE_BUCKET_KEYWORDS above
# 	if your Leave Type names don't match these keywords."""
# 	if not leave_type:
# 		return None
# 	lt = leave_type.lower()
# 	for bucket, keywords in LEAVE_BUCKET_KEYWORDS.items():
# 		for kw in keywords:
# 			if kw in lt:
# 				return bucket
# 	return "Spl/ML"


# def _leave_abbr(leave_type):
# 	"""Short 2-3 letter code shown inside a day cell, e.g. 'Casual Leave' -> 'CL'."""
# 	if not leave_type:
# 		return ""
# 	words = [w for w in leave_type.split() if w.lower() != "leave"]
# 	if not words:
# 		return leave_type[:2].upper()
# 	if len(words) == 1:
# 		return words[0][:2].upper()
# 	return "".join(w[0] for w in words).upper()


# @frappe.whitelist()
# def get_payroll_attendance(employee, year):
# 	"""Build the 21st-to-20th payroll-cycle attendance table: one row per
# 	month with day-level status codes, plus calculated totals per row
# 	(Calendar Days, Working Days, Worked Days, EE/CC/SS/Spl-ML, WW/HH,
# 	Paid Days, AA, Late, Permission)."""
# 	year = cint(year)
# 	holiday_list = get_holiday_list_for_employee(employee)

# 	span_start = f"{year - 1}-12-01"
# 	span_end = f"{year}-12-31"

# 	# "late_entry" is a standard Attendance checkbox. The "Permission
# 	# Request" link fieldname on Attendance varies by customization, so we
# 	# try a few common names and use whichever one actually exists. If your
# 	# custom fieldname isn't in this list, add it here.
# 	late_field = "late_entry" if frappe.get_meta("Attendance").has_field("late_entry") else None
# 	permission_field = _get_optional_fieldname(
# 		"Attendance",
# 		[
# 			"permission_request",
# 			"custom_permission_request",
# 			"permission_request_id",
# 			"custom_permission_request_id",
# 		],
# 	)

# 	att_fields = ["attendance_date", "status", "leave_type"]
# 	if late_field:
# 		att_fields.append(late_field)
# 	if permission_field:
# 		att_fields.append(permission_field)

# 	att_records = frappe.get_all(
# 		"Attendance",
# 		filters={
# 			"employee": employee,
# 			"docstatus": 1,
# 			"attendance_date": ["between", [span_start, span_end]],
# 		},
# 		fields=att_fields,
# 	)
# 	day_info = {}
# 	for r in att_records:
# 		day_info[getdate(r.attendance_date)] = {
# 			"status": r.status,
# 			"leave_type": r.leave_type,
# 			"late_entry": bool(r.get(late_field)) if late_field else False,
# 			"permission_request": r.get(permission_field) if permission_field else None,
# 		}

# 	holiday_info = {}
# 	if holiday_list:
# 		holidays = frappe.get_all(
# 			"Holiday",
# 			filters={"parent": holiday_list, "holiday_date": ["between", [span_start, span_end]]},
# 			fields=["holiday_date", "weekly_off"],
# 		)
# 		for h in holidays:
# 			holiday_info[getdate(h.holiday_date)] = bool(h.weekly_off)

# 	rows = []
# 	for m in range(1, 13):
# 		end_date = getdate(f"{year}-{m:02d}-20")
# 		if m == 1:
# 			start_date = getdate(f"{year - 1}-12-21")
# 		else:
# 			start_date = getdate(f"{year}-{m - 1:02d}-21")

# 		days = []
# 		bucket_totals = {"EE": 0, "CC": 0, "SS": 0, "Spl/ML": 0}
# 		ww_hh = 0
# 		aa = 0
# 		present_days = 0
# 		late_count = 0
# 		permission_count = 0

# 		d = start_date
# 		while d <= end_date:
# 			info = day_info.get(d)
# 			code, css = "", "att-blank"

# 			if info:
# 				status = info["status"]
# 				leave_type = info["leave_type"]
# 				if status == "Present":
# 					code, css = "XX", "att-present"
# 					present_days += 1
# 				elif status == "Absent":
# 					code, css = "AA", "att-absent"
# 					aa += 1
# 				elif status == "Half Day":
# 					abbr = _leave_abbr(leave_type)
# 					code, css = (f"0.5{abbr}" if abbr else "0.5"), "att-halfday"
# 					bucket = _bucket_for_leave_type(leave_type)
# 					if bucket:
# 						bucket_totals[bucket] += 0.5
# 					present_days += 0.5
# 				elif status == "On Leave":
# 					abbr = _leave_abbr(leave_type)
# 					code, css = (abbr or "LV"), "att-leave"
# 					bucket = _bucket_for_leave_type(leave_type)
# 					if bucket:
# 						bucket_totals[bucket] += 1
# 				elif status == "Work From Home":
# 					code, css = "WFH", "att-wfh"
# 				else:
# 					code, css = (status[:2].upper() if status else ""), "att-other"

# 				# late entry / permission are overlaid on top of whatever the
# 				# day's status already is - they mark the cell, they don't
# 				# replace it.
# 				if info.get("late_entry"):
# 					late_count += 1
# 					css = f"{css} att-late-flag"
# 				if info.get("permission_request"):
# 					permission_count += 1
# 					css = f"{css} att-permission-flag"
# 			elif d in holiday_info:
# 				if holiday_info[d]:
# 					code, css = "WW", "att-weeklyoff"
# 				else:
# 					code, css = "HH", "att-holiday"
# 				ww_hh += 1

# 			days.append({"date": str(d), "day": d.day, "code": code, "css": css})
# 			d = add_days(d, 1)

# 		calendar_days = (end_date - start_date).days + 1
# 		working_days = calendar_days - ww_hh
# 		worked_days = present_days
# 		paid_days = calendar_days - aa

# 		rows.append(
# 			{
# 				"month_name": calendar.month_name[m],
# 				"start_date": str(start_date),
# 				"end_date": str(end_date),
# 				"days": days,
# 				"totals": {
# 					"calendar_days": calendar_days,
# 					"working_days": working_days,
# 					"worked_days": worked_days,
# 					"ee": bucket_totals["EE"],
# 					"cc": bucket_totals["CC"],
# 					"ss": bucket_totals["SS"],
# 					"spl_ml": bucket_totals["Spl/ML"],
# 					"ww_hh": ww_hh,
# 					"paid_days": paid_days,
# 					"aa": aa,
# 					"late": late_count,
# 					"permission": permission_count,
# 				},
# 			}
# 		)

# 	grand = {
# 		"calendar_days": 0, "working_days": 0, "worked_days": 0,
# 		"ee": 0, "cc": 0, "ss": 0, "spl_ml": 0,
# 		"ww_hh": 0, "paid_days": 0, "aa": 0,
# 		"late": 0, "permission": 0,
# 	}
# 	for row in rows:
# 		for k in grand:
# 			grand[k] += row["totals"][k]

# 	return {"year": year, "rows": rows, "grand_totals": grand}



import calendar

import frappe
from frappe import _
from frappe.utils import add_days, cint, getdate


def _safe_get(doc, fieldname):
	"""Return a field value if it exists on the doctype, else None.
	Different HRMS versions/customizations name Aadhaar/PAN/UAN fields
	differently, so this avoids hard failures."""
	return doc.get(fieldname) if fieldname in doc.as_dict() else None


def _get_optional_fieldname(doctype, candidates):
	"""Return the first fieldname from `candidates` that actually exists on
	`doctype`, else None. Used for fields that may be named differently
	across customizations (e.g. the "Permission Request" link field on
	Attendance)."""
	meta = frappe.get_meta(doctype)
	for fieldname in candidates:
		if meta.has_field(fieldname):
			return fieldname
	return None


@frappe.whitelist()
def get_employee_details(employee):
	"""Fetch the employee profile card data."""
	if not frappe.has_permission("Employee", "read", employee):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	doc = frappe.get_doc("Employee", employee)

	reports_to = None
	if doc.reports_to:
		reports_to = frappe.db.get_value("Employee", doc.reports_to, "employee_name")

	return {
		"employee": doc.name,
		"employee_name": doc.employee_name,
		"designation": doc.designation,
		"department": doc.department,
		"status": doc.status,
		"image": doc.image,
		"date_of_joining": doc.date_of_joining,
		"date_of_birth": doc.date_of_birth,
		"gender": doc.gender,
		"marital_status": doc.marital_status,
		"blood_group": doc.blood_group,
		"reports_to": reports_to,
		"company_email": doc.company_email or doc.personal_email,
		"cell_number": doc.cell_number,
		"current_address": doc.current_address,
		"pan_number": _safe_get(doc, "pan_number"),
		"aadhaar_number": _safe_get(doc, "aadhaar_number") or _safe_get(doc, "aadhar_number"),
		"provident_fund_account": _safe_get(doc, "provident_fund_account"),
		"uan": _safe_get(doc, "uan"),
		"esic_no": _safe_get(doc, "esic_no") or _safe_get(doc, "esi_number"),
	}


def get_holiday_list_for_employee(employee):
	holiday_list, company = frappe.db.get_value(
		"Employee", employee, ["holiday_list", "company"]
	) or (None, None)

	if not holiday_list and company:
		holiday_list = frappe.get_cached_value("Company", company, "default_holiday_list")

	return holiday_list


@frappe.whitelist()
def get_attendance_calendar(employee, year):
	"""Return day-level attendance records for the given year (merged with
	the employee's Holiday List), plus a month-wise summary of status
	counts (Present, Absent, Half Day, On Leave, Work From Home, Holiday)."""
	year = cint(year)
	from_date = f"{year}-01-01"
	to_date = f"{year}-12-31"

	records = frappe.get_all(
		"Attendance",
		filters={
			"employee": employee,
			"docstatus": 1,
			"attendance_date": ["between", [from_date, to_date]],
		},
		fields=["attendance_date", "status", "leave_type"],
	)

	day_info = {}
	for r in records:
		day_info[getdate(r.attendance_date)] = {
			"status": r.status,
			"leave_type": r.leave_type,
		}

	holiday_list = get_holiday_list_for_employee(employee)
	if holiday_list:
		holidays = frappe.get_all(
			"Holiday",
			filters={"parent": holiday_list, "holiday_date": ["between", [from_date, to_date]]},
			fields=["holiday_date", "description"],
		)
		for h in holidays:
			d = getdate(h.holiday_date)
			if d not in day_info:
				day_info[d] = {"status": "Holiday", "leave_type": h.description}

	summary = {m: {} for m in range(1, 13)}
	days_by_month = {m: [] for m in range(1, 13)}
	leave_type_summary = {m: {} for m in range(1, 13)}
	leave_types_seen = set()

	for d, info in day_info.items():
		status = info["status"]
		summary[d.month][status] = summary[d.month].get(status, 0) + 1
		days_by_month[d.month].append(
			{"day": d.day, "status": status, "leave_type": info["leave_type"]}
		)
		if info["leave_type"]:
			leave_type_summary[d.month][info["leave_type"]] = (
				leave_type_summary[d.month].get(info["leave_type"], 0) + 1
			)
			leave_types_seen.add(info["leave_type"])

	months = []
	for m in range(1, 13):
		months.append(
			{
				"month": m,
				"month_name": calendar.month_name[m],
				"days_in_month": calendar.monthrange(year, m)[1],
				"days": days_by_month[m],
				"summary": summary[m],
				"leave_type_summary": leave_type_summary[m],
			}
		)

	return {
		"year": year,
		"months": months,
		"holiday_list": holiday_list,
		"leave_types": sorted(leave_types_seen),
	}


@frappe.whitelist()
def get_leave_summary(employee, year):
	"""Return allocated / taken / balance per leave type for the year."""
	year = cint(year)
	from_date = f"{year}-01-01"
	to_date = f"{year}-12-31"

	leave_types = frappe.get_all("Leave Type", pluck="name")
	result = []

	for lt in leave_types:
		allocation = frappe.db.sql(
			"""
			SELECT SUM(total_leaves_allocated) AS allocated
			FROM `tabLeave Allocation`
			WHERE employee=%s AND leave_type=%s AND docstatus=1
			AND from_date <= %s AND to_date >= %s
			""",
			(employee, lt, to_date, from_date),
			as_dict=True,
		)
		allocated = (allocation[0].allocated if allocation else 0) or 0

		taken = frappe.db.sql(
			"""
			SELECT SUM(total_leave_days) AS taken
			FROM `tabLeave Application`
			WHERE employee=%s AND leave_type=%s AND docstatus=1
			AND YEAR(from_date)=%s
			""",
			(employee, lt, year),
			as_dict=True,
		)
		taken = (taken[0].taken if taken else 0) or 0

		if allocated or taken:
			result.append(
				{
					"leave_type": lt,
					"allocated": allocated,
					"taken": taken,
					"balance": allocated - taken,
				}
			)

	loss_of_pay = frappe.db.sql(
		"""
		SELECT COUNT(*) AS lop
		FROM `tabAttendance`
		WHERE employee=%s AND status='Absent' AND docstatus=1
		AND YEAR(attendance_date)=%s
		""",
		(employee, year),
		as_dict=True,
	)
	lop = (loss_of_pay[0].lop if loss_of_pay else 0) or 0

	return {"leave_types": result, "loss_of_pay": lop}


# ---------------------------------------------------------------------------
# Payroll-cycle (21st-to-20th) attendance table
# ---------------------------------------------------------------------------

LEAVE_BUCKET_KEYWORDS = {
	"EE": ["earned"],
	"CC": ["casual"],
	"SS": ["sick"],
	"Spl/ML": ["special", "maternity", "compensatory", "paternity"],
}


def _bucket_for_leave_type(leave_type):
	"""Map a Leave Type name to one of the 4 fixed summary columns
	(EE / CC / SS / Spl-ML). Anything unrecognised falls into Spl/ML
	so it's still counted somewhere - adjust LEAVE_BUCKET_KEYWORDS above
	if your Leave Type names don't match these keywords."""
	if not leave_type:
		return None
	lt = leave_type.lower()
	for bucket, keywords in LEAVE_BUCKET_KEYWORDS.items():
		for kw in keywords:
			if kw in lt:
				return bucket
	return "Spl/ML"


def _leave_abbr(leave_type):
	"""Short 2-3 letter code shown inside a day cell, e.g. 'Casual Leave' -> 'CL'."""
	if not leave_type:
		return ""
	words = [w for w in leave_type.split() if w.lower() != "leave"]
	if not words:
		return leave_type[:2].upper()
	if len(words) == 1:
		return words[0][:2].upper()
	return "".join(w[0] for w in words).upper()


@frappe.whitelist()
def get_payroll_attendance(employee, year):
	"""Build the 21st-to-20th payroll-cycle attendance table: one row per
	month with day-level status codes, plus calculated totals per row
	(Calendar Days, Working Days, Worked Days, EE/CC/SS/Spl-ML, WW/HH,
	Paid Days, AA, Late, Permission)."""
	year = cint(year)
	holiday_list = get_holiday_list_for_employee(employee)

	span_start = f"{year - 1}-12-01"
	span_end = f"{year}-12-31"

	late_field = "late_entry" if frappe.get_meta("Attendance").has_field("late_entry") else None
	permission_field = _get_optional_fieldname(
		"Attendance",
		[
			"permission_request",
			"custom_permission_request",
			"permission_request_id",
			"custom_permission_request_id",
		],
	)

	att_fields = ["attendance_date", "status", "leave_type"]
	if late_field:
		att_fields.append(late_field)
	if permission_field:
		att_fields.append(permission_field)

	att_records = frappe.get_all(
		"Attendance",
		filters={
			"employee": employee,
			"docstatus": 1,
			"attendance_date": ["between", [span_start, span_end]],
		},
		fields=att_fields,
	)
	day_info = {}
	for r in att_records:
		day_info[getdate(r.attendance_date)] = {
			"status": r.status,
			"leave_type": r.leave_type,
			"late_entry": bool(r.get(late_field)) if late_field else False,
			"permission_request": r.get(permission_field) if permission_field else None,
		}

	holiday_info = {}
	if holiday_list:
		holidays = frappe.get_all(
			"Holiday",
			filters={"parent": holiday_list, "holiday_date": ["between", [span_start, span_end]]},
			fields=["holiday_date", "weekly_off"],
		)
		for h in holidays:
			holiday_info[getdate(h.holiday_date)] = bool(h.weekly_off)

	rows = []
	for m in range(1, 13):
		end_date = getdate(f"{year}-{m:02d}-20")
		if m == 1:
			start_date = getdate(f"{year - 1}-12-21")
		else:
			start_date = getdate(f"{year}-{m - 1:02d}-21")

		days = []
		bucket_totals = {"EE": 0, "CC": 0, "SS": 0, "Spl/ML": 0}
		ww_hh = 0
		aa = 0
		present_days = 0
		late_count = 0
		permission_count = 0

		d = start_date
		while d <= end_date:
			info = day_info.get(d)
			code, css = "", "att-blank"

			if info:
				status = info["status"]
				leave_type = info["leave_type"]
				if status == "Present":
					code, css = "XX", "att-present"
					present_days += 1
				elif status == "Absent":
					code, css = "AA", "att-absent"
					aa += 1
				elif status == "Half Day":
					abbr = _leave_abbr(leave_type)
					code, css = (f"0.5{abbr}" if abbr else "0.5"), "att-halfday"
					bucket = _bucket_for_leave_type(leave_type)
					if bucket:
						bucket_totals[bucket] += 0.5
					present_days += 0.5
				elif status == "On Leave":
					abbr = _leave_abbr(leave_type)
					code, css = (abbr or "LV"), "att-leave"
					bucket = _bucket_for_leave_type(leave_type)
					if bucket:
						bucket_totals[bucket] += 1
				elif status == "Work From Home":
					code, css = "WFH", "att-wfh"
				else:
					code, css = (status[:2].upper() if status else ""), "att-other"

				if info.get("late_entry"):
					late_count += 1
					css = f"{css} att-late-flag"
				if info.get("permission_request"):
					permission_count += 1
					css = f"{css} att-permission-flag"
			elif d in holiday_info:
				if holiday_info[d]:
					code, css = "WW", "att-weeklyoff"
				else:
					code, css = "HH", "att-holiday"
				ww_hh += 1

			days.append({"date": str(d), "day": d.day, "code": code, "css": css})
			d = add_days(d, 1)

		calendar_days = (end_date - start_date).days + 1
		working_days = calendar_days - ww_hh
		worked_days = present_days
		paid_days = calendar_days - aa

		rows.append(
			{
				"month_name": calendar.month_name[m],
				"start_date": str(start_date),
				"end_date": str(end_date),
				"days": days,
				"totals": {
					"calendar_days": calendar_days,
					"working_days": working_days,
					"worked_days": worked_days,
					"ee": bucket_totals["EE"],
					"cc": bucket_totals["CC"],
					"ss": bucket_totals["SS"],
					"spl_ml": bucket_totals["Spl/ML"],
					"ww_hh": ww_hh,
					"paid_days": paid_days,
					"aa": aa,
					"late": late_count,
					"permission": permission_count,
				},
			}
		)

	grand = {
		"calendar_days": 0, "working_days": 0, "worked_days": 0,
		"ee": 0, "cc": 0, "ss": 0, "spl_ml": 0,
		"ww_hh": 0, "paid_days": 0, "aa": 0,
		"late": 0, "permission": 0,
	}
	for row in rows:
		for k in grand:
			grand[k] += row["totals"][k]

	return {"year": year, "rows": rows, "grand_totals": grand}


# ---------------------------------------------------------------------------
# Monthly History (Leave / Late / Permission) - independent Jan-Dec charts,
# each with its own year, that sit above the Leave Summary section.
# ---------------------------------------------------------------------------

HISTORY_LEAVE_BUCKET_KEYWORDS = {
	"EL": ["earned"],
	"CL": ["casual"],
	"SL": ["sick"],
}


def _history_bucket_for_leave_type(leave_type):
	"""Map a Leave Type name to EL / CL / SL for the history charts.
	Anything unrecognised (e.g. Maternity, Compensatory) is skipped here -
	LOP is derived separately from Attendance 'Absent' records, not from
	Leave Type. Extend HISTORY_LEAVE_BUCKET_KEYWORDS if you have more
	leave types you want folded into EL/CL/SL."""
	if not leave_type:
		return None
	lt = leave_type.lower()
	for bucket, keywords in HISTORY_LEAVE_BUCKET_KEYWORDS.items():
		for kw in keywords:
			if kw in lt:
				return bucket
	return None


def _empty_month_leave_rows():
	return [
		{"month": m, "month_name": calendar.month_name[m], "EL": 0, "CL": 0, "SL": 0, "LOP": 0}
		for m in range(1, 13)
	]


@frappe.whitelist()
def get_leave_history(employee, year):
	"""Month-wise (Jan-Dec) leave taken, split into EL / CL / SL / LOP,
	for the given calendar year. Used for the 'Leave History' chart."""
	year = cint(year)
	from_date = f"{year}-01-01"
	to_date = f"{year}-12-31"

	rows = _empty_month_leave_rows()
	by_month = {r["month"]: r for r in rows}

	leave_apps = frappe.get_all(
		"Leave Application",
		filters={
			"employee": employee,
			"docstatus": 1,
			"from_date": ["between", [from_date, to_date]],
		},
		fields=["from_date", "leave_type", "total_leave_days"],
	)
	for la in leave_apps:
		bucket = _history_bucket_for_leave_type(la.leave_type)
		if not bucket:
			continue
		m = getdate(la.from_date).month
		by_month[m][bucket] += la.total_leave_days or 0

	lop_records = frappe.get_all(
		"Attendance",
		filters={
			"employee": employee,
			"docstatus": 1,
			"status": "Absent",
			"attendance_date": ["between", [from_date, to_date]],
		},
		fields=["attendance_date"],
	)
	for r in lop_records:
		m = getdate(r.attendance_date).month
		by_month[m]["LOP"] += 1

	total_leave = sum(r["EL"] + r["CL"] + r["SL"] for r in rows)
	total_lop = sum(r["LOP"] for r in rows)

	return {
		"year": year,
		"months": rows,
		"total_leave": total_leave,
		"total_lop": total_lop,
	}


@frappe.whitelist()
def get_late_history(employee, year):
	"""Month-wise (Jan-Dec) count of late-entry marked Attendance records
	for the given calendar year. Used for the 'Late History' chart."""
	year = cint(year)
	from_date = f"{year}-01-01"
	to_date = f"{year}-12-31"

	late_field = "late_entry" if frappe.get_meta("Attendance").has_field("late_entry") else None
	months = [{"month": m, "month_name": calendar.month_name[m], "count": 0} for m in range(1, 13)]

	if late_field:
		by_month = {r["month"]: r for r in months}
		records = frappe.get_all(
			"Attendance",
			filters={
				"employee": employee,
				"docstatus": 1,
				"attendance_date": ["between", [from_date, to_date]],
				late_field: 1,
			},
			fields=["attendance_date"],
		)
		for r in records:
			m = getdate(r.attendance_date).month
			by_month[m]["count"] += 1

	total_late = sum(r["count"] for r in months)
	return {"year": year, "months": months, "total_late": total_late}


@frappe.whitelist()
def get_permission_history(employee, year):
	"""Month-wise (Jan-Dec) count of Attendance records linked to a
	Permission Request, for the given calendar year. Used for the
	'Permission' chart."""
	year = cint(year)
	from_date = f"{year}-01-01"
	to_date = f"{year}-12-31"

	permission_field = _get_optional_fieldname(
		"Attendance",
		[
			"permission_request",
			"custom_permission_request",
			"permission_request_id",
			"custom_permission_request_id",
		],
	)
	months = [{"month": m, "month_name": calendar.month_name[m], "count": 0} for m in range(1, 13)]

	if permission_field:
		by_month = {r["month"]: r for r in months}
		records = frappe.get_all(
			"Attendance",
			filters={
				"employee": employee,
				"docstatus": 1,
				"attendance_date": ["between", [from_date, to_date]],
				permission_field: ["is", "set"],
			},
			fields=["attendance_date"],
		)
		for r in records:
			m = getdate(r.attendance_date).month
			by_month[m]["count"] += 1

	total_permission = sum(r["count"] for r in months)
	return {"year": year, "months": months, "total_permission": total_permission}