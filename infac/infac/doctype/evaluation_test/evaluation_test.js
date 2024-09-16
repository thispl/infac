// Copyright (c) 2023, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Evaluation Test', {
	
	email_address(frm) {
		if (!validate_email(frm.doc.email_addresss)) {
			frappe.throw(__("Invalid Email Address"))
		}
	},
	mobile_number(frm){
		frappe.call({
			method:'infac.infac.doctype.evaluation_test.evaluation_test.validate_phone_number',
			args:{
				number:frm.doc.mobile_number
			},
			callback(r){
			}
		})
	},
	date(frm){
		frappe.call({
			method:'infac.infac.doctype.evaluation_test.evaluation_test.not_entered_past_date',
			args:{
				past_date:frm.doc.date
			},
			callback(r){
				console.log(r.message)
			}
		})
	},
	numbers(frm){
		var num = Math.sign(frm.doc.numbers)
		if (num == -1){
			frappe.throw(__("Negative Numbers Not Allowed"));
		} 
	},
	payterms(frm){
		var date = new Date()
		var dates = frappe.datetime.add_days(date,frm.doc.payterms)
		frm.set_value('due_date',dates)
	},
	refresh(frm){
		if (frappe.session.user == 'Administrator'){
			cur_frm.set_df_property("information", "hidden", 1)
		}
	}
	  
	  
});
