// Copyright (c) 2021, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Report Dashboard', {
	// refresh: function(frm) {

	// }
	download:function(frm){
		//Attendance log
		if(frm.doc.report == 'Attendance Log'){
			var path = 'infac.infac.doctype.report_dashboard.attendance_log.download'
			var args = 'date=%(date)s&from_date=%(from_date)s&to_date=%(to_date)s'

		}
		else if(frm.doc.report == 'Form 12'){
			var path = 'infac.infac.doctype.report_dashboard.form_12.download'
			var args = 'date=%(date)s&from_date=%(from_date)s&to_date=%(to_date)s'

		}
		else if(frm.doc.report == 'Form 25'){
			var path = 'infac.infac.doctype.report_dashboard.form_25_report.download'
			var args = 'date=%(date)s&from_date=%(from_date)s&to_date=%(to_date)s'

		}
		else if(frm.doc.report == 'Permission Report'){
			if (!frm.doc.from_date || !frm.doc.to_date) {
				frappe.msgprint("Please select From Date and To Date");
				return;
			}

			if (frm.doc.from_date > frm.doc.to_date) {
				frappe.msgprint("From Date should not be greater than To Date");
					return;
				}

			window.open(
				"/api/method/infac.infac.doctype.report_dashboard.permission_report.download"
				+ "?from_date=" + frm.doc.from_date
				+ "&to_date=" + frm.doc.to_date
			);
		}
		else if(frm.doc.report == 'Shift Deviation Report'){
			if (!frm.doc.from_date || !frm.doc.to_date) {
				frappe.msgprint("Please select From Date and To Date");
				return;
			}

			if (frm.doc.from_date > frm.doc.to_date) {
				frappe.msgprint("From Date should not be greater than To Date");
					return;
				}

			window.open(
				"/api/method/infac.infac.doctype.report_dashboard.shift_deviation_report.download"
				+ "?from_date=" + frm.doc.from_date
				+ "&to_date=" + frm.doc.to_date
			);
		}
		else if (frm.doc.report == 'Attendance Comparison Sheet') {

			if (!frm.doc.date) {
				frappe.msgprint("Please select Date");
				return;
			}

			window.open(
				"/api/method/infac.infac.doctype.report_dashboard.attendance_comp_report.download"
				+ "?doc_date=" + encodeURIComponent(frm.doc.date)
			);
		}
		else if(frm.doc.report == "Migrant Employee Attendance") {
			console.log(frm.doc.report)
			var path = "infac.infac.doctype.report_dashboard.migrant_emp_attendance.download";
			var args = "from_date=%(from_date)s&to_date=%(to_date)s";
		}
	
		else if(frm.doc.report == "New Joinee Attendance") {
			console.log(frm.doc.report)
			var path = "infac.infac.doctype.report_dashboard.new_joinee_attendance.download";
			var args = "from_date=%(from_date)s&to_date=%(to_date)s";
		}

		else if(frm.doc.report == "Shift Continue Report") {
			console.log(frm.doc.report)
			var path = "infac.infac.doctype.report_dashboard.shift_continue_report.download_shift_continue_report";
			var args = "date=%(date)s";
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
					date:frm.doc.date,
					from_date:frm.doc.from_date,
					to_date:frm.doc.to_date
				}
				)

			}
			
		}
	});
