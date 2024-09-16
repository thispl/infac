import frappe

@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
    if not frappe.db.exists('Employee Checkin',{'employee':args['employee'],'time':args['time']}):
        if frappe.db.exists('Employee',{'name':args['employee']}):
            try:
                ec = frappe.new_doc('Employee Checkin')
                ec.employee = args['employee'].upper()
                ec.time = args['time']
                ec.device_id = args['device_id']
                ec.save(ignore_permissions=True)
                frappe.db.commit()
                return "Checkin Marked"
            except:
                print("HI")
                # frappe.log_error(title="checkin error",message=args)
        else:
            print("HI")
            # frappe.log_error(title="checkin error",message=args)
    else:
        return "Checkin Marked"
