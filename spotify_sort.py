import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
from dotenv import load_dotenv

# Spotify API load from env
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public"

# Authentification for Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# insert playlist
playlist_id = '1BXxWTkSke5ikD81qbQjGi'


def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    while results:
        for item in results['items']:
            track = item['track']
            tracks.append(track)
        # get next page (only 100 songs per Page)
        if results['next']:
            results = sp.next(results)
        else:
            break
    return tracks


def sort_tracks_by_release_date(tracks):
    return sorted(tracks, key=lambda track: track['album']['release_date'])

def update_playlist(playlist_id, tracks):
    track_ids = [track['id'] for track in tracks]

    # Break the track_ids list into chunks of 100
    chunk_size = 100
    track_chunks = [track_ids[i:i + chunk_size] for i in range(0, len(track_ids), chunk_size)]

    # Clear the existing playlist
    sp.playlist_replace_items(playlist_id, [])

    # Add the tracks in chunks
    for chunk in track_chunks:
        sp.playlist_add_items(playlist_id, chunk)
def main():
    tracks = get_playlist_tracks(playlist_id)
    print(f"Number of tracks in the playlist: {len(tracks)}")

    sorted_tracks = sort_tracks_by_release_date(tracks)
    print("Tracks sorted by date")

    update_playlist(playlist_id, sorted_tracks)
    print("Playlist updated")

if __name__ == '__main__':
    main()
