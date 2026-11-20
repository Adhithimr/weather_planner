import frappe
from frappe import _
import requests
from frappe.utils import now_datetime, getdate

URL = "https://api.open-meteo.com/v1/forecast"
DAILY = "temperature_2m_max,precipitation_sum,precipitation_probability_max"


def build_values(day, temp, rain, prob):
    """Map API values to your fieldnames and flag missing ones."""
    vals = {
        "max_tempc": temp,
        "rainfallmm": rain,
        "max_rain_probability_": prob,
    }
    # Past days need temp + rainfall; forecast days need temp + probability
    if getdate(day) < getdate():
        required = ["max_tempc", "rainfallmm"]
    else:
        required = ["max_tempc", "max_rain_probability_"]

    vals["data_quality"] = (
        "Incomplete" if any(vals[f] is None for f in required) else "Complete"
    )
    vals["fetched_on"] = now_datetime()
    return vals


@frappe.whitelist()
def get_day_weather(city, date):
    """Fetch one day's weather for a city. Used by the Daily Weather form."""
    lat, lon = frappe.db.get_value("City", city, ["latitude", "longitude"])
    if lat is None or lon is None:
        frappe.throw(f"City {city} has no latitude/longitude yet.")

    try:
        r = requests.get(
            URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": DAILY,
                "start_date": str(date),
                "end_date": str(date),
                "timezone": "auto",
            },
            timeout=15,
        )
        r.raise_for_status()
        d = r.json()["daily"]
    except Exception:
        frappe.log_error(title=f"Day weather fetch failed: {city} {date}")
        frappe.throw(
            "Could not fetch weather for this date. It may be outside the "
            "range the API allows, or the service is unreachable."
        )

    return build_values(
        date,
        d["temperature_2m_max"][0],
        d["precipitation_sum"][0],
        d["precipitation_probability_max"][0],
    )


def sync_all():
    for city in frappe.get_all("City", pluck="name"):
        sync_city(city)


@frappe.whitelist()
def sync_now():
    frappe.only_for("System Manager")
    sync_all()
    return "ok"


def sync_city(city_name):
    city = frappe.get_doc("City", city_name)
    try:
        r = requests.get(
            URL,
            params={
                "latitude": city.latitude,
                "longitude": city.longitude,
                "daily": DAILY,
                "past_days": 30,
                "forecast_days": 7,
                "timezone": "auto",
            },
            timeout=15,
        )
        r.raise_for_status()
        d = r.json()["daily"]
    except Exception:
        frappe.log_error(title=f"Weather sync failed: {city_name}")
        frappe.db.set_value("City", city_name, "last_sync_status", "Failed")
        return False  # old Daily Weather rows stay untouched

    for i, day in enumerate(d["time"]):
        vals = build_values(
            day,
            d["temperature_2m_max"][i],
            d["precipitation_sum"][i],
            d["precipitation_probability_max"][i],
        )
        name = f"{city_name}-{day}"
        if frappe.db.exists("Daily Weather", name):
            doc = frappe.get_doc("Daily Weather", name)
            doc.update(vals)
        else:
            doc = frappe.get_doc(
                {"doctype": "Daily Weather", "city": city_name, "date": day, **vals}
            )
        doc.flags.from_sync = True  # stops the controller from calling the API again
        doc.save(ignore_permissions=True)

    frappe.db.set_value(
        "City",
        city_name,
        {"last_successful_sync": now_datetime(), "last_sync_status": "Success"},
    )
    return True

@frappe.whitelist()
def recommend(city):
    rows = frappe.get_all(
        "Daily Weather",
        filters={
            "city": city,
            "date": [">=", frappe.utils.today()],
            "data_quality": "Complete",
        },
        fields=["date", "max_tempc", "max_rain_probability_"],
        order_by="date asc",
        limit=7,
    )

    if not rows:
        return {
            "indoor": True,
            "reason": "No complete forecast data is saved for this city. Run a sync first.",
        }

    eligible = [r for r in rows if r.max_tempc <= 35]
    if not eligible:
        return {
            "indoor": True,
            "reason": "Every forecast day has a high above 35°C, so an indoor venue is safer.",
        }

    best = min(eligible, key=lambda r: (r.max_rain_probability_, r.date))

    if best.max_rain_probability_ >= 60:
        return {
            "indoor": True,
            "reason": (
                f"The best eligible day ({best.date}) still has a "
                f"{best.max_rain_probability_}% chance of rain (60% or more), "
                "so an indoor venue is suggested."
            ),
        }

    return {
        "indoor": False,
        "date": str(best.date),
        "temp": best.max_tempc,
        "rain_probability": best.max_rain_probability_,
        "reason": (
            f"{best.date}: high of {best.max_tempc}°C (35°C or below) and the lowest "
            f"rain probability ({best.max_rain_probability_}%) among "
            f"{len(eligible)} eligible days. Ties go to the earlier date."
        ),
    }

@frappe.whitelist()
def get_sync_status(city):
    return frappe.db.get_value(
        "City", city, ["last_successful_sync", "last_sync_status"], as_dict=True
    )

@frappe.whitelist()
def get_week(city):
    rows = frappe.get_all(
        "Daily Weather",
        filters={"city": city, "date": [">=", frappe.utils.today()]},
        fields=["date", "max_tempc", "max_rain_probability_", "data_quality"],
        order_by="date asc",
        limit=7,
    )
    week = []
    for r in rows:
        if r.data_quality != "Complete":
            status = "unknown"
        elif r.max_tempc > 35 or r.max_rain_probability_ >= 60:
            status = "bad"
        else:
            status = "good"
        week.append({
            "date": str(r.date),
            "temp": r.max_tempc,
            "rain": r.max_rain_probability_,
            "status": status,
        })
    return week

@frappe.whitelist()
def check_trip_date(city, date):
    date = getdate(date)

    if date < getdate():
        return {"status": "unknown", "reason": _("That date is in the past. Please pick today or a later date.")}

    row = frappe.db.get_value(
        "Daily Weather",
        {"city": city, "date": date},
        ["max_tempc", "max_rain_probability_", "data_quality"],
        as_dict=True,
    )

    if not row:
        return {
            "status": "unknown",
            "reason": _("No forecast is saved for {0} on {1}. Forecasts cover about the next 7 days.").format(city, date),
        }

    if row.data_quality != "Complete":
        return {
            "status": "unknown",
            "reason": _("The forecast for this day has missing values, so it can't be judged."),
        }

    temp, prob = row.max_tempc, row.max_rain_probability_
    result = {"temp": temp, "rain_probability": prob}

    problems = []
    if temp > 35:
        problems.append(_("the high of {0}°C is above 35°C").format(temp))
    if prob >= 60:
        problems.append(_("the chance of rain is {0}% (60% or more)").format(prob))

    if problems:
        result["status"] = "bad"
        result["reason"] = _("Not recommended: ") + _(" and ").join(problems) + "."
    else:
        result["status"] = "good"
        result["reason"] = _("Looks good: a high of {0}°C and a {1}% chance of rain.").format(temp, prob)

    best = recommend(city) or {}
    if best.get("indoor"):
        if result["status"] == "bad":
            result["suggestion"] = _("No day in the forecast is suitable, so an indoor venue is suggested.")
    elif best.get("date") and best["date"] != str(date) and (
        result["status"] == "bad" or best["rain_probability"] < prob
    ):
        result["suggestion"] = _(
            "Best day in the forecast: {0}, with a high of {1}°C and a {2}% chance of rain."
        ).format(best["date"], best["temp"], best["rain_probability"])
        result["suggestion_date"] = best["date"]

    return result