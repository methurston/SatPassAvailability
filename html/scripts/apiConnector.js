baseApiEndpoint = "http://localhost:8000/user/"

function old_getUserForm() {
    userform = document.forms.namedItem("userinput");
    console.log(userform.elements)
    userinfo = {
        "callsign": userform.elements["callsign"].value,
        "timezone": userform.elements["timezone"].value,
        "street_address": userform.elements["street_address"].value,
        "lat": userform.elements["lat"].value,
        "lon": userform.elements["lon"].value,
        "elev": userform.elements["elev"].value
    };
    console.log(userinfo.callsign);
    output = document.getElementById("storedinfo");
    output.innerHTML = userinfo.callsign;
    return userinfo;
};

function getUserForm() {
     //var form_input = $("#userinput");
     userinfo = {
         "callsign": $('#userinput input[id="callsign"]').val(),
         "timezone": $('#userinput input[id="timezone"]').val(),
         "street_address": $('#userinput input[id="street_address"]').val(),
         "lat": $('#userinput input[id="lat"]').val(),
         "lon": $('#userinput input[id="lon"]').val(),
         "elev": $('#userinput input[id="elev"]').val()
     }
     console.log(userinfo)

     $('#storedinfo').html(userinfo.callsign + "<br>" + userinfo.timezone)
     return userinfo
}

function getUserApi(user_info_obj){
    resp = $.ajax({
        url: baseApiEndpoint + user_info_obj.callsign,

    })
}