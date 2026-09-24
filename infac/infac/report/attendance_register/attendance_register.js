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
            "options": "Employee"
        },
        {
            "fieldname": "employment_type",
            "label": __("Employment Type"),
            "fieldtype": "Link",
            "options": "Employment Type"
        }
    ],

    onload: function(report) {
        // Default date setup
        let to_date = report.get_filter('to_date');
        to_date.set_input(frappe.datetime.add_days(frappe.datetime.month_start(), 19));
        let from_date = report.get_filter('from_date');
        from_date.set_input(frappe.datetime.add_days(frappe.datetime.add_months(frappe.datetime.month_start(), -1), 20));

        // Employee -> Employment Type logic
        report.page.fields_dict.employee.$input.on('change', function() {
            let employee = $(this).val();
            const emp_type_filter = report.page.fields_dict.employment_type;

            if(employee) {
                frappe.db.get_value('Employee', employee, 'employment_type')
                    .then(r => {
                        if(r.message) {
                            report.set_filter_value('employment_type', r.message.employment_type);
                            // Make Employment Type read-only
                            emp_type_filter.df.read_only = 1;
                            emp_type_filter.refresh();
                        }
                    });
            } else {
                // Clear Employment Type and make editable
                report.set_filter_value('employment_type', '');
                emp_type_filter.df.read_only = 0;
                emp_type_filter.refresh();
            }
        });
    }
};
