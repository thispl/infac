import frappe
@frappe.whitelist(allow_guest=True)
def mark_checkin(**args):
    # frappe.log_error(
    #     title="Checkin Debug",
    #     message=f"Received: {args}"
    # )
    device=args['device_id'].upper()
    employee = args['employee']
    # if args['employee'] == "S248":
    if frappe.db.exists('Employee',{'name':args['employee'],'status':'Active'}):
        if employee:
            try:
                if device in ['STAFF IN','WORKERS IN','CL GENTS IN','CL LADIES IN']:
                    if not frappe.db.exists('Employee Checkin',{'employee':employee,'time':args['time']}):
                        ec = frappe.new_doc('Employee Checkin')
                        ec.employee = employee
                        ec.time = args['time']
                        ec.device_id = device
                        ec.log_type = 'IN'
                        ec.save(ignore_permissions=True)
                        frappe.db.commit()
                        return {"message": "Checkin Marked"}

                    else:
                        return {"message": "Checkin Marked"}

                elif device in ['STAFF OUT','WORKERS OUT','CL GENTS OUT','CL LADIES OUT']:
                    if not frappe.db.exists('Employee Checkin',{'employee':employee,'time':args['time']}):
                        ec = frappe.new_doc('Employee Checkin')
                        ec.employee = employee
                        ec.time = args['time']
                        ec.device_id = device
                        ec.log_type = 'OUT'
                        ec.save(ignore_permissions=True)
                        frappe.db.commit()
                        return {"message": "Checkin Marked"}

                    else:
                        return {"message": "Checkin Marked"}

                
                else:
                    if not frappe.db.exists('Employee Checkin',{'employee':employee,'time':args['time']}):
                        ec = frappe.new_doc('Employee Checkin')
                        ec.employee = employee
                        ec.time = args['time']
                        ec.device_id = device
                        # ec.log_type = 'OUT'
                        ec.save(ignore_permissions=True)
                        frappe.db.commit()
                        return {"message": "Checkin Marked"}

                    else:
                        return {"message": "Checkin Marked"}

        
            # except:
            #     frappe.log_error(title="checkin error1",message=args)
            except Exception as e:
                frappe.log_error(title="checkin error", message=frappe.get_traceback())
                return {"message": "Error", "error": str(e)}

    else:
            try:
                if device in ['STAFF IN','WORKERS IN','CL GENTS IN','CL LADIES IN']:
                    if not frappe.db.exists('Unregistered Employee Checkin',{'biometric_pin':args['employee'],'biometric_time':args['time']}):
                        ec = frappe.new_doc('Unregistered Employee Checkin')
                        ec.biometric_pin = args['employee']
                        ec.biometric_time = args['time']
                        ec.locationdevice_id = device
                        ec.log_type = 'IN'
                        ec.save(ignore_permissions=True)
                        frappe.db.commit()
                        return {"message": "Checkin Unmarked"}
                    else:
                        return {"message": "Checkin Unmarked"}
                    
                elif device in ['STAFF OUT','WORKERS OUT','CL GENTS OUT','CL LADIES OUT']:
                    if not frappe.db.exists('Unregistered Employee Checkin',{'biometric_pin':args['employee'],'biometric_time':args['time']}):
                        ec = frappe.new_doc('Unregistered Employee Checkin')
                        ec.biometric_pin = args['employee']
                        ec.biometric_time = args['time']
                        ec.locationdevice_id = device
                        ec.log_type = 'OUT'
                        ec.save(ignore_permissions=True)
                        frappe.db.commit()
                        return {"message": "Checkin Unmarked"}
                    else:
                        return {"message": "Checkin Unmarked"}
                else:
                    if not frappe.db.exists('Unregistered Employee Checkin',{'biometric_pin':args['employee'],'biometric_time':args['time']}):
                        ec = frappe.new_doc('Unregistered Employee Checkin')
                        ec.biometric_pin = args['employee']
                        ec.biometric_time = args['time']
                        ec.locationdevice_id = device
                        # ec.log_type = 'OUT'
                        ec.save(ignore_permissions=True)
                        frappe.db.commit()
                        return {"message": "Checkin Unmarked"}
                    else:
                        return {"message": "Checkin Unmarked"}
        
            # except:
            #     frappe.log_error(title="checkin error1",message=args)
            except Exception as e:
                frappe.log_error(title="checkin error", message=frappe.get_traceback())
                return {"message": "Error", "error": str(e)}
