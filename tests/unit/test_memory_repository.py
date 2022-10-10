from datetime import date, datetime
from typing import List

import pytest

from music.domainmodel.track import Track


from music.adapters.repository import RepositoryException


def test_repository_test_track_length_using_get_all(in_memory_repo):
    user = in_memory_repo.get_all_tracks()
    assert len(user) == 2000


def test_repository_can_get_tracks_by_range(in_memory_repo):

    tracks = in_memory_repo.get_tracks_by_range([2,3])
    assert len(tracks) == 2


def test_repository_does_not_retrieve_a_non_existent_track(in_memory_repo):
    track = in_memory_repo.get_track(999999)
    assert track is None


def test_repository_can_retrieve_track_count_using_method(in_memory_repo):
    number_of_tracks = in_memory_repo.get_number_of_tracks()

    # Check that the query returned 2000 tracks.
    assert number_of_tracks == 2000


def test_repository_can_add_track(in_memory_repo):
    track = Track(
        1,
        'Nicholas wrote this song'
    )
    in_memory_repo.add_tracks(track)

    assert in_memory_repo.get_track(1) is track


def test_repository_can_add_track_existing_id(in_memory_repo):
    track = Track(
        2,
        'I wrote this song'
    )
    in_memory_repo.add_tracks(track)

    assert in_memory_repo.get_track(2) is track

def test_repository_add_tracks_and_get_size(in_memory_repo):
    track = Track(
        2,
        'Nick is testing'
    )
    in_memory_repo.add_tracks(track)

    track1 = Track(
        3,
        'Paty Kerry'
    )
    in_memory_repo.add_tracks(track1)

    size = in_memory_repo.get_number_of_tracks()

    assert in_memory_repo.get_track(2) is track
    assert in_memory_repo.get_track(3) is track1
    assert size == 2002

