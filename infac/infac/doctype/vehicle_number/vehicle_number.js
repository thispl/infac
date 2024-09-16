// Copyright (c) 2023, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Number', {
	vehicle_name(frm){
		var route = frm.doc.vehicle_name
		var change_to_upper_case = route.toUpperCase()
		frm.set_value('vehicle_name',change_to_upper_case)
	}
});
