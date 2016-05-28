function validateStart() {
    var start = $('#slotinfo input[id="start_time"]').val();
    if (!start.match(/^([01]\d|2[0-3]):?([0-5]\d)$/)) {
        $('#slotinput div[id=timeerror]').html("Time must in 24 hour format (HH:MM)");
        $('#slotinput div[id=timeerror]').show();
        $('#stotinput button[id="addSlotBtn"]').prop('disabled', true);
    } else {
        $('#stotinput button[id="addSlotBtn"]').prop('disabled', false);
        $('#slotinput div[id=timeerror]').hide();
    }
}

function validateDuration() {
    var duration = $('#slotinfo input[id="duration"]').val();
    if (!Number(duration)) {
        $('#slotinput div[id=durationerror]').html("Duration must be a number of seconds (3600=1 hour)");
        $('#slotinput div[id=durationerror]').show();
        $('#slotinput button[id="addSlotBtn"]').prop('disabled', true);
    } else {
        $('#slotinput button[id="addSlotBtn"]').prop('disabled', false);
        $('#slotinput div[id=durationerror]').hide();
    }
}