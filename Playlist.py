class Playlist:
    song_ids = []
    audio_features = []

    def __init__(self, user, spotipy, id=None, playlist_name=None):
        self.user = user
        self.sp = spotipy
        self.id = id
        if id:
            self._load()
        elif playlist_name:
            self._get_id_by_name(playlist_name)
            if not self.id:
                self.create(playlist_name)
            self._load()
    
    def get_all_song_ids_and_audio_features(self):
        retrieving = True
        tracks = self.playlist['tracks']
        if not tracks['items']: return

        while retrieving:
            batch_songs = tracks['items']
            batch_song_ids = []
            for s in batch_songs:
                song_id = s['track']['id']
                batch_song_ids.append(song_id)
                self.song_ids.append(song_id)
            
            afs = self.sp.audio_features(tracks=batch_song_ids)
            for idx, af in enumerate(afs):
                af['song_name'] = batch_songs[idx]['track']['name']
                af['artist'] = batch_songs[idx]['track']['artists'][0]['name']
                self.audio_features.append(af)

            if tracks['next']:
                tracks = self.sp.next(tracks)
            else:
                retrieving = False
    
    def create(self, playlist_name):
        new_playlist = self.sp.user_playlist_create(
            user=self.user,
            name=playlist_name,
            public=True,
            collaborative=False,
            description=playlist_name
        )
        self.id = new_playlist['id']
    
    def update(self, song_id_list):
        self._clear()
        self._stagger_spotipy_request(self.sp.playlist_add_items, song_id_list)
    
    def _clear(self):
        self.get_all_song_ids_and_audio_features()
        self._stagger_spotipy_request(self.sp.playlist_remove_all_occurrences_of_items, self.song_ids)

    def _stagger_spotipy_request(self, operation, song_ids):
        staggering = True
        while staggering:
            if len(song_ids) > 100:
                operation(self.id, song_ids[:100])
                song_ids = song_ids[100:]
            elif len(song_ids) < 100 and len(song_ids) > 0:
                operation(self.id, song_ids)
                staggering = False
            else:  # Song array is empty (either no songs or exactly 100, 200, 300... songs)
                staggering = False

    def _load(self):
        self.playlist = self.sp.playlist(playlist_id=self.id)
    
    def _get_id_by_name(self, playlist_name):
        playlist_metadata = self.sp.user_playlists(self.user)
        _playlists = playlist_metadata['items']
        while _playlists:
            for p in _playlists:
                if p['name'] == playlist_name:
                    self.id = p['id']
                    return
            if playlist_metadata['next']:
                _playlists = self.sp.next(playlist_metadata)
            else:
                self.id = None
                break