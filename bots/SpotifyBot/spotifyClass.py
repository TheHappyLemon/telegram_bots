# for working with spotify
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler

# to adjust timezone
from datetime import datetime
from datetime import timezone
from datetime import timedelta
# system stuff
from spotifyConstants import *
from itertools import islice

class spotifyUpdater:
    def __init__(self) -> None:
        # Variable initialization
        self.tracks = []
        self.today = (datetime.today() - timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%SZ')
        self.last_update = last_update
        self.response = ""

        cache_one = CacheFileHandler(".cache_one", "first")
        cache_two = CacheFileHandler(".cache_two", "second")

        self.sp_one = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id_one,
                                                   client_secret=client_secret_one,
                                                   redirect_uri=redirect,
                                                   scope=scope,
					                               open_browser = False,
                                                   cache_handler=cache_one)
                                    )
        
        self.sp_two = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id_two,
                                                   client_secret=client_secret_two,
                                                   redirect_uri=redirect,
                                                   scope=scope,
					                               open_browser = False,
                                                   cache_handler=cache_two)
                                    )
        print(self.sp_one.me())
        print(self.sp_two.me())


    def gather_songs(self):
        self.tracks = self.get_new_tracks()
        return "Have gathered folowing songs:" + "\n\n" + self.response

    def clear_gathered(self):
        self.tracks = []
        self.response = ""

    def chunked(self, iterable, size):
        """Yield successive chunks of given size from iterable."""
        it = iter(iterable)
        while chunk := list(islice(it, size)):
            yield chunk

    def add_tracks(self):
        if len(self.tracks) <= 0:
            return

        for chunk in self.chunked(self.tracks, 50):
            self.sp_one.playlist_add_items(playlist_id=dest_id, items=chunk)
        self.response = "\nPlaylist updated!"

        self.change_update_date()
        self.last_update = (datetime.today() - timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%SZ')
        self.sp_one.playlist_change_details(dest_id, description=description + self.today)
        return self.response

    def get_header(self):
        return ("Starting to gather information...")

    def change_update_date(self):
        # Replaces variable 'last_update' in file constants.py with a new value
        file = open('spotifyConstants.py', 'r')
        lines = file.readlines()
        tmp = last_update
        file = open('spotifyConstants.py', 'w')
        for line in lines:
            if line.strip("\n") != "last_update = " + '"' + tmp + '"':
                file.write(line)
            else:
                file.write("last_update = " + '"' + self.today + '"' + '\n')

    def get_user_tracks(self, spoti : spotipy.Spotify, playlist_id : str = None):

        trs = []
        offset = 0
        while True:
            if playlist_id == None:
                tr = spoti.current_user_saved_tracks(limit=50, offset=offset, market=None)
            else:
                tr = spoti.playlist_items(playlist_id, limit=50, offset=offset, market=None)
            offset += 50
            trs.extend(tr['items'])
            if tr['total'] <= len(trs):
                break
        return trs

    def get_playlist_tracks(self, playlist_id : str):
        return self.get_user_tracks(self.sp_one, playlist_id)

    def get_new_tracks(self):
        # Return tracks's uris that both users liked after last update
        # and which are not in destination playlist.

        result = []
        i = 0

        tracks_one = self.get_user_tracks(self.sp_one)
        tracks_two = self.get_user_tracks(self.sp_two)
        tracks_one.extend(tracks_two)
        tracks_playlist = self.get_playlist_tracks(dest_id)
        #last_date = datetime.strptime(self.last_update, '%Y-%m-%dT%H:%M:%SZ')
        
        for track in tracks_one:
            #added_day = datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ')
            # if added_day > last_date and track['track']['uri'] not in tracks_playlist:
            if not track['track']['uri'] in tracks_playlist:
                i = i + 1
                self.response = self.response + str(i) + ")" + " " +  track['track']['artists'][0]['name'] +  " - " + track['track']['name'] + '\n'
                result.append(track['track']['uri'])

        return result

    def add_items_to_dest(self, tracks):
        self.sp_one.playlist_add_items(playlist_id=dest_id, items=tracks)
