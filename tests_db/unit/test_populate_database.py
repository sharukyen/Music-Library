from sqlalchemy import select, inspect

from music.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['tracks', 'genres', 'track_genres', 'albums', 'artists', 'reviews', 'users']

def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['genre_name'])

        nr_genres = len(all_genre_names)
        assert nr_genres == 20

        assert all_genre_names[0] == ('Hip-Hop')

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['tiger']

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['id'], row['review_text'], row['rating'], row['track_id'], row['user_id']))

        nr_reviews = len(all_reviews)
        assert nr_reviews == 20

        assert all_reviews[0] == (1, 'test', 5, 2, 1)

def test_database_populate_select_all_tracks(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_tracks_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_tracks_table]])
        result = connection.execute(select_statement)

        all_tracks = []
        for row in result:
            all_tracks.append((row['tracks_id'], row['title']))

        nr_tracks = len(all_tracks)
        assert nr_tracks == 20

        assert all_tracks[0] == (2, 'Food')

def test_database_populate_select_all_artists(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_artists_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_artists_table]])
        result = connection.execute(select_statement)

        all_artists = []
        for row in result:
            all_tracks.append((row['artists_id'], row['artist_name']))

        nr_artists = len(all_artists)
        assert nr_artists == 20

        assert all_artists[0] ==(3966, 'AWOL')


def test_database_populate_select_all_albums(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_albums_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_albums_table]])
        result = connection.execute(select_statement)

        all_albums = []
        for row in result:
            all_albums.append((row['albums_id'], row['album_name']))

        nr_albums = len(all_albums)
        assert nr_albums == 20

        assert all_albums[0] ==(2393, 'AWOL - A Way Of Life')

