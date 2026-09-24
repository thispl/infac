# # Copyright (c) 2025, teampro and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class Approval(Document):
#      pass

# @frappe.whitelist(allow_guest=True)
# def submit_leave_doc(self,doctype,name,workflow_state):
# 	frappe.log_error(doctype,workflow_state)
# 	doc = frappe.get_doc(doctype,name)
# 	if workflow_state == 'Approved':
# 		doc.status = 'Approved'
# 		doc.flags.ignore_permissions = 1
# 		doc.workflow_state = workflow_state
# 		doc.save(ignore_permissions=True)
# 		doc.submit()
# 	elif workflow_state == 'Rejected' and doctype=='Leave Application':
# 		doc.workflow_state = workflow_state
# 		doc.status='Rejected'
# 		doc.save(ignore_permissions=True) 
# 		doc.submit()          
# 	else:
# 		if workflow_state == 'Incharge Pending':
# 			doc.workflow_state = 'Superior Pending'
# 			doc.save(ignore_permissions=True)
# 			# if not doc.is_hod == 0:
# 			# 	doc.workflow_state = 'Superior Pending'
# 			# 	doc.save(ignore_permissions=True)
# 			# else:
# 			# 	doc.workflow_state = workflow_state
# 			# 	doc.save(ignore_permissions=True)
# 		else:
# 			doc.workflow_state = workflow_state
# 			doc.save(ignore_permissions=True)
# 	return "ok"


import frappe
from frappe.model.document import Document

#All the below lines based on change workflow state
class Approval(Document):
    @frappe.whitelist(allow_guest=True)
    def submit_leave_doc(self,doctype,name,workflow_state):
        # frappe.log_error(doctype,workflow_state)
        doc = frappe.get_doc(doctype,name)
        if workflow_state == 'Approved':
            doc.status = 'Approved'
            doc.flags.ignore_permissions = 1
            doc.workflow_state = workflow_state
            doc.save(ignore_permissions=True)
            doc = frappe.get_doc(doctype, name)
            doc.submit()
        elif workflow_state == 'Rejected' and doctype=='Leave Application':
            doc.workflow_state = workflow_state
            doc.status='Rejected'
            doc.save(ignore_permissions=True) 
            doc = frappe.get_doc(doctype, name)
            doc.submit()          
        else:
            if workflow_state == 'Superior Pending':
                doc.workflow_state = 'Approved'
                doc.status = 'Approved'
                doc.flags.ignore_permissions = 1
                doc.save(ignore_permissions=True)
                doc = frappe.get_doc(doctype, name)
                doc.submit()
                doc.save(ignore_permissions=True)
            elif workflow_state == 'Incharge Pending':
                doc.workflow_state = 'Superior Pending'
                doc.save(ignore_permissions=True)
            else:
                doc.workflow_state = workflow_state
                doc.save(ignore_permissions=True)
        return "ok"

    @frappe.whitelist(allow_guest=True)
    def submit_miss_punch_doc(self,doctype,name,workflow_state):
        # frappe.log_error(doctype,workflow_state)
        doc = frappe.get_doc(doctype,name)
        if workflow_state == 'Approved':
            # doc.status = 'Approved'
            doc.flags.ignore_permissions = 1
            doc.workflow_state = workflow_state
            doc.save(ignore_permissions=True)
            doc = frappe.get_doc(doctype, name)
            doc.submit()
        elif workflow_state == 'Rejected':
            doc.workflow_state = workflow_state
            # doc.status='Rejected'
            doc.save(ignore_permissions=True) 
            doc = frappe.get_doc(doctype, name)
            doc.submit()          
        else:
            if workflow_state == 'Superior Pending':
                doc.workflow_state = 'Approved'
                # doc.status = 'Approved'
                doc.flags.ignore_permissions = 1
                doc.save(ignore_permissions=True)
                doc = frappe.get_doc(doctype, name)
                # doc.submit()
                doc.save(ignore_permissions=True)
            elif workflow_state == 'Incharge Pending':
                doc.workflow_state = 'Superior Pending'
                doc.save(ignore_permissions=True)
            else:
                doc.workflow_state = workflow_state
                doc.save(ignore_permissions=True)
        return "ok"

    @frappe.whitelist(allow_guest=True)
    def submit_pr_doc(self,doctype,name,workflow_state):
        # frappe.log_error(doctype,workflow_state)
        doc = frappe.get_doc(doctype,name)
        if workflow_state == 'Approved':
            # doc.status = 'Approved'
            doc.flags.ignore_permissions = 1
            doc.workflow_state = workflow_state
            doc.save(ignore_permissions=True)
            doc = frappe.get_doc(doctype, name)
            doc.submit()
        elif workflow_state == 'Rejected':
            doc.workflow_state = workflow_state
            # doc.status='Rejected'
            doc.save(ignore_permissions=True) 
            doc = frappe.get_doc(doctype, name)
            doc.submit()          
        else:
            if workflow_state == 'HOD Pending':
                doc.workflow_state = 'Approved'
                # doc.status = 'Approved'
                doc.flags.ignore_permissions = 1
                doc.save(ignore_permissions=True)
                doc = frappe.get_doc(doctype, name)
                # doc.submit()
                doc.save(ignore_permissions=True)
            elif workflow_state == 'Incharge Pending':
                doc.workflow_state = 'Superior Pending'
                doc.save(ignore_permissions=True)
            elif workflow_state == 'Superior Pending':
                doc.workflow_state = 'HOD Pending'
                doc.save(ignore_permissions=True)    
            else:
                doc.workflow_state = workflow_state
                doc.save(ignore_permissions=True)
        return "ok"    
    @frappe.whitelist(allow_guest=True)
    def submit_od_doc(self,doctype,name,workflow_state):
        # frappe.log_error(doctype,workflow_state)
        doc = frappe.get_doc(doctype,name)
        if workflow_state == 'Approved':
            # doc.status = 'Approved'
            doc.flags.ignore_permissions = 1
            doc.workflow_state = workflow_state
            doc.save(ignore_permissions=True)
            doc = frappe.get_doc(doctype, name)
            doc.submit()
        elif workflow_state == 'Rejected':
            doc.workflow_state = workflow_state
            # doc.status='Rejected'
            doc.save(ignore_permissions=True) 
            doc = frappe.get_doc(doctype, name)
            doc.submit()          
        else:
            if workflow_state == 'Superior Pending':
                doc.workflow_state = 'Approved'
                # doc.status = 'Approved'
                doc.flags.ignore_permissions = 1
                doc.save(ignore_permissions=True)
                doc = frappe.get_doc(doctype, name)
                # doc.submit()
                doc.save(ignore_permissions=True)
            elif workflow_state == 'Incharge Pending':
                doc.workflow_state = 'Superior Pending'
                doc.save(ignore_permissions=True)
            # elif workflow_state == 'Superior Pending':
            #     doc.workflow_state = 'HOD Pending'
            #     doc.save(ignore_permissions=True)    
            else:
                doc.workflow_state = workflow_state
                doc.save(ignore_permissions=True)
        return "ok"     
    @frappe.whitelist(allow_guest=True)
    def submit_ot_doc(self,doctype,name,workflow_state):
        # frappe.log_error(doctype,workflow_state)
        doc = frappe.get_doc(doctype,name)
        if workflow_state == 'Approved':
            # doc.status = 'Approved'
            doc.flags.ignore_permissions = 1
            doc.workflow_state = workflow_state
            doc.save(ignore_permissions=True)
            doc = frappe.get_doc(doctype, name)
            doc.submit()
        elif workflow_state == 'Rejected':
            doc.workflow_state = workflow_state
            # doc.status='Rejected'
            doc.save(ignore_permissions=True) 
            doc = frappe.get_doc(doctype, name)
            doc.submit()          
        else:
            if workflow_state == 'HOD Pending':
                doc.workflow_state = 'Approved'
                # doc.status = 'Approved'
                doc.flags.ignore_permissions = 1
                doc.save(ignore_permissions=True)
                doc = frappe.get_doc(doctype, name)
                # doc.submit()
                doc.save(ignore_permissions=True)
            elif workflow_state == 'Incharge Pending':
                doc.workflow_state = 'Superior Pending'
                doc.save(ignore_permissions=True)
            elif workflow_state == 'Superior Pending':
                doc.workflow_state = 'HOD Pending'
                doc.save(ignore_permissions=True)    
            else:
                doc.workflow_state = workflow_state
                doc.save(ignore_permissions=True)
        return "ok"     