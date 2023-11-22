# for working with spotify
import spotipy
import sys
from spotipy.oauth2 import SpotifyOAuth
# to adjust timezone
from datetime import datetime
from datetime import timezone
from datetime import timedelta
# system stuff
from spotifyConstants import *


class spotifyUpdater:
    def __init__(self) -> None:
        # Variable initialization
        self.tracks = []
        self.today = (datetime.today() - timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%SZ')
        self.last_update = last_update
        self.response = ""
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect,
                                                   scope=scope,
					           open_browser = False)
        )

    def gather_songs(self):
        self.tracks = self.get_new_tracks()
        return "Have gathered folowing songs:" + "\n\n" + self.response

    def clear_gathered(self):
        self.tracks = []
        self.response = ""

    def add_tracks(self):
        #print(self.last_update)
        if len(self.tracks) > 0:
            self.sp.playlist_add_items(playlist_id=dest_id, items=self.tracks)
            self.response = '\nEnjoy! 😘😘😘'
        else:
            self.response = "Ahh, silly me! There are no songs today 🥺👉👈"
        # technicall stuff
        self.change_update_date()
        self.last_update = (datetime.today() - timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%SZ')
        self.sp.playlist_change_details(dest_id, description=description + self.today)
        return self.response

    def get_header(self):
        return ("Starting to gather information...")
        # print('{:^24s}'.format("MyString"))

    def get_response(self):
        return self.response


    def change_update_date(self):
        # Replaces variable 'last_update' in file constants.py with a new value
        # deprecated because now i run bot constnatly, so it imports only once
        file = open('spotifyConstants.py', 'r')
        lines = file.readlines()
        tmp = last_update
        file = open('spotifyConstants.py', 'w')
        for line in lines:
            if line.strip("\n") != "last_update = " + '"' + tmp + '"':
                file.write(line)
            else:
                file.write("last_update = " + '"' + self.today + '"' + '\n')


    def get_tracks(self, my=True, to_print=False):
        #  my -> return all my liked tracks
        # !my -> return all destination tracks
        offset = 0
        trs = []
        i = 0
        result = []
        while True:
            if my:
                tr = self.sp.current_user_saved_tracks(
                limit=50, offset=offset, market=None)
            else:
                tr = self.sp.playlist_items(
                    dest_id, limit=50, offset=offset, market=None)
            offset += 50
            trs.extend(tr['items'])
            if tr['total'] <= len(trs):
                break
        for t in trs:
            if to_print:
                self.response = self.response + str(i) + " " + t['track']['name'] + '\n'
            result.append(t['track']['uri'])
            i = i + 1
        return result


    def get_new_tracks(self):
        # Return tracks's uris that I liked after last update
        # and which are not in destination playlist.
        offset = 0
        trs = []
        i = 0
        result = []
        sonechkini = []
        while True:
            tr = self.sp.current_user_saved_tracks(limit=50, offset=offset, market=None)
            offset += 50
            trs.extend(tr['items'])
            if tr['total'] <= len(trs):
                break
        last_date = datetime.strptime(self.last_update, '%Y-%m-%dT%H:%M:%SZ')
        sonechkini = self.get_tracks(False)
        for t in trs:
            added_day = datetime.strptime(t['added_at'], '%Y-%m-%dT%H:%M:%SZ')
            if added_day > last_date and t['track']['uri'] not in sonechkini:
                i = i + 1
                self.response = self.response + str(i) + ")" + " " +  t['track']['artists'][0]['name'] +  " - " + t['track']['name'] + '\n'
                result.append(t['track']['uri'])
        return result

    def add_items_to_dest(self, tracks):
        self.sp.playlist_add_items(playlist_id=dest_id, items=tracks)
