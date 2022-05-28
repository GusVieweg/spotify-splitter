import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

playlist = sp.playlist(playlist_id="5hfkBedabkUiLAJdHBgIAa")
playlist_info = playlist['tracks']

songs_audio_features = []

while playlist_info:
    song_ids = []
    # print(b_sides_redux['tracks']['items'][0]['track']['id'])
    songs = playlist_info['items']

    for track in songs:
        song_ids.append(track['track']['id'])
    
    afs = sp.audio_features(tracks=song_ids)
    for idx, af in enumerate(afs):
        af['song_name'] = songs[idx]['track']['name']
        af['artist'] = songs[idx]['track']['artists'][0]['name']
        songs_audio_features.append(af)
    
    if playlist_info['next']:
        playlist_info = sp.next(playlist_info)
    else:
        break

print(songs_audio_features)
print(len(songs_audio_features))

bops_ids = []
softs_ids = []