
// add event handler to buttons

function favSong(evt) {

    var songId = $(this).data('songid');
    console.log(songId);
    $.post('add_fav.json', {'song_id': songId}, changeButton)
    $(this).one('click', unfavSong);
}

function changeButton(data) {

    if (data['success']) {
        var songId = data['song_id'];
        $('#song-button-' + songId).toggleClass('favorite');

    } else {
        alert('something went wrong');
    }
}

function unfavSong(evt) {
    var songId = $(this).data('songid');
    console.log(songId);
    $.post('rem_fav.json', {'song_id': songId}, changeButton)
    $(this).one('click', favSong);
}

$('.fav-btn').one('click', favSong);