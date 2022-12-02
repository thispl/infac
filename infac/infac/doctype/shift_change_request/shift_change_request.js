// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Change Request', {

	to_date(frm){
		frappe.call({
			'method':'infac.infac.doctype.shift_change_request.shift_change_request.get_shift_assignment',
			'args':{
				emp:frm.doc.employee,
				from_date:frm.doc.from_date,
				to_date:frm.doc.to_date,
				name:frm.doc.name
			},
			callback(r){
				frm.set_value('assigned_shift',r.message[0])
			}
		})
	}
	
	
	
});
