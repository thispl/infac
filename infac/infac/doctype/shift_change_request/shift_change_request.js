// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Change Request', {
	
	attendance_date(frm){
		frappe.call({
			'method':'frappe.client.get_value',
			'args':{
				'doctype':'Attendance',
				'filters':{
					'employee':frm.doc.employee,
					'attendance_date':frm.doc.attendance_date
				},
				'fieldname':['shift','shift_type','actual_shift','name']
			},
			callback(r){
				if (r.message.shift_type){
					frm.set_value('assigned_shift',r.message.shift_type)
					frm.set_value('attended_shift',r.message.actual_shift)
					frm.set_value('attendance_marked',r.message.name)
				}
				else{
					frm.set_value('assigned_shift',r.message.shift)
					frm.set_value('attended_shift',r.message.actual_shift)
					frm.set_value('attendance_marked',r.message.name)
				}		
			}	
		}),
		frappe.call({
			'method':'frappe.client.get_value',
			'args':{
				'doctype':'Shift Assignment',
				'filters':{
					'employee':frm.doc.employee,
					'start_date':frm.doc.attendance_date
				},
				'fieldname':['name','shift_type']
			},
			callback(r){
				if (r.message.name){
					frm.set_value('shift_marked',r.message.name)
				}
				else{
					frm.set_value('shift_marked','')
				}

			}

		})
	},
	validate:function(frm){
		frappe.call({
			'method':'infac.infac.doctype.shift_change_request.shift_change_request.shift_change',
			'args':{
				emp:frm.doc.employee,
				start_date:frm.doc.attendance_date,
				end_date:frm.doc.attendance_date,
				name:frm.doc.shift_marked,
				shift:frm.doc.corrected_shift,
			},
			callback(r){
				if (r.message == "shift_changed"){
				}
			}
		})
		frappe.call({
			'method':'infac.infac.doctype.shift_change_request.shift_change_request.remove_checkins',
			'args':{
				emp:frm.doc.employee,
				att_date:frm.doc.attendance_date,
				shift:frm.doc.corrected_shift,
			},
			callback(r){
				console.log(r.message)
				// if (r.message == "shift_corrected"){
				// }
			}
		})
	},
	on_submit:function(frm){
		frappe.call({
			method:'infac.shift_attendance.mark_attendance',
			args:{
				emp:frm.doc.employee,
				att_date:frm.doc.attendance_date,
			},
			freeze: true,
			freeze_message: 'Processing Attendance....',
			callback(r){
				if(r.message == "Attendnace_marked"){
					console.log(r.message)
					frappe.msgprint("Attendance Marked Successfully")
				}
			}
		})
	}	
	
		
	

	// attendance_date:function(frm){
	// 	if (frm.doc.__islocal){
	// 		frappe.call({
	// 			'method':'frappe.client.get_value',
	// 			'args':{
	// 				'doctype':'Shift Assignment',
	// 				'filters':{
	// 					'employee':frm.doc.employee,
	// 					'start_date':frm.doc.attendance_date,
	// 				},
	// 				'fieldname':['shift_type','name']
	// 			},
	// 			callback(r){
	// 				if(r.message){
	// 					frm.set_value('actual_shift',r.message.shift_type)
	// 					frm.set_value('shift_marked',r.message.name)
	// 				}
	// 			}
	// 		})

	// 	}
	// },
});
