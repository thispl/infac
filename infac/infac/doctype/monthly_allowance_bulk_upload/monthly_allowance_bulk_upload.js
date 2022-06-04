// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Allowance Bulk upload', {
	// refresh: function(frm) {

	// }
	get_template:function(frm){
		window.location.href = repl(frappe.request.url +
            '?cmd=%(cmd)s&payroll_date=%(payroll_date)s&employee_categpory=%(employee_category)s', {
            cmd: "infac.infac.doctype.monthly_allowance_bulk_upload.monthly_allowance_bulk_upload.get_template",
            payroll_date: frm.doc.payroll_date,
            employee_category:frm.doc.employee_category,
			})

	},
	after_save(frm){
		frappe.call({
			'method':'infac.infac.doctype.monthly_allowance_bulk_upload.monthly_allowance_bulk_upload'

		})

	}
});
