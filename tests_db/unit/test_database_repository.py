from datetime import date, datetime

import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel.user import User
from music.domainmodel.track import Track, Review
from music.domainmodel.genre import Genre
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('tiger')
    assert user == User('tiger', '123')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_track_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_tracks = repo.get_number_of_tracks()

    # Check that the query returned 177 Articles.
    assert number_of_tracks == 2000

def test_repository_can_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_articles = repo.get_number_of_tracks()

    new_track_id = number_of_articles + 1

    track = Track(new_track_id, 'kia ora')
    repo.add_tracks(track)

    assert repo.get_tracks(new_track_id) == track

def test_repository_can_retrieve_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(2)

    # Check that the Article has the expected title.
    assert track.title == 'Food'

    # Check that the Article is commented as expected.
    #comment_one = [comment for comment in article.comments if comment.comment == 'Oh no, COVID-19 has hit New Zealand'][
       # 0]
    #comment_two = [comment for comment in article.comments if comment.comment == 'Yeah Freddie, bad news'][0]

    #assert comment_one.user.user_name == 'fmercury'
    #assert comment_two.user.user_name == "thorke"

    # Check that the Article is tagged as expected.
    assert track.has_genre(Genre('Noise'))

def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(4)
    assert track is None


def test_repository_can_get_first_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_first_track()
    assert article.title == 'Food'


def test_repository_can_get_last_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article = repo.get_last_track()
    assert article.title == 'yet to be titled'

def test_repository_can_get_articles_by_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    articles = repo.get_tracks_by_id([2, 5, 10])

    assert len(tracks) == 3
    assert tracks[
               0].title == 'Food'
    assert articles[1].title == "Electric Ave"
    assert articles[2].title == 'This World'


def test_repository_does_not_retrieve_track_for_non_existent_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_tracks_by_id([2, 6])

    assert len(tracks) == 1
    assert tracks[
               0].title == 'Food'

def test_repository_returns_an_empty_list_for_non_existent_ids(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_track([0, 12])

    assert len(tracks) == 0

def test_repository_returns_article_ids_for_existing_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track_ids = repo.get_track_ids_for_genre('Noise')

    assert track_ids == [2, 3, 5]

def test_repository_returns_an_empty_list_for_non_existent_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    article_ids = repo.get_track_ids_for_genre('United States')

    assert len(article_ids) == 0


def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genre = Genre('Motoring')
    repo.add_genres(genre)

    assert genre in repo.get_genres()


def test_repository_can_add_a_comment(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('tiger')
    track = repo.get_track(2)
    comment = Review(track, "I like this track!", 5, user)

    repo.add_review(comment)

    assert comment in repo.get_reviews()


def test_repository_does_not_add_a_comment_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    track = repo.get_track(2)
    comment = Review(track, "I like this track!", 5, None)

    with pytest.raises(RepositoryException):
        repo.add_review(comment)


def test_repository_can_retrieve_comments(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews()) == 3


def make_track(new_track_id):
    track = Track(new_track_id, 'boogey man')
    return track

def test_can_retrieve_a_track_and_add_a_comment_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Fetch Article and User.
    track = repo.get_track(5)
    user = repo.get_user('tiger')

    # Create a new Comment, connecting it to the Article and User.
    comment = Review(track, 'This song is ok', 2, user)

    track_fetched = repo.get_track(5)
    user_fetched = repo.get_user('tiger')

    assert comment in track_fetched.reviews
    assert comment in user_fetched.reviews

