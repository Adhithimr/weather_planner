# Copyright (c) 2026, Adhithi M R and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document


# class DailyWeather(Document):
# 	pass
from frappe.model.document import Document
from weather_planner.weather_planner.api import get_day_weather


class DailyWeather(Document):
    def validate(self):
        # The sync job sets values itself; only fetch for records made by hand
        if self.flags.from_sync or not self.is_new():
            return
        self.update(get_day_weather(self.city, self.date))