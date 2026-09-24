# import frappe
# import pymysql
# # import mysql.connector
# from frappe.utils import getdate
# from datetime import timedelta

# @frappe.whitelist()
# def process_checkin_from_easytimepro(from_date, to_date):
#     """Called from Attendance Settings button — pulls punch data from EasyTimePro"""

#     cfg = (frappe.conf.get("easytimepro_mysql") or {})
#     host = cfg.get("host", "localhost")
#     user = cfg.get("user", "root")
#     password = cfg.get("password", "Pa55w0rd@")
#     database = cfg.get("database", "easytimepro")

#     conn = pymysql.connect(host=host, user=user, password=password, database=database, cursorclass=pymysql.cursors.DictCursor)
#     cur = conn.cursor()

#     def daterange(date1, date2):
#         for n in range(int((date2 - date1).days) + 1):
#             yield date1 + timedelta(n)

#     start_dt = getdate(from_date)
#     end_dt = getdate(to_date)

#     created = 0
#     skipped = 0

#     for dt in daterange(start_dt, end_dt):
#         sql = """
#             SELECT
#                 id,
#                 emp_code AS biometric_pin,
#                 punch_time AS log_time,
#                 terminal_alias AS log_type,
#                 DATE(punch_time) AS log_date
#             FROM iclock_transaction
#             WHERE DATE(punch_time) = %s
#         """
#         cur.execute(sql, (dt.strftime("%Y-%m-%d"),))
#         devicelog = cur.fetchall()

#         for d in devicelog or []:
#             bio_pin = d.get("biometric_pin")
#             log_time = d.get("log_time")
#             if not bio_pin or not log_time:
#                 continue

#             emp = frappe.db.get_value(
#                 "Employee",
#                 {"attendance_device_id": bio_pin, "status": "Active"},
#                 ["name"],
#                 as_dict=True,
#             )
#             if not emp:
#                 skipped += 1
#                 continue

#             log_time = log_time.replace(second=0, microsecond=0)

#             exists = frappe.db.exists(
#                 "Employee Checkin",
#                 {"employee": emp["name"], "time": log_time},
#             )
#             if exists:
#                 skipped += 1
#                 continue

#             doc = frappe.get_doc({
#                 "doctype": "Employee Checkin",
#                 "employee": emp["name"],
#                 "time": log_time,
#                 "log_type": "IN",
#                 "biometric_pin": bio_pin,
#             })
#             doc.insert(ignore_permissions=True)
#             created += 1

#     cur.close()
#     conn.close()

#     frappe.msgprint(f"Checkin processing completed.<br>Created: {created}<br>Skipped: {skipped}")



import frappe
import pymysql
from frappe.utils import getdate
from datetime import timedelta


@frappe.whitelist()
def process_checkin_from_easytimepro(from_date, to_date):
    """
    Pull punch data from EasyTimePro (MySQL)
    and create Employee Checkin records safely
    """

    # cfg = frappe.conf.get("easytimepro_mysql") or {}

    # host = cfg.get("host", "localhost")
    # user = cfg.get("user", "root")
    # password = cfg.get("password", "Pass")
    # database = cfg.get("database", "eapro")

    cfg = (frappe.conf.get("easytimepro_mysql") or {})
    host = cfg.get("host", "localhost")
    user = cfg.get("user", "root")
    password = cfg.get("password", "Pa55w0rd@")
    database = cfg.get("database", "easytimepro")

    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor,
    )
    cur = conn.cursor()

    def daterange(date1, date2):
        for n in range((date2 - date1).days + 1):
            yield date1 + timedelta(days=n)

    start_dt = getdate(from_date)
    end_dt = getdate(to_date)

    created = 0
    skipped = 0

    for dt in daterange(start_dt, end_dt):

        from_dt = f"{dt} 00:00:00"
        to_dt = f"{dt} 23:59:59"

        sql = """
            SELECT
                emp_code AS biometric_pin,
                punch_time AS log_time,
                terminal_alias AS device
            FROM iclock_transaction
            WHERE punch_time BETWEEN %s AND %s
        """
        cur.execute(sql, (from_dt, to_dt))
        devicelog = cur.fetchall()

        for d in devicelog or []:

            bio_pin = d.get("biometric_pin")
            log_time = d.get("log_time")
            device = (d.get("device") or "").upper()

            if not bio_pin or not log_time:
                skipped += 1
                continue

            emp = frappe.db.get_value(
                "Employee",
                {
                    "name": bio_pin,
                    "status": "Active",
                },
                "name",
            )

            if not emp:
                skipped += 1
                continue

            if "OUT" in device:
                log_type = "OUT"
            else:
                log_type = "IN"

            exists = frappe.db.exists(
                "Employee Checkin",
                {
                    "employee": emp,
                    "time": [
                        "between",
                        [
                            log_time - timedelta(seconds=30),
                            log_time + timedelta(seconds=30),
                        ],
                    ],
                },
            )

            if exists:
                skipped += 1
                continue
            try:
                doc = frappe.get_doc(
                    {
                        "doctype": "Employee Checkin",
                        "employee": emp,
                        "time": log_time,
                        "log_type": log_type,
                        "device_id": device,
                        "biometric_pin": bio_pin,
                    }
                )
                doc.insert(ignore_permissions=True)
                created += 1

            except Exception:
                skipped += 1
                frappe.log_error(
                    title="EasyTimePro Checkin Sync Error",
                    message=frappe.get_traceback(),
                )
    cur.close()
    conn.close()

    frappe.msgprint(
        f"""
        <b>EasyTimePro Checkin Sync Completed</b><br>
        Created : {created}<br>
        Skipped : {skipped}
        """
    )
