import abc
from typing import List
from datetime import date

from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.user import User

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def get_track(self, id:int)-> Track:
        """Gets tracks by id"""
        raise NotImplementedError

        
    @abc.abstractmethod
    def add_tracks(self, track: Track):
        """ Adds tracks """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genres(self, genre: Genre):
        """Adds Genres"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_albums(self, album: Album):
        """Adds Albums"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_artists(self, album: Artist):
        """Adds Artists"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_tracks(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_tracks(self):
        """Gets all tracks as list"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_range(self, range):
        """Gets track within a certain range"""
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_reviews(self):
    #     """ Returns the Comments stored in the repository. """
    #     raise NotImplementedError

