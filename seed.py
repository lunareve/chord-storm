"""Utility file to seed favorites database from SongLens data in seed_data/"""

from sqlalchemy import func

from model import User, Artist, Song, Chord, Chord_List, Favorite

from model import connect_to_db, db
from server import app

import guitar_party_api as gp


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    email=email,
                    password=password)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_songs():
    """Load songs from u.item into database."""
    print "Songs"

    Song.query.delete()

        song = Song(song_id=song_id,
                      title=title,
                      released_at=released_at,
                      imdb_url=imdb_url)

        db.session.add(song)

    db.session.commit()


def load_favorites():
    """Load favorites from u.data into database."""
    print "Favorites"

    Favorite.query.delete()

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        user_id, song_id, score, timestamp = row.split("\t")

        favorite = Favorite(user_id=user_id,
                        song_id=song_id)

        db.session.add(favorite)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
    load_songs()
    # load_favorites()
    # set_val_user_id()
