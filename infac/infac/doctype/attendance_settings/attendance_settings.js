// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance Settings', {
	refresh:function(frm){
		frm.add_custom_button(__('Refresh'), function (){
			if(frm.doc.deleted_attendance == 1){
				frm.set_value('employee','')
				frm.set_value('attendance_date','')
			}
			else{
				frm.reload_doc()
			}
		}).css('background-color', '#0EE30E');
		frm.trigger('shift_incentive_amount')
		document.querySelectorAll("[data-fieldname='update_ot_incentive_process']")[1].style.backgroundColor = "#0BEBB5"
		document.querySelectorAll("[data-fieldname='update_ot_incentive']")[1].style.backgroundColor = "#CAB0D3"
		document.querySelectorAll("[data-fieldname='submit_attendance']")[1].style.backgroundColor = "#F13944"
		document.querySelectorAll("[data-fieldname='update_holiday_attendance']")[1].style.backgroundColor = "#87DFA2"
		document.querySelectorAll("[data-fieldname='delete_attendance']")[1].style.backgroundColor = "#F4D03F "
		
	},
	ot_incentive_settings(frm){
		if (frm.doc.ot_incentive_settings == 1){
			cur_frm.set_df_property("payroll_start_date", "reqd", (frm.doc.ot_incentive_settings == 1))
			cur_frm.set_df_property("payroll_end_date", "reqd", (frm.doc.ot_incentive_settings == 1))
			cur_frm.set_df_property("employee_id", "reqd", (frm.doc.ot_incentive_settings == 1))
			cur_frm.set_df_property("shift_incetive_amount_settings", "hidden", 1)
			cur_frm.set_df_property("attendance_submit_settings", "hidden", 1)
			cur_frm.set_df_property("holiday_attendance_settings", "hidden", 1)
			cur_frm.set_df_property("deleted_attendance", "hidden", 1)
		}
		else{
			cur_frm.set_df_property("shift_incetive_amount_settings", "hidden", 0)
			cur_frm.set_df_property("attendance_submit_settings", "hidden", 0)
			cur_frm.set_df_property("holiday_attendance_settings", "hidden", 0)
			cur_frm.set_df_property("deleted_attendance", "hidden", 0)
		}
	},
	shift_incetive_amount_settings(frm){
		if(frm.doc.shift_incetive_amount_settings == 1){
			cur_frm.set_df_property("ot_incentive_settings", "hidden", 1)
			cur_frm.set_df_property("attendance_submit_settings", "hidden", 1)
			cur_frm.set_df_property("holiday_attendance_settings", "hidden", 1)
			cur_frm.set_df_property("deleted_attendance", "hidden", 1)
		}
		else{
			cur_frm.set_df_property("ot_incentive_settings", "hidden", 0)
			cur_frm.set_df_property("attendance_submit_settings", "hidden", 0)
			cur_frm.set_df_property("holiday_attendance_settings", "hidden", 0)
			cur_frm.set_df_property("deleted_attendance", "hidden", 0)
		}
	},
	shift_incentive_amount(frm){
		cur_frm.set_df_property("e_slap_ot_incentive_amount", "read_only", 1)
	    cur_frm.set_df_property("t_slap_ot_incentive_amount", "read_only", 1)
	    cur_frm.set_df_property("m_slap_ot_incentive_amount", "read_only", 1)
	    cur_frm.set_df_property("e_slap_ot_start", "read_only", 1)
	    cur_frm.set_df_property("t_slap_ot_start", "read_only", 1)
	    cur_frm.set_df_property("m_slap_ot_start", "read_only", 1)
	    cur_frm.set_df_property("e_slap_ot_end", "read_only", 1)
	    cur_frm.set_df_property("t_slap_ot_end", "read_only", 1)
	    cur_frm.set_df_property("m_slap_ot_end", "read_only", 1)
	},
	update_ot_incentive(frm){
		cur_frm.set_df_property("e_slap_ot_incentive_amount", "read_only", 0)
	    cur_frm.set_df_property("t_slap_ot_incentive_amount", "read_only", 0)
	    cur_frm.set_df_property("m_slap_ot_incentive_amount", "read_only", 0)
	    cur_frm.set_df_property("e_slap_ot_start", "read_only", 0)
	    cur_frm.set_df_property("t_slap_ot_start", "read_only", 0)
	    cur_frm.set_df_property("m_slap_ot_start", "read_only", 0)
	    cur_frm.set_df_property("e_slap_ot_end", "read_only", 0)
	    cur_frm.set_df_property("t_slap_ot_end", "read_only", 0)
	    cur_frm.set_df_property("m_slap_ot_end", "read_only", 0)
	},
	attendance_submit_settings(frm){
		if(frm.doc.attendance_submit_settings == 1){
			cur_frm.set_df_property("employee_category", "reqd", (frm.doc.attendance_submit_settings == 1))
			cur_frm.set_df_property("att_from_date", "reqd", (frm.doc.attendance_submit_settings == 1))
			cur_frm.set_df_property("att_to_date", "reqd", (frm.doc.attendance_submit_settings == 1))
			cur_frm.set_df_property("ot_incentive_settings", "hidden", 1)
			cur_frm.set_df_property("shift_incetive_amount_settings", "hidden", 1)
			cur_frm.set_df_property("holiday_attendance_settings", "hidden", 1)
			cur_frm.set_df_property("deleted_attendance", "hidden", 1)
		}
		else{
			cur_frm.set_df_property("ot_incentive_settings", "hidden", 0)
			cur_frm.set_df_property("shift_incetive_amount_settings", "hidden", 0)
			cur_frm.set_df_property("holiday_attendance_settings", "hidden", 0)
			cur_frm.set_df_property("deleted_attendance", "hidden", 0)
		}
	},
	holiday_attendance_settings(frm){
		if(frm.doc.holiday_attendance_settings == 1){
			frm.disable_save()
			cur_frm.set_df_property("start_date", "reqd", (frm.doc.holiday_attendance_settings == 1))
			cur_frm.set_df_property("end_date", "reqd", (frm.doc.holiday_attendance_settings == 1))
			cur_frm.set_df_property("ot_incentive_settings", "hidden", 1)
			cur_frm.set_df_property("shift_incetive_amount_settings", "hidden", 1)
			cur_frm.set_df_property("attendance_submit_settings", "hidden", 1)
			cur_frm.set_df_property("deleted_attendance", "hidden", 1)
		}
		else{
			cur_frm.set_df_property("ot_incentive_settings", "hidden", 0)
			cur_frm.set_df_property("shift_incetive_amount_settings", "hidden", 0)
			cur_frm.set_df_property("attendance_submit_settings", "hidden", 0)
			cur_frm.set_df_property("deleted_attendance", "hidden", 0)
		}
	},
	deleted_attendance(frm){
		if(frm.doc.deleted_attendance ==1){
			cur_frm.set_df_property("employee", "reqd", (frm.doc.deleted_attendance == 1))
			cur_frm.set_df_property("attendance_date", "reqd", (frm.doc.deleted_attendance == 1))
			cur_frm.set_df_property("shift_incetive_amount_settings", "hidden", 1)
			cur_frm.set_df_property("attendance_submit_settings", "hidden", 1)
			cur_frm.set_df_property("ot_incentive_settings", "hidden", 1)
			cur_frm.set_df_property("holiday_attendance_settings", "hidden", 1)
		}
		else{
			cur_frm.set_df_property("shift_incetive_amount_settings", "hidden", 0)
			cur_frm.set_df_property("attendance_submit_settings", "hidden", 0)
			cur_frm.set_df_property("ot_incentive_settings", "hidden", 0)
			cur_frm.set_df_property("holiday_attendance_settings", "hidden", 0)
		}
	},
	mark_ot(frm){
		if(frm.doc.mark_ot ==  1){
			cur_frm.set_df_property("mark_ot_incentive", "hidden", 1)
		}
		else{
			cur_frm.set_df_property("mark_ot_incentive", "hidden", 0)
		}
	},
	mark_ot_incentive(frm){
		if(frm.doc.mark_ot_incentive == 1){
			cur_frm.set_df_property("mark_ot", "hidden", 1)
		}
		else{
			cur_frm.set_df_property("mark_ot", "hidden", 0)
		}
	},
	update_ot_incentive_process(frm){
		if(frm.doc.mark_ot == 1){
			frappe.call({
				method:'infac.shift_attendance.mark_att',
				args:{
					from_date:frm.doc.payroll_start_date,
					to_date:frm.doc.payroll_end_date,
					// emp:frm.doc.employee_id
				},
				freeze: true,
				freeze_message: 'Overtime Updated',
				callback(r){
				}
			})
		}
	},
	// holiday_attendance_run(frm){
	// 	if (frm.doc.holiday_attendance_run ==1){
	// 		cur_frm.set_df_property("attendance_submit", "hidden", 1)
	// 		cur_frm.set_df_property("submit_attendance", "hidden", 1)
	// 		cur_frm.set_df_property("employee_category", "reqd", (frm.doc.holiday_attendance_run == 1))
	// 		cur_frm.set_df_property("att_from_date", "reqd", (frm.doc.holiday_attendance_run == 1))
	// 		cur_frm.set_df_property("att_to_date", "reqd", (frm.doc.holiday_attendance_run == 1))
	// 	}
	// 	else{
	// 		cur_frm.set_df_property("attendance_submit", "hidden", 0)
	// 		cur_frm.set_df_property("submit_attendance", "hidden", 0)
	// 	}
	// },
	// ot_process(frm){
	// 	if (frm.doc.ot_process ==1){
	// 		cur_frm.set_df_property("attendance_run", "hidden", 1)
	// 		cur_frm.set_df_property("attendance_process", "hidden", 1)
	// 	}
	// 	else{
	// 		cur_frm.set_df_property("attendance_run", "hidden", 0)
	// 		cur_frm.set_df_property("attendance_process", "hidden", 0)
	// 	}
	// },
	// attendance_run(frm){
	// 	if(frm.doc.attendance_run ==1){
	// 		cur_frm.set_df_property("ot_process", "hidden", 1)
	// 		cur_frm.set_df_property("update_ot_incentive_process", "hidden", 1)
	// 	}
	// 	else{
	// 		cur_frm.set_df_property("ot_process", "hidden", 0)
	// 		cur_frm.set_df_property("update_ot_incentive_process", "hidden", 0)
	// 	}
	// },
	//submit attendace button to action the payroll month submit all the in a single slot
	submit_attendance(frm){
		if (frm.doc.attendance_submit_settings ==1){
			frappe.call({
				method:'infac.utils.enqueue_mark_att',
				args:{
					emp_cate:frm.doc.employee_category,
					from_date:frm.doc.att_from_date,
					to_date:frm.doc.att_to_date
				},
				freeze: true,
				freeze_message: 'Submitting Attendance',
				callback(r){
					if (r.message == 'Completed'){
						frappe.msgprint(__('ATTENDANCE SUBMITTED SUCCESSFULLY'))
					}
				}
			})
		}
	},
	delete_attendance(frm){
		frm.save()
	},
	update_holiday_attendance(frm){
		if(frm.doc.start_date && frm.doc.end_date){
			frappe.call({
				method:'infac.shift_attendance.mark_holiday_attendance',
				args:{
					from_date:frm.doc.start_date,
					to_date:frm.doc.end_date,
				},
				freeze: true,
				freeze_message: 'Submitting Attendance',
				callback(r){
					if (r.message == "Holiday Attendance"){
						frappe.msgprint(__('Holiday Attendance Moved'))
					}

				}
			})
		}
	},
	attendance_process(frm){
		frappe.call({
			method:'infac.mark_attendance.mark_att',
			args:{
				emp:frm.doc.employee_attendance,
				from_date:frm.doc.payroll_start_date,
				to_date:frm.doc.payroll_end_date
			},
			freeze: true,
			freeze_message: 'Attendance Process',
			callback(r){
				if (r.message == 'Completed'){
					frappe.msgprint(__('ATTENDANCE MARKED SUCCESSFULLY'))
				}
			}	
		})
	}
	
});
