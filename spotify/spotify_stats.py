"""
This script uses the Spotify Web API to fetch and print a user's top artists and tracks on Spotify.

To run this script, you need to have a `secrets.yml` file in the same directory as the script. The `secrets.yml` file should contain your Spotify API client ID and client secret in the following format:

```yaml
spotify:
  client_id: YOUR_CLIENT_ID
  client_secret: YOUR_CLIENT_SECRET
```

You can then run the script from the command line like so:

```bash
python3 spotify_stats.py
```

This will print your top artists and tracks on Spotify.
"""

from collections import namedtuple
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yaml

Credentials = namedtuple("Credentials", ["client_id", "client_secret"])


def load_secrets(file_path):
    try:
        with open(file_path, "r") as stream:
            secrets = yaml.safe_load(stream)
            return Credentials(
                secrets["spotify"]["client_id"],
                secrets["spotify"]["client_secret"],
            )
    except Exception as e:
        print(f"Error loading secrets file: {e}")
        exit(1)


def authenticate_spotify(creds):
    try:
        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=creds.client_id,
                client_secret=creds.client_secret,
                redirect_uri="http://localhost:8888",
                scope="user-top-read",
            )
        )
    except Exception as e:
        print(f"Error authenticating with Spotify: {e}")
        exit(1)


def get_top_artists(sp, limit=10, time_range="medium_term"):
    try:
        return sp.current_user_top_artists(limit=limit, time_range=time_range)
    except Exception as e:
        print(f"Error fetching top artists: {e}")
        exit(1)


def get_top_tracks(sp, limit=10, time_range="medium_term"):
    try:
        return sp.current_user_top_tracks(limit=limit, time_range=time_range)
    except Exception as e:
        print(f"Error fetching top tracks: {e}")
        exit(1)


def print_top_artists(artists):
    print("Top Artists:")
    for i, artist in enumerate(artists["items"], start=1):
        print(f"{i}. {artist['name']}")


def print_top_tracks(tracks):
    print("Top Tracks:")
    for i, track in enumerate(tracks["items"], start=1):
        print(f"{i}. {track['name']} by {track['artists'][0]['name']}")


def main():
    creds = load_secrets("secrets.yml")

    sp = authenticate_spotify(creds)

    top_artists = get_top_artists(sp)
    print_top_artists(top_artists)

    print("\n")

    top_tracks = get_top_tracks(sp)
    print_top_tracks(top_tracks)


if __name__ == "__main__":
    main()
