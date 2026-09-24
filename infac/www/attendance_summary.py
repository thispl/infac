from __future__ import unicode_literals
import frappe
from frappe.utils import nowdate
from datetime import datetime

no_cache = 1

@frappe.whitelist(allow_guest=True)
def get_att_data():
    now = datetime.now()
    date_now = now.strftime("%d/%m/%Y")
    time_now = now.strftime("%H:%M:%S")
    time_now_combined = f"{date_now} {time_now}"
    date = nowdate()

    apprentice_in = frappe.db.count("Attendance", {"in_time": ['!=', ''], "attendance_date": date, "employment_type": 'Apprentice', "docstatus": ['!=', 2]})
    contract_in   = frappe.db.count("Attendance", {"in_time": ['!=', ''], "attendance_date": date, "employment_type": 'Contract', "docstatus": ['!=', 2]})
    diplamo_in    = frappe.db.count("Attendance", {"in_time": ['!=', ''], "attendance_date": date, "employment_type": 'DIPLOMA', "docstatus": ['!=', 2]})
    trainee_in    = frappe.db.count("Attendance", {"in_time": ['!=', ''], "attendance_date": date, "employment_type": 'DRE', "docstatus": ['!=', 2]})
    staff_in      = frappe.db.count("Attendance", {"in_time": ['!=', ''], "attendance_date": date, "employment_type": 'STAFF', "docstatus": ['!=', 2]})

    apprentice_out = frappe.db.count("Attendance", {"out_time": ['!=', ''], "attendance_date": date, "employment_type": 'Apprentice', "docstatus": ['!=', 2]})
    contract_out   = frappe.db.count("Attendance", {"out_time": ['!=', ''], "attendance_date": date, "employment_type": 'Contract', "docstatus": ['!=', 2]})
    diplamo_out    = frappe.db.count("Attendance", {"out_time": ['!=', ''], "attendance_date": date, "employment_type": 'DIPLOMA', "docstatus": ['!=', 2]})
    trainee_out    = frappe.db.count("Attendance", {"out_time": ['!=', ''], "attendance_date": date, "employment_type": 'DRE', "docstatus": ['!=', 2]})
    staff_out      = frappe.db.count("Attendance", {"out_time": ['!=', ''], "attendance_date": date, "employment_type": 'STAFF', "docstatus": ['!=', 2]})

    in_total  = apprentice_in + staff_in + diplamo_in + contract_in + trainee_in
    out_total = apprentice_out + staff_out + diplamo_out + contract_out + trainee_out
    bal_total = in_total - out_total

    app_bal   = apprentice_in - apprentice_out
    staff_bal = staff_in - staff_out
    dip_bal   = diplamo_in - diplamo_out
    con_bal   = contract_in - contract_out
    train_bal = trainee_in - trainee_out

    html = f"""
    <table border="1" width="100%" style="font-size:20px; line-height:2.5; text-align:center;">
        <thead>
            <tr>
                <td colspan="7" style="background-color:#FF8080;">
                    <b>Manpower Attendance - {time_now_combined}</b>
                </td>
            </tr>
            <tr style="background-color:darkgray;">
                <td><b>Description</b></td>
                <td><b>Staff</b></td>
                <td><b>Diploma</b></td>
                <td><b>Apprentice</b></td>
                <td><b>Contractor</b></td>
                <td><b>Dre</b></td>
                <td><b>Total</b></td>
            </tr>
        </thead>
        <tbody>
            <tr style="color:green;">
                <td><b>Checkin (Present)</b></td>
                <td>{staff_in}</td>
                <td>{diplamo_in}</td>
                <td>{apprentice_in}</td>
                <td>{contract_in}</td>
                <td>{trainee_in}</td>
                <td><b>{in_total}</b></td>
            </tr>
            <tr style="color:brown;">
                <td><b>Checkout</b></td>
                <td>{staff_out}</td>
                <td>{diplamo_out}</td>
                <td>{apprentice_out}</td>
                <td>{contract_out}</td>
                <td>{trainee_out}</td>
                <td><b>{out_total}</b></td>
            </tr>
            <tr style="color:red;">
                <td><b>Balance</b></td>
                <td>{staff_bal}</td>
                <td>{dip_bal}</td>
                <td>{app_bal}</td>
                <td>{con_bal}</td>
                <td>{train_bal}</td>
                <td><b>{bal_total}</b></td>
            </tr>
        </tbody>
    </table>
    """

    return html
