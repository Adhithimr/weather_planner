app_name = "weather_planner"
app_title = "Weather Planner"
app_publisher = "Adhithi M R"
app_description = "Plan your trip by knowing the weather: pick the best day with low rain risk and manageable heat"
app_email = "adhitimr@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "weather_planner",
# 		"logo": "/assets/weather_planner/logo.png",
# 		"title": "Weather Planner",
# 		"route": "/weather_planner",
# 		"has_permission": "weather_planner.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/weather_planner/css/weather_planner.css"
# app_include_js = "/assets/weather_planner/js/weather_planner.js"

# include js, css files in header of web template
# web_include_css = "/assets/weather_planner/css/weather_planner.css"
# web_include_js = "/assets/weather_planner/js/weather_planner.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "weather_planner/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "weather_planner/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "weather_planner.utils.jinja_methods",
# 	"filters": "weather_planner.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "weather_planner.install.before_install"
# after_install = "weather_planner.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "weather_planner.uninstall.before_uninstall"
# after_uninstall = "weather_planner.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "weather_planner.utils.before_app_install"
# after_app_install = "weather_planner.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "weather_planner.utils.before_app_uninstall"
# after_app_uninstall = "weather_planner.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "weather_planner.build.after_build"

# To hook into the build process of other apps
# The list of apps being built is passed as an argument

# after_app_build = "weather_planner.build.after_app_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "weather_planner.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["weather_planner.search.awesomebar_results"]

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"weather_planner.tasks.all"
# 	],
# 	"daily": [
# 		"weather_planner.tasks.daily"
# 	],
# 	"hourly": [
# 		"weather_planner.tasks.hourly"
# 	],
# 	"weekly": [
# 		"weather_planner.tasks.weekly"
# 	],
# 	"monthly": [
# 		"weather_planner.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "weather_planner.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "weather_planner.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "weather_planner.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["weather_planner.utils.before_request"]
# after_request = ["weather_planner.utils.after_request"]

# Job Events
# ----------
# before_job = ["weather_planner.utils.before_job"]
# after_job = ["weather_planner.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"weather_planner.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

