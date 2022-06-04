// Copyright (c) 2021, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report Dashboard', {
	// refresh: function(frm) {

	// }
	download:function(frm){
		//Attendance log
		if(frm.doc.report == 'Attendance Log'){
			var path = 'infac.infac.doctype.report_dashboard.attendance_log.download'
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'

		}
		//Employee Grade excel report
		else if(frm.doc.report == 'Employee Grade'){
			var path = 'infac.infac.doctype.report_dashboard.employee_grade.download'
			var args = 'from_date=%(from_date)s&to_date=%(to_date)s'
		}	
		if(path){
			window.location.href = repl(frappe.request.url+
				'?cmd=%(cmd)s&%(args)s',{
					cmd:path,
					args:args,
					from_date:frm.doc.from_date,
					to_date:frm.doc.to_date

				}
				)

			}
			
		}
	});
