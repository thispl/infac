// Copyright (c) 2023, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Source', {
	source_name(frm){
		var route = frm.doc.source_name
		var change_to_upper_case = route.toUpperCase()
		frm.set_value('source_name',change_to_upper_case)
	}
});
