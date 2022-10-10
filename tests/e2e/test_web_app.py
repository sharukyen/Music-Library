import pytest

from flask import session

def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'COMPSCI235 Assignment 2 - Music Library' in response.data


def test_tracks_with_on_page(client):
    # Check that we can retrieve the track page.
    response = client.get('/list_track?cursor=160')
    assert response.status_code == 200

    # Check that the first track and the last track on the requested page are included on the page.
    # First track
    assert b'348' in response.data
    assert b'Excretia' in response.data
    assert b'165' in response.data
    assert b'http://freemusicarchive.org/music/Blah_Blah_Blah/30th_Anniversary_Blah_Blah_Blah/Excretia' in response.data

    assert b'367' in response.data
    assert b'There goes my greenhouse' in response.data
    assert b'110' in response.data
    assert b'http://freemusicarchive.org/music/Blah_Blah_Blah/30th_Anniversary_Blah_Blah_Blah/There_goes_my_greenhouse' in response.data



def test_range_of_tracks(client):
    # Check that we can retrieve the articles page.
    response = client.get('/list_track?cursor=1820')
    assert response.status_code == 200

    # Check that all articles tagged with 'Health' are included on the page.
    assert b'Current range of tracks: 1820 - 1840' in response.data

