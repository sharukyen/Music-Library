import csv
from multiprocessing.managers import DictProxy
from pathlib import Path
from datetime import date, datetime
from typing import List
from werkzeug.security import generate_password_hash

from music.adapters.csvdatareader import TrackCSVReader

from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.domainmodel.review import Review
from music.domainmodel.user import User

class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__track = list()
        self.__tracks_index =dict()
        self.__genre = list()
        self.__album = list()
        self.__artist = list()
    


    def add_tracks(self, track: Track):
        self.__track.append(track)
        self.__tracks_index[track.track_id] = track

    def add_genres(self, genre: Genre):
        self.__genre.append(genre)
    
    def add_albums(self, album: Album):
        self.__album.append(album)

    def add_artists(self, artist: Artist):
        self.__artist.append(artist)


    def get_track(self, id: int) -> Track:
        track = None
        try:
            track = self.__tracks_index[id]
        except KeyError:
            pass  
        return track

    def get_all_tracks(self):
        return self.__track

    def get_number_of_tracks(self):
        return len(self.__track)

    def get_tracks_by_range(self, range):
        existing_ids = [id for id in range if id in self.__tracks_index]
        tracks = [self.__tracks_index[id] for id in existing_ids]
        return tracks

#def load_repo(repo: MemoryRepository):



def populate(data_path: Path, repo: MemoryRepository):
    load = TrackCSVReader(str(data_path )+ "/raw_albums_excerpt.csv", str(data_path) + "/raw_tracks_excerpt.csv")

    load.read_csv_files()

    for track in load.dataset_of_tracks:
        repo.add_tracks(track)

    for album in load.dataset_of_albums:
        repo.add_albums(album)

    for genre in load.dataset_of_genres:
        repo.add_genres(genre)

    for artist in load.dataset_of_artists:
        repo.add_artists(artist)
