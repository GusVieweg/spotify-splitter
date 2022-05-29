# Spotify Splitter

### Goals and Purpose
[Addie](https://github.com/addiejackson) and I have created a large playlist of all the tunes we currently like.

Oftentimes, we will want to put on a mood - currently either `bops` or `softs`.

Bops are for when things are good. The kids call them bangers. Think a boisterous Friday evening.

Softs are for when things are mellow. The kids call them chill tunes. Think a ~~hungover~~ sleepy Saturday morning.

There was no way for us to put on one mood of songs we currently like. We had to skip softs when we were in a bop mood and bops when we were in a soft mood.

Enter Spotify Splitter.

### Methodology
This program splits a large playlist into `bops` and `softs` based on a separation algorithm.

Spotify characterizes all of their songs with various criteria called [Audio Features](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features).

Using these, we can run each song through a filter to determine if it is a bop, a soft, both, or neither.

A rudimentary, pseudocode filter may look like:
```
if song['danceability'] > 0.7:
    bops.add(song)
if song['energy'] < 0.45:
    softs.add(song)
```

The current sorting algorithm can be found on the [spotify-splitter.py file](https://github.com/GusVieweg/spotify-splitter/blob/main/spotify-splitter.py). 

### Deployment
To run this on your own playlists:

1. Go to your [Spotify for Developers Dashboard](https://developer.spotify.com/dashboard/login) (SfDD).
2. Create an account if needed.
3. Create a new app and call it "Spotify Splitter."
4. Edit the "Spotify Splitter" app's settings and add an entry to "Redirect URIs": `http://localhost:8080/`. Be sure to save! 
5. Create a `.env` in the base `spotify-splitter/` folder with the following environment variables:
- `SPOTIFY_CLIENT_ID`: your client id from the SfDD
- `SPOTIFY_CLIENT_SECRET`: your client secret from the SfDD
- `SPOTIFY_REDIRECT_URI`: `http://localhost:8080/`
- `SPOTIFY_USER`: your spotify username, as written on your Spotify Account page
- `MAIN_PLAYLIST_ID`: the playlist id to split; you can find it on the Spotify Web Client in the url: `https://open.spotify.com/playlist/<playlist_id>`
6. Curate the sorting algorithm to your liking. Refer to the [Audio Features](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features) page for more sorting criteria.
7. Change the `Playlist` objects' initialization (`playlist_name`) to your liking.

You will have to authorize your Spotify account on first run.

Enjoy your split music!
