import abc
from typing import List
from datetime import date, datetime

from music.domainmodel.track import Track, Review
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
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

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name: str) -> User:
        """ Returns the User named user_name from the repository.

        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        # if review.user is None or review not in review.user.comments:
        #     raise RepositoryException('Comment not correctly attached to a User')
        if review.track is None:
            raise RepositoryException('Track not correctly attached to Review')


    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError