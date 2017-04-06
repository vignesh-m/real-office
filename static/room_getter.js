function get_available_rooms() {
    start = $('#start').val();
    end = $('#end').val();
    vs = $('#venue-select');
    $.get({
        url: 'http://localhost:8000/meeting/available_rooms/?start=' + start
            + '&end='+end,
        success: function (data) {
            data = JSON.parse(data);
            console.log(data, data.length);
            vs.empty();
            l = data.suggested;
            sugg = $('<optgroup label="Suggested">')
            for (var i = 0; i < l.length; i++){
                var room = l[i];
                console.log(room);
                var opt = $("<option>")
                opt.attr('value', room.id).text(room.name);
                opt.appendTo(sugg);
            }
            l = data.rest;
            rest = $('<optgroup label="Other Rooms">')
            for (var i = 0; i < l.length; i++) {
                var room = l[i];
                console.log(room);
                var opt = $("<option>")
                opt.attr('value', room.id).text(room.name);
                opt.appendTo(rest);
            }
            sugg.appendTo(vs);
            rest.appendTo(vs);
            
        }
    });
}