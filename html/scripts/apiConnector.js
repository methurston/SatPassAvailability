/*jslint browser: true*/
/*global $, jQuery, alert, console, confirm*/

var baseApiEndpoint = "http://localhost:8000/user/";

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

function emptyStringToNull(input_string) {
    "use strict";
    var output_string;
    if (input_string === "") {
        output_string = null;
    } else {
        output_string = input_string;
    }
    return output_string;
}
/*end formatters*/

function getUserCallsign() {
    "use strict";
    var sign = $("#userinput input[id='callsign']").val();
    return sign;
}

function getUserForm() {
    "use strict";
     //var form_input = $("#userinput");
    var userinfo = {
        "callsign": $('#userinput input[id="callsign"]').val(),
        "timezone": $('#userinput input[id="timezone"]').val(),
        "street_address": $('#userinput input[id="street_address"]').val(),
        "lat": $('#userinput input[id="lat"]').val(),
        "long": $('#userinput input[id="long"]').val(),
        "elevation": $('#userinput input[id="elevation"]').val()
    };
     //console.log('street address: ' + userinfo.street_address + '***')

    $('#storedinfo').html(userinfo.callsign + "<br>" + userinfo.timezone);
    return userinfo;
}


function getTimeslotForm() {
    "use strict";
    var available_days = [];
    $.each($('#slotinfo input[name="days"]:checked'), function () {
        available_days.push($(this).val());
    });
    var start = $('#slotinfo input[id="start_time"]').val(),
        timeinfo = {
            "days": available_days.toString(),
            "start_time": start,
            "duration": $('#slotinfo input[id="duration"]').val()
        };
    return timeinfo;
}

/* ajax functions to access api */
function ajaxGetAllAvailability(callsign) {
    "use strict";
    var finalUrl = baseApiEndpoint + callsign + "/allslots",
        allslots = $.get({
            url: finalUrl,
            context: $("#storedinfo")
        }).success(function (data) {
            if (data.timeslots.length === 0) {
                $(this).html("No stored availability slots<BR> enter one below to get started.");
            } else {
                $(this).html(formatTimeSlots(data));
            }
        });
}

function ajaxPutTimeslot(callsign, timeslot_info) {
    "use strict";
    var finalUrl = baseApiEndpoint + callsign + "/allslots";
    //console.log(timeslot_info.days);
    if (timeslot_info) {
        $.post({
            url: finalUrl,
            dataType: "json",
            contentType: "application/json",
            timeout: 5000,
            data: JSON.stringify({
                "callsign": callsign,
                "days": timeslot_info.days,
                "start_time": timeslot_info.start_time,
                "duration": timeslot_info.duration
            })
        }).success(function (data) {
            $("#slottitle").html("<h3>Timeslot stored</h3>");
            ajaxGetAllAvailability(getUserCallsign());
        }).fail(function (data) {
            console.log(data);
        });
    } else {
        return false;
    }
}


function ajaxDeleteTimeslot(callsign, id) {
    "use strict";
    var finalUrl = baseApiEndpoint + callsign + "/allslots/" + id,
        areYouSure = confirm("Delete slot with id: " + id + "? This change is permanent.");
    if (areYouSure) {
        var deleted = $.ajax({
            url: finalUrl,
            type: "DELETE",
            context: $("#storedinfo"),
            success: function (result) {
                alert("Deleted slot with ID=" + id);
                ajaxGetAllAvailability(callsign);
            }
        });
    }
}

function ajaxGetAvailablePasses(satname, minelev) {
    "use strict";
    var finalUrl = baseApiEndpoint + getUserCallsign() + "/availablepass";
    $.get({
        url: finalUrl,
        data: {
            "satellite": satname,
            "min_elevation": minelev
        }
    }).success(function (data) {
        //console.log(data);
        $("#availablepass").html(formatAvailablePasses(data));
    });
}

function ajaxFetchAllSats() {
    "use strict";
    var finalUrl = "http://localhost:8000/satellites";
    
    $.get({
        "url": finalUrl
    }).success(function (data) {
        $.each(data, function (key, value) {
            $("#satselect").append($("<option>", {value: value})
                                   .text(value));
        });
    });
}

function ajaxGetUserApi(user_info_obj) {
    "use strict";
    var res = $.get({
        url: baseApiEndpoint + user_info_obj.callsign.toLocaleUpperCase(),
        context: $("#userinput"),
        dataType: 'json',
        timeout: 5000 //5 seconds
    })
        .done(function (data) {
            // console.log(data);
            $("#usertitle").html("<h3>" + data.callsign + " User Info</h3>");
            $(this).find('input[id="callsign"]').val(data.callsign);
            $(this).find('input[id="timezone"]').val(data.timezone);
            $(this).find('input[id="street_address"]').hide();
            $(this).find('input[id="lat"]').val(data.lat);
            $(this).find('input[id="long"]').val(data.lon);
            $(this).find('input[id="elevation"]').val(data.elevation);
            $(this).find('button[id="getUserBtn"]').prop('disabled', true);
            $("#slotinfo").show();
            $("#slottitle").html("<h3>Enter another availability</h3>");
            $("#withpass").show();
            ajaxGetAllAvailability(getUserCallsign());
        })
        .fail(function () {
            $("#usertitle").html(user_info_obj.callsign + " not found<br/>Enter a US Callsign or any other identifier AND a street address<br />Click Add/Update to store.");
            $(this).find('input[id="callsign"]').val(user_info_obj.callsign);
            $(this).find('input[id="timezone"]').val('');
            $(this).find('input[id="street_address"]').val('');
            $(this).find('input[id="long"]').val('');
            $(this).find('input[id="lat"]').val('');
            $(this).find('input[id="elevation"]').val('');
            $(this).find('button[id="getUserBtn"]').prop('disabled', true);
        });
}

function ajaxPutUserApi(user_info_obj) {
    "use strict";
    var res = $.post({
        url: baseApiEndpoint + user_info_obj.callsign,
        dataType: "json",
        contentType: "application/json",
        timeout: 5000,
        data: JSON.stringify({
            "callsign": emptyStringToNull($('#userinput input[id="callsign"]').val()),
            "timezone": emptyStringToNull($('#userinput input[id="timezone"]').val()),
            "street_address": emptyStringToNull($('#userinput input[id="street_address"]').val()),
            "lat": emptyStringToNull($('#userinput input[id="lat"]').val()),
            "long": emptyStringToNull($('#userinput input[id="long"]').val()),
            "elevation": emptyStringToNull($('#userinput input[id="elevation"]').val())
        })
    }).success(function (data) {
        ajaxGetUserApi(user_info_obj);
        $(this).find('button[id="addUserBtn"]').prop('disabled', true);
        $(this).find('button[id="getUserBtn"]').prop('disabled', false);
    }).fail(function (data) {
        $(this).find('button[id="addUserBtn"]').prop('disabled', false);
        $(this).find('button[id="getUserBtn"]').prop('disabled', false);
    });
}
    
function createSatOption(satname) {
    "use strict";
    var option = '<option value = "' + satname + '">' + satname + "</option>";
    return option;
}

function toggleUpcomingSlots() {
    "use strict";
    if ($("#storedinfo").is(":hidden")) {
        $("#allheader").html("Click to hide upcoming slots");
    } else {
        $("#allheader").html("Click to show upcoming slots");
    }
    $("#storedinfo").toggle();
}

