import pylast, sys
from collections import namedtuple

#Importing my credentials
from credientials import *

LASTFM_API_KEY = credientials["LASTFM_API_KEY"]

Track = namedtuple('Track', ['artist', 'track'])

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
            print(currentSong)
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
        topTracks = getTopTracks(userName)
    except Exception as e:
        print(e)
        