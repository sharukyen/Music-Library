from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel import track, album, artist, genre, playlist, review, user

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('users_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', String(255), unique=True, nullable=False),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)


tracks_table = Table(
    'tracks', metadata,
    Column('tracks_id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('duration', String(1024), nullable=True),
    Column('Url', String(255), nullable=True),
    Column('artist_id', ForeignKey('artists.artists_id')),
    Column('genre_id', ForeignKey('genres.genres_id')),
    Column('album_id', ForeignKey('albums.albums_id'))
)

genres_table = Table(
    'genres', metadata,
    Column('genres_id', Integer, primary_key=True),
    Column('genre_name', String(64), nullable=True)
)

track_genres_table = Table(
    'track_genres', metadata,
    Column('track_genres_id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.tracks_id')),
    Column('genres_id', ForeignKey('genres.genres_id'))
)

album_table = Table(
    'albums', metadata,
    Column('albums_id', Integer, primary_key=True),
    Column('album_name', String(255), nullable=True)
)

artist_table = Table(
    'artists', metadata,
    Column('artists_id', Integer, primary_key=True),
    Column('artist_name', String(255), nullable=False)
)



def map_model_to_tables():
    mapper(user.User, users_table, properties={
        '_User__users_id': users_table.c.user_id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
    })
    mapper(track.Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.tracks_id,
        '_Track__title': tracks_table.c.title,
        '_Track__track_duration': tracks_table.c.duration,
        '_Track__track_url': tracks_table.c.Url,
        '_Track__artist': relationship(artist.Artist, backref='_Artist__track'),  #remove backref if error
        '_Track__album': relationship(album.Album, backref='_Album__track'),
        '_Track__genres': relationship(genre.Genre, secondary=track_genres_table)
    })
    mapper(genre.Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
        '_Genre__genre_id': genres_table.c.genres_id
    })
    mapper(album.Album, album_table, properties={
        '_Albums__id': album_table.c.albums_id,
        '_Album__name': album_table.c.album_name
    })
    mapper(artist.Artist, artist_table, properties={
        '_Artists__id': artist_table.c.artists_id,
        '_Artist__full_name': artist_table.c.artist_name
    })

