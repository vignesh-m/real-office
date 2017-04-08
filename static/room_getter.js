function get_available_rooms() {
    start = $('#start').val();
    end = $('#end').val();
    has_proj = $('#has-projector').is(':checked');
    has_ac= $('#has-ac').is(':checked');
    has_mic= $('#has-mic').is(':checked');
    capacity = $('#capacity').val();
    vs = $('#venue-select');
    params = $.param({
        'start': start,
        end: end,
        has_proj: has_proj,
        has_ac: has_ac,
        has_mic: has_mic,
        capacity: capacity
    });
    $.get({
        url: 'http://localhost:8000/meeting/available_rooms/?'+params,
        success: function (data) {
            data = JSON.parse(data);
            vs.empty();
            l = data.suggested;
            sugg = $('<optgroup label="Suggested">')
            for (var i = 0; i < l.length; i++){
                var room = l[i];
                var opt = $("<option>")
                opt.attr('value', room.id).text(room.name);
                opt.appendTo(sugg);
            }
            l = data.rest;
            rest = $('<optgroup label="Other Rooms">')
            for (var i = 0; i < l.length; i++) {
                var room = l[i];
                var opt = $("<option>")
                opt.attr('value', room.id).text(room.name);
                opt.appendTo(rest);
            }
            sugg.appendTo(vs);
            rest.appendTo(vs);
            
        }
    });
}

$(document).ready(function () {
    get_available_rooms();
    $('#start').on('change', get_available_rooms);
    $('#end').on('change', get_available_rooms);
    $('#has-projector').on('change', get_available_rooms);
    $('#has-ac').on('change', get_available_rooms);
    $('#has-mic').on('change', get_available_rooms);
    $('#capacity').on('change', get_available_rooms);
});