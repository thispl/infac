// Copyright (c) 2025, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime Request', {
	employee(frm){
		if(frm.doc.ot_date && frm.doc.employee){
			frappe.call({
				method:'infac.infac.doctype.overtime_request.overtime_request.check_attendance',
				args:{
					emp:frm.doc.employee,
					date:frm.doc.ot_date
				},
				callback(r){
					if (r.message != 'NO'){
						frm.set_value('in_time', r.message[0])
						frm.set_value('out_time', r.message[1])
						frm.set_value('ot_hours', r.message[2])
						frm.set_value('payable_ot', r.message[2])
						if (r.message[0] ==''){
							frappe.throw('In time not found')
						}else if (r.message[1] ==''){
							frappe.throw('Out time not found')
						}else if (r.message[2] ==0){
							frappe.throw('OT hours is 0.Not eligible to apply')
						}
					}else{
						frappe.throw('No Attendance record found against this date')
					}
				}
			})
		}else{
			frm.set_value('in_time','')
			frm.set_value('out_time', '')
			frm.set_value('ot_hours', '')
			frm.set_value('payable_ot', '')
		}
		
	},
	ot_date(frm){
		if(frm.doc.ot_date && frm.doc.employee){
			frappe.call({
				method:'infac.infac.doctype.overtime_request.overtime_request.check_attendance',
				args:{
					emp:frm.doc.employee,
					date:frm.doc.ot_date
				},
				callback(r){
					if (r.message != 'NO'){
						frm.set_value('in_time', r.message[0])
						frm.set_value('out_time', r.message[1])
						frm.set_value('ot_hours', r.message[2])
						frm.set_value('payable_ot', r.message[2])
						if (r.message[0] ==''){
							frappe.throw('In time not found')
						}else if (r.message[1] ==''){
							frappe.throw('Out time not found')
						}else if (r.message[2] ==0){
							frappe.throw('OT hours is 0.Not eligible to apply')
						}
					}else{
						frappe.throw('No Attendance record found against this date')
					}
				}
			})
		}else{
			frm.set_value('in_time','')
			frm.set_value('out_time', '')
			frm.set_value('ot_hours', '')
			frm.set_value('payable_ot', '')
		}
		
	}
});
