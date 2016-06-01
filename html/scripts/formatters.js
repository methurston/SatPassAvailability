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

function formatTimeSlots(user_timeslots) {
    "use strict";
    var allslots = user_timeslots.timeslots,
        slotshtml = '<table class="table">',
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
    availhtml += "<td>" + available_pass.aos.time + "</td>";
    availhtml += "<td>" + available_pass.max_elevation.time + "</td>";
    availhtml += "<td>" + available_pass.los.time + "</td></tr>";
    availhtml += "<tr><td></td><td>" + available_pass.aos.azimuth + "</td>";
    availhtml += "<td>AZ: " + available_pass.max_elevation.azimuth;
    availhtml += " EL: " + available_pass.max_elevation.elevation + "</td>";
    availhtml += "<td>" + available_pass.los.azimuth + "</td></tr>";
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
