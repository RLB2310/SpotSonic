import spotipy, os
from spotipy.oauth2 import SpotifyClientCredentials

class Search:
    def __init__(self):
        
        cache_dir = '.cache'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        os.chmod(cache_dir, 0o700)
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    def search(self, query):
        results = {
            "spotify": []
        }
        try:
            response = self.spotify.search(q=query, type='track', limit=10)
            tracks = response["tracks"]["items"]

            for track in tracks:
                results["spotify"].append({
                    "name": track["name"],
                    "artists": track["artists"],
                    "uri": track["uri"],
                })
        except Exception as e:
            print(f"Error during search: {e}")

        return results
