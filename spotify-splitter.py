import spotipy
import os
from Playlist import Playlist
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

testing = False

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
        open_browser=False,
    )
)

main_playlist = Playlist(user, sp, id=main_playlist_id)
print("Created main playlist object.")
main_playlist.get_all_song_ids_and_audio_features()
print("Pulled all songs and audio features from main playlist.")

bops_ids = []
softs_ids = []
dance_ids = []

# Sorting algorithm(s)
for af in main_playlist.audio_features:
    # bops vs. softs
    if af["energy"] > 0.5:
        bops_ids.append(af["id"])
        # print(af["song_name"], "by", af["artist"], "is a bop")
    else:
        softs_ids.append(af["id"])
        # print(af["song_name"], "by", af["artist"], "is a soft")

    # DANCE
    if af["danceability"] > 0.75 or (af["valence"] > 0.75 and af["tempo"] > 130):
        dance_ids.append(af["id"])
        # print(af["song_name"], "by", af["artist"], "is a DANCE bop")


print(
    f"Sorted playlist into {len(bops_ids)} bops, {len(softs_ids)} softs, and {len(dance_ids)} dance bops."
)

if testing != True:
    bops_playlist = Playlist(user, sp, playlist_name="b bops")
    softs_playlist = Playlist(user, sp, playlist_name="b softs")
    dance_playlist = Playlist(user, sp, playlist_name="b dance")

    bops_playlist.update(bops_ids)
    print("Updated b bops playlist.")
    softs_playlist.update(softs_ids)
    print("Updated b softs playlist.")
    dance_playlist.update(dance_ids)
    print("Updated b dance playlist.")
