// Copyright (c) 2023, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Attendance Regularize Tool', {
	refresh: function(frm) {
		frm.disable_save()
	},
	attach: function(frm) {
		// frm.disable_save()
		var file_field = frm.doc.attach;
		if (file_field) {
		  var file_extension = file_field.split('.').pop().toLowerCase();
		  if (file_extension !== 'csv') {
			frappe.msgprint(__('Only CSV files are allowed'));
			frm.set_value('attach', ''); // Clear the field value
		  }
		}
	},
	process(frm){
		// console.log("HI")
		frappe.call({
			"method": "infac.custom.att_reg_bulk_upload_csv",
			"args":{
				"filename" : frm.doc.attach
			},
			freeze: true,
			freeze_message: 'Processing Attendance....',
			callback(r){
				console.log(r.message)
				if(r.message == "ok"){
					frappe.msgprint(__("Attendance's are uploaded in Successfully"))
				}
			}
		})
	},
});
