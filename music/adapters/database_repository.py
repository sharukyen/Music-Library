from datetime import date
from typing import List
from pathlib import Path

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.domainmodel.track import Track
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.genre import Genre
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import TrackCSVReader


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    '''Methods'''

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_tracks(self, track: Track):
        with self._session_cm as scm:
            # scm.session.add(track) use merge instead of add
            scm.session.merge(track)
            scm.commit()

    def add_albums(self, album: Album):
        with self._session_cm as scm:
            # scm.session.add(track) use merge instead of add
            scm.session.merge(album)
            scm.commit()

    def add_artists(self, artist: Artist):
        with self._session_cm as scm:
            # scm.session.add(track) use merge instead of add
            scm.session.merge(artist)
            scm.commit()

    def get_track(self, id: int, ) -> Track:
        track = None
        try:
            track = self._session_cm.session.query(Track).filter(Track.track_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return track

    def get_all_tracks(self):
        track = self._session_cm.session.query(Track).all()
        return track

    def get_tracks_by_range(self, range):
        existing_ids = [id for id in range if id in self._session_cm.session.query(Track)]
        tracks = [self._session_cm.session.query(Track).filter(Track.track_id == id) for id in existing_ids]
        return tracks

    def get_number_of_tracks(self):
        number_of_articles = self._session_cm.session.query(Track).count()
        return number_of_articles

    def get_first_track(self):
        tracks = self._session_cm.session.query(Track).first()
        return tracks

    def get_last_track(self):
        tracks = self._session_cm.session.query(Track).order_by(desc(Track.track_id)).first()
        return tracks

    def get_tracks_by_id(self, id_list: List[int]):
        tracks = self._session_cm.session.query(Track).filter(Track.track_id.in_(id_list)).all()
        return tracks

    def get_track_ids_for_genre(self, genre_name: str):
        track_ids = []

        # Use native SQL to retrieve article ids, since there is no mapped class for the article_tags table.
        row = self._session_cm.session.execute('SELECT id FROM genres WHERE genre_name = :genre_name',
                                               {'genre_name': genre_name}).fetchone()

        if row is None:
            # No tag with the name tag_name - create an empty list.
            track_ids = list()
        else:
            genre_id = row[0]
            # Retrieve article ids of articles associated with the tag.
            track_ids = self._session_cm.session.execute(
                'SELECT track_id FROM track_genres WHERE genre_id = :genre_id ORDER BY track_ids ASC',
                {'genre_id': genre_id}
            ).fetchall()
            track_ids = [id[0] for id in track_ids]

        return track_ids

    def get_genres(self) -> List[Genre]:
        tags = self._session_cm.session.query(Genre).all()
        return tags

    def add_genres(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()


def populate(data_path: Path, repo: SqlAlchemyRepository, database_made: bool):
    load = TrackCSVReader(str(data_path) + "/raw_albums_excerpt.csv", str(data_path) + "/raw_tracks_excerpt.csv")

    load.read_csv_files()

    for track in load.dataset_of_tracks:
        repo.add_tracks(track)

    for album in load.dataset_of_albums:
        repo.add_albums(album)

    for genre in load.dataset_of_genres:
        repo.add_genres(genre)

    for artist in load.dataset_of_artists:
        repo.add_artists(artist)

