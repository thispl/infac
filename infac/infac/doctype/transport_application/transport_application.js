// Copyright (c) 2023, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transport Application', {
	refresh(frm){
		frm.add_custom_button(__("Print Transport Application"), function () {
			var f_name = frm.doc.name
			var print_format = "Transport Entry";
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Transport Application")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			))
		}).css('background-color', '#0EE30E');
	}
});
