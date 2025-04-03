from . import __version__ as app_version

app_name = "infac"
app_title = "Infac"
app_publisher = "teampro"
app_description = "Custom APP for Infac"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "jagadeesan.a@groupteampro.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/infac/css/infac.css"
# app_include_js = "/assets/infac/js/infac.js"

# include js, css files in header of web template
# web_include_css = "/assets/infac/css/infac.css"
# web_include_js = "/assets/infac/js/infac.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "infac/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "infac.install.before_install"
# after_install = "infac.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "infac.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

override_doctype_class = {
	"Salary Slip": "infac.overrides.CustomSalarySlip",
	"Payroll Entry": "infac.overrides.CustomPayrollEntry",
	"Leave Application":"infac.overrides.CustomLeaveApplication",
	"Leave Allocation":"infac.overrides.CustomLeaveAllocation",
	"Employee":"infac.overrides.CustomEmployee",
	"Holiday List":"infac.overrides.CustomHolidayList",


}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Leave Application":{
		"on_submit":"infac.utils.leave_application"
	},
	"Employee":{
		"validate": "infac.custom.inactive_employee"
	},
	# "Attendance": {
	# 	'before_save':'infac.utils.get_attendance',
		# 'after_save':'infac.utils.mark_status_absent',
		# "on_update_on_submit": "infac.custom.set_late_hours_empty",
		# "on_update_before_save":"infac.custom.set_late_hours_empty",
		# "on_cancel": "method",
		# "on_trash": "method"
	# }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"infac.tasks.all"
# 	],
	# "daily": [
	# 		"infac.mark_attendance.mark_att"
	# ],
# 	"hourly": [
# 		"infac.tasks.hourly"
# 	],
# 	"weekly": [
# 		"infac.tasks.weekly"
# 	]
# 	"monthly": [
# 		"infac.tasks.monthly"
# 	]
"cron":{
		"*/20 * * * *" :[
			'infac.shift_attendance.mark_att'
		],
        "0 7 * * *" :[
			'infac.utils.miss_punch_mail_alert'
		],
        "0 7 * * *" :[
			'infac.utils.wrong_shift_mail_alert'
		],
		"0 7 21 * *" :[
			'infac.infac.doctype.payroll_dates_automatic.payroll_dates_automatic.payroll_date_automatic'
		],
		"0 12 * * *" :[
			'infac.doctype.payroll_process_settings.payroll_process_settings.payroll_date_change_automatic'
		]

	}
}

# Testing
# -------

# before_tests = "infac.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "infac.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "infac.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"infac.auth.validate"
# ]

