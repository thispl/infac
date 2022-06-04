// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Correction', {
	onload:function(frm){
		if(frm.doc.__islocal){
			var previous_month = frappe.datetime.add_months(frappe.datetime.month_start(),-1)
			var from_date = frappe.datetime.add_days(previous_month,20)
			frm.set_value('from_date',from_date)
			frm.set_value('to_date',frappe.datetime.add_days(frappe.datetime.month_start(),19))

		}
	},
	get_employees:function(frm) {
		frm.call('get_employees').then((r) =>  {
			console.log(r.message)
		})
	}
});
