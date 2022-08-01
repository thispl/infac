// Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance Register"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
		},
		
	],
	// "formatter": function(value, row, column, data, default_formatter) {
	// 	value = default_formatter(value, row, column, data);
	// 	console.log(column)
	// 	if (data) {
	// 		$.each(row,function(i,d){
	// 			if(['content'] == 'A'){
	// 				value = "<span style='color:red'>" + value + "</span>";
	// 			}
	// 			if(d['content'] == 'P'){
	// 				value = "<span style='color:green'>" + value + "</span>";
	// 			}
				
	// 		})
			

	// 	}
	// 	return value;
	// },
	onload: function (report) {
		var to_date = frappe.query_report.get_filter('to_date');
		to_date.refresh();
		to_date.set_input(frappe.datetime.add_days(frappe.datetime.month_start(), 19))
		var from_date = frappe.query_report.get_filter('from_date');
		from_date.refresh();
		var d = frappe.datetime.add_months(frappe.datetime.month_start(), -1)
		from_date.set_input(frappe.datetime.add_days(d, 20))
	// },
	// formatter:function (row, cell, value, columnDef, default_formatter) {
    //     value = default_formatter(row,value,column,data)
	// 	if(frm.doc){
	// 		console.log('HI')
	// 		// value = "<span style = 'color:red' "

	// 	}
	
	}
	
};

	
