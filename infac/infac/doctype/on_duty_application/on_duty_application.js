// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('On Duty Application', {
	validate(frm){
		frappe.call({
			'method':'infac.infac.doctype.on_duty_application.on_duty_application.get_time_difference',
			'args':{
				in_time:frm.doc.in_time,
				out_time : frm.doc.out_time,
				od_date : frm.doc.od_date,
				hours:frm.doc.hours
			},
			callback(r){
				frm.set_value('hours',r.message[0])
			}
		})
	},
});
