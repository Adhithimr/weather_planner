// frappe.pages['weather-planner'].on_page_load = function(wrapper) {
// 	var page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'None',
// 		single_column: true
// 	});
// }

frappe.pages["weather-planner"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("Weather Planner"),
        single_column: true,
    });

    const city_field = page.add_field({
        fieldname: "city",
        label: __("City"),
        fieldtype: "Link",
        options: "City",
        default: "Bengaluru",
        change: () => load(),
    });

    page.set_primary_action(__("Sync Now"), () => {
        frappe.call({
            method: "weather_planner.weather_planner.api.sync_now",
            freeze: true,
            freeze_message: __("Syncing weather for all cities..."),
            callback: () => {
                frappe.show_alert({ message: __("Sync finished"), indicator: "green" });
                load();
            },
        });
    });

    page.add_inner_button(__("Rainfall Report"), () =>
        frappe.set_route("query-report", "City Weather Analytics")
    );

    const $body = $('<div class="mt-4"></div>').appendTo(page.main);

    function load() {
        const city = city_field.get_value();
        if (!city) {
            $body.html("");
            return;
        }

        Promise.all([
            frappe.xcall("weather_planner.weather_planner.api.get_sync_status", { city }),
            frappe.xcall("weather_planner.weather_planner.api.recommend", { city }),
        ]).then(([status, rec]) => render(city, status || {}, rec));
    }

    function render(city, status, rec) {
        const synced = status.last_successful_sync
            ? frappe.datetime.str_to_user(status.last_successful_sync)
            : __("never");

        const warning =
            status.last_sync_status === "Failed"
                ? `<div class="alert alert-warning">
                       ${__("The last sync failed. Showing the last saved data.")}
                   </div>`
                : "";

        const heading = rec.indoor
            ? __("Suggest an indoor venue")
            : __("Recommended date: {0}", [frappe.datetime.str_to_user(rec.date)]);

        $body.html(`
            ${warning}
            <div class="frappe-card p-4">
                <div class="text-muted">${__("Last successful sync")}: ${synced}</div>
                <h3 class="mt-2">${frappe.utils.escape_html(city)}: ${heading}</h3>
                <p class="mb-0"><b>${__("Why")}:</b> ${frappe.utils.escape_html(rec.reason)}</p>
            </div>
        `);
    }

    load();
};