// Copyright (c) 2025, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Att settings', {
	update_att: function(frm) {
		frappe.call({
			'method':'infac.create_attendance.mark_att',
			// callback(r){
			// 	frm.set_value('hours',r.message[0])
			// }
		})
	}
});
