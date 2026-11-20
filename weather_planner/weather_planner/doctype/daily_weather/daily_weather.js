// Copyright (c) 2026, Adhithi M R and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Daily Weather", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Daily Weather", {
    city(frm) {
        frm.trigger("fetch_weather");
    },
    date(frm) {
        frm.trigger("fetch_weather");
    },
    fetch_weather(frm) {
        if (!frm.doc.city || !frm.doc.date) return;
        frappe.call({
            method: "weather_planner.weather_planner.api.get_day_weathe",
            args: { city: frm.doc.city, date: frm.doc.date },
            freeze: true,
            freeze_message: __("Fetching weather..."),
            callback(r) {
                if (r.message) frm.set_value(r.message);
            },
        });
    },
});