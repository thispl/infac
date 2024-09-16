frappe.pages['monthly-attendance-s'].on_page_load = function(wrapper) {
	let me = this;
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Attendance Summary',
		single_column: true,
		card_layout : true	
	});

	let emp_details = {}
	frappe.call({
		'method':'infac.monthly_attendance_summary.get_attendance',
		args:{
			user:frappe.session.user
		},
		callback:function(r){
			attendance = r.message
			page.main.html(frappe.render_template('monthly_attendance_summary',{data:attendance}))
		}
	})

}