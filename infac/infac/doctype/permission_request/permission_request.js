// Copyright (c) 2021, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Permission Request', {
	validate(frm){
		frappe.call({
			'method':'infac.infac.doctype.permission_request.permission_request.get_time_difference',
			'args':{
				from_time:frm.doc.from_time,
				to_time : frm.doc.to_time,
				permission_date : frm.doc.permission_date,
				hours:frm.doc.hours
			},
			callback(r){
				frm.set_value('hours',r.message[0])
			}
		})
	},
	// from_time:function(frm) {
	// 	if(frm.doc.from_time){
	// 		frappe.call({
	// 			'method':'infac.infac.doctype.permission_request.permission_request.to_time',
	// 			'args':{
	// 				from_time:frm.doc.from_time
	// 			},
	// 			callback(r){
	// 				console.log(r.message)
	// 				frm.set_value('to_time',r.message)
	// 			}
	// 		})
	// }
});