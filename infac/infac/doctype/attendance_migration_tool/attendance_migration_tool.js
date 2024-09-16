// Copyright (c) 2023, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Migration Tool', {
	refresh: function(frm) {
		frm.disable_save()
		frm.set_value('from_date',"")
	},
	convert(frm){
		frappe.call({
			'method':'infac.infac.doctype.attendance_migration_tool.attendance_migration_tool.holiday_att_to_att',
			args:{
				"from_date": frm.doc.from_date,
				'document':frm.doc.from || ""
			},
			freeze:true,
			freeze_message: 'Updating....',
			callback:function(r){
				if(r.message){
					frappe.msgprint(__("Attendance Updated Successfully"));

				}
			}
		})
	},
});
