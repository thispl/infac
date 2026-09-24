// Copyright (c) 2021, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Permission Request', {
	// validate(frm){
	// 	// frm.trigger('employee_id')
	// 	// frappe.call({
	// 	// 	'method':'infac.infac.doctype.permission_request.permission_request.get_time_difference',
	// 	// 	'args':{
	// 	// 		from_time:frm.doc.from_time,
	// 	// 		to_time : frm.doc.to_time,
	// 	// 		permission_date : frm.doc.permission_date,
	// 	// 		hours:frm.doc.hours
	// 	// 	},
	// 	// 	callback(r){
	// 	// 		frm.set_value('hours',r.message[0])
	// 	// 	}
	// 	// })
	// 	frappe.call({
	// 		method: "infac.infac.doctype.permission_request.permission_request.get_time_difference",
	// 		args: {
	// 			permission_date: frm.doc.permission_date,
	// 			from_time: frm.doc.from_time,
	// 			to_time: frm.doc.to_time
	// 		},
	// 		callback: function(r) {
	// 			if(r.message) {
	// 				console.log("Total Hours:", r.message.total_hours);
	// 				console.log("Permission Hours:", r.message.perm_hr);
	// 				frm.set_value("total_hours", r.message.perm_hr);  // example
	// 			}
	// 		}
	// 	});
	// 	if (frm.doc.employee_id){
	// 		frappe.call({
	// 			'method':'infac.infac.doctype.permission_request.permission_request.permission_validation',
	// 			'args':{
	// 				'emp':frm.doc.employee_id,
	// 				'att_date':frm.doc.permission_date
	// 			},
	// 			callback(r){
	// 				if(r.message == 'On Leave'){
	// 					frappe.msgprint("Employee Permission and Leave can not Applied same Time")
	// 					frappe.validated = false
	// 				}
	// 			}
	// 		})
	// 	}
	// },
	// permission_hour(frm){
	// 	if (frm.doc.from_time){
	// 		frappe.call({
	// 			'method':'infac.infac.doctype.permission_request.permission_request.validate_time',
	// 			'args':{	
	// 				hour:frm.doc.permission_hour,
	// 				from_time:frm.doc.from_time,
	// 			},
	// 			callback(r){
	// 				$.each(r.message,function(i,v){
	// 					frm.set_value('to_time',v.get_time)
	// 				})
	// 			}
	// 		})
	// 	}
	// },
	onload(frm){
		if (frm.doc.employee_id){
			if (frm.doc.permission_date){
				frappe.call({
					'method':'infac.infac.doctype.permission_request.permission_request.permission_validation',
					'args':{
						'emp':frm.doc.employee_id,
						'att_date':frm.doc.permission_date
					},
					callback(r){
						if(r.message == 'On Leave'){
							frappe.msgprint("Employee Permission and Leave can not Applied same Time")
							frappe.validated = false
						}
					}
				})
			}	
		}
	},
	permission_date(frm){
		if (frm.doc.employee_id){
			if (frm.doc.permission_date){
				frappe.call({
					'method':'infac.infac.doctype.permission_request.permission_request.permission_validation',
					'args':{
						'emp':frm.doc.employee_id,
						'att_date':frm.doc.permission_date
					},
					callback(r){
						if(r.message == 'On Leave'){
							frappe.msgprint("Employee Permission and Leave can not Applied same Time")
							frappe.validated = false
						}
					}
				})
			}	
		}
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
		// if (frm.doc.level_1_approved_by) {
        //     frm.fields_dict.level_1_approved_by.$wrapper
        //         .find('.control-label')
        //         .css('color', 'blue');
        // }
		// if (frm.doc.level_1_timing) {
        //     frm.fields_dict.level_1_timing.$wrapper
        //         .find('.control-label')
        //         .css('color', 'blue');
        // }
		// if (frm.doc.level_1_approved_by) {
        //     frm.fields_dict.level_1_approved_by.$wrapper
        //         .find('input, textarea, .control-value')
        //         .css({
        //             "background-color": "#fff3cd",   // light orange
        //             "border": "1px solid #ff9800"
        //         });
        // }

		// if (frm.doc.level_2_approved_by) {
        //     frm.fields_dict.level_2_approved_by.$wrapper
        //         .find('.control-label')
        //         .css('color', 'orange');
        // }
		// if (frm.doc.level_2_timing) {
        //     frm.fields_dict.level_2_timing.$wrapper
        //         .find('.control-label')
        //         .css('color', 'orange');
        // }
		
		// if (frm.doc.rejected) {
        //     frm.fields_dict.rejected.$wrapper
        //         .find('.control-label')
        //         .css('color', 'orange');
        // }

	},
	// before_workflow_action(frm) {
    //     if (frm.doc.workflow_state === "Incharge Pending" && frm.selected_workflow_action === "Approve") {
    //         return new Promise((resolve, reject) => {
    //             let d = new frappe.ui.Dialog({
    //                 title: "Approved Through",
    //                 fields: [{
    //                     fieldtype: "Select",
    //                     fieldname: "approved_through",
    //                     label: "Approved Through",
    //                     reqd: 1,
    //                     options: "\nBy Call\nBy Direct Discussion\nBy Message\nBy WhatsApp"
    //                 }],
    //                 primary_action_label: "Submit",
    //                 primary_action(values) {
    //                     d.hide();
    //                     frappe.db.set_value("Permission Request", frm.doc.name, "approved_through", values.approved_through)
    //                         .then(() => {
    //                             resolve();
    //                         });
    //                 },
    //                 secondary_action_label: "Cancel",
    //                 secondary_action() {
    //                     d.hide();
    //                     reject();
    //                 }
    //             });
    //             d.show();
    //         });
    //     }
    // },
    
	onload(frm){
			frm.fields_dict.approval_mark.$wrapper.empty();
			frm.fields_dict.html_1.$wrapper.empty();
	}

	// employee_id(frm){
	// 	if (frm.doc.employee_id){
	// 		frappe.call({
	// 			method:'infac.infac.doctype.permission_request.permission_request.get_employee_validation',
	// 			args:{
	// 				emp:frm.doc.employee_id
	// 			},
	// 			callback(r){
	// 			}
	// 		})
	// 	}
	// },
	// from_time(frm){
	// 	frm.call('get_session').then((r)=>{
	// 		frm.set_value('session',r.message)
	// 	})	
	// }
	
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
