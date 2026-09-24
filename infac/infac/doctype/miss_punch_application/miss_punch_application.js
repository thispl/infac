// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Miss Punch Application', {
	date(frm){
		frappe.call({
			'method':'infac.infac.doctype.miss_punch_application.miss_punch_application.get_attendance',
			'args':{
				emp:frm.doc.employee,
				att_date:frm.doc.date,
			},
			callback(r){
				$.each(r.message,function(i,v){
					frm.set_value('in_time',v.in_time)
					frm.set_value('out_time',v.out_time)
					frm.set_value('shift',v.shift)
				})
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