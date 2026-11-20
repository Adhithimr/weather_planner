# Weather Planner

A Frappe app that helps someone planning an outdoor event pick a day with lower rain risk and manageable heat. It pulls forecasts and recent weather from [Open-Meteo](https://open-meteo.com/), stores one record per city per date, and recommends the best day for a chosen city. A login-protected page lets a user check any date for any saved city.

Demo cities: Bengaluru, Chennai and Coimbatore.

<!-- Add screenshots here, for example:
![Desk planner page](docs/desk-page.png)
![Rainfall report](docs/report.png)
![Trip check page](docs/trip-check.png)
-->

## Features

- **API integration.** Fetches the past 30 days and the next 7 days of weather for each city from Open-Meteo. No API key needed.
- **Data storage.** One `Daily Weather` record per city and date. Running a sync twice updates existing records and never creates duplicates.
- **Sync.** A manual **Sync Now** button on the Desk page and a daily scheduled sync.
- **Analytics.** A Script Report, `City Weather Analytics`, with a date filter. It shows total rainfall, the number of days with at least 1 mm of rain, and the average daily high for each city, plus a chart comparing daily rainfall across cities.
- **Recommendation.** For the selected city, picks the forecast day with the lowest maximum rain probability among days with a high of 35°C or lower. Ties go to the earlier date. If every eligible day has a rain probability of 60% or more, or every day is too hot, it suggests an indoor venue. The reason is always shown.
- **Error handling.** If the API fails, the app keeps showing the last saved data along with the last successful sync time. Days with missing values are marked `Incomplete` and are left out of recommendations and totals.
- **Trip check page.** A website page at `/trip-check`, for logged-in users only. The user picks a city and a date and sees whether the day is good, with the reason, a 7-day overview and a suggested better day.

## How it works

| Piece | Where |
|---|---|
| `City` DocType | City name, latitude, longitude, timezone, last successful sync, last sync status |
| `Daily Weather` DocType | City, date, max temperature, rainfall, max rain probability, data quality, fetched on |
| Naming | `Daily Weather` is named `{city}-{date}`, so each city and date has exactly one record |
| Sync and recommendation logic | `weather_planner/weather_planner/api.py` |
| Scheduler | `scheduler_events` in `hooks.py` runs the daily sync |
| Report | `City Weather Analytics` (Script Report on `Daily Weather`) |
| Desk page | `/app/weather-planner` |
| User page | `/trip-check` (`weather_planner/www/trip-check.html` and `.py`) |

### Missing data

Past days need a temperature and rainfall value. Forecast days need a temperature and a rain probability. If a required value is missing, the day is saved with `data_quality = Incomplete`. Incomplete days are excluded from the recommendation, the report totals and the trip check, and the report shows how many days were excluded.

### Recommendation rules

1. Keep forecast days (today onward) with complete data and a high of 35°C or lower.
2. Pick the day with the lowest maximum rain probability. Ties go to the earlier date.
3. If no day qualifies, or the best day has a rain probability of 60% or more, suggest an indoor venue.

## Installation

Requires a working [Frappe bench](https://docs.frappe.io/framework/user/en/installation).

```bash
bench get-app https://github.com/Adhithimr/weather_planner.git
bench --site <your-site> install-app weather_planner
bench --site <your-site> enable-scheduler
bench restart
```

## Setup

1. Create the cities at `/app/city`. For the demo:

   | City | Latitude | Longitude |
   |---|---|---|
   | Bengaluru | 12.9716 | 77.5946 |
   | Chennai | 13.0827 | 80.2707 |
   | Coimbatore | 11.0168 | 76.9558 |

2. Open `/app/weather-planner` and click **Sync Now** to load the data. After that, the scheduler runs the sync once a day.
3. For the trip check page, create a user with **User Type** set to **Website User**. Users can then log in and open `/trip-check`.

## Demo

1. Open the Desk page and pick **Bengaluru**. The card shows the recommended date and the reason.
2. Open **City Weather Analytics** and compare Bengaluru's recent rainfall with Chennai's on the chart.
3. Open `/trip-check` as a website user, pick a city and a date, and see the verdict.

## Notes and limitations

- Forecasts cover about the next 7 days, so the trip check can only judge dates in that window.
- The daily sync depends on the Frappe scheduler being enabled on the site.
- Data is only as fresh as the last successful sync.

## Data source

Weather data by [Open-Meteo.com](https://open-meteo.com/). The free API is for non-commercial use. Please check their [terms](https://open-meteo.com/en/terms) for attribution requirements.

## License

MIT
