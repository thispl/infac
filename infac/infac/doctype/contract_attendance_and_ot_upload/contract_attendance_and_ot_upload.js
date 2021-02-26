// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contract Attendance and OT Upload', {
	// refresh: function(frm) {

	// }
	start_date: function (frm) {
		frappe.call({
			method: 'infac.infac.doctype.contract_attendance_and_ot_upload.contract_attendance_and_ot_upload.get_end_date',
			args: {
				frequency: "monthly",
				start_date: frm.doc.start_date
			},
			callback: function (r) {
				if (r.message) {
					frm.set_value('end_date', r.message.end_date);
				}
			}
		});
	},
	mark_attendance: function (frm) {
		frappe.call({
			method: 'infac.infac.doctype.contract_attendance_and_ot_upload.contract_attendance_and_ot_upload.mark_attendance',
			args: {
				file_url: frm.doc.csv_attachment,
				start_date: frm.doc.start_date,
				end_date: frm.doc.end_date
			},
			callback: function (r) {
				if (r.message) {
				}
			}
		});
	},
});
