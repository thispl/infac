import frappe
@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
    if frappe.db.exists('Employee',{'name':args['employee'],'status':'Active'}):
        employee = args['employee']
        if employee:
            try:
                if args['device_id'] in ['Staff IN','Workers IN','Tr. CL Gents - IN','Tr. CL Ladies - IN']:
                    if not frappe.db.exists('Employee Checkin',{'employee':employee,'time':args['time']}):
                        ec = frappe.new_doc('Employee Checkin')
                        ec.employee = employee
                        ec.time = args['time']
                        ec.device_id = args['device_id']
                        ec.log_type = 'IN'
                        ec.save(ignore_permissions=True)
                        frappe.db.commit()
                        return "Checkin Marked"
                    else:
                        return "Checkin Marked"
                elif args['device_id'] in ['Staff OUT','Workers OUT','Tr. CL Gents - OUT','Tr. CL Ladies - OUT']:
                    if not frappe.db.exists('Employee Checkin',{'employee':employee,'time':args['time']}):
                        ec = frappe.new_doc('Employee Checkin')
                        ec.employee = employee
                        ec.time = args['time']
                        ec.device_id = args['device_id']
                        ec.log_type = 'OUT'
                        ec.save(ignore_permissions=True)
                        frappe.db.commit()
                        return "Checkin Marked" 
                    else:
                        return "Checkin Marked" 
                else:
                    return "Checkin Unmarked"
        
            except:
                frappe.log_error(title="checkin error1",message=args)
    else:
        try:
            if args['device_id'] in ['Staff IN','Workers IN','Tr. CL Gents - IN','Tr. CL Ladies - IN']:
                if not frappe.db.exists('Unregistered Employee Checkin',{'biometric_pin':args['employee'],'biometric_time':args['time']}):
                    ec = frappe.new_doc('Unregistered Employee Checkin')
                    ec.biometric_pin = args['employee']
                    ec.biometric_time = args['time']
                    ec.locationdevice_id = args['device_id']
                    ec.log_type = 'IN'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Checkin Unmarked"
                else:
                    return "Checkin Unmarked"
            elif args['device_id'] in ['Staff OUT','Workers OUT','Tr. CL Gents - OUT','Tr. CL Ladies - OUT']:
                if not frappe.db.exists('Unregistered Employee Checkin',{'biometric_pin':args['employee'],'biometric_time':args['time']}):
                    ec = frappe.new_doc('Unregistered Employee Checkin')
                    ec.biometric_pin = args['employee']
                    ec.biometric_time = args['time']
                    ec.locationdevice_id = args['device_id']
                    ec.log_type = 'OUT'
                    ec.save(ignore_permissions=True)
                    frappe.db.commit()
                    return "Checkin Unmarked"
                else:
                    return "Checkin Unmarked"
            else:
                return "Checkin Unmarked"
    
        except:
            frappe.log_error(title="checkin error",message=args)

