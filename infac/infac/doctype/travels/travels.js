// Copyright (c) 2023, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Travels', {
	travels_name(frm){
		var travel = frm.doc.travels_name
		var change_to_upper_case = travel.toUpperCase()
		frm.set_value('travels_name',change_to_upper_case)
	}
});
