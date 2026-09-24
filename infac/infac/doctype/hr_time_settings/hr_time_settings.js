// Copyright (c) 2025, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('HR Time Settings', {
	refresh(frm) {
       if (frappe.session.user !== "kumarans@infacindia.com") {
            frm.set_df_property("employee_creation_limit", "read_only", 1);
        } else {
            frm.set_df_property("employee_creation_limit", "read_only", 0);
        }
    }

});
