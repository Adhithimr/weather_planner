# Copyright (c) 2026, Adhithi M R and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class City(Document):
# 	pass

import frappe
import requests
from frappe.model.document import Document

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"


class City(Document):
    def before_validate(self):
        # Only look up when something is missing, so saving again doesn't re-fetch
        if self.latitude and self.longitude and self.timezone:
            return
        self.fetch_location()

    def fetch_location(self):
        try:
            r = requests.get(
                GEOCODE_URL,
                params={"name": self.city_name, "count": 1, "language": "en", "format": "json"},
                timeout=10,
            )
            r.raise_for_status()
            results = r.json().get("results")
        except Exception:
            frappe.log_error(title=f"Geocoding failed: {self.city_name}")
            frappe.throw("Could not reach the location service. Please try again in a moment.")

        if not results:
            frappe.throw(f"No location found for '{self.city_name}'. Check the spelling.")

        place = results[0]
        self.latitude = place.get("latitude")
        self.longitude = place.get("longitude")
        self.timezone = place.get("timezone")
        self.country = place.get("country")
        self.state = place.get("admin1")
