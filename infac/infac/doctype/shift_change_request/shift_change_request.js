// // Copyright (c) 2022, teampro and contributors
// // For license information, please see license.txt

// frappe.ui.form.on('Shift Change Request', {

// 	to_date(frm){
// 		frappe.call({
// 			'method':'infac.infac.doctype.shift_change_request.shift_change_request.get_shift_assignment',
// 			'args':{
// 				emp:frm.doc.employee,
// 				from_date:frm.doc.from_date,
// 				to_date:frm.doc.to_date,
// 				name:frm.doc.name
// 			},
// 			callback(r){
// 				frm.set_value('assigned_shift',r.message[0])
// 			}
// 		})
// 	}
	
	
	
// });


frappe.ui.form.on('Shift Change Request', {
    onload: function(frm) {
        restrict_past_dates(frm);
    },
    refresh: function(frm) {
        restrict_past_dates(frm);

        highlight_field(frm, 'level_1_approved_by');
        highlight_field(frm, 'level_1_timing');

        highlight_field(frm, 'created_by');
        highlight_field(frm, 'created_on');
    },
    validate: function(frm) {
        validate_past_date(frm);
    },

	to_date(frm){
		frappe.call({
			'method':'infac.infac.doctype.shift_change_request.shift_change_request.get_shift_assignment',
			'args':{
				emp:frm.doc.employee,
				from_date:frm.doc.from_date,
				to_date:frm.doc.to_date,
				name:frm.doc.name
			},
			callback(r){
				frm.set_value('assigned_shift',r.message[0])
			}
		})
	}
});

function restrict_past_dates(frm) {
    frm.set_query('from_date', function() {
        return {};
    });

    frm.set_query('to_date', function() {
        return {};
    });

    if (frm.fields_dict['from_date'] && frm.fields_dict['from_date'].datepicker) {
        frm.fields_dict['from_date'].datepicker.update({
            minDate: frappe.datetime.str_to_obj(frappe.datetime.now_date())
        });
    }

    if (frm.fields_dict['to_date'] && frm.fields_dict['to_date'].datepicker) {
        let min_date = frm.doc.from_date || frappe.datetime.now_date();
        frm.fields_dict['to_date'].datepicker.update({
            minDate: frappe.datetime.str_to_obj(min_date)
        });
    }
}

function validate_past_date(frm) {
    let today = frappe.datetime.get_today();

    if (frm.doc.from_date && frm.doc.from_date < today) {
        frappe.throw(__('From Date cannot be a past date.'));
    }

    if (frm.doc.to_date && frm.doc.to_date < today) {
        frappe.throw(__('To Date cannot be a past date.'));
    }
}



function highlight_field(frm, fieldname) {
    if (frm.doc[fieldname]) {

        const wrapper = frm.fields_dict[fieldname].$wrapper;

        // label color
        wrapper.find('.control-label').css({
            "color": "grey",
            "font-weight": "bold"
        });

        // field background
        wrapper.find('input, textarea, .control-value').css({
            "background-color": "#fadede"
            
        });
    }
}