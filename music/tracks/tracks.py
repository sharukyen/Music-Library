from webbrowser import get
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


from music.tracks.services import get_all_tracks, get_tracks_by_range
from music.adapters.repository import repo_instance
from music.tracks import services
from music.domainmodel.track import Track


track_blueprint = Blueprint('track_blueprint', __name__)



@track_blueprint.route('/')
def home():
    # Task 3: Render our home page.
    return render_template('homepage.html')

@track_blueprint.route('/list_track', methods=['GET'])
def list_track():
    records_per_page = 20
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    track_test = get_all_tracks(repo_instance)
    tracklist = track_test[cursor:cursor+20]

    first_track_url = None
    last_track_url = None
    next_track_url = None
    prev_track_url = None

    if cursor > 0:
        prev_track_url = url_for('track_blueprint.list_track', cursor=cursor - records_per_page)
        first_track_url = url_for('track_blueprint.list_track')

    if cursor + records_per_page < len(track_test):
        next_track_url = url_for('track_blueprint.list_track', cursor=cursor + records_per_page)
        
        last_cursor = records_per_page * int(len(track_test) / records_per_page)

        if len(track_test) % records_per_page == 0:
            last_cursor -= records_per_page

        last_track_url = url_for('track_blueprint.list_track',cursor=last_cursor)


    toprange = cursor + records_per_page
    return render_template('tracks/track_list.html', 
    track=tracklist,
    first_track_url = first_track_url,
    last_track_url = last_track_url,
    next_track_url = next_track_url,
    prev_track_url = prev_track_url,
    rangebottom= str(cursor),
    rangetop = str(toprange),

    )


 