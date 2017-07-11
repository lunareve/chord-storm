
// add event handler to buttons
$('.fav-btn').on('click', favSong);

function favSong(evt) {

    var songId = $(this).data('songid');
    console.log(songId);
    $.post('add_fav.json', {'song_id': songId}, changeButton)
}

function changeButton(data) {

    if (data['success']) {
        var songId = data['song_id'];

        $('#song-button-' + songId).addClass('favorite');
        $('.fav-btn').attr("disabled", "disabled");
    } else {
        alert('something went wrong');
    }

}