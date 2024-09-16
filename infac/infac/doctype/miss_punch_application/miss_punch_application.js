// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Miss Punch Application', {
	date(frm){
		frappe.call({
			'method':'infac.infac.doctype.miss_punch_application.miss_punch_application.get_attendance',
			'args':{
				emp:frm.doc.employee,
				att_date:frm.doc.date,
			},
			callback(r){
				$.each(r.message,function(i,v){
					frm.set_value('in_time',v.in_time)
					frm.set_value('out_time',v.out_time)
					frm.set_value('shift',v.shift)
				})
			}
		})
	},
});
