""" application.py by Sebastiaan van der Laan
    for RoboTurtle, final project
    as part of WebApps, Minor Programmeren.

    Used primarily for flask routing.
"""

import os, requests, spotipy

from flask import Flask, session, render_template, request, redirect, flash, Markup
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from app.models import User, Playlist, db
from flask_migrate import Migrate
from roboturtle import RoboTurtle


# configure Flask app
app = Flask(__name__)

# configure database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# configure session, use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure API client details
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
client_redirect_uri = 'http://127.0.0.1:5000/'

# configure oAuth as per spotipy instructions
cache_path = ".cache-" + "test"
auth_manager = spotipy.oauth2.SpotifyOAuth(cache_path=cache_path)

# initiate spotipy client
spo = spotipy.Spotify(auth_manager=auth_manager)

# configure migrations
Migrate(app, db)


@app.route('/')
def index():
    """ The RoboTurtle landing page handles Spotify user authorization.
        There are three options:
        1) if there's no session, offer user to authorize via the url.
        2) if there is an info token, offer spotify to trade it for access
        3) if user is signed in and authorized, redirect towards classic
    """
    # upon redirect with code, trade it for a token (2)
    if request.args.get("code"):
        session['token_info'] = auth_manager.get_access_token(request.args["code"])
        return redirect('/')
    
    # ask new users to authorize via the url (1) and get redirected
    if not session.get('token_info'):
        auth_url = auth_manager.get_authorize_url()
        return render_template("authorize.html", auth_url=auth_url)

    # load the page for authorized users (3)
    return redirect("classic")


@app.route("/classic", methods=["GET", "POST"])
def classic():
    """ Displays classic template (GET) and
        handles RoboClassic requests (POST).
    """
    # run roboturtle with classic settings
    if request.method=="POST":

        # initiate RoboTurtle instance
        robo=RoboTurtle(spo)
        
        # run robo
        robo.classic()

        # extract playlist URI and flash message
        new_playlist_uri = robo.new_playlist_uri
        flash(Markup(f"<a href='{new_playlist_uri}'> Check out your new 🤖classic playlist</a>"))

    # greet user by name to appear less robotic and more turtlelike
    username = spo.me()['id']

    # or render classic template where users can click the generate button
    return render_template("classic.html", username=username)


@app.route("/turtlemode", methods=["GET", "POST"])
def turtlemode():
    """ Displays the turtlemode template (GET) and
        handles RoboTurtle turtlemode requests (POST).
    """
    # run RoboTurtle with special settings
    if request.method=="POST":

        # initiate RoboTurtle instance
        robo = RoboTurtle(spo)

        # extract metrics from form
        popularity = int(request.form['popularity'])
        energy = float(request.form['energy'])
        instrumentalness = float(request.form['instrumentalness'])
        acousticness = float(request.form['acousticness'])
        valence = float(request.form['valence'])
        time_range = request.form['time_range']
        public = True if request.form['public'] == "true" else False

        # run robo with said metrics
        robo.turtle(target_popularity=popularity,
                      target_energy=energy,
                      target_instrumentalness=instrumentalness,
                      target_acousticness=acousticness,
                      target_valence=valence,
                      time_range=time_range,
                      public=public)
        
        # extract playlist URI and flash message
        new_playlist_uri = robo.new_playlist_uri
        flash(Markup(f"<a href='{new_playlist_uri}'> Check out your new 🐢mode playlist</a>"))
    
    # greet user by name to appear less robotic and more turtlelike
    username = spo.me()['id']

    # first render turtle template where users can specify their needs
    return render_template("turtlemode.html", username=username)


@app.route("/playlists")
def playlists():
    """ Displays all RoboTurtle-made playlists.
    """
    # ask robo to list all previously created playlists
    robo = RoboTurtle(spo)
    playlists = robo.list_playlists()

    # greet user by name to appear less robotic and more turtlelike
    username = spo.me()['id']

    return render_template("playlists.html", playlists=playlists, username=username)


@app.route("/about")
def about():
    """ Displays mission statement.
    """
    # greet user by name to appear less robotic and more turtlelike
    username = spo.me()['id']
    return render_template("about.html", username=username)
    
    
@app.route('/sign_out')
def sign_out():
    """ Signs out the user.
    """
    session.clear()
    return redirect('/')