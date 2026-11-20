# Copyright (c) 2026, Adhithi M R and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# def execute_snapshot_report(filters: dict | None = None):
# 	"""Return columns and data for the report.

# 	This is the main entry point for snapshot report. When 'Synced
# 	Report' is enabled in report, framework will call this method
# 	every time the report is refreshed or a filter is updated. It
# 	accepts the same filters as normal execute. But a utility method -
# 	get_latest_sync, is also imported.

# 	"""
# 	from frappe.database.duckdb.database import get_latest_sync

# 	columns, data = [], []
# 	return columns, data

import frappe
from frappe import _


def execute(filters=None):
    filters = frappe._dict(filters or {})
    return get_columns(), get_data(filters), None, get_chart(filters)


def get_columns():
    return [
        {"label": _("City"), "fieldname": "city", "fieldtype": "Link", "options": "City", "width": 150},
        {"label": _("Total Rainfall (mm)"), "fieldname": "total_rainfall", "fieldtype": "Float", "precision": 1, "width": 160},
        {"label": _("Days with ≥ 1 mm"), "fieldname": "rainy_days", "fieldtype": "Int", "width": 140},
        {"label": _("Avg Daily High (°C)"), "fieldname": "avg_high", "fieldtype": "Float", "precision": 1, "width": 150},
        {"label": _("Days Excluded (Incomplete)"), "fieldname": "incomplete_days", "fieldtype": "Int", "width": 190},
    ]


def get_data(filters):
    return frappe.db.sql(
        """
        SELECT
            city,
            SUM(CASE WHEN data_quality = 'Complete' THEN rainfallmm ELSE 0 END) AS total_rainfall,
            SUM(CASE WHEN data_quality = 'Complete' AND rainfallmm >= 1 THEN 1 ELSE 0 END) AS rainy_days,
            AVG(CASE WHEN data_quality = 'Complete' THEN max_tempc END) AS avg_high,
            SUM(CASE WHEN data_quality = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete_days
        FROM `tabDaily Weather`
        WHERE date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY city
        ORDER BY city
        """,
        filters,
        as_dict=True,
    )


def get_chart(filters):
    rows = frappe.db.sql(
        """
        SELECT city, date, rainfallmm
        FROM `tabDaily Weather`
        WHERE date BETWEEN %(from_date)s AND %(to_date)s
          AND data_quality = 'Complete'
        ORDER BY date
        """,
        filters,
        as_dict=True,
    )
    if not rows:
        return None

    labels = sorted({str(r.date) for r in rows})
    by_city = {}
    for r in rows:
        by_city.setdefault(r.city, {})[str(r.date)] = r.rainfallmm

    datasets = [
        {"name": city, "values": [vals.get(d, 0) for d in labels]}
        for city, vals in by_city.items()
    ]
    return {"data": {"labels": labels, "datasets": datasets}, "type": "line"}