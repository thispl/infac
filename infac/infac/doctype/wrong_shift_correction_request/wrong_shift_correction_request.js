// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wrong Shift Correction Request', {

	attendance_date(frm){
		frappe.call({
			'method':'frappe.client.get_value',
			'args':{
				'doctype':'Attendance',
				'filters':{
					'employee':frm.doc.employee,
					'attendance_date':frm.doc.attendance_date
				},
				'fieldname':['shift','shift_type','shift_in_time','shift_out_time','actual_shift','actual_in_time','out_time','name']
			},
			callback(r){
				if (r.message.shift_type){
					frm.set_value('assigned_shift',r.message.shift_type)
					frm.set_value('shift_in_time',r.message.shift_in_time)
					frm.set_value('shift_out_time',r.message.shift_out_time)
					frm.set_value('attendance_marked',r.message.name)
					frm.set_value('attended_shift',r.message.actual_shift)
					frm.set_value('actual_in_time',r.message.actual_in_time)
					frm.set_value('actual_out_time',r.message.out_time)
				}
				else{
					frm.set_value('assigned_shift',r.message.shift)
					frm.set_value('attended_shift',r.message.actual_shift)
					frm.set_value('actual_in_time',r.message.actual_in_time)
					frm.set_value('actual_out_time',r.message.out_time)
					frm.set_value('attendance_marked',r.message.name)

				}
			}
			
		})
		frm.refresh()
	},
	corrected_shift(frm){
		frappe.call({
			'method':'infac.infac.doctype.wrong_shift_correction_request.wrong_shift_correction_request.mark_attendance',
			'args':{
				attendance_date:frm.doc.attendance_date,
				emp:frm.doc.employee,
				shift:frm.doc.corrected_shift,
				out_time:frm.doc.actual_out_time,
			},
			freeze: true,
			freeze_message: __("Creating Shift..."),
			callback(r){
				console.log(r.message)
				if (r.message[1] == 'A'){
					frm.set_value('corrected_shift','A')
				}
				else if(r.message[1] == 'B'){
					frm.set_value('corrected_shift','B')
				}
				else if(r.message[1] == 'G'){
					frm.set_value('corrected_shift','G')
				}
				else{
					frm.set_value('actual_out_time',r.message[0])
					frm.set_value('night_shift_attendance',r.message[2])
				}
				// 	if(r.message){
				// 		frm.set_value('actual_out_time',r.message)
				// 	}
				// 	else{
				// 		console.log('yes')
				// 	}
				// }
			}	
		})
	}
});
