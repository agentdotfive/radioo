#
# Playlist generation
#

import json
import optparse
import random

import pylast

PLAYLIST_TYPE_TOP_SONGS=0
PLAYLIST_TYPE_SIMILAR_TO=1
PLAYLIST_TYPE_REGION=2
PLAYLIST_TYPE_GENRE=3
PLAYLIST_TYPE_ERA=4

PLAYLIST_TYPES = [PLAYLIST_TYPE_TOP_SONGS,
                  PLAYLIST_TYPE_SIMILAR_TO,
                  PLAYLIST_TYPE_REGION,
                  PLAYLIST_TYPE_GENRE,
                  PLAYLIST_TYPE_ERA]

class TrackStream:

    def __init__(self, lastfm_api):
        self.history = []
        self.position = -1
        
        self.lastfm_api = lastfm_api
        self.cached = []

    def load(history, position):
        self.history = history
        self.position = position

    def find_next_track(self):
        raise Exception("Not implemented")

    def next_track(self):
        
        track = None
        self.position = self.position + 1
        
        if self.position < len(self.history):
            track = get_track_at(self.position)
        else:
            track = find_next_track(track) 
            self.history.append(track.get_mbid())
            self.cached.append(track)

        return track

    def get_track_at(self, position):
        if not cached[position]:
            cached[position] = lastfm_api.get_track_by_mbid(history[position])

        return cached[position]

class SimilarTrackStream:
   
    def __init__(self, lastfm_api):
        
        TrackStream.__init__(self)
        
        self.lastfm_api = lastfm_api
   
    def load(random_state, **kwargs):
        TrackStream.__load__(self, **kwargs) 
        self.random = random.Random()
        self.random.setstate(random_state)
        
    def initial_track(self, track):
        self.history[0] = track.get_mbid()

    def find_next_track(self):
                
        

    

def get_lastfm_api(api_key, api_secret, username, password):
    password = pylast.md5(password)
    return pylast.LastFMNetwork(api_key=api_key,
                                api_secret=api_secret,
                                username=username,
                                password_hash=password)

def get_top_songs(rng, lastfm_api):
    
    top_artists = lastfm_api.get_top_artists(limit=10)
    
    for artist, weight in top_artists:
        print artist.get_name(properly_capitalized=True)

def random_playlist(rng, lastfm_api):
    
    playlist_types = [] + PLAYLIST_TYPES
    rng.shuffle(playlist_types)
    
    playlist_types = playlist_types[0:rng.randrange(1, len(playlist_types))]
    
    for playlist_type in playlist_types:
        
        if playlist_type == PLAYLIST_TYPE_TOP_SONGS or True:
            get_top_songs(rng, lastfm_api)

def parse_args():

    parser = optparse.OptionParser()

    help = \
        """Credentials for API access""" 

    parser.add_option("--credentials-file", dest="credentials_filename", help=help)

    return parser.parse_args()

def main():
    
    options, args = parse_args()
    
    lastfm_api = None
    with open(options.credentials_filename) as credentials_file:
        credentials = json.load(credentials_file)
        lastfm_api = get_lastfm_api(**credentials)
   
    random_playlist(random.Random(0), lastfm_api)


if __name__ == "__main__":
    main()

