import pylast, sys, datetime, spotipy
from collections import namedtuple
from funcy.seqs import first

from spotipy.oauth2 import SpotifyOAuth

#Importing my credentials
from credientials import *

LASTFM_API_KEY = credientials["LASTFM_API_KEY"]
SPOTIFY_API_KEY = credientials["SPOTIFY_API_KEY"]
SPOTIFY_API_SECRET = credientials["SPOTIFY_API_SECRET"]
SPOTIFY_URI = credientials["SPOTIFY_URI"]

Track = namedtuple('Track', ['artist', 'track'])
scope = 'playlist-modify-public'

def generate_spotify_playlist(tracks, playlist_name, username):
    """
    Generates a Spotify playlist from the given tracks
    :param tracks: list of Track objects
    :param playlist_name: name of playlist to create
    :param username: Spotify username
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_API_KEY, 
                                                   client_secret=SPOTIFY_API_SECRET, 
                                                   redirect_uri=SPOTIFY_URI,
                                                   scope=scope
                                                ))
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
        playlist = sp.user_playlist_create(username, playlist_name)

        if playlist and playlist.get('id'):
            sp.user_playlist_add_tracks(username, playlist.get('id'), track_ids)
            print("Playlist has been processed.")
    else:
        print("Can't get token for", username)


def getTopTracks(userName, numberOfTracks=15):
    """
        Gets the top tracks from LastFMNetwork
        :param userName: the lastFM user name
    """
    listOfTracks=[]
    try:
        network = pylast.LastFMNetwork(api_key = LASTFM_API_KEY, username=userName)
        user = network.get_user(userName)
        tracks = user.get_weekly_track_charts()
        trackDump = open(userName + "_Top_Tracks.txt",'w')
        for i in range(0, numberOfTracks):
            currentSong = tracks[i]
            trackDump.write(str(currentSong[0]) + "\n")
            parsedTrack = str(currentSong[0]).split(" - ")
            artist = parsedTrack[0]
            trackName = parsedTrack[1]
            listOfTracks.append( Track(artist,trackName) )
        trackDump.close()
        return listOfTracks
    except pylast.WSError:
        print("User does not exist. Aborting Program")
        sys.exit(-1)

if __name__ == '__main__':
    '''
        : param userName : Your Last FM name
    '''
    try:
        userName = "Roymond"
        spotifyUserName = "r0ym0nd"
        topTracks = getTopTracks(userName)

        today = datetime.date.today()
        lastWeek = datetime.timedelta(days=7)
        today = today - lastWeek;
        currentDate = today.strftime("%Y-%m-%d")

        playlistName = "Hot Songs on " + currentDate
        generate_spotify_playlist(topTracks,playlistName, spotifyUserName)
    except Exception as e:
        print(e)
        