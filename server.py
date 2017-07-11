"""song favorites."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Artist, ArtistSong, Song, Chord, SongChord, Favorite

import guitar_party_api as gp

from chord_helper import find_songs_with_n_chords, find_songs_chords, extract_song_info, most_chord_combos, shortest_chord_combos, search_by_title, search_by_artist


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    a = jsonify([1, 3])

    songs3 = find_songs_with_n_chords(3)
    songs_list = extract_song_info(songs3)

    return render_template('homepage.html',
                           songs_list=songs_list)


@app.route("/users/<user_id>", methods=["GET"])
def user_details(user_id):
    """Shows a user's details."""

    user = User.query.get(user_id)
    user_songs = []

    try:
        for favorite in user.favorites:
            user_songs.append(favorite.songs)

    except AttributeError:
        print "no favorites"

    songs_list = extract_song_info(user_songs)

    return render_template("user_details.html",
                           user=user,
                           songs_list=songs_list)


@app.route("/register", methods=["POST"])
def register_process():
    """Registers new user, checks for existing user"""
    # Check for existing user
    email = request.form.get("email")
    password = request.form.get("password")
    verify = request.form.get("verify")

    if User.query.filter(User.email == email).first():
        flash('Email already exists, please login.')

    elif password != verify:
        flash('Passwords do not match, please try again.')

    else:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered new user, please login.')

    return redirect("/login")


@app.route("/login", methods=["GET"])
def login_form():
    """Allows the user to enter login or registration info."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def log_user_in():
    """Logs in the user if details match."""
    email = request.form.get("email")
    password = request.form.get("password")
    # Check db for email and pw

    user = User.query.filter(User.email == email).first()

    if user and user.password == password:
        session['user'] = user.user_id
        flash('Logged in')
        return redirect("/users/{}".format(user.user_id))

    else:
        flash('Incorrect email/password')
        return redirect("/login")


@app.route("/logout")
def log_user_out():
    """Logs out the user."""
    # session.clear()
    session.pop('user')
    flash('Logged out')

    return redirect("/")


@app.route("/songs", methods=["GET"])
def song_search():
    """Searches for songs based on chords."""

    chord_string = request.args.get("chord_string")
    title_string = request.args.get("title_string")
    artist_string = request.args.get("artist_string")

    if chord_string:
        songs = find_songs_chords(chord_string)

    elif title_string:
        songs = search_by_title(title_string)

    elif artist_string:
        songs = search_by_artist(artist_string)

    songs_list = extract_song_info(songs)
    popular = most_chord_combos()
    shortest = shortest_chord_combos()

    return render_template("song_chords.html",
                           songs_list=songs_list,
                           popular=popular,
                           shortest=shortest)


@app.route("/songs/<song_id>", methods=["GET"])
def song_details(song_id):
    """Shows a song's details."""

    song = Song.query.get(song_id)

    return render_template("song_details.html",
                           song=song)


@app.route("/songs/add_fav.json", methods=['POST'])
def add_favorite():
    """Add favorited song to db."""

    song_id = int(request.form.get('song_id'))
    current_user = session['user']

    # add data to db that song is a favorite
    new_favorite = Favorite(song_id=song_id, user_id=current_user)
    db.session.add(new_favorite)
    db.session.commit()
    print "adding song_id {} as favorite in db".format(song_id)

    return jsonify({
        'success': True,
        'song_id': song_id
        })


# @app.route("/songs/<song_id>", methods=["POST"])
# def rate_song(song_id):
#     """Allows user to add or update favorite for a song."""

#     song_score = request.form.get("score")
#     current_song = song_id
#     current_user = session['user']

#     favorite_exist = db.session.query(favorite).filter(favorite.user_id==current_user,
#                                                        favorite.song_id==current_song).first()

#     #if user_id exists, update score column in favorites table
#     if favorite_exist:
#         favorite_exist.score = song_score
#         db.session.commit()
#     else:
#         new_favorite = favorite(song_id=current_song, user_id=current_user, score=song_score)
#         db.session.add(new_favorite)
#         db.session.commit()

#     return redirect("/songs/{}".format(current_song))



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
