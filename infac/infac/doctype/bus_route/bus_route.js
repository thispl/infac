// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bus Route', {
	bus_route(frm){
		var route = frm.doc.bus_route
		var change_to_upper_case = route.toUpperCase()
		frm.set_value('bus_route',change_to_upper_case)
	}
});
