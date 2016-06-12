/*jslint browser: true*/
/*global $, jQuery, alert, console, confirm*/

/*formatting functions */

function formatSlot(user_timeslot) {
    "use strict";
    var slothtml = "<tr><td>" + user_timeslot.id + "</td>";
    slothtml += "<td>" + user_timeslot.date + "</td>";
    slothtml += "<td>" + (user_timeslot.duration / 3600).toFixed(2) + "</td>";
    slothtml += "<td><p onclick='ajaxDeleteTimeslot(getUserCallsign(),";
    slothtml += user_timeslot.id + ")'>DELETE</p></td></tr>";
    return slothtml;
}

function formatTime(isotimestring) {
    "use strict";
    var weekday = new Array(7);
    weekday[0] = "Sunday";
    weekday[1] = "Monday";
    weekday[2] = "Tuesday";
    weekday[3] = "Wednesday";
    weekday[4] = "Thursday";
    weekday[5] = "Friday";
    weekday[6] = "Saturday";
    var jsDate = new Date(isotimestring),
        datestring = weekday[jsDate.getDay()] + " " + (jsDate.getMonth() + 1) + "/" + jsDate.getDate() + "/" + jsDate.getFullYear();
    datestring += " " + jsDate.getHours() + ":" + jsDate.getMinutes() + ":" + jsDate.getSeconds();
    return datestring;
    
    
}

function formatTimeSlots(user_timeslots) {
    "use strict";
    var allslots = user_timeslots.timeslots,
        slotshtml = '<table class="table table-sm">',
        index = 0;
    slotshtml += "<tr><th>ID</th><th>Starting date/time</th><th>Duration</th><th>Delete</th></tr>";
    for (index; index < allslots.length; index += 1) {
        slotshtml += formatSlot(allslots[index]);
    }
    slotshtml += "</table>";
    return slotshtml;
}

function formatAvailableSlot(available_pass) {
    "use strict";
    var availhtml = "<tr><td>" + available_pass.sat_name + "</td>";
    availhtml += "<td>" + formatTime(available_pass.aos.time) + "</td>";
    availhtml += "<td>" + formatTime(available_pass.max_elevation.time) + "</td>";
    availhtml += "<td>" + formatTime(available_pass.los.time) + "</td></tr>";
    availhtml += "<tr><td></td><td>AZ: " + available_pass.aos.azimuth + "</td>";
    availhtml += "<td>AZ: " + available_pass.max_elevation.azimuth;
    availhtml += " EL: " + available_pass.max_elevation.elevation + "</td>";
    availhtml += "<td>AZ: " + available_pass.los.azimuth + "</td></tr>";
    return availhtml;
}

function formatAvailablePasses(all_available) {
    "use strict";
    var allhtml = '<table class="table">',
        index = 0;
    allhtml += "<tr><th>Name</th><th>AOS</th><th>Max Elevation</th><th>LOS</th></tr>";
    for (index; index < all_available.length; index += 1) {
        allhtml += formatAvailableSlot(all_available[index]);
    }
    allhtml += "</table>";
    return allhtml;
}

function resetAll() {
    "use strict";
    location.reload();
}
