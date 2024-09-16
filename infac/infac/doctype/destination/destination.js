// Copyright (c) 2023, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Destination', {
	destination_name(frm){
		var route = frm.doc.destination_name
		var change_to_upper_case = route.toUpperCase()
		frm.set_value('destination_name',change_to_upper_case)
	}
});
