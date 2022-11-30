// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Upload Shift Schedule', {
	get_template: function (frm) {
        window.location.href = repl(frappe.request.url +
            '?cmd=%(cmd)s&from_date=%(from_date)s&to_date=%(to_date)s&department=%(department)s', {
            cmd: "infac.infac.doctype.bulk_upload_shift_schedule.bulk_upload_shift_schedule.get_template",
            from_date: frm.doc.from_date,
            to_date: frm.doc.to_date,
            department:frm.doc.department,
			department_line:frm.doc.department_line
        })
	},
	from_date(frm) {
		if (frm.doc.from_date) {
			if (frm.doc.from_date < frappe.datetime.now_date()) {
				frappe.msgprint("From Date should not be a Past Date")
				frm.set_value('from_date', '')
			}
			// if (frm.doc.from_date > frappe.datetime.add_days(frappe.datetime.now_date(), 7)) {
			// 	frappe.msgprint("From Date should be within 7 days from Today")
			// 	frm.set_value('from_date', '')
			// }
		}
	},
	to_date(frm) {
		if (frm.doc.to_date) {
			if (frm.doc.to_date < frappe.datetime.now_date()) {
				frappe.msgprint("To Date should not be a Past Date")
				frm.set_value('to_date', '')
			}
			else if (frm.doc.to_date < frm.doc.from_date) {
				frappe.msgprint("To Date should not be greater than From Date")
				frm.set_value('to_date', '')
			}
			else if (frm.doc.to_date > frappe.datetime.add_days(frm.doc.from_date, 7)) {
				frappe.msgprint("To Date should be within 8 days from From Date")
				frm.set_value('to_date', '')
			}
		}
	},	
});
