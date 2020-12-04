""" roboturtle.py by Sebastiaan van der Laan
    for RoboTurtle, final project
    as part of WebApps, Minor Programmeren.

    Contains the RoboTurtle class.
    RoboTurtle performs all Spotify API-related functions.
    Heavily leans on "spotipy" module for handling API requests.
"""

import os, spotipy, time
from datetime import datetime
from app.models import *


class RoboTurtle():
    """ RoboTurtle activate!
    """
    def __init__(self, spo):
        # spo is the spotipy client instance doing the heavy API lifting
        self.spo = spo
        self.user = spo.me()['id']

        # lists for URIs of artists, tracks, tracks, and a playlist, resp.
        self.top_artists = []
        self.top_tracks = []
        self.recommendations = []
        self.new_playlist_uri = ""


    def classic(self, top_limit=50, rec_limit=3, time_range='long_term'):
        """ The all in one RoboTurtle special will analyze a user,
            get user recommendations, create a playlist, 
            and add the recommended tracks to that list.
            Returns URI of the new playlist.
        """
        self.analyze(limit=top_limit, time_range=time_range)
        self.get_recommendations(rec_limit=rec_limit)
        self.create_playlist()
        self.add_to_playlist()


    def turtle(self, top_limit=50, rec_limit=3, time_range='long_term', public=True, **kwargs):
        """ Slow wins the race.
            This function passes the user supplied metrics through to 
            the get_recommendations function in order to influence the types
            of tracks Spotify responds with to our API requests.
            Returns URI of the new playlist.
        """
        self.analyze(limit=top_limit, time_range=time_range)
        self.get_recommendations(rec_limit=rec_limit, **kwargs)
        self.create_playlist(public=public, description=kwargs)
        self.add_to_playlist()


    def analyze(self, limit=20, time_range='medium_term'):
        """ Find out what a user likes. 
            Saves the resulting tracks and artists to self.top_tracks/artists
            to use as seeds for get_recommendations' API requests.
            Usage:
            limit: number of tracks/artists to receive. 1-50.
            time_range: short, medium(default) or long_term.
            Collects user data of the past 4 weeks, 6 months or a few years.
        """
        # API GET user top artists
        results = self.spo.current_user_top_artists(limit=limit, time_range=time_range)

        for idx, item in enumerate(results['items']):
            print(idx+1, item['name'], " - genres: ", item['genres'])
            self.top_artists.append(item['uri'])

        # turtle knows: slow wins the race
        time.sleep(.5)

        # API GET user top tracks
        results = self.spo.current_user_top_tracks(limit=limit, time_range=time_range)

        for idx, item in enumerate(results['items']):
            print(idx+1, item['artists'][0]['name'], " – ", item['name'])
            self.top_tracks.append(item['uri'])
 

    def get_recommendations(self, rec_limit=3, **kwargs):
        """ Uses top artists and top tracks to acquire a number (limit)
            of track recommendations and appends the URI's of the resulting
            tracks to self.recommendations.
            TODO kwargs: extra min/max/target recommendation filters
        """
        # request limit number of recommendations per top artist
        for artist in self.top_artists:
            
            # issue request
            results = self.spo.recommendations(seed_artists=[artist],
                                         limit=rec_limit, **kwargs)

            # append all resulting tracks to recommendations
            for idx, item in enumerate(results['tracks']):
                print(idx+1, item['artists'][0]['name'], " – ", item['name'])
                self.recommendations.append(item['uri'])

            # turtle knows: slow wins the race
            time.sleep(.1)
            
        # request limit number of recommendations per top track
        for track in self.top_tracks:

            # issue request
            results = self.spo.recommendations(seed_tracks=[track],
                                         limit=rec_limit, **kwargs)

            # append all resulting tracks to recommendations
            for idx, item in enumerate(results['tracks']):
                print(idx+1, item['artists'][0]['name'], " – ", item['name'])
                self.recommendations.append(item['uri'])

            # turtle knows: slow wins the race
            time.sleep(.1)
        
        # remove duplicates from our recommendations list
        self.recommendations = list(set(self.recommendations))      


    def create_playlist(self, public=True, description="classic"):
        """ Creates a new private playlist in the user account.
        """
        # time to situate RoboTurtle in the here and now
        now = datetime.now()
        day = now.strftime("%m.%d.%Y")

        # playlist description
        if description == "classic":
            # robo classic description
            description = f'🤖Classic for {self.user} by 🤖RoboTurtle🐢 on {day}.'
        else: 
            # turtle mode description
            metrics = ""
            for key in description:
                metrics += f" {key[7:]}={description[key]}"
            description = f'🐢Mode for {self.user} by 🤖RoboTurtle🐢 on {day}. Metrics: {metrics}' 
        
        # create new (empty) list
        new_playlist = self.spo.user_playlist_create(self.user,
                                               '🤖RoboTurtle🐢',
                                               public=public,
                                               description=description)

        # save playlist uri (extracted from response)
        self.new_playlist_uri = new_playlist['uri']

        # add playlists to the SQL database under the username TODO uncomment
        # load or create user object
        u = User.query.filter_by(username=self.user).first()
        if u is None:
            u = User(username=self.user)
            db.session.add(u)
            db.session.commit()

        # create playlist object with URI, descripton and user id
        p = Playlist(uri=self.new_playlist_uri, description=description, user_id=u.id)
        db.session.add(p)
        db.session.commit()


    def add_to_playlist(self, **kwargs):
        """ Adds tracks to an existing playlist.
            kwargs: tracks_to_add(URI list), playlist_uri (URI)
        """

        # collect **kwargs or set values from defaults
        tracks_to_add = kwargs.get('tracks_list', self.recommendations)
        playlist_uri = kwargs.get('playlist_uri', self.new_playlist_uri)
        
        # add selected tracks to playlist max 100 at a time
        print(f"Total number of tracks to add: {len(tracks_to_add)}")
        for i in range(0, len(tracks_to_add), 100):
            tracks_subset = tracks_to_add[i:i+100]
            print(f"Tracks to add in this API request: {len(tracks_subset)}")
            self.spo.user_playlist_add_tracks(self.user,
                                        playlist_id=playlist_uri,
                                        tracks=tracks_subset)

            # turtle knows: slow wins the race
            time.sleep(.1)


    def list_playlists(self):
        """ Collects all RoboTurtle playlists from the database.
        """
        playlists = Playlist.query.all()
        return playlists
