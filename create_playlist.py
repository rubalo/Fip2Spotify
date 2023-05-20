import datetime

import pandas as pd

from config import Config, init_spotify_client


def add_track_to_playlist(spotify, playlist_id: str, tracks_id: list) -> None:
    """
    Add a track to a playlist
    """
    spotify.user_playlist_add_tracks(
        user=spotify.me()["id"], playlist_id=playlist_id, tracks=tracks_id
    )


def parse_titles_id_file(filepath: str) -> pd.DataFrame:
    """
    Parse csv titles file with the following fields:
    * date
    * title
    * artist
    * id
    """
    return pd.read_csv(filepath, sep=";")


def create_playlist(spotify, name: str) -> str:
    """
    Create a playlist on Spotify
    """
    user = spotify.me()["id"]
    return spotify.user_playlist_create(user=user, name=name, public=False)["id"]


def populate_playlist(config: Config) -> None:
    titles = parse_titles_id_file(config.tracks_id_file)

    spotify = init_spotify_client(config)

    ids = list(set(titles["id"].dropna().tolist()))

    playlist_id = create_playlist(spotify, config.playlist_name)

    for i in range(0, len(ids), 100):
        add_track_to_playlist(spotify, playlist_id, ids[i : i + 100])


if __name__ == "__main__":
    populate_playlist(Config())
