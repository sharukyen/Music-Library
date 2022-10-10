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
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', String(255), unique=True, nullable=False),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('track_id', ForeignKey('tracks.id')),
    Column('reviews', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

tracks_table = Table(
    'tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('date', Date, nullable=False),
    Column('title', String(255), nullable=False),
    Column('duration', String(1024), nullable=False),
    Column('Url', String(255), nullable=False),
    Column('artist_id', ForeignKey('artist.id')),
    Column('album_id', ForeignKey('album.id'))
)

genres_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String(64), nullable=False)
)

track_genres_table = Table(
    'track_tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.id')),
    Column('genres_id', ForeignKey('genres.id'))
)

album_table = Table(
    'album', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('album_id', Integer, nullable=False),
    Column('album_name', String(255), nullable=False)
)

artist_table = Table(
    'artist', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('artist_id', Integer, nullable=False),
    Column('artist_name', String(255), nullable=False)
)



def map_model_to_tables():
    mapper(user.User, users_table, properties={
        '_User__user_id': users_table.c.user_id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(review.Review, backref='_Reviews__user')
    })
    mapper(review.Review, reviews_table, properties={
        '_Review__review': reviews_table.c.comment,
        '_Review__timestamp': reviews_table.c.timestamp
    })
    mapper(track.Track, tracks_table, properties={
        '_Track__id': tracks_table.c.id,
        '_Track__date': tracks_table.c.date,
        '_Track__title': tracks_table.c.title,
        '_Track__url': tracks_table.c.url,
        '_Track__hyperlink': tracks_table.c.hyperlink,
        '_Track__reviews': relationship(review.Review, backref='_Review__track'),
        '_Track__genres': relationship(genre.Genre, secondary=track_genres_table,
                                       back_populates='_Genre__tagged_tracks'),
        '_Track__artist': relationship(artist.Artist, backref='_Artist__track'),  #remove backref if error
        '_Track__album': relationship(album.Album, backref='_Album__track')
    })
    mapper(genre.Genre, genres_table, properties={
        '_Tag__tag_name': genres_table.c.tag_name,
        '_Tag__tagged_articles': relationship(
            track.Track,
            secondary=track_genres_table,
            back_populates="_Track__genres"
        )
    })
    mapper(album.Album, album_table, properties={
        '_Album__id': album_table.c.id,
        '_Album__name': album_table.c.album_name
    })
    mapper(artist.Artist, artist_table, properties={
        '_Artist__id': artist_table.c.id,
        '_Artist__full_name': artist_table.c.artist_name
    })