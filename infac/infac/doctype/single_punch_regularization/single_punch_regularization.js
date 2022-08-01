// Copyright (c) 2022, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Single Punch Regularization', {
	onload:function(frm){
		if(frm.doc.__islocal){
			var previous_month = frappe.datetime.add_months(frappe.datetime.month_start(),-1)
			var from_date = frappe.datetime.add_days(previous_month,20)
			frm.set_value('from_date',from_date)
			frm.set_value('to_date',frappe.datetime.add_days(frappe.datetime.month_start(),19))

		}
	},   
	get_employees:function(frm) {
			frm.call('get_employees').then((r) =>  {
				// console.log(r.message)
				frm.clear_table('single_punch_table')
				var c = 0
				$.each(r.message,function(i,v){
					var time = [v.in_time,v.out_time]
					if (time.includes(null)){
						if(!frm.doc.permission_request){
							if (v.in_time || v.out_time){
								c= c+1
								frm.add_child('single_punch_table',{
									'employee':v.employee,
									'attendance_date':v.attendance_date,
									'in_time':v.in_time,
									'out_time':v.out_time,
									'attendance_marked':v.name	
								})
							}	
						}
					}
				})
				frm.refresh_field('single_punch_table')
				frm.set_value('number_of_employees',c)
			})	
	},
	mark_present:function(frm){
		var items = frm.get_field('single_punch_table').grid.get_selected_children();
		$.each(items,function(i,v){
			frm.call({
				'method':'infac.infac.doctype.single_punch_regularization.single_punch_regularization.single_punch_mark ',
				args:{
					att:v.attendance_marked,
					out_time:v.out_time,
					name:frm.doc.name,
				}
			})
			frm.refresh_field('single_punch_mark')

		})
	},
});

