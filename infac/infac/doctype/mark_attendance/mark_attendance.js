// Copyright (c) 2026, abdulla.pi@groupteampro.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Mark Attendance", {
    after_save(frm){
        frm.reload_doc();
    },
	check_in(frm) {
        if (!navigator.geolocation) {
            frappe.msgprint(__('Geolocation is not supported by your browser.'));
        }

        const now = new Date();
        frm.set_value('in_time', frappe.datetime.now_datetime());
        console.log("HI Checkin ...1")
        function get_high_accuracy_location(retry = false) {
            console.log("HI Checkin ...2")
            navigator.geolocation.getCurrentPosition(
                function (position) {
                    const { latitude, longitude } = position.coords;

                    frm.set_value('check_in_latitude', latitude);
                    frm.set_value('check_in_longitude', longitude);

                    const geocoder = new google.maps.Geocoder();
                    geocoder.geocode(
                        { location: { lat: latitude, lng: longitude } },
                        function (results, status) {
                            console.log("HI Checkin ...")
                            // if (status === 'OK' && results[0]) {
                            //     frm.set_value('checkin_address', results[0].formatted_address);
                            //     frm.save()
                            // } else {
                            //     frappe.msgprint(__('Unable to fetch address. Try again.'));
                            // }
                            if (status === 'OK' && results[0]) {
                                console.log("HI Print OUT Address")
                                frm.set_value('checkin_address', results[0].formatted_address);
                                frm.save()
                            } else {
                                console.error('Geocoding failed:', status, results);
                                frappe.msgprint(__('Unable to fetch address ({0}). Check console for details.', [status]));
                            }
                        }
                    );
                },
                function (error) {
                    if (error.code === error.PERMISSION_DENIED) {
                        const siteSettingsUrl =
                            "chrome://settings/content/siteDetails?site=https%3A%2F%2F103.103.9.11";
                    
                        window.copySiteSettingsLink = function () {
                            if (window.__site_settings_copied) return;
                    
                            navigator.clipboard.writeText(siteSettingsUrl).then(() => {
                                window.__site_settings_copied = true;
                    
                                const el = document.getElementById("site-settings-msg");
                                if (el) {
                                    el.innerHTML = "✔ Link copied! Paste it in Chrome address bar";
                                    el.style.color = "#16a34a"; 
                                    el.style.fontWeight = "600";
                                }
                            });
                        };
                        // frm.set_value('in_time', '');
                        frm.save()
                        frappe.msgprint({
                            title: __('Location Access Blocked'),
                            message: __(
                                'Location access is required to create this record.<br><br>' +
                                '<b>How to enable:</b><br>' +
                                '1. Open <b><a href="#" onclick="copySiteSettingsLink(); return false;">Site Settings</a></b><br>' +
                                '2. Enable <b>Location</b> for this site<br>' +
                                '3. Also make sure <b>Location</b> enabled in device<br>' +
                                '4. Refresh the page and try again<br><br>' +
                                '<div id="site-settings-msg" style="color:#6b7280;"></div>'
                            )
                        });
                    }



                    if (error.code === error.TIMEOUT && !retry) {
                        setTimeout(() => get_high_accuracy_location(true), 5000);
                        return;
                    }

                    frappe.msgprint(__('Unable to capture GPS location. Move outdoors and retry.'));
                },
                {
                    enableHighAccuracy: true,
                    timeout: 30000,
                    maximumAge: 0
                }
            );
        }

        setTimeout(() => {
            get_high_accuracy_location();
        }, 2000);
        
	},
    check_out(frm) {
        if (!navigator.geolocation) {
            frappe.msgprint(__('Geolocation is not supported by your browser.'));
        }

        const now = new Date();
        frm.set_value('out_time', frappe.datetime.now_datetime());
        
        
        function get_high_accuracy_location(retry = false) {
            navigator.geolocation.getCurrentPosition(
                function (position) {
                    const { latitude, longitude } = position.coords;

                    frm.set_value('check_out_latitude', latitude);
                    frm.set_value('check_out_longitude', longitude);

                    const geocoder = new google.maps.Geocoder();
                    geocoder.geocode(
                        { location: { lat: latitude, lng: longitude } },
                        function (results, status) {
                            if (status === 'OK' && results[0]) {
                                console.log("HI Print OUT Address")
                                frm.set_value('check_out_address', results[0].formatted_address);
                                frm.save()
                            } else {
                                frappe.msgprint(__('Unable to fetch address. Try again.'));
                            }
                        }
                    );
                },
                function (error) {
                    if (error.code === error.PERMISSION_DENIED) {
                        const siteSettingsUrl =
                            "chrome://settings/content/siteDetails?site=https%3A%2F%103.103.9.11";
                    
                        window.copySiteSettingsLink = function () {
                            if (window.__site_settings_copied) return;
                    
                            navigator.clipboard.writeText(siteSettingsUrl).then(() => {
                                window.__site_settings_copied = true;
                    
                                const el = document.getElementById("site-settings-msg");
                                if (el) {
                                    el.innerHTML = "✔ Link copied! Paste it in Chrome address bar";
                                    el.style.color = "#16a34a"; 
                                    el.style.fontWeight = "600";
                                }
                            });
                        };
                        // frm.set_value('out_time', '');
                        frm.save()
                        frappe.msgprint({
                            title: __('Location Access Blocked'),
                            message: __(
                                'Location access is required to create this record.<br><br>' +
                                '<b>How to enable:</b><br>' +
                                '1. Open <b><a href="#" onclick="copySiteSettingsLink(); return false;">Site Settings</a></b><br>' +
                                '2. Enable <b>Location</b> for this site<br>' +
                                '3. Also make sure <b>Location</b> enabled in device<br>' +
                                '4. Refresh the page and try again<br><br>' +
                                '<div id="site-settings-msg" style="color:#6b7280;"></div>'
                            )
                        });
                    }



                    if (error.code === error.TIMEOUT && !retry) {
                        setTimeout(() => get_high_accuracy_location(true), 5000);
                        return;
                    }

                    frappe.msgprint(__('Unable to capture GPS location. Move outdoors and retry.'));
                },
                {
                    enableHighAccuracy: true,
                    timeout: 30000,
                    maximumAge: 0
                }
            );
        }

        setTimeout(() => {
            get_high_accuracy_location();
        }, 2000);
        
	},
});
