baseApiEndpoint = "/user/"

function getUserForm() {
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