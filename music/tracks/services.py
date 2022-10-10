from pathlib import Path
from datetime import date, datetime
from typing import List, Iterable


from music.domainmodel.track import Track
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.adapters.repository import AbstractRepository
from music.adapters.repository import repo_instance

class NonExistentTrackException(Exception):
    pass


class UnknownUserException(Exception):
    pass

def get_track(track_id: int,repo: AbstractRepository ):
    track = repo.get_track(track_id)

    if track is None:
        raise NonExistentTrackException

    return track_to_dict(track)


def get_all_tracks(repo: AbstractRepository):
    tracks = repo.get_all_tracks()
    return tracks

def get_number_of_tracks(repo:AbstractRepository):
    tracks = repo.get_number_of_tracks()
    return tracks

def get_tracks_by_range(range, repo: AbstractRepository):
    tracks = repo.get_tracks_by_range(range)
    track_var = tracks_to_dict(tracks)
    return track_var



def track_to_dict(track: Track):
    track_dict = {
        'track_id': track.track_id,
        'track_title': track.title,
        'track_url': track.track_url,
        'track_duration': track.track_duration,
    }
    return track_dict


def tracks_to_dict(tracks: Iterable[Track]):
    return [track_to_dict(track) for track in tracks]
