import dbus


class SpotifyController:
    def __init__(self):
        try:
            self.spotify_object = dbus.SessionBus().get_object(
                'org.mpris.MediaPlayer2.spotify',
                '/org/mpris/MediaPlayer2'
            )
            self.interface = dbus.Interface(
                self.spotify_object,
                'org.mpris.MediaPlayer2.Player'
            )
            self.properties_interface = dbus.Interface(
                self.spotify_object,
                'org.freedesktop.DBus.Properties'
            )
        except dbus.exceptions.DBusException:
            raise RuntimeError("Spotify is not running or dbus is unavailable.")

    def play_pause(self):
        self.interface.PlayPause()

    def pause(self):
        self.interface.Pause()

    def next(self):
        self.interface.Next()

    def prev(self):
        self.interface.Previous()

    def play_track(self, uri):
        self.interface.OpenUri(uri)
        self.get_current_playing()
    def play_album(self, album_uri):
        self.interface.OpenUri(album_uri)
        self.get_current_playing()
    

    def get_current_playing(self):
        metadata = self.properties_interface.Get(
            'org.mpris.MediaPlayer2.Player', 'Metadata'
        )
        title = metadata.get("xesam:title", "Unknown Title")
        artist = metadata.get("xesam:artist", ["Unknown Artist"])[0]
        return f"{title} by {artist}"
