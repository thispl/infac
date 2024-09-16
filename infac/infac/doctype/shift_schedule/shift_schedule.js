// Copyright (c) 2021, teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Schedule', {
    refresh(frm) {
        frm.fields_dict['employee_details'].grid.wrapper.find('.grid-add-row').remove(); 
        if (frm.doc.docstatus == 0) {
            frm.add_custom_button(__('Get Employees'), function (){
                frm.call('get_employees').then((r)=>{
                    frm.clear_table('employee_details')
                    var c = 0
                    $.each(r.message,function(i,v){
                        c = c+1
                        frm.add_child('employee_details',{
                            'employee':v.employee,
                            'employee_name':v.employee_name, 
                            'shift':v.shift
                        })
                    })
                    frm.refresh_field('employee_details')
                    frm.set_value('number_of_employees',c)
                })
            })    
        }
    },
    // department_line(frm){
    //     frappe.call({
    //         method:"infac.infac.doctype.shift_schedule.shift_schedule.department_line",
    //         args:{
    //             dept:frm.doc.department_line
    //         },
    //         callback(r){
    //             if (r.message == 'IQC'){
    //                 frm.disable_save()
    //             }
    //         }
    //     })
    // },
    // from_date(frm){
    //     if(frm.doc.from_date){
    //         if (frm.doc.from_date < frappe.datetime.now_date()) {
	// 			frappe.msgprint("From Date should not be a Past Date")
	// 			frm.set_value('from_date', '')
	// 		} 
    //     }
    //     var to_date = frappe.datetime.add_days(frm.doc.from_date, 5)
    //     frm.set_value('to_date',to_date)
    // },
    // to_date(frm){
    //     if (frm.doc.to_date){
    //         var to_date = frappe.datetime.add_days(frm.doc.from_date, 5)
    //         if (to_date < frm.doc.to_date){
    //             frappe.msgprint("To Date should not be greater than From Date")
    //             frm.set_value('to_date','')
    //         }

    //     }
    // }
   
    
    
});
