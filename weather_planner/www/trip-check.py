import frappe

no_cache = 1


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/trip-check"
        raise frappe.Redirect

    context.title = "Trip Weather Check"
    context.cities = frappe.get_all("City", pluck="name", order_by="name")