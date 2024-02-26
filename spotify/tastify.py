from collections import namedtuple
import random
import re
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yaml

MAX_TRACKS = 100

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
                scope=["user-top-read", "playlist-modify-public"],
            )
        )
    except Exception as e:
        print(f"Error authenticating with Spotify: {e}")
        exit(1)


def get_playlist(sp, playlist_url):
    try:
        playlist_id = re.search(r"playlist\/([a-zA-Z0-9]+)[?\/]?", playlist_url).group(
            1
        )
        return sp.playlist(playlist_id)
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        exit(1)


def get_top_track_ids(sp, limit=10, time_range="medium_term"):
    try:
        tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)
        return [track["id"] for track in tracks["items"]]
    except Exception as e:
        print(f"Error fetching top tracks: {e}")
        exit(1)


def get_playlist_track_ids(playlist):
    return [track["track"]["id"] for track in playlist["tracks"]["items"]]


def get_recommendations(sp, tracks):
    try:
        random.shuffle(tracks)
        recommendations = []
        for i in range(0, len(tracks), 5):
            track_items = sp.recommendations(
                seed_tracks=tracks[i : min(i + 5, len(tracks))], limit=5
            )["tracks"]
            recommendations.extend([track["id"] for track in track_items])
        return recommendations
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        exit(1)


def create_tastified_playlist(sp, user_id, playlist):
    tastified_playlist = sp.user_playlist_create(
        user_id, f"Tastified {playlist['name']}", public=True
    )
    return tastified_playlist


def add_tracks_to_playlist(sp, user_id, playlist, tracks):
    sp.user_playlist_add_tracks(
        user_id,
        playlist["id"],
        tracks=random.sample(tracks, min(MAX_TRACKS, len(tracks))),
    )


def main():
    try:
        creds = load_secrets("secrets.yml")
        sp = authenticate_spotify(creds)

        playlist_url = input("Enter the playlist URL: ")
        playlist = get_playlist(sp, playlist_url)
        playlist_track_ids = get_playlist_track_ids(playlist)
        user_top_track_ids = get_top_track_ids(sp, limit=len(playlist_track_ids))
        all_tracks = list(playlist_track_ids)
        all_tracks.extend(x for x in user_top_track_ids if x not in all_tracks)
        recommended_tracks = get_recommendations(sp, all_tracks)
        all_tracks.extend(x for x in recommended_tracks if x not in all_tracks)

        user_id = sp.me()["id"]
        tastified_playlist = create_tastified_playlist(sp, user_id, playlist)
        add_tracks_to_playlist(sp, user_id, tastified_playlist, all_tracks)

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()
