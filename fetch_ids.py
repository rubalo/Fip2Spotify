import urllib.parse
from pathlib import Path

import pandas as pd
import spotipy

from config import Config, init_spotify_client


class FipError(Exception):
    pass


def format_search_query(track: str, artist: str) -> str:
    """
    Format search query for Spotify API, make it url safe
    """
    # return urllib.parse.quote(f"track:{track} artist:{artist}")

    # Limit too long artists names
    artist = " ".split(artist)
    if len(artist) > 4:
        artist = artist[:2]
    artist = " ".join(artist)

    q = f'track:"{track}" artist:"{artist}"'
    q = q.replace("'", "")
    return q
    # return urllib.parse.quote(q)


def parse_titles_file(filepath: str) -> pd.DataFrame:
    """
    Parse csv titles file with the following fields:
    * date
    * title
    * artist
    """
    return pd.read_csv(filepath, sep=";")


def log_failed_search(track: str, artist: str, file_path: Path) -> None:
    """
    Log failed search
    """
    with open(file_path, "a") as f:
        f.write(f"{track} - {artist}\n")


def search_spotify(spotify: spotipy.Spotify, query: str) -> dict:
    """
    Search on Spotify API
    """
    try:
        results = spotify.search(q=query, type="track", market="FR")
        return results["tracks"]["items"][0]["id"]
    except (spotipy.exceptions.SpotifyException, IndexError):
        raise FipError("Could not search on Spotify API")


def search_track(spotify, track: str, artist: str, failed_search_file: Path) -> str:
    """
    Search for a track on Spotify API
    """
    qsearch = format_search_query(track, artist)
    try:
        return search_spotify(spotify, qsearch)
    except FipError:
        print(f"Could not find {track} from {artist}")
        log_failed_search(track, artist, failed_search_file)
        return pd.NA


def fetch_tracks_ids(conf: Config) -> None:
    spotify = init_spotify_client(conf)

    print(f"Parsing titles from {conf.tracks_file_name}")
    titles = parse_titles_file(conf.tracks_file)

    ids = titles.apply(
        lambda x: search_track(
            spotify, x["titre"], x["artiste"], conf.failed_searches_file
        ),
        axis=1,
    )

    titles["id"] = ids

    titles.to_csv(conf.tracks_id_file, sep=";")


if __name__ == "__main__":
    conf = Config()
    fetch_tracks_ids()
