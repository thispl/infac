// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('On Duty Application', {
	validate(frm){
		frappe.call({
			'method':'infac.infac.doctype.on_duty_application.on_duty_application.get_time_difference',
			'args':{
				in_time:frm.doc.in_time,
				out_time : frm.doc.out_time,
				od_date : frm.doc.od_date,
				hours:frm.doc.hours
			},
			callback(r){
				frm.set_value('hours',r.message[0])
			}
		})
	},
	refresh(frm){
		frm.ignore_user_permission = false;
		frm.fields_dict.html_1.$wrapper.empty();
		frm.fields_dict.approval_mark.$wrapper.empty();
		if (!frm.is_new()) {
				frm.call('show_html').then(r => {
					frm.fields_dict.html_1.$wrapper.empty().append(r.message);
				});
		}
		if (!frm.is_new()) {
			if (frm.doc.workflow_state == 'Approved') {
				frm.fields_dict.approval_mark.$wrapper.empty().append('<img src="/files/Infac Approved.jpeg" alt="Approved" width="300" height="200">');
			}
			if (frm.doc.workflow_state == 'Incharge Pending' || frm.doc.workflow_state == 'Superior Pending' || frm.doc.workflow_state == 'HOD Pending') {
				frm.fields_dict.approval_mark.$wrapper.empty().append('<img src="/files/Infac Pending.jpeg" alt="Pending" width="300" height="200">');
			}
		}
		if (frm.doc.employee) {
            frappe.db.get_value("Employee", frm.doc.employee, "employment_type")
                .then(r => {
                    if (r.message && r.message.employment_type !== "STAFF") {

                        frm.disable_save();
                        frm.set_value("employee", "");

                        frappe.msgprint({
                            title: "Access Restricted",
                            message: 'Only <span style="color:red; font-weight:bold;">Staff</span> employees are allowed to apply for On Duty.',
                            indicator: "red"
                        });
                    } else {
                        frm.enable_save();
                    }
                });
        }

		highlight_field(frm, 'level_1_approved_by');
        highlight_field(frm, 'level_1_timing');

		highlight_field(frm, 'level_2_approved_by');
        highlight_field(frm, 'level_2_timing');

		highlight_field(frm, 'rejected');
        highlight_field(frm, 'rejected_timing');

        highlight_field(frm, 'created_by');
        highlight_field(frm, 'created_on');

	},
	onload(frm){
			frm.fields_dict.approval_mark.$wrapper.empty();
			frm.fields_dict.html_1.$wrapper.empty();
	},
	employee(frm){
		if (frm.doc.employee) {
            frappe.db.get_value("Employee", frm.doc.employee, "employment_type")
                .then(r => {
                    if (r.message && r.message.employment_type !== "STAFF") {

                        frm.disable_save();
                        frm.set_value("employee", "");

                        frappe.msgprint({
                            title: "Access Restricted",
                            message: 'Only <span style="color:red; font-weight:bold;">Staff</span> employees are allowed to apply for On Duty.',
                            indicator: "red"
                        });
                    } else {
                        frm.enable_save();
                    }
                });
        }
	}
});


function highlight_field(frm, fieldname) {
    if (frm.doc[fieldname]) {

        const wrapper = frm.fields_dict[fieldname].$wrapper;

        // label color
        wrapper.find('.control-label').css({
            "color": "grey",
            "font-weight": "bold"
        });

        // field background
        wrapper.find('input, textarea, .control-value').css({
            "background-color": "#fadede"
            
        });
    }
}