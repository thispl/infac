// Copyright (c) 2016, teampro and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary Register INFAC"] = {
	"filters":[
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department"
		},
		{
			"fieldname": "employee_category",
			"label": __("Employee Category"),
			"fieldtype": "Link",
			"options": "Employee Category"
		},
		
		// {
		// 	"fieldname": "to_date",
		// 	"label": __("To Date"),
		// 	"fieldtype": "Date",
			
		// }
	]
	// frappe.query_reports["WC Wage Register"] = {
// 		"filters": [
// 			{
// 				"fieldname": "from_date",
// 				"label": __("From Date"),
// 				"fieldtype": "Date",
// 				"reqd": 1,
// 				on_change: function () {
// 					var from_date = frappe.query_report.get_filter_value('from_date')
// 					frappe.call({
// 						method: "infac.infac.report.salary_register_infac.salary_register_infac.get_to_date",
// 						args: {
// 							from_date: from_date
// 						},
// 						callback(r) {
// 							frappe.query_report.set_filter_value('to_date', r.message);
// 							frappe.query_report.refresh();
// 						}
// 					})
// 				}
// 			},
// 			{
// 				"fieldname": "to_date",
// 				"label": __("To Date"),
// 				"fieldtype": "Date",
// 				"reqd": 1,
// 				"read_only": 0
// 			},
			
// 		],
// 		onload: function (report) {
// 			var to_date = frappe.query_report.get_filter('to_date');
// 			to_date.refresh();
// 			to_date.set_input(frappe.datetime.add_days(frappe.datetime.month_start(), 24))

// 			var from_date = frappe.query_report.get_filter('from_date');
// 			from_date.refresh();
// 			var d = frappe.datetime.add_months(frappe.datetime.month_start(), -1)
// 			from_date.set_input(frappe.datetime.add_days(d, 25))
// 			}
}
		

