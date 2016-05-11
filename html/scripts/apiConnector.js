baseApiEndpoint = "http://localhost:8000/user/"

function getUserForm() {
     //var form_input = $("#userinput");
     userinfo = {
         "callsign": $('#userinput input[id="callsign"]').val(),
         "timezone": $('#userinput input[id="timezone"]').val(),
         "street_address": $('#userinput input[id="street_address"]').val(),
         "lat": $('#userinput input[id="lat"]').val(),
         "lon": $('#userinput input[id="lon"]').val(),
         "elevation": $('#userinput input[id="elevation"]').val()
     }

     $('#storedinfo').html(userinfo.callsign + "<br>" + userinfo.timezone)
     return userinfo
}


function ajaxGetUserApi(user_info_obj){
    res = $.get({
            url: baseApiEndpoint + user_info_obj.callsign,
            type: "GET",
            context: $("#userinput"),
            dataType: 'json',
            timeout: 2000 //2 seconds
        })
        .done(function (data){
            console.log(data);
            $("#usertitle").html("<h3>" + data.callsign + " User Info</h3>")
            $( this ).find('input[id="callsign"]').val(data.callsign);
            $( this ).find('input[id="timezone"]').val(data.timezone);
            $( this ).find('input[id="street_address"]').val("Not stored");
            $( this ).find('input[id="lat"]').val(data.lat);
            $( this ).find('input[id="lon"]').val(data.lon);
            $( this ).find('input[id="elevation"]').val(data.elevation);
        })
        .fail(function(){
            $("#usertitle").html(user_info_obj.callsign + " not found<br/>Fill in the fields below to store.")
            $( this ).find('input[id="callsign"]').val(user_info_obj.callsign);
        })
}