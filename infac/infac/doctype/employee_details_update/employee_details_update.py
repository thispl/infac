# Copyright (c) 2025, teampro and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeDetailsUpdate(Document):
    def validate(self):
        emp_name = frappe.db.get_value("Employee", {"employee_number": self.employee}, "name")
        
        if emp_name:
            if self.mobile:
                frappe.db.set_value("Employee", emp_name, "cell_number", self.mobile)
            # else:
            #     frappe.db.set_value("Employee", emp_name, "cell_number", "")
            if self.prefered_email:    
                frappe.db.set_value("Employee", emp_name, "prefered_email", self.prefered_email)
            if self.personal_email:    
                frappe.db.set_value("Employee", emp_name, "personal_email", self.personal_email)
            if self.unsubscribed:    
                frappe.db.set_value("Employee", emp_name, "unsubscribed", self.unsubscribed)
            if self.permanent_address_is:    
                frappe.db.set_value("Employee", emp_name, "permanent_accommodation_type", self.permanent_address_is)
            if self.permanent_address:    
                frappe.db.set_value("Employee", emp_name, "permanent_address", self.permanent_address)
            if self.prefered_contact_email:    
                frappe.db.set_value("Employee", emp_name, "prefered_contact_email", self.prefered_contact_email)
            if self.company_email:    
                frappe.db.set_value("Employee", emp_name, "company_email", self.company_email)
            if self.current_address_is:    
                frappe.db.set_value("Employee", emp_name, "current_accommodation_type", self.current_address_is)
            if self.current_address:    
                frappe.db.set_value("Employee", emp_name, "current_address", self.current_address)
            if self.bio__cover_letter:    
                frappe.db.set_value("Employee", emp_name, "bio", self.bio__cover_letter)
            if self.passport_number:    
                frappe.db.set_value("Employee", emp_name, "passport_number", self.passport_number)
            if self.date_of_issue:    
                frappe.db.set_value("Employee", emp_name, "date_of_issue", self.date_of_issue)    
            if self.valid_upto:    
                frappe.db.set_value("Employee", emp_name, "valid_upto", self.valid_upto)
            if self.place_of_issue:    
                frappe.db.set_value("Employee", emp_name, "place_of_issue", self.place_of_issue)
            if self.marital_status:    
                frappe.db.set_value("Employee", emp_name, "marital_status", self.marital_status)
            if self.blood_group:    
                frappe.db.set_value("Employee", emp_name, "blood_group", self.blood_group)
            if self.family_background:    
                frappe.db.set_value("Employee", emp_name, "family_background", self.family_background)
            if self.health_details:    
                frappe.db.set_value("Employee", emp_name, "health_details", self.health_details)
            if self.name1:    
                frappe.db.set_value("Employee", emp_name, "name_of_family_member", self.name1)
            if self.relationship:    
                frappe.db.set_value("Employee", emp_name, "relationship", self.relationship)
            if self.no_of_kids:    
                frappe.db.set_value("Employee", emp_name, "no_of_kids", self.no_of_kids)

            emp_doc = frappe.get_doc("Employee", emp_name)
            emp_doc.education = []
            for row in self.education:
                emp_doc.append("education", {
                    "school_univ": row.school_univ,
                    "qualification":row.qualification,
                    "level":row.level,
                    "year_of_passing":row.year_of_passing,
                    "class_per":row.class_per,
                    "maj_opt_subj":row.maj_opt_subj
            })
            emp_doc.external_work_history = []
            for row in self.external_work_history:
                emp_doc.append("external_work_history", {
                    "company_name": row.company_name,
                    "designation":row.designation,
                    "salary":row.salary,
                    "address":row.address,
                    "contact":row.contact,
                    "total_experience":row.total_experience
            })
            emp_doc.internal_work_history = []
            for row in self.internal_work_history:
                emp_doc.append("internal_work_history", {
                    "branch": row.branch,
                    "department":row.department,
                    "designation":row.designation,
                    "from_date":row.from_date,
                    "to_date":row.to_date,
            })
            emp_doc.save(ignore_permissions=True)

@frappe.whitelist()
def get_employee_education(emp_id):
    education = frappe.get_all(
        "Employee Education",
        filters={"parent": emp_id},   
        fields=["school_univ","qualification","level","year_of_passing","class_per","maj_opt_subj"]
    )
    external_work_history = frappe.get_all(
        "Employee External Work History",
        filters={"parent": emp_id},   
        fields=["company_name","designation","address","salary","contact","total_experience"]
    )
    internal_work_history = frappe.get_all(
        "Employee Internal Work History",
        filters={"parent": emp_id},   
        fields=["branch","department","designation","from_date","to_date"]
    )
    return {
        "education": education,
        "external_work_history": external_work_history,
        "internal_work_history": internal_work_history
    }
