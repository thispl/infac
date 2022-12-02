// Copyright (c) 2021, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Permission Request', {
	validate(frm){
		frappe.call({
			'method':'infac.infac.doctype.permission_request.permission_request.get_time_difference',
			'args':{
				from_time:frm.doc.from_time,
				to_time : frm.doc.to_time,
				permission_date : frm.doc.permission_date,
				hours:frm.doc.hours
			},
			callback(r){
				frm.set_value('hours',r.message[0])
			}
		})
		if (frm.doc.employee_id){
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
	},
	permission_hour(frm){
		if (frm.doc.from_time){
			frappe.call({
				'method':'infac.infac.doctype.permission_request.permission_request.validate_time',
				'args':{	
					hour:frm.doc.permission_hour,
					from_time:frm.doc.from_time,
				},
				callback(r){
					$.each(r.message,function(i,v){
						frm.set_value('to_time',v.get_time)
					})
				}
			})
		}
	},
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
		// if (frm.doc.permission_hour){
		// 	frappe.call({
		// 		'method':'infac.infac.doctype.permission_request.permission_request.validate_time',
		// 		'args':{
		// 			hour:frm.doc.permission_hour,
		// 			from_time:frm.doc.from_time,
		// 		},
		// 		callback(r){
		// 			frm.set_value('to_time',r.message)
		// 		}
		// 	})

		// }
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
	}
	// on_cancel(frm){
	// 	frappe.call({
	// 		'method':'infac.infac.doctype.permission_request.permission_request.remove_per_id',
	// 		'args':{
	// 			employee_id:frm.doc.employee_id,
	// 			permission_date : frm.doc.permission_date,
	// 		},
	// 		callback(r){
	// 			console.log(r.message)
	// 		}

	// 	})
	// }
	// from_time:function(frm) {
	// 	if(frm.doc.from_time){
	// 		frappe.call({
	// 			'method':'infac.infac.doctype.permission_request.permission_request.to_time',
	// 			'args':{
	// 				from_time:frm.doc.from_time
	// 			},
	// 			callback(r){
	// 				console.log(r.message)
	// 				frm.set_value('to_time',r.message)
	// 			}
	// 		})
	// }
});