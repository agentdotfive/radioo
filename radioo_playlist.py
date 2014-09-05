#
# Playlist generation
#

import json
import optparse
import random
import urllib

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

    def __init__(self):
        self.mbid_history = []
        self.position = -1
    
    def attach_api(self, lastfm_api):
        self.lastfm_api = lastfm_api
    
    def track_history(self):
        
        if not hasattr(self, "_track_history"):
            self._track_history = []
        
        if len(self._track_history) != len(self.mbid_history):
            diff = len(self.mbid_history) - len(self._track_history)
            if diff < 0:
                self._track_history = self._track_history[0:diff]
            else:
                self._track_history = self._track_history + ([None] * diff)
        
        return self._track_history

    def get_track_at(self, position):
        
        if not self.track_history()[position]:
            if self.mbid_history[position][0]:
                self.track_history()[position] = \
                    self.lastfm_api.get_track_by_mbid(self.mbid_history[position][0])
            else:
                self.track_history()[position] = \
                    self.lastfm_api.get_track(self.mbid_history[position][1],
                                              self.mbid_history[position][2])

        return self.track_history()[position]
    
    def add_to_history(self, track):
        self.mbid_history.append([track.get_mbid(), track.get_artist(), track.get_name()])
        self.track_history().append(track)

    def next_track(self):
        
        track = None
        self.position = self.position + 1
        
        if self.position < len(self.mbid_history):
            track = self.get_track_at(self.position)
        else:
            track = self.find_next_track()
            self.add_to_history(track)

        return track

    def prev_track(self):
        self.position = self.position - 1
        return self.get_track_at(self.position)

    def find_next_track(self):
        raise Exception("Not implemented")


class SimilarTrackStream(TrackStream):
   
    def __init__(self, initial_track, rng):
        TrackStream.__init__(self)
        self.rng = rng
        self.add_to_history(initial_track)

    def find_next_track(self):

        last_position = self.position
        similar_tracks = []
        while len(similar_tracks) == 0:
            last_position = last_position - 1
            last_track = self.get_track_at(last_position)
            similar_tracks = last_track.get_similar()

        return similar_tracks[self.rng.randrange(0, len(similar_tracks))][0]

def get_lastfm_api(api_key, api_secret, username, password):
    
    password = pylast.md5(password)

    print "Connecting to LastFM..."
    api = pylast.LastFMNetwork(api_key=api_key,
                               api_secret=api_secret,
                               username=username,
                               password_hash=password)
    print "Connected to LastFM."
    
    return api

def get_top_songs(rng, lastfm_api):
    
    top_tracks = lastfm_api.get_top_tracks()

    track_stream = SimilarTrackStream(top_tracks[rng.randrange(0, len(top_tracks))][0], rng)
    track_stream.attach_api(lastfm_api)

    while True:
        track = track_stream.next_track()
        
        lastfm_link = track.get_url()
        
        mb_link = "???"
        if track.get_mbid():
            mb_link = "http://musicbrainz.org/recording/%s" % track.get_mbid()
        
        youtube_link = "http://gdata.youtube.com/feeds/api/videos?q=%s+%s" % \
            (urllib.quote(track.get_artist().get_name()), urllib.quote(track.get_name()))

        print "%s -- %s\n  %s\n  %s\n  %s" % \
            (track.get_artist(), track.get_name(), 
             lastfm_link, mb_link, youtube_link)

#    top_artists = lastfm_api.get_top_artists(limit=10)
    
#    for artist, weight in top_artists:
#        print artist.get_name(properly_capitalized=True)

def random_playlist(rng, lastfm_api):
    
    playlist_types = [] + PLAYLIST_TYPES
    rng.shuffle(playlist_types)
    
    playlist_types = playlist_types[0:rng.randrange(1, len(playlist_types))]
   
    get_top_songs(rng, lastfm_api)

#    for playlist_type in playlist_types:
        
#        if playlist_type == PLAYLIST_TYPE_TOP_SONGS or True:
#            get_top_songs(rng, lastfm_api)

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
   
    random_playlist(random.Random(), lastfm_api)


if __name__ == "__main__":
    main()

