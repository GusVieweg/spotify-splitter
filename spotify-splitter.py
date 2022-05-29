import spotipy
import os
from Playlist import Playlist
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
user = os.getenv("SPOTIFY_USER")
main_playlist_id = os.getenv("MAIN_PLAYLIST_ID")

scope = "playlist-read-collaborative,playlist-modify-public"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        open_browser=False
    )
)

main_playlist = Playlist(user, sp, id=main_playlist_id)
print("Created main playlist object.")
main_playlist.get_all_song_ids_and_audio_features()
print("Pulled all songs and audio features from main playlist.")

bops_ids = []
softs_ids = []

# Sorting algorithm goes here
for idx, af in enumerate(main_playlist.audio_features):
    if idx % 2:
        bops_ids.append(af['id'])
    else:
        softs_ids.append(af['id'])

print(f"Separated playlist into {len(bops_ids)} bops and {len(softs_ids)} softs.")

bops_playlist = Playlist(user, sp, playlist_name="b bops")
print("Created b bops playlist object.")
softs_playlist = Playlist(user, sp, playlist_name="b softs")
print("Created b softs playlist object.")

bops_playlist.update(bops_ids)
print("Updated b bops playlist.")
softs_playlist.update(softs_ids)
print("Updated b softs playlist.")