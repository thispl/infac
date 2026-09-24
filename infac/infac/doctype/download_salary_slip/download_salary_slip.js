// Copyright (c) 2025, teampro and contributors
// For license information, please see license.txt


frappe.ui.form.on("Download Salary Slip", {
    // refresh(frm) {
    //     const user = frappe.session.user;
    //     if ( frappe.session.user == 'Administrator') {
    //         frm.set_value("employee_id", user);
    //     }
    //     const currentYear = new Date().getFullYear();
    //     frm.set_value("year", currentYear);

    //     if ( frappe.session.user != 'Administrator') {
    //         frappe.db.get_value(
    //             "Employee",
    //             { user_id: frappe.session.user },
    //             ["employee", "employee_name", "employment_type"],
    //             (r) => {
    //                 if (r) {
    //                     frm.set_value("employee_id", r.employee);
    //                     frm.set_value("employee_name", r.employee_name);
    //                     frm.set_value("employment_type", r.employment_type);
    //                 }
    //             }
    //         );
    //         if (!frappe.user.has_role('HR')) {
    //             frm.set_df_property("employee_id", "read_only", 1);
    //         }
    //     } else {
    //         frm.set_df_property("employee_id", "read_only", 0);
    //     }
    //     frm.disable_save();
    // },
     refresh(frm) {
        const user = frappe.session.user;
        const currentYear = new Date().getFullYear();
        frm.set_value("year", currentYear);

        if (frappe.user.has_role('Administrator') || frappe.user.has_role('HR Manager') || frappe.user.has_role('HR User')) {
            frm.set_df_property("employee_id", "read_only", 0);
        } 
        else {
            frappe.db.get_value(
                "Employee",
                { user_id: user },
                ["employee", "employee_name",  "employment_type"],
                (r) => {
                    if (r) {
                        frm.set_value("employee_id", r.employee);
                        frm.set_value("employee_name", r.employee_name);
                        frm.set_value("employment_type", r.employment_type);
                    }
                }
            );
            frm.set_df_property("employee_id", "read_only", 1);
        }

        frm.disable_save();
    },
    month(frm) {
        frm.trigger("get_slip");
    },
    year(frm) {
        frm.trigger("get_slip");
    },
    employee_id(frm) {
        frm.trigger("get_slip");
    },
   async get_slip(frm) {
    if (frm.doc.employee_id && frm.doc.month && frm.doc.year) {
        try {
            const response = await frm.call("get_salary_slip");

            if (response.message) {
                frm.set_value("salary_slip", response.message[0].name);
            } else {
                frm.set_value("salary_slip", "");
            }

        } catch (error) {
            // Python frappe.throw() message-ah appadiye kaatu.
            frm.set_value("salary_slip", "");
            return;
        }
    }
},
    // async download(frm) {
    //     if (frm.doc.employee_id && frm.doc.month && frm.doc.year) {
    //         await frm.trigger("get_slip");

    //         if (frm.doc.salary_slip) {
    //             {
    //                 const f_name = frm.doc.salary_slip;
    //                 const print_format = "INFAC Salary Slip";
    //                 window.open(
    //                     frappe.urllib.get_full_url(
    //                         "/api/method/frappe.utils.print_format.download_pdf?" +
    //                             "doctype=" +
    //                             encodeURIComponent("Salary Slip") +
    //                             "&name=" +
    //                             encodeURIComponent(f_name) +
    //                             "&trigger_print=1" +
    //                             "&format=" +
    //                             print_format +
    //                             "&no_letterhead=0" +
    //                             "&letterhead=" +
    //                             encodeURIComponent
    //                     )
    //                 );
    //             }
    //         } else {
    //             frappe.throw("Salary Slip Not Found");
    //         }
    //     } else if (!frm.doc.employee_id) {
    //         frappe.throw("Please choose Employee ID");
    //     } else if (!frm.doc.month) {
    //         frappe.throw("Please choose Month");
    //     } else if (!frm.doc.year) {
    //         frappe.throw("Please choose Year");
    //     }
    // },
    async download(frm) {
    if (frm.doc.employee_id && frm.doc.month && frm.doc.year) {
        await frm.trigger("get_slip");

        if (frm.doc.salary_slip) {

            // -------- SELECT PRINT FORMAT BASED ON STAFF / WORKER -------- //
            let print_format = "";
            
            if (frm.doc.employment_type == "STAFF") {
                print_format = "Salary Slip Staff";      // staff print format
            } 
            else if (frm.doc.employment_type == "WORKER") {
                print_format = "INFAC Salary Slip";     // worker print format
            } 
            else {
                frappe.throw("Invalid Employee Type. Select Staff or Worker.");
            }

            const f_name = frm.doc.salary_slip;

            window.open(
                frappe.urllib.get_full_url(
                    "/api/method/frappe.utils.print_format.download_pdf?" +
                        "doctype=" +
                        encodeURIComponent("Salary Slip") +
                        "&name=" +
                        encodeURIComponent(f_name) +
                        "&trigger_print=1" +
                        "&format=" +
                        encodeURIComponent(print_format) +
                        "&no_letterhead=0"
                )
            );

        } else {
    return;
}

    } else if (!frm.doc.employee_id) {
        frappe.throw("Please choose Employee ID");

    } else if (!frm.doc.month) {
        frappe.throw("Please choose Month");

    } else if (!frm.doc.year) {
        frappe.throw("Please choose Year");
    }
}

});

