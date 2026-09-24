// Copyright (c) 2025, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Incentive Request', {
	employee(frm){
		if (frm.doc.employee) {
            frappe.db.get_value("Employee", frm.doc.employee, "designation", (r) => {
                if (r && r.designation) {
                    frappe.db.get_value("Designation", r.designation, ["shift_incentive_applicable", "ot_incentive_applicable"], (d) => {
                        if (d) {
                            if (!d.shift_incentive_applicable && !d.ot_incentive_applicable) {
                                frappe.msgprint("Shift Incentive and OT Incentive is not enabled in Designation");
                                frm.set_value("employee", ""); 
								frm.set_value("employee_name", "");
								frm.set_value("hod", "");
								frm.set_value("department", "");
								frm.set_value("designation", "");
								frm.set_value("factory_head", "");
								frm.set_value("hr", "");

                            }
                        }
                    });
                }
            });
        }
		if(frm.doc.ot_date && frm.doc.employee){
			frappe.call({
				method:'infac.infac.doctype.incentive_request.incentive_request.check_attendance',
				args:{
					emp:frm.doc.employee,
					date:frm.doc.ot_date
				},
				callback(r){
					if (r.message != 'NO'){
						frm.set_value('in_time', r.message[0])
						frm.set_value('out_time', r.message[1])
						frm.set_value('ot_hours', r.message[2])
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
		}
		
		
	},
	
	ot_date(frm) {
	if (frm.doc.ot_date && frm.doc.employee) {
		frappe.call({
			method: 'infac.infac.doctype.incentive_request.incentive_request.check_attendance',
			args: {
				emp: frm.doc.employee,
				date: frm.doc.ot_date,
				desig: frm.doc.designation
			},
			callback(r) {
				if (r.message != 'NO') {
					frm.set_value('in_time', r.message[0]);
					frm.set_value('out_time', r.message[1]);
					frm.set_value('ot_hours', r.message[2]);
					frm.set_value('incentive_amount', r.message[3] || 0);
					frappe.call({
						method: 'infac.infac.doctype.incentive_request.incentive_request.check_ot_incentive',
						args: {
							desig: frm.doc.designation,
							ot_hours: r.message[2], 
							employee: frm.doc.employee,
							ot_date: frm.doc.ot_date,
						},
						callback(r2) {
							if (r2.message) {
								frm.set_value('ot_incentive', r2.message);
							}else{
								frm.set_value('ot_incentive','0.00');
							}
						}
					});

					if (r.message[0] == '') {
						frappe.throw('In time not found');
					} else if (r.message[1] == '') {
						frappe.throw('Out time not found');
					} else if (r.message[2] == 0) {
						frappe.throw('OT hours is 0. Not eligible to apply');
					}
				} else {
					frappe.throw('No Attendance record found against this date');
				}
			}
		});

	} else {
		frm.set_value('in_time', '');
		frm.set_value('out_time', '');
		frm.set_value('ot_hours', '');
		frm.set_value('incentive_amount', '');
		frm.set_value('ot_incentive', '');
		
	}
	
}

});
