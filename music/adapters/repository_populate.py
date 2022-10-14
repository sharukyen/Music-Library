from pathlib import Path

from music.adapters import repository
from music.adapters.csvdatareader import TrackCSVReader


def populate(data_path: Path, repo: repository, database_mode : bool):
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