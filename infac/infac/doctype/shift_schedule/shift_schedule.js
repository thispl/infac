// Copyright (c) 2021, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Schedule', {
    // refresh: function(frm) {

    // }
    get_template: function (frm) {
        window.location.href = repl(frappe.request.url +
            '?cmd=%(cmd)s&from_date=%(from_date)s&to_date=%(to_date)s&department=%(department)s', {
            cmd: "infac.infac.doctype.shift_schedule.shift_schedule.get_template",
            from_date: frm.doc.from_date,
            to_date: frm.doc.to_date,
            department:frm.doc.department,
            // department: (frm.doc.department).replace("&", "1")
        });
    },
    // from_date(frm) {
    //     if (frm.doc.from_date) {
    //         if (frm.doc.from_date < frappe.datetime.now_date()) {
    //             frappe.msgprint("From Date should not be a Past Date")
    //             frm.set_value('from_date', '')
    //         }
    //     }
    // },
    // to_date(frm) {
    //     if (frm.doc.to_date) {
    //         if (frm.doc.to_date < frappe.datetime.now_date()) {
    //             frappe.msgprint("To Date should not be a Past Date")
    //             frm.set_value('to_date', '')
    //         }
    //         else if (frm.doc.to_date < frm.doc.from_date) {
    //             frappe.msgprint("To Date should not be greater than From Date")
    //             frm.set_value('to_date', '')
    //         }
    //     }
    // },
    // after_save(frm){
	// 	frappe.call({
	// 		"method": "infac.infac.doctype.shift_schedule.shift_schedule.create_shift_assignment",
	// 		"args":{
	// 			"file" : frm.doc.upload,
	// 			"from_date" : frm.doc.from_date,
	// 			"to_date" : frm.doc.to_date,
	// 			"name" : frm.doc.name
	// 		},
	// 		freeze: true,
	// 		freeze_message: 'Submitting Shift Schedule....',
	// 		callback(r){
	// 			if(r.message == "ok"){
	// 				// frappe.msgprint("Attendance Marked Successfully")
	// 			}
	// 		}
	// 	})
	// },			
});
