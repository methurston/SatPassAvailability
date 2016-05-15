var baseApiEndpoint = "http://localhost:8000/user/";


function emptyStringToNull(input_string) {
    if (input_string === "") {
        output_string = null;
    } else {
        output_string = input_string;
    }
    return output_string;
}

function getUserCallsign () {
    sign = $("#userinput input[id='callsign']").val();
    return sign
} 
function getUserForm() {
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


function ajaxGetUserApi(user_info_obj) {
    var res = $.get({
        url: baseApiEndpoint + user_info_obj.callsign.toLocaleUpperCase(),
        context: $("#userinput"),
        dataType: 'json',
        timeout: 2000 //2 seconds
    })
        .done(function (data) {
            console.log(data);
            $("#usertitle").html("<h3>" + data.callsign + " User Info</h3>");
            $(this).find('input[id="callsign"]').val(data.callsign);
            $(this).find('input[id="timezone"]').val(data.timezone);
            $(this).find('input[id="street_address"]').val("Not stored");
            $(this).find('input[id="lat"]').val(data.lat);
            $(this).find('input[id="long"]').val(data.lon);
            $(this).find('input[id="elevation"]').val(data.elevation);
            $(this).find('button[id="getUserBtn"]').prop('disabled', true);
            $("#slotinfo").show();
            $("#slottitle").html("<h3>Enter another availability</h3>");
            ajaxGetAllAvailability(getUserCallsign());
        })
        .fail(function () {
            $("#usertitle").html(user_info_obj.callsign + " not found<br/>Enter a US Callsign and Timezone<br />Click Add/Update to store.");
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
    if (!$('#userinput input[id="timezone"]').val()) {
            $('#usertitle').html('Time Zone is mandatory for submission');
    } else {
        var res = $.post({
            url: baseApiEndpoint + user_info_obj.callsign,
            dataType: "json",
            contentType: "application/json",
            timeout: 2000,
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
            console.log(data);
            $(this).find('button[id="addUserBtn"]').prop('disabled', false);
            $(this).find('button[id="getUserBtn"]').prop('disabled', false);
        });
    }
}


function getTimeslotForm() {
    available_days = new Array()
    $.each($('#slotinfo input[name="days"]:checked'), function () {
        available_days.push($(this).val());
    });
    var timeinfo = {
        "days": available_days.toString(),
        "start_time": $('#slotinfo input[id="start_time"]').val(),
        "duration": $('#slotinfo input[id="duration"]').val()
    };
    return timeinfo;
}

function ajaxPutTimeslot(callsign, timeslot_info) {
    finalUrl = baseApiEndpoint + callsign + "/allslots"
    
    $.post({
        url: finalUrl,
        dataType: "json",
        contentType: "application/json",
        timeout: 2000,
        data: JSON.stringify({
            "callsign": callsign,
            "days": timeslot_info.days,
            "start_time": timeslot_info.start_time,
            "duration": timeslot_info.duration})
        }).success(function (data){
            $("#slottitle").html("<h3>Timeslot stored</h3>")
            ajaxGetAllAvailability(getUserCallsign());
        }).fail (function (data){
            console.log(data);
        })
    }

function ajaxGetAllAvailability(callsign) {
    finalUrl = baseApiEndpoint + callsign + "/allslots";
    var allslots = $.get({
        url: finalUrl,
        context: $("#storedinfo")
    }).success( function(data){
        if (data.timeslots.length === 0) {
            $(this).html("No stored availability slots<BR> enter one below to get started.")
        } else {
            $(this).html(formatTimeSlots(data))
        }
    })
}

function ajaxDeleteTimeslot(callsign, id) {
    finalUrl = baseApiEndpoint + callsign + "/allslots/" + id;
    areYouSure = confirm("Delete slot with id: " + id +"? This change is permanent." )
    if (areYouSure) {
        var deleted = $.ajax({
            url: finalUrl,
            type: "DELETE",
            success: function(result) {
                alert("Deleted slot with ID=" + id)
            }
        })
        }
}
function formatSlot(user_timeslot) {
    var slothtml = "<tr><td>" + user_timeslot.id + "</td>"
    slothtml += "<td>" + user_timeslot.date + "</td>"
    slothtml += "<td>" + (user_timeslot.duration / 3600).toFixed(2) + "</td>"
    slothtml += "<td>DELETE</td></tr>"

    return slothtml
}

function formatTimeSlots(user_timeslots) {
    var allslots = user_timeslots.timeslots;
    var slotshtml = '<table class="table table-striped">';
    slotshtml += "<th>ID</th><th>Starting date/time</th><th>Duration</th><th>Delete</th>";
    for (index=0; index < allslots.length; ++index) {
        slotshtml += formatSlot(allslots[index]);
    }
    slotshtml += "</table>";
    return slotshtml
}