from functools import wraps
from webbrowser import get
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange

from music.adapters.csvdatareader import TrackCSVReader
from music.tracks.services import get_all_tracks, get_tracks_by_range, get_track
import music.adapters.repository as repo
from music.tracks import services
from music.authentication.services import get_user
from music.domainmodel.track import Track
from music.domainmodel.user import User

track_blueprint = Blueprint('track_blueprint', __name__)

@track_blueprint.route('/')
def home():
    # Task 3: Render our home page.
    return render_template('homepage.html')

@track_blueprint.route('/list_track', methods=['GET'])
def list_track():
    form = CommentForm()
    records_per_page = 20
    user_input = request.args.get("filter", "").lower()
    # user_logged_in = session['user_name'] != ""
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    all_tracks = get_all_tracks(repo.repo_instance)
    tracks = [
        track for track in all_tracks if
        user_input in track.title.lower() or
        user_input in track.artist.full_name.lower()
    ]
    tracklist = tracks[cursor:cursor+20]

    first_track_url = None
    last_track_url = None
    next_track_url = None
    prev_track_url = None

    if cursor > 0:
        prev_track_url = url_for('track_blueprint.list_track', cursor=cursor - records_per_page)
        first_track_url = url_for('track_blueprint.list_track')

    if cursor + records_per_page < len(all_tracks):
        next_track_url = url_for('track_blueprint.list_track', cursor=cursor + records_per_page)
        
        last_cursor = records_per_page * int(len(all_tracks) / records_per_page)

        if len(all_tracks) % records_per_page == 0:
            last_cursor -= records_per_page

        last_track_url = url_for('track_blueprint.list_track',cursor=last_cursor)


    toprange = cursor + records_per_page
    return render_template('tracks/track_list.html',
    # user_logged_in= user_logged_in,
    tracks=tracklist,
    first_track_url = first_track_url,
    last_track_url = last_track_url,
    next_track_url = next_track_url,
    prev_track_url = prev_track_url,
    rangebottom= str(cursor),
    rangetop = str(toprange),
    form = form,
    )

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view
@track_blueprint.route('/comment', methods=['POST'])
def comment():
    form = CommentForm()
    if form.validate_on_submit():
        user_name = session['user_name']
        user = repo.repo_instance.get_user(user_name)
        rating = int(form.rating.data)
        track = repo.repo_instance.get_track(int(form.track_id.data))
        review = services.add_review(user, track, form.comment.data, rating, repo.repo_instance)
        #review = services.add_review('test', track, form.comment.data, rating, repo_instance)
        return redirect('/list_track')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
    ])
    rating = IntegerField('Rating', [
        DataRequired(),
        NumberRange(1, 5)
    ])
    track_id = HiddenField('Track ID')
    submit = SubmitField('Submit')