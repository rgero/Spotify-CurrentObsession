import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import namedtuple
from funcy.seqs import first
from datetime import date

#Importing my credentials
from credientials import *

class SpotifyObsession:
    def __init__(self, API_KEY, API_SECRET, API_URI):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.API_URI = API_URI

        # Setting Defaults
        self.targetPlaylistName = "Hot Songs"
        self.targetUser = ""
        self.tracks = []
        self.targetLimit = 20
        self.timeRange = "short_term"

        # Setting Default Permissions
        self.Track = namedtuple('Track', ['artist', 'track'])
        self.Scope = 'user-top-read playlist-modify-public'

        # Getting Default Spotify Instance
        self.Spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.API_KEY, 
                                                client_secret=self.API_SECRET, 
                                                redirect_uri=self.API_URI,
                                                scope=self.Scope
                                            ))

    def setUser(self, targetUser):
        self.targetUser = targetUser
        return self

    def setPlaylistName(self, targetName):
        self.targetPlaylistName = targetName
        return self

    def setTargetLimit(self, targetLimit):
        self.targetLimit = targetLimit
        return self

    def setTimeRange(self, timeRange):
        self.timeRange = timeRange
        return self

    def getTopTracks(self):
        currentTracks = self.Spotify.current_user_top_tracks(limit=self.targetLimit, offset=0, time_range=self.timeRange)

        listOfTracks=[]
        for song in currentTracks["items"]:
            artistName = song["artists"][0]["name"]
            songName = song["name"]
            listOfTracks.append( self.Track(artistName,songName) )
        self.tracks = listOfTracks

    def generateSpotifyPlaylist(self):
        self.getTopTracks()

        formatted_tracks = []
        for t in self.tracks:
            try:
                formatted_tracks.append(u'artist:"{artist}" track:"{track}"'.format(artist=t.artist, track=t.track))
            except UnicodeDecodeError:
                pass
        search_res = [self.Spotify.search(q=t, type='track', limit=1) for t in formatted_tracks]
        track_ids = [(first(r.get('tracks', {}).get('items', {})) or {}).get('uri') for r in search_res if
                    r.get('tracks', {}).get('items')]

        token = spotipy.util.prompt_for_user_token(self.targetUser, scope=self.Scope, 
                                                            client_id=self.API_KEY, 
                                                            client_secret=self.API_SECRET, 
                                                            redirect_uri=self.API_URI)

        if token:
            # Recreate the Spotify instance because we have a new token with more permissions.
            self.Spotify = spotipy.Spotify(auth=token)
            self.Spotify.trace = False
            playlist = self.Spotify.user_playlist_create(self.targetUser, self.targetPlaylistName, description=date.today().isoformat())

            if playlist and playlist.get('id'):
                self.Spotify.user_playlist_add_tracks(self.targetUser, playlist.get('id'), track_ids)
                print("Playlist has been processed.")
        else:
            print("Can't get token for", self.targetUser)




'''         Getting set up          '''
SPOTIFY_API_KEY = credientials["SPOTIFY_API_KEY"]
SPOTIFY_API_SECRET = credientials["SPOTIFY_API_SECRET"]
SPOTIFY_URI = credientials["SPOTIFY_URI"]
if __name__ == '__main__':
  try:
      spotifyObsession = SpotifyObsession(SPOTIFY_API_KEY, SPOTIFY_API_SECRET, SPOTIFY_URI)
      spotifyObsession.setUser("r0ym0nd")
      spotifyObsession.setTargetLimit(30)
      spotifyObsession.generateSpotifyPlaylist()
  except Exception as e:
      print(e)