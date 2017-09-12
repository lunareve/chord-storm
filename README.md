# [Chord Storm](http://jellymorph.ddns.net:5000/)

One of my hobbies is playing ukulele, so I decided to create a site to help beginner guitar and ukulele players find songs at their skill levels. Users can search for songs by chords, song title, and artist, but I wanted to focus more on finding songs by chords because when I was starting out, I wasn’t familiar with that many chords and I couldn’t think of good songs to play. If the search doesn’t return any results, the page makes some suggestions on common chords, or less complicated songs with fewer chords. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Built in a Vagrant environment.

### Installing

Mac OS specific instructions

Create a new virtual environment and install prerequisites from requirements.txt.

```
$ virtualenv/env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

Reconstitute database

```
$ createdb chordfinder
$ psql chordfinder < seed_data/chordfinder.sql
```

If you’d like to seed the database with your choice of songs, get an API key from [GuitarParty](http://www.guitarparty.com/developers/). Create a secrets.sh file to export the key to your environment.

This would also be a good time to get a YouTube API key and add it to the secrets file in the same manner.

```
export GUITAR_PARTY_API_KEY='secretkeyhere'
```

Update ```seed_data/u.item``` with desired artists and songs.
Source the secrets file and run seed.py to seed the database.

```
$ source secrets.sh
$ python seed.py
```

Start the server and access in the browser from ```localhost:5000```.

```
$ python server.py
```

## Built With

* Guitar Party API - song data
* Flask - The web framework used
* Jinja - HTML templating
* PostgreSQL - Database
* SQLalchemy - ORM
* YouTube API - video search and embedding
* Bcrypt  - password salting and hashing

## Authors

* [Connie Chow](https://github.com/lunareve) - Initial work

## Acknowledgments

* [Guitar Party API](http://www.guitarparty.com/developers/)
* YouTube API
* [PurpleBooth Readme template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
