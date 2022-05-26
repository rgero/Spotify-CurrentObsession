import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import namedtuple
from funcy.seqs import first
from datetime import date

#Importing my credentials
from credientials import *

SPOTIFY_API_KEY = credientials["SPOTIFY_API_KEY"]
SPOTIFY_API_SECRET = credientials["SPOTIFY_API_SECRET"]
SPOTIFY_URI = credientials["SPOTIFY_URI"]

Track = namedtuple('Track', ['artist', 'track'])
scope = 'user-top-read playlist-modify-public'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_API_KEY, 
                                                client_secret=SPOTIFY_API_SECRET, 
                                                redirect_uri=SPOTIFY_URI,
                                                scope=scope
                                            ))

def generate_spotify_playlist(tracks, playlist_name, username):
    """
    Generates a Spotify playlist from the given tracks
    :param tracks: list of Track objects
    :param playlist_name: name of playlist to create
    :param username: Spotify username
    """
    formatted_tracks = []
    for t in tracks:
        try:
            formatted_tracks.append(u'artist:"{artist}" track:"{track}"'.format(artist=t.artist, track=t.track))
        except UnicodeDecodeError:
            pass
    search_res = [sp.search(q=t, type='track', limit=1) for t in formatted_tracks]
    track_ids = [(first(r.get('tracks', {}).get('items', {})) or {}).get('uri') for r in search_res if
                 r.get('tracks', {}).get('items')]

    token = spotipy.util.prompt_for_user_token(username, scope=scope, 
                                                         client_id=SPOTIFY_API_KEY, 
                                                         client_secret=SPOTIFY_API_SECRET, 
                                                         redirect_uri=SPOTIFY_URI)

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlist = sp.user_playlist_create(username, playlist_name, description=date.today().isoformat())

        if playlist and playlist.get('id'):
            sp.user_playlist_add_tracks(username, playlist.get('id'), track_ids)
            print("Playlist has been processed.")
    else:
        print("Can't get token for", username)

def getTopTracks():
    currentTracks = sp.current_user_top_tracks(limit=20, offset=0, time_range='short_term')

    listOfTracks=[]
    for song in currentTracks["items"]:
        artistName = song["artists"][0]["name"]
        songName = song["name"]
        listOfTracks.append( Track(artistName,songName) )
    return listOfTracks

if __name__ == '__main__':
  '''
      : param spotifyUserName : Your Spotify name
  '''
  try:
      spotifyUserName = "r0ym0nd"
      playlistName = "Hot Songs"
      topTracks = getTopTracks()
      generate_spotify_playlist(topTracks,playlistName, spotifyUserName)
  except Exception as e:
      print(e)