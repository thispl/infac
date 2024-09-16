// Copyright (c) 2024, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Live Attendance', {
	refresh: function(frm) {
		frm.disable_save()
		frappe.call({
			method:"infac.infac.doctype.live_attendance.live_attendance.get_data_system",
			args:{
			},
			callback(r){
				frm.fields_dict.attendance.$wrapper.empty().append(r.message)
			}
		})
	},
	onload: function(frm) {
		frm.disable_save()
		frappe.call({
			method:"infac.infac.doctype.live_attendance.live_attendance.get_data_system",
			args:{
			},
			callback(r){
				frm.fields_dict.attendance.$wrapper.empty().append(r.message)
			}
		})
	}
});
