import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from music.domainmodel.track import Track, Review
from music.domainmodel.user import User
from music.domainmodel.album import Album
from music.domainmodel.genre import Genre
from music.domainmodel.artist import Artist
from music.tracks.services import add_review
import music.adapters.repository as repo
article_date = datetime.date(2020, 2, 28)

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (track_id, title, duration, Url, artist_id, album_id) VALUES '
        '(1109,'
        '"hocuspooisdf",'
        '189,'
        '"https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus",'
        '1234,'
        '3453425'
    )
    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genres_id, genre_name) VALUES '
        '(7,'
        '"anime")'
    )
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track_genre_associations(empty_session, track_key, genre_keys):
    stmt = 'INSERT INTO track_genres (track_id, genres_id) VALUES (:track_id, :genres_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'track_id': track_key, 'genres_id': genre_key})


def insert_commented_article(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session)

    empty_session.execute(
        'INSERT INTO reviews (review_text, rating, track_id, user_id) VALUES '
        '("Review 1", 5, :track_id, user_id),'
        '("Review 1", 5, :track_id, user_id)',
        {'track_id': track_key, 'user_id': user_key}
    )

    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]


def make_track():
    track = Track(9,
                  "harry potter"
                  )
    return track


def make_user():
    user = User("Andrew", "111")
    return user


def make_genre():
    genre = Genre("dragon")
    return genre


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("Andrew", "111")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_track(empty_session):
    track_key = insert_track(empty_session)
    expected_track = make_track()
    fetched_track = empty_session.query(Track).one()

    assert expected_track == fetched_track
    assert track_key == fetched_track.id


def test_loading_of_genred_track(empty_session):
    track_key = insert_track(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_track_genre_associations(empty_session, track_key, genre_keys)

    track = empty_session.query(Track).get(track_key)
    genres = [empty_session.query(Genre).get(key) for key in genre_keys]

    for genre in genres:
        assert track.is_tagged_by(genre)
        assert genre.is_applied_to(track)


def test_loading_of_commented_track(empty_session):
    insert_commented_article(empty_session)

    rows = empty_session.query(Track).all()
    track = rows[0]

    for review in track.reviews:
        assert review.track is track


def test_saving_of_review(empty_session):
    article_key = insert_track(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Track).all()
    track = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    review_text = "Some comment text."
    review = add_review(user, track, review_text, 5, AbstractRepository )

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, article_id, comment FROM reviews'))

    assert rows == [(user_key, article_key, review_text)]


def test_saving_of_track(empty_session):
    track = make_track()
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, duration, Url, artist_id, album_id FROM tracks'))

    assert rows == [("dragonball",
                     153,
                     "https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus",
                     4300,
                     2700
                     )]




def test_save_commented_article(empty_session):
    # Create Article User objects.
    article = make_article()
    user = make_user()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    comment_text = "Some comment text."
    comment = make_comment(comment_text, user, article)

    # Save the new Article.
    empty_session.add(article)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT id FROM articles'))
    article_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the comments table has a new record that links to the articles and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, article_id, comment FROM comments'))
    assert rows == [(user_key, article_key, comment_text)]