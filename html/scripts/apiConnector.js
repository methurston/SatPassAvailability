baseApiEndpoint = "http://localhost:8000/user/"

function emptyStringToNull(input_string) {
    if (input_string === "") {
        output_string = null;
        }
    else {
        output_string = input_string
        }
    return output_string;
    }

function getUserForm() {
     //var form_input = $("#userinput");
     userinfo = {
         "callsign": $('#userinput input[id="callsign"]').val(),
         "timezone": $('#userinput input[id="timezone"]').val(),
         "street_address": $('#userinput input[id="street_address"]').val(),
         "lat": $('#userinput input[id="lat"]').val(),
         "long": $('#userinput input[id="long"]').val(),
         "elevation": $('#userinput input[id="elevation"]').val()
     }
     //console.log('street address: ' + userinfo.street_address + '***')

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
            $( this ).find('input[id="long"]').val(data.lon);
            $( this ).find('input[id="elevation"]').val(data.elevation);
            $( this ).find('button[id="getUserBtn"]').prop('disabled', true);
        })
        .fail(function(){
            $("#usertitle").html(user_info_obj.callsign + " not found<br/>Enter a US Callsign and Timezone<br />Click Add/Update to store.")
            $( this ).find('input[id="callsign"]').val(user_info_obj.callsign);
            $( this ).find('input[id="timezone"]').val('');
            $( this ).find('input[id="street_address"]').val('');
            $( this ).find('input[id="long"]').val('');
            $( this ).find('input[id="lat"]').val('');
            $( this ).find('input[id="elevation"]').val('');
            $( this ).find('button[id="getUserBtn"]').prop('disabled', true);
        })
}

function ajaxPutUserApi(user_info_obj){
    if (!$('#userinput input[id="timezone"]').val()) {
            $('#usertitle').html('Time Zone is mandatory for submission');
        }
    else {
        res = $.post({
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
            }).success(function( data ) {
                ajaxGetUserApi(user_info_obj)
                $( this ).find('button[id="addUserBtn"]').prop('disabled', true);
                $( this ).find('button[id="getUserBtn"]').prop('disabled', false);
            }).fail(function (data){
                console.log(data)
                $( this ).find('button[id="addUserBtn"]').prop('disabled', false);
                $( this ).find('button[id="getUserBtn"]').prop('disabled', false);
            })
        }
    }