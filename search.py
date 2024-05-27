import spotipy, os
from spotipy.oauth2 import SpotifyClientCredentials
import logging

logging.getLogger('spotipy').setLevel(logging.ERROR)
class Search:
    def __init__(self):
        cache_dir = '~/.cache'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        os.chmod(cache_dir, 0o777)
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())        

    def search(self, query):
        """Search for both tracks and albums on Spotify."""
        results = {
            "tracks": [],
            "albums": []
        }

        try:
            # Search for tracks and albums with a limit of 10 results each
            track_response = self.spotify.search(q=query, type="track", limit=10)
            album_response = self.spotify.search(q=query, type="album", limit=10)

            # Process track results
            for track in track_response["tracks"]["items"]:
                results["tracks"].append({
                    "name": track["name"],
                    "artists": track["artists"],
                    "uri": track["uri"],
                })

            # Process album results
            for album in album_response["albums"]["items"]:
                results["albums"].append({
                    "name": album["name"],
                    "artists": album["artists"],
                    "uri": album["uri"],
                })

        except Exception as e:
            print(f"Error during search: {e}")

        return results
