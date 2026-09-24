frappe.ui.form.on('Approval', {
	refresh: function (frm) {
		if(frappe.user.has_role(['System Manager'])){
			frm.disable_save()
			frm.clear_table("la_approval")
			frm.clear_table("pr_approval")
			frm.clear_table("od_approval")
			frm.clear_table("mp_approval")
			frm.clear_table("ot_approval")
			// frm.clear_table("sr_approval")
			// frm.clear_table("compoff_approval")
			$('*[data-fieldname="od_approval"]').find('.grid-remove-rows').hide();
			$('*[data-fieldname="od_approval"]').find('.grid-remove-all-rows').hide();
			$('*[data-fieldname="od_approval"]').find('.grid-add-row').remove()

			$('*[data-fieldname="pr_approval"]').find('.grid-remove-rows').hide();
			$('*[data-fieldname="pr_approval"]').find('.grid-remove-all-rows').hide();
			$('*[data-fieldname="pr_approval"]').find('.grid-add-row').remove()

			$('*[data-fieldname="la_approval"]').find('.grid-remove-rows').hide();
			$('*[data-fieldname="la_approval"]').find('.grid-remove-all-rows').hide();
			$('*[data-fieldname="la_approval"]').find('.grid-add-row').remove()

			$('*[data-fieldname="ot_approval"]').find('.grid-remove-rows').hide();
			$('*[data-fieldname="ot_approval"]').find('.grid-remove-all-rows').hide();
			$('*[data-fieldname="ot_approval"]').find('.grid-add-row').remove()

			$('*[data-fieldname="mp_approval"]').find('.grid-remove-rows').hide();
			$('*[data-fieldname="mp_approval"]').find('.grid-remove-all-rows').hide();
			$('*[data-fieldname="mp_approval"]').find('.grid-add-row').remove()

			// LA Table-FM
			if (frappe.user.has_role(['Superior'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Leave Application",
						"filters": [
							['workflow_state', '=', 'Incharge Pending'],
						],
						'field':['*'],
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Leave Application",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('la_approval', {
										'leave_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										'designation': r.message.designation,
										'department': r.message.department,
										'leave_type': r.message.leave_type,
										'leave_balance': r.message.leave_balance,
										'from_date': r.message.from_date,
                                        'to_date': r.message.to_date,
										'half_day': r.message.half_day,
										'half_day_date': r.message.half_day_date,
										// 'total_leave_days': r.message.total_leave_days,
										'total_leave_days': Number(r.message.total_leave_days).toFixed(1),
										// 'session': r.message.custom_session,
										// 'description': r.message.to_time,
										'level_1_approver': r.message.superior,
										'level_2_approver': r.message.hod,
										'posting_date': r.message.posting_date,
										// 'approver_name':r.message.custom_first_manager_name,
										'level_3_approver':r.message.factory_head,
										'hr':r.message.hr,
									})
									frm.refresh_field('la_approval')
								}
							})

						})
					}
				})
			}
			// LA Table-SM
			if (frappe.user.has_role(['HOD']) || frappe.user.has_role(['Plant Head'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Leave Application",
						"filters": [
							['workflow_state', '=', 'Superior Pending'],
						],
						'field':['*'],
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Leave Application",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('la_approval', {
										'leave_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										'designation': r.message.designation,
										'department': r.message.department,
										'leave_type': r.message.leave_type,
										'leave_balance': r.message.leave_balance,
										'from_date': r.message.from_date,
                                        'to_date': r.message.to_date,
										'half_day': r.message.half_day,
										'half_day_date': r.message.half_day_date,
										// 'total_leave_days': r.message.total_leave_days,
										'total_leave_days': Number(r.message.total_leave_days).toFixed(1),
										// 'session': r.message.custom_session,
										// 'description': r.message.to_time,
										'level_1_approver': r.message.superior,
										'level_2_approver': r.message.hod,
										'posting_date': r.message.posting_date,
										// 'approver_name':r.message.custom_first_manager_name,
										'level_3_approver':r.message.factory_head,
										'hr':r.message.hr,
									})
									frm.refresh_field('la_approval')
								}
							})

						})
					}
				})
			}
			// LA Table-HR 
			// if (frappe.user.has_role(['HR User'])) {
			// 	frappe.call({
			// 		"method": "frappe.client.get_list",
			// 		"args": {
			// 			"doctype": "Leave Application",
			// 			"filters": [
			// 				['workflow_state', '=', 'HR Pending'],
			// 			],
			// 			'field':['*'],
			// 			limit_page_length: 500
			// 		},
			// 		callback(r) {
			// 			$.each(r.message, function (i, d) {
			// 				frappe.call({
			// 					"method": "frappe.client.get",
			// 					"args": {
			// 						"doctype": "Leave Application",
			// 						"name": d.name
			// 					},
			// 					freeze: true,
			// 					freeze_message: "Loading...",
			// 					callback(r) {
			// 						frm.add_child('la_approval', {
			// 							'leave_application': r.message.name,
			// 							'employee': r.message.employee,
			// 							'employee_name': r.message.employee_name,
			// 							'workflow_state': r.message.workflow_state,
			// 							'request_date': r.message.request_date,
			// 							'department': r.message.department,
			// 							'leave_type': r.message.leave_type,
			// 							'leave_balance': r.message.leave_balance,
			// 							'from_date': r.message.from_date,
			// 							'half_day': r.message.half_day,
			// 							'half_day_date': r.message.half_day_date,
			// 							'total_leave_days': r.message.total_leave_days,
			// 							'session': r.message.custom_session,
			// 							'description': r.message.to_time,
			// 							'leave_approver': r.message.leave_approver,
			// 							'leave_approver_name': r.message.leave_approver_name,
			// 							'posting_date': r.message.posting_date
			// 						})
			// 						frm.refresh_field('la_approval')
			// 					}
			// 				})

			// 			})
			// 		}
			// 	})
			// }

			// LA Approval
			frm.fields_dict["la_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.la_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_leave_doc', {
								doctype: "Leave Application",
								name: d.leave_application,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						frm.refresh_field('la_approval')
					})
				}).addClass('btn-danger')

			frm.fields_dict["la_approval"].grid.add_custom_button(__('Approve'),
				function () {
					$.each(frm.doc.la_approval, function (i, d) {
						if (d.__checked == 1) {
							if (d.workflow_state == 'Incharge Pending') {
								frappe.msgprint(__("The Leave Application {0} has been Move to Superior Pending", [d.leave_application]));
								frm.call('submit_leave_doc', {
									doctype: "Leave Application",
									name: d.leave_application,
									workflow_state: 'Incharge Pending'
								}).then(r => {
									frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
									
								})
								
							}
							frm.refresh_field('la_approval')
							if (d.workflow_state == 'Superior Pending') {
								frappe.msgprint(__("The Leave Application {0} has been Approved", [d.leave_application]));
								frm.call('submit_leave_doc', {
									doctype: "Leave Application",
									name: d.leave_application,
									workflow_state: 'Superior Pending'
								}).then(r => {
									frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
									
								})
							}
						}
					})
					frappe.after_ajax(() => {
						location.reload();
					});
				}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

			// PR Table- FM
			if (frappe.user.has_role(['Superior'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Permission Request",
						"filters": [
							['workflow_state', '=', 'Incharge Pending'],
						],
						'field':['*'],
						
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Permission Request",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('pr_approval', {
										'permission_request': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										// 'requested_date': r.message.requested_date,
										'department': r.message.department,
										'designation': r.message.designation,
										'level_1_approver': r.message.superior,
										'level_2_approver': r.message.hod,
										'permission_date': r.message.permission_date,
										'shift': r.message.shift,
										'reason': r.message.reason,
										'session': r.message.session,
										'from_time': r.message.from_time,
										'to_time': r.message.to_time,
										// 'hours': r.message.hours,
										'level_3_approver':r.message.factory_head,
										'hr':r.message.hr

									})
									frm.refresh_field('pr_approval')
								}
							})

						})
					}
				})
			
			}
			// PR Table- SM
			if (frappe.user.has_role(['HOD'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Permission Request",
						"filters": [
							['workflow_state', '=', 'Superior Pending'],
						],
						'field':['*'],
						
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Permission Request",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('pr_approval', {
										'permission_request': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										// 'requested_date': r.message.requested_date,
										'department': r.message.department,
										'designation': r.message.designation,
										'level_1_approver': r.message.superior,
										'level_2_approver': r.message.hod,
										'permission_date': r.message.permission_date,
										'shift': r.message.shift,
										'reason': r.message.reason,
										'session': r.message.session,
										'from_time': r.message.from_time,
										'to_time': r.message.to_time,
										// 'hours': r.message.hours,
										'level_3_approver':r.message.factory_head,
										'hr':r.message.hr

									})
									frm.refresh_field('pr_approval')
								}
							})

						})
					}
				})
			
			}
			// PR Table- HR
			if (frappe.user.has_role(['Plant Head'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Permission Request",
						"filters": [
							['workflow_state', '=', 'HOD Pending'],
						],
						'field':['*'],
						
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Permission Request",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('pr_approval', {
										'permission_request': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										// 'requested_date': r.message.requested_date,
										'department': r.message.department,
										'designation': r.message.designation,
										'level_1_approver': r.message.superior,
										'level_2_approver': r.message.hod,
										'permission_date': r.message.permission_date,
										'shift': r.message.shift,
										'reason': r.message.reason,
										'session': r.message.session,
										'from_time': r.message.from_time,
										'to_time': r.message.to_time,
										// 'hours': r.message.hours,
										'level_3_approver':r.message.factory_head,
										'hr':r.message.hr

									})
									frm.refresh_field('pr_approval')
								}
							})

						})
					}
				})
			
			}
			frm.fields_dict["pr_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.pr_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_pr_doc', {
								doctype: "Permission Request",
								name: d.permission_request,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
					})
				}).addClass('btn-danger')
			frm.fields_dict["pr_approval"].grid.add_custom_button(__('Approve'),
			function () {
				$.each(frm.doc.pr_approval, function (i, d) {
					if (d.__checked == 1) {
						if (d.workflow_state == 'Incharge Pending') {
							frappe.msgprint(__("The Permission Request {0} has been Move to Superior Pending", [d.permission_request]));
							frm.call('submit_pr_doc', {
								doctype: "Permission Request",
								name: d.permission_request,
								workflow_state: 'Incharge Pending'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						if (d.workflow_state == 'Superior Pending') {
							frappe.msgprint(__("The Permission Request {0} has been Move to Superior Pending", [d.permission_request]));
							frm.call('submit_pr_doc', {
								doctype: "Permission Request",
								name: d.permission_request,
								workflow_state: 'Superior Pending'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						if (d.workflow_state == 'HOD Pending') {
							frappe.msgprint(__("The Permission Request {0} has been Approved", [d.permission_request]));
							frm.call('submit_pr_doc', {
								doctype: "Permission Request",
								name: d.permission_request,
								workflow_state: 'HOD Pending'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
					}
				})
				frappe.after_ajax(() => {
						location.reload();
					});
			}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

			// MPA Table - HR
			if (frappe.user.has_role(['Superior'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Miss Punch Application",
						"filters": [
							['workflow_state', '=', 'Incharge Pending'],
						],
						'field':['*'],
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Miss Punch Application",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('mp_approval', {
										'miss_punch_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'department': r.message.department,
										'workflow_state': r.message.workflow_state,
										'attendance_date': r.message.date,
										'attendance': r.message.attendance,
										'in_time': r.message.in_time,
										'out_time': r.message.out_time,
										'qr_shift': r.message.shift
									})
									frm.refresh_field('mp_approval')
								}
							})

						})
					}
				})
			}
			if (frappe.user.has_role(['HOD']) || frappe.user.has_role(["Plant Head"])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Miss Punch Application",
						"filters": [
							['workflow_state', '=', 'Superior Pending'],
						],
						'field':['*'],
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Miss Punch Application",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('mp_approval', {
										'miss_punch_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'department': r.message.department,
										'workflow_state': r.message.workflow_state,
										'attendance_date': r.message.date,
										'attendance': r.message.attendance,
										'in_time': r.message.in_time,
										'out_time': r.message.out_time,
										'qr_shift': r.message.shift
									})
									frm.refresh_field('mp_approval')
								}
							})

						})
					}
				})
			}
			frm.fields_dict["mp_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.mp_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_miss_punch_doc', {
								doctype: "Miss Punch Application",
								name: d.miss_punch_application,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
					})
				}).addClass('btn-danger')
			frm.fields_dict["mp_approval"].grid.add_custom_button(__('Approve'),
				function () {
					$.each(frm.doc.mp_approval, function (i, d) {
						if (d.__checked == 1) {
							if (d.workflow_state == "Incharge Pending") {
								frappe.msgprint(__("The Miss Punch Application {0} has been Move to Superior Pending", [d.miss_punch_application]));
								frm.call('submit_miss_punch_doc', {
									doctype: "Miss Punch Application",
									name: d.miss_punch_application,
									workflow_state: 'Incharge Pending'
								}).then(r => {
									frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
								})
							}
							if (d.workflow_state == "Superior Pending") {
								frappe.msgprint(__("The Miss Punch Application {0} has been Approved", [d.miss_punch_application]));
								frm.call('submit_miss_punch_doc', {
									doctype: "Miss Punch Application",
									name: d.miss_punch_application,
									workflow_state: 'Superior Pending'
								}).then(r => {
									frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
								})
							}
						}
					})
					frappe.after_ajax(() => {
						location.reload();
					});
			}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

			//  OD Table - FM
			if (frappe.user.has_role(['Superior'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "On Duty Application",
						"filters": [
							['workflow_state', '=', 'Incharge Pending'],
						],
						'field':['*'],
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "On Duty Application",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('od_approval', {
										'on_duty_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'department': r.message.department,
										'workflow_state': r.message.workflow_state,
										'from_date': r.message.od_date,
										// 'to_date': r.message.to_date,
										'from_time': r.message.in_time,
										'to_time': r.message.out_time,
										'od_time':r.message.hours,
										'travel': r.message.travel,
										'session': r.message.session,
										'place': r.message.place,
										'person_to_meet': r.message.person_to_meet,
										'company_name': r.message.company_name,
										'purpose': r.message.description,
										'approver_name':r.message.custom_first_manager_name
									})
									frm.refresh_field('od_approval')
								}
							})
		
						})
					}
				})
			}
			//  OD Table - SM
			if (frappe.user.has_role(['HOD'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "On Duty Application",
						"filters": [
							['workflow_state', '=', 'Superior Pending'],
						],
						'field':['*'],
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "On Duty Application",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('od_approval', {
										'on_duty_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'department': r.message.department,
										'workflow_state': r.message.workflow_state,
										'from_date': r.message.od_date,
										// 'to_date': r.message.to_date,
										'from_time': r.message.in_time,
										'to_time': r.message.out_time,
										'od_time':r.message.hours,
										'travel': r.message.travel,
										'session': r.message.session,
										'place': r.message.place,
										'person_to_meet': r.message.person_to_meet,
										'company_name': r.message.company_name,
										'purpose': r.message.description,
										'approver_name':r.message.custom_first_manager_name
									})
									frm.refresh_field('od_approval')
								}
							})
		
						})
					}
				})
			}
			//  OD Table - HR
			if (frappe.user.has_role(['Plant Head'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "On Duty Application",
						"filters": [
							['workflow_state', '=', 'HOD Pending'],
						],
						'field':['*'],
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "On Duty Application",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('od_approval', {
										'on_duty_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'department': r.message.department,
										'workflow_state': r.message.workflow_state,
										'from_date': r.message.od_date,
										// 'to_date': r.message.to_date,
										'from_time': r.message.in_time,
										'to_time': r.message.out_time,
										'od_time':r.message.hours,
										'travel': r.message.travel,
										'session': r.message.session,
										'place': r.message.place,
										'person_to_meet': r.message.person_to_meet,
										'company_name': r.message.company_name,
										'purpose': r.message.description,
										'approver_name':r.message.custom_first_manager_name
									})
									frm.refresh_field('od_approval')
								}
							})
		
						})
					}
				})
			}
			frm.fields_dict["od_approval"].grid.add_custom_button(__('Reject'),	
				function () {
					$.each(frm.doc.od_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_od_doc', {
								doctype: "On Duty Application",
								name: d.on_duty_application,
								workflow_state: 'Rejected'
							})
							frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
						}
					})
				}).addClass('btn-danger')
			frm.fields_dict["od_approval"].grid.add_custom_button(__('Approve'),
			function () {
				$.each(frm.doc.od_approval, function (i, d) {
					if (d.__checked == 1) {
						if (d.workflow_state == 'Incharge Pending') {
							frappe.msgprint(__("The On Duty Application {0} has been Move to Superior Pending", [d.on_duty_application]));
							frm.call('submit_od_doc', {
								doctype: "On Duty Application",
								name: d.on_duty_application,
								workflow_state: 'Incharge Pending'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						if (d.workflow_state == 'Superior Pending') {
							frappe.msgprint(__("The On Duty Application {0} has been Move to HOD Pending", [d.on_duty_application]));
							frm.call('submit_od_doc', {
								doctype: "On Duty Application",
								name: d.on_duty_application,
								workflow_state: 'Superior Pending'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						if (d.workflow_state == 'HOD Pending') {
							frappe.msgprint(__("The On Duty Application {0} has been Approved", [d.on_duty_application]));
							frm.call('submit_od_doc', {
								doctype: "On Duty Application",
								name: d.on_duty_application,
								workflow_state: 'HOD Pending'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						
					}
				})
				frappe.after_ajax(() => {
						location.reload();
					});
			}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

			// OT Table-FM
			if (frappe.user.has_role(['Superior'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Overtime Request",
						"filters": [
							['workflow_state', '=', 'Incharge Pending'],
							
						],
						'field':['*'],
						limit_page_length: 2000
					},
					callback(r) {
						
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Overtime Request",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									// frm.clear_table("ot_approval")
									if (r.message.ot_hour != '0:00:00'){
										frm.add_child('ot_approval', {
											'overtime_request': r.message.name,
											'employee': r.message.employee,
											'employee_name': r.message.employee_name,
											'workflow_state': r.message.workflow_state,
											'ot_date': r.message.ot_date,
											'department': r.message.department,
											'shift': r.message.shift,
											'from_time': r.message.from_time,
											'to_time': r.message.to_time,
											'total_hours': r.message.total_hours,
											'ot_hours': r.message.ot_hours,
											'bio_in': r.message.bio_in,
											'bio_out': r.message.bio_out,
											'total_wh': r.message.total_wh,
											'approver': r.message.approver,
											'approver_id': r.message.approver_id,
											'approver_name':r.message.custom_first_manager_name
										})
										frm.refresh_field('ot_approval')
									}
								}
							})

						})
					}
				})
			}
			//OT Table-SM
			if (frappe.user.has_role(['HOD'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Overtime Request",
						"filters": [
							['workflow_state', '=', 'Superior Pending'],
							
						],
						'field':['*'],
						limit_page_length: 2000
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Overtime Request",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									if (r.message.ot_hour != '0:00:00'){
										frm.add_child('ot_approval', {
											'overtime_request': r.message.name,
											'employee': r.message.employee,
											'employee_name': r.message.employee_name,
											'workflow_state': r.message.workflow_state,
											'ot_date': r.message.ot_date,
											'department': r.message.department,
											'shift': r.message.shift,
											'from_time': r.message.from_time,
											'to_time': r.message.to_time,
											'total_hours': r.message.total_hours,
											'ot_hours': r.message.ot_hours,
											'bio_in': r.message.bio_in,
											'bio_out': r.message.bio_out,
											'total_wh': r.message.total_wh,
											'approver': r.message.approver,
											'approver_id': r.message.approver_id,
											'approver_name':r.message.custom_first_manager_name
										})
										frm.refresh_field('ot_approval')
									}
								}
							})

						})
					}
				})
			}
			// OT Table-PM
			if (frappe.user.has_role(['Plant Head'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Overtime Request",
						"filters": [
							['workflow_state', '=', 'HOD Pending'],
						],
						'field':['*'],
						limit_page_length: 2000
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Overtime Request",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									if (r.message.ot_hour != '0:00:00'){
										frm.add_child('ot_approval', {
											'overtime_request': r.message.name,
											'employee': r.message.employee,
											'employee_name': r.message.employee_name,
											'workflow_state': r.message.workflow_state,
											'ot_date': r.message.ot_date,
											'department': r.message.department,
											'shift': r.message.shift,
											'from_time': r.message.from_time,
											'to_time': r.message.to_time,
											'payable_ot': r.message.payable_ot,
											'ot_hours': r.message.ot_hours,
											'bio_in': r.message.bio_in,
											'bio_out': r.message.bio_out,
											'total_wh': r.message.total_wh,
											'approver': r.message.approver,
											'approver_id': r.message.approver_id,
											'approver_name':r.message.custom_first_manager_name
										})
										frm.refresh_field('ot_approval')
									}
								}
							})

						})
					}
				})
			}
			
			frm.fields_dict["ot_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.ot_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_ot_doc', {
								doctype: "Overtime Request",
								name: d.overtime_request,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
					})
				}).addClass('btn-danger')
			frm.fields_dict["ot_approval"].grid.add_custom_button(__('Approve'),
			function () {
				$.each(frm.doc.ot_approval, function (i, d) {
					if (d.__checked == 1) {
						if (d.workflow_state == 'Incharge Pending') {
							frappe.msgprint(__("The Overtime Request {0} has been Move to Superior Pending", [d.overtime_request]));
							frm.call('submit_ot_doc', {
								doctype: "Overtime Request",
								name: d.overtime_request,
								workflow_state: 'Incharge Pending'
							}).then(r => {
								frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						if (d.workflow_state == 'Superior Pending') {
							frappe.msgprint(__("The Overtime Request {0} has been Move to HOD Pending", [d.overtime_request]));
							frm.call('submit_ot_doc', {
								doctype: "Overtime Request",
								name: d.overtime_request,
								workflow_state: 'Superior Pending'
							}).then(r => {
								frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						if (d.workflow_state == 'HOD Pending') {
							frappe.msgprint(__("The Overtime Request {0} has been Approved", [d.overtime_request]));
							frm.call('submit_ot_doc', {
								doctype: "Overtime Request",
								name: d.overtime_request,
								workflow_state: 'HOD Pending'
							}).then(r => {
								frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						
					}
				})
				frappe.after_ajax(() => {
						location.reload();
					});
			}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

			
			
			
		}
	else{
		frm.disable_save()
		frm.clear_table("la_approval")
		frm.clear_table("pr_approval")
		frm.clear_table("od_approval")
		frm.clear_table("mp_approval")
		frm.clear_table("ot_approval")
		// frm.clear_table("sr_approval")
		$('*[data-fieldname="od_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="od_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="od_approval"]').find('.grid-add-row').remove()

		$('*[data-fieldname="pr_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="pr_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="pr_approval"]').find('.grid-add-row').remove()

		$('*[data-fieldname="la_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="la_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="la_approval"]').find('.grid-add-row').remove()

		$('*[data-fieldname="ot_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="ot_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="ot_approval"]').find('.grid-add-row').remove()

		$('*[data-fieldname="mp_approval"]').find('.grid-remove-rows').hide();
		$('*[data-fieldname="mp_approval"]').find('.grid-remove-all-rows').hide();
		$('*[data-fieldname="mp_approval"]').find('.grid-add-row').remove()

		// $('*[data-fieldname="sr_approval"]').find('.grid-remove-rows').hide();
		// $('*[data-fieldname="sr_approval"]').find('.grid-remove-all-rows').hide();
		// $('*[data-fieldname="sr_approval"]').find('.grid-add-row').remove()
		// LA Table-FM
		if (frappe.user.has_role(['Superior'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Leave Application",
						"filters": [
							['workflow_state', '=', 'Incharge Pending'],
						],
						'field':['*'],
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Leave Application",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('la_approval', {
										'leave_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										'designation': r.message.designation,
										'department': r.message.department,
										'leave_type': r.message.leave_type,
										'leave_balance': r.message.leave_balance,
										'from_date': r.message.from_date,
                                        'to_date': r.message.to_date,
										'half_day': r.message.half_day,
										'half_day_date': r.message.half_day_date,
										// 'total_leave_days': r.message.total_leave_days,
										'total_leave_days': Number(r.message.total_leave_days).toFixed(1),
										// 'session': r.message.custom_session,
										// 'description': r.message.to_time,
										'level_1_approver': r.message.superior,
										'level_2_approver': r.message.hod,
										'posting_date': r.message.posting_date,
										// 'approver_name':r.message.custom_first_manager_name,
										'level_3_approver':r.message.factory_head,
										'hr':r.message.hr,
									})
									frm.refresh_field('la_approval')
								}
							})

						})
					}
				})
			}
			// LA Table-SM
		if (frappe.user.has_role(['HOD']) || frappe.user.has_role(['Plant Head'])) {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Leave Application",
					"filters": [
						['workflow_state', '=', 'Superior Pending'],
					],
					'field':['*'],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Leave Application",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								frm.add_child('la_approval', {
									'leave_application': r.message.name,
									'employee': r.message.employee,
									'employee_name': r.message.employee_name,
									'workflow_state': r.message.workflow_state,
									'designation': r.message.designation,
									'department': r.message.department,
									'leave_type': r.message.leave_type,
									'leave_balance': r.message.leave_balance,
									'from_date': r.message.from_date,
									'to_date': r.message.to_date,
									'half_day': r.message.half_day,
									'half_day_date': r.message.half_day_date,
									// 'total_leave_days': r.message.total_leave_days,
									'total_leave_days': Number(r.message.total_leave_days).toFixed(1),
									// 'session': r.message.custom_session,
									// 'description': r.message.to_time,
									'level_1_approver': r.message.superior,
									'level_2_approver': r.message.hod,
									'posting_date': r.message.posting_date,
									// 'approver_name':r.message.custom_first_manager_name,
									'level_3_approver':r.message.factory_head,
									'hr':r.message.hr,
								})
								frm.refresh_field('la_approval')
							}
						})

					})
				}
			})
		}
		
			// LA Approval
		frm.fields_dict["la_approval"].grid.add_custom_button(__('Reject'),
			function () {
				$.each(frm.doc.la_approval, function (i, d) {
					if (d.__checked == 1) {
						frm.call('submit_leave_doc', {
							doctype: "Leave Application",
							name: d.leave_application,
							workflow_state: 'Rejected'
						}).then(r => {
							frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
					frm.refresh_field('la_approval')
				})
			}).addClass('btn-danger')

		frm.fields_dict["la_approval"].grid.add_custom_button(__('Approve'),
			function () {
				$.each(frm.doc.la_approval, function (i, d) {
					if (d.__checked == 1) {
						if (d.workflow_state == 'Incharge Pending') {
							frappe.msgprint(__("The Leave Application {0} has been Move to Superior Pending", [d.leave_application]));
							frm.call('submit_leave_doc', {
								doctype: "Leave Application",
								name: d.leave_application,
								workflow_state: 'Incharge Pending'
							}).then(r => {
								frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
								
							})
							frm.refresh_field('la_approval')
						}
						if (d.workflow_state == 'Superior Pending') {
							frappe.msgprint(__("The Leave Application {0} has been Approved", [d.leave_application]));
							frm.call('submit_leave_doc', {
								doctype: "Leave Application",
								name: d.leave_application,
								workflow_state: 'Superior Pending'
							}).then(r => {
								frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
								
							})
							frm.refresh_field('la_approval')
						}
						if (d.workflow_state == 'HR Pending') {
							frappe.msgprint(__("The Leave Application {0} has been Approved", [d.leave_application]));
							frm.call('submit_leave_doc', {
								doctype: "Leave Application",
								name: d.leave_application,
								workflow_state: 'Approved'
							}).then(r => {
								frm.refresh_field('la_approval')
								frm.get_field("la_approval").grid.grid_rows[d.idx - 1].remove();
								
							})
							
						}
					}
				})
				frappe.after_ajax(() => {
						location.reload();
					});
			}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })


		// PR Table- FM
		if (frappe.user.has_role(['Superior'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Permission Request",
						"filters": [
							['workflow_state', '=', 'Incharge Pending'],
						],
						'field':['*'],
						
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Permission Request",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('pr_approval', {
										'permission_request': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										// 'requested_date': r.message.requested_date,
										'department': r.message.department,
										'designation': r.message.designation,
										'level_1_approver': r.message.superior,
										'level_2_approver': r.message.hod,
										'permission_date': r.message.permission_date,
										'shift': r.message.shift,
										'reason': r.message.reason,
										'session': r.message.session,
										'from_time': r.message.from_time,
										'to_time': r.message.to_time,
										// 'hours': r.message.hours,
										'level_3_approver':r.message.factory_head,
										'hr':r.message.hr

									})
									frm.refresh_field('pr_approval')
								}
							})

						})
					}
				})
			
			}
			// PR Table- SM
		if (frappe.user.has_role(['HOD'])) {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Permission Request",
					"filters": [
						['workflow_state', '=', 'Superior Pending'],
					],
					'field':['*'],
					
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Permission Request",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								frm.add_child('pr_approval', {
									'permission_request': r.message.name,
									'employee': r.message.employee,
									'employee_name': r.message.employee_name,
									'workflow_state': r.message.workflow_state,
									// 'requested_date': r.message.requested_date,
									'department': r.message.department,
									'designation': r.message.designation,
									'level_1_approver': r.message.superior,
									'level_2_approver': r.message.hod,
									'permission_date': r.message.permission_date,
									'shift': r.message.shift,
									'reason': r.message.reason,
									'session': r.message.session,
									'from_time': r.message.from_time,
									'to_time': r.message.to_time,
									// 'hours': r.message.hours,
									'level_3_approver':r.message.factory_head,
									'hr':r.message.hr

								})
								frm.refresh_field('pr_approval')
							}
						})

					})
				}
			})
		
		}
			// PR Table- HR
		if (frappe.user.has_role(['Plant Head'])) {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Permission Request",
					"filters": [
						['workflow_state', '=', 'HOD Pending'],
					],
					'field':['*'],
					
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Permission Request",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								frm.add_child('pr_approval', {
									'permission_request': r.message.name,
									'employee': r.message.employee,
									'employee_name': r.message.employee_name,
									'workflow_state': r.message.workflow_state,
									// 'requested_date': r.message.requested_date,
									'department': r.message.department,
									'designation': r.message.designation,
									'level_1_approver': r.message.superior,
									'level_2_approver': r.message.hod,
									'permission_date': r.message.permission_date,
									'shift': r.message.shift,
									'reason': r.message.reason,
									'session': r.message.session,
									'from_time': r.message.from_time,
									'to_time': r.message.to_time,
									// 'hours': r.message.hours,
									'level_3_approver':r.message.factory_head,
									'hr':r.message.hr

								})
								frm.refresh_field('pr_approval')
							}
						})

					})
				}
			})
		
		}
		frm.fields_dict["pr_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.pr_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_pr_doc', {
								doctype: "Permission Request",
								name: d.permission_request,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
					})
				}).addClass('btn-danger')
		frm.fields_dict["pr_approval"].grid.add_custom_button(__('Approve'),
		function () {
			$.each(frm.doc.pr_approval, function (i, d) {
				if (d.__checked == 1) {
					if (d.workflow_state == 'Incharge Pending') {
						frappe.msgprint(__("The Permission Request {0} has been Move to Superior Pending", [d.permission_request]));
						frm.call('submit_pr_doc', {
							doctype: "Permission Request",
							name: d.permission_request,
							workflow_state: 'Incharge Pending'
						}).then(r => {
							frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
					if (d.workflow_state == 'Superior Pending') {
						frappe.msgprint(__("The Permission Request {0} has been Move to Superior Pending", [d.permission_request]));
						frm.call('submit_pr_doc', {
							doctype: "Permission Request",
							name: d.permission_request,
							workflow_state: 'Superior Pending'
						}).then(r => {
							frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
					if (d.workflow_state == 'HOD Pending') {
						frappe.msgprint(__("The Permission Request {0} has been Approved", [d.permission_request]));
						frm.call('submit_pr_doc', {
							doctype: "Permission Request",
							name: d.permission_request,
							workflow_state: 'HOD Pending'
						}).then(r => {
							frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
				}
			})
			frappe.after_ajax(() => {
						location.reload();
					});
		}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

		// MPA Table - HR
		if (frappe.user.has_role(['Superior'])) {
				frappe.call({
					"method": "frappe.client.get_list",
					"args": {
						"doctype": "Miss Punch Application",
						"filters": [
							['workflow_state', '=', 'Incharge Pending'],
						],
						'field':['*'],
						limit_page_length: 500
					},
					callback(r) {
						$.each(r.message, function (i, d) {
							frappe.call({
								"method": "frappe.client.get",
								"args": {
									"doctype": "Miss Punch Application",
									"name": d.name
								},
								freeze: true,
								freeze_message: "Loading...",
								callback(r) {
									frm.add_child('mp_approval', {
										'miss_punch_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'department': r.message.department,
										'workflow_state': r.message.workflow_state,
										'attendance_date': r.message.date,
										'attendance': r.message.attendance,
										'in_time': r.message.in_time,
										'out_time': r.message.out_time,
										'qr_shift': r.message.shift
									})
									frm.refresh_field('mp_approval')
								}
							})

						})
					}
				})
			}
		if (frappe.user.has_role(['HOD']) || frappe.user.has_role(["Plant Head"])) {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Miss Punch Application",
					"filters": [
						['workflow_state', '=', 'Superior Pending'],
					],
					'field':['*'],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Miss Punch Application",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								frm.add_child('mp_approval', {
									'miss_punch_application': r.message.name,
									'employee': r.message.employee,
									'employee_name': r.message.employee_name,
									'department': r.message.department,
									'workflow_state': r.message.workflow_state,
									'attendance_date': r.message.date,
									'attendance': r.message.attendance,
									'in_time': r.message.in_time,
									'out_time': r.message.out_time,
									'qr_shift': r.message.shift
								})
								frm.refresh_field('mp_approval')
							}
						})

					})
				}
			})
		}
		frm.fields_dict["mp_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.mp_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_miss_punch_doc', {
								doctype: "Miss Punch Application",
								name: d.miss_punch_application,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
					})
				}).addClass('btn-danger')
		frm.fields_dict["mp_approval"].grid.add_custom_button(__('Approve'),
			function () {
				$.each(frm.doc.mp_approval, function (i, d) {
					if (d.__checked == 1) {
						if (d.workflow_state == "Incharge Pending") {
							frappe.msgprint(__("The Miss Punch Application {0} has been Move to Superior Pending", [d.miss_punch_application]));
							frm.call('submit_miss_punch_doc', {
								doctype: "Miss Punch Application",
								name: d.miss_punch_application,
								workflow_state: 'Incharge Pending'
							}).then(r => {
								frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						if (d.workflow_state == "Superior Pending") {
							frappe.msgprint(__("The Miss Punch Application {0} has been Approved", [d.miss_punch_application]));
							frm.call('submit_miss_punch_doc', {
								doctype: "Miss Punch Application",
								name: d.miss_punch_application,
								workflow_state: 'Superior Pending'
							}).then(r => {
								frm.get_field("mp_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
					}
				})
				frappe.after_ajax(() => {
						location.reload();
					});
		}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

		//  OD Table - FM
		if (frappe.user.has_role(['Superior'])) {
			frappe.db.get_value('Employee',{'user_id':frappe.session.user},['name'])
			.then(r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "On Duty Application",
					"filters": [
						['workflow_state', '=', 'Incharge Pending'],
						['employee','!=',r.message.name]
					],
					'field':['*'],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "On Duty Application",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								frm.add_child('od_approval', {
									'on_duty_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'department': r.message.department,
										'workflow_state': r.message.workflow_state,
										'from_date': r.message.od_date,
										// 'to_date': r.message.to_date,
										'from_time': r.message.in_time,
										'to_time': r.message.out_time,
										'od_time':r.message.hours,
										'travel': r.message.travel,
										'session': r.message.session,
										'place': r.message.place,
										'person_to_meet': r.message.person_to_meet,
										'company_name': r.message.company_name,
										'purpose': r.message.description,
										'approver_name':r.message.custom_first_manager_name
								})
								frm.refresh_field('od_approval')
							}
						})
	
					})
				}
			})
		})
		}
		//  OD Table - SM
		if (frappe.user.has_role(['HOD'])) {
			frappe.db.get_value('Employee',{'user_id':frappe.session.user},['name'])
			.then(r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "On Duty Application",
					"filters": [
						['workflow_state', '=', 'Superior Pending'],
						['employee','!=',r.message.name]
					],
					'field':['*'],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "On Duty Application",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								frm.add_child('od_approval', {
									'on_duty_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'department': r.message.department,
										'workflow_state': r.message.workflow_state,
										'from_date': r.message.od_date,
										// 'to_date': r.message.to_date,
										'from_time': r.message.in_time,
										'to_time': r.message.out_time,
										'od_time':r.message.hours,
										'travel': r.message.travel,
										'session': r.message.session,
										'place': r.message.place,
										'person_to_meet': r.message.person_to_meet,
										'company_name': r.message.company_name,
										'purpose': r.message.description,
										'approver_name':r.message.custom_first_manager_name
								})
								frm.refresh_field('od_approval')
							}
						})
	
					})
				}
			})
		})
		}
		//  OD Table - HR
		if (frappe.user.has_role(['Plant Head'])) {
			frappe.db.get_value('Employee',{'user_id':frappe.session.user},['name'])
			.then(r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "On Duty Application",
					"filters": [
						['workflow_state', '=', 'HOD Pending'],
						['employee','!=',r.message.name]
					],
					'field':['*'],
					limit_page_length: 500
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "On Duty Application",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								frm.add_child('od_approval', {
									'on_duty_application': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'department': r.message.department,
										'workflow_state': r.message.workflow_state,
										'from_date': r.message.od_date,
										// 'to_date': r.message.to_date,
										'from_time': r.message.in_time,
										'to_time': r.message.out_time,
										'od_time':r.message.hours,
										'travel': r.message.travel,
										'session': r.message.session,
										'place': r.message.place,
										'person_to_meet': r.message.person_to_meet,
										'company_name': r.message.company_name,
										'purpose': r.message.description,
										'approver_name':r.message.custom_first_manager_name
								})
								frm.refresh_field('od_approval')
							}
						})
	
					})
				}
			})
		})
		}
		frm.fields_dict["od_approval"].grid.add_custom_button(__('Reject'),	
				function () {
					$.each(frm.doc.od_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_od_doc', {
								doctype: "On Duty Application",
								name: d.on_duty_application,
								workflow_state: 'Rejected'
							})
							frm.get_field("od_approval").grid.grid_rows[d.idx - 1].remove();
						}
					})
				}).addClass('btn-danger')
			frm.fields_dict["od_approval"].grid.add_custom_button(__('Approve'),
			function () {
				$.each(frm.doc.od_approval, function (i, d) {
					if (d.__checked == 1) {
						if (d.workflow_state == 'Incharge Pending') {
							frappe.msgprint(__("The On Duty Application {0} has been Move to Superior Pending", [d.on_duty_application]));
							frm.call('submit_od_doc', {
								doctype: "On Duty Application",
								name: d.on_duty_application,
								workflow_state: 'Incharge Pending'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						if (d.workflow_state == 'Superior Pending') {
							frappe.msgprint(__("The On Duty Application {0} has been Move to HOD Pending", [d.on_duty_application]));
							frm.call('submit_od_doc', {
								doctype: "On Duty Application",
								name: d.on_duty_application,
								workflow_state: 'Superior Pending'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						if (d.workflow_state == 'HOD Pending') {
							frappe.msgprint(__("The On Duty Application {0} has been Approved", [d.on_duty_application]));
							frm.call('submit_od_doc', {
								doctype: "On Duty Application",
								name: d.on_duty_application,
								workflow_state: 'HOD Pending'
							}).then(r => {
								frm.get_field("pr_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
						
					}
				})
				frappe.after_ajax(() => {
						location.reload();
					});
			}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

		// OT Table-FM
		if (frappe.user.has_role(['Superior'])) {
			frappe.db.get_value('Employee',{'user_id':frappe.session.user},['name'])
			.then(r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Overtime Request",
					"filters": [
						['workflow_state', '=', 'FM Pending'],
						['employee','!=',r.message.name],
					],
					'field':['*'],
					limit_page_length: 2000
				},
				callback(r) {
					
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Overtime Request",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								// frm.clear_table("ot_approval")
								if (r.message.ot_hour != '0:00:00'){
									frm.add_child('ot_approval', {
										'overtime_request': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										'ot_date': r.message.ot_date,
										'department': r.message.department,
										'shift': r.message.shift,
										'from_time': r.message.from_time,
										'to_time': r.message.to_time,
										'total_hours': r.message.total_hours,
										'ot_hours': r.message.ot_hours,
										'bio_in': r.message.bio_in,
										'bio_out': r.message.bio_out,
										'total_wh': r.message.total_wh,
										'approver': r.message.approver,
										'approver_id': r.message.approver_id,
										'approver_name':r.message.custom_first_manager_name
									})
									frm.refresh_field('ot_approval')
								}
							}
						})

					})
				}
			})
		})
		}
		//OT Table-SM
		if (frappe.user.has_role(['HOD'])) {
			frappe.db.get_value('Employee',{'user_id':frappe.session.user},['name'])
			.then(r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Overtime Request",
					"filters": [
						['workflow_state', '=', 'SM Pending'],
						['employee','!=',r.message.name],
						
					],
					'field':['*'],
					limit_page_length: 2000
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Overtime Request",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								if (r.message.ot_hour != '0:00:00'){
									frm.add_child('ot_approval', {
										'overtime_request': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										'ot_date': r.message.ot_date,
										'department': r.message.department,
										'shift': r.message.shift,
										'from_time': r.message.from_time,
										'to_time': r.message.to_time,
										'total_hours': r.message.total_hours,
										'ot_hours': r.message.ot_hours,
										'bio_in': r.message.bio_in,
										'bio_out': r.message.bio_out,
										'total_wh': r.message.total_wh,
										'approver': r.message.approver,
										'approver_id': r.message.approver_id,
										'approver_name':r.message.custom_first_manager_name
									})
									frm.refresh_field('ot_approval')
								}
							}
						})

					})
				}
			})
		})
		}
		// OT Table-PM
		if (frappe.user.has_role(['Plant Head'])) {
			frappe.db.get_value('Employee',{'user_id':frappe.session.user},['name'])
			.then(r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Overtime Request",
					"filters": [
						['workflow_state', '=', 'Pending for Plant Manager'],
						['employee','!=',r.message.name],
					],
					'field':['*'],
					limit_page_length: 2000
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Overtime Request",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								if (r.message.ot_hour != '0:00:00'){
									frm.add_child('ot_approval', {
										'overtime_request': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										'ot_date': r.message.ot_date,
										'department': r.message.department,
										'shift': r.message.shift,
										'from_time': r.message.from_time,
										'to_time': r.message.to_time,
										'total_hours': r.message.total_hours,
										'ot_hours': r.message.ot_hours,
										'bio_in': r.message.bio_in,
										'bio_out': r.message.bio_out,
										'total_wh': r.message.total_wh,
										'approver': r.message.approver,
										'approver_id': r.message.approver_id,
										'approver_name':r.message.custom_first_manager_name
									})
									frm.refresh_field('ot_approval')
								}
							}
						})

					})
				}
			})
		})
		}
		// OT Table-HR
		if (frappe.user.has_role(['HR User'])) {
			frappe.db.get_value('Employee',{'user_id':frappe.session.user},['name'])
			.then(r => {
			frappe.call({
				"method": "frappe.client.get_list",
				"args": {
					"doctype": "Overtime Request",
					"filters": [
						['workflow_state', '=', 'HR Pending'],
						['employee','!=',r.message.name],
					],
					'field':['*'],
					limit_page_length: 2000
				},
				callback(r) {
					$.each(r.message, function (i, d) {
						frappe.call({
							"method": "frappe.client.get",
							"args": {
								"doctype": "Overtime Request",
								"name": d.name
							},
							freeze: true,
							freeze_message: "Loading...",
							callback(r) {
								if (r.message.ot_hour != '0:00:00'){
									frm.add_child('ot_approval', {
										'overtime_request': r.message.name,
										'employee': r.message.employee,
										'employee_name': r.message.employee_name,
										'workflow_state': r.message.workflow_state,
										'ot_date': r.message.ot_date,
										'department': r.message.department,
										'shift': r.message.shift,
										'from_time': r.message.from_time,
										'to_time': r.message.to_time,
										'total_hours': r.message.total_hours,
										'ot_hours': r.message.ot_hour,
										'bio_in': r.message.bio_in,
										'bio_out': r.message.bio_out,
										'total_wh': r.message.total_wh,
										'approver': r.message.approver,
										'approver_id': r.message.approver_id
									})
									frm.refresh_field('ot_approval')
								}
							}
						})

					})
				}
			})
		})
		}
		frm.fields_dict["ot_approval"].grid.add_custom_button(__('Reject'),
				function () {
					$.each(frm.doc.ot_approval, function (i, d) {
						if (d.__checked == 1) {
							frm.call('submit_ot_doc', {
								doctype: "Overtime Request",
								name: d.overtime_request,
								workflow_state: 'Rejected'
							}).then(r => {
								frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
							})
						}
					})
				}).addClass('btn-danger')
		frm.fields_dict["ot_approval"].grid.add_custom_button(__('Approve'),
		function () {
			$.each(frm.doc.ot_approval, function (i, d) {
				if (d.__checked == 1) {
					if (d.workflow_state == 'Incharge Pending') {
						frappe.msgprint(__("The Overtime Request {0} has been Move to Superior Pending", [d.overtime_request]));
						frm.call('submit_ot_doc', {
							doctype: "Overtime Request",
							name: d.overtime_request,
							workflow_state: 'Incharge Pending'
						}).then(r => {
							frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
					if (d.workflow_state == 'Superior Pending') {
						frappe.msgprint(__("The Overtime Request {0} has been Move to HOD Pending", [d.overtime_request]));
						frm.call('submit_ot_doc', {
							doctype: "Overtime Request",
							name: d.overtime_request,
							workflow_state: 'Superior Pending'
						}).then(r => {
							frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
					if (d.workflow_state == 'HOD Pending') {
						frappe.msgprint(__("The Overtime Request {0} has been Approved", [d.overtime_request]));
						frm.call('submit_ot_doc', {
							doctype: "Overtime Request",
							name: d.overtime_request,
							workflow_state: 'HOD Pending'
						}).then(r => {
							frm.get_field("ot_approval").grid.grid_rows[d.idx - 1].remove();
						})
					}
					
				}
			})
			frappe.after_ajax(() => {
						location.reload();
					});
		}).addClass('btn-primary').css({ "margin-left": "10px", "margin-right": "10px" })

		
		}
	},

	

	od_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['od_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
	pr_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['pr_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
	la_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['la_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
	ot_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['ot_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
	mp_approval_on_form_rendered: function (frm, cdt, cdn) {
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-delete-row').hide();
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-duplicate-row').hide();
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-move-row').hide();
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-append-row').hide();
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-insert-row-below').hide();
		frm.fields_dict['mp_approval'].grid.wrapper.find('.grid-insert-row').hide();
	},
})