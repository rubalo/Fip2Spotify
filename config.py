import datetime
from pathlib import Path

import git
import spotipy
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

scope = "playlist-modify-private"


class Config:
    """
    Config class to load dotenv file
    """

    def __init__(self) -> None:
        git_repo = git.Repo(".", search_parent_directories=True)
        git_root = git_repo.git.rev_parse("--show-toplevel")

        env = dotenv_values(git_root + "/.env")
        self._read_env(env, "client_id", "SPOTIFY_CLIENT_ID")
        self._read_env(env, "client_secret", "SPOTIFY_CLIENT_SECRET")
        self._read_env(env, "redirect_uri", "SPOTIFY_REDIRECT_URI", mandatory=False)
        self._read_env(env, "_data_path", "DATA_PATH", mandatory=False)
        self._read_env(env, "tracks_file_name", "TRACKS_FILE_NAME", mandatory=False)
        self._read_env(
            env, "tracks_id_file_name", "TRACKS_ID_FILE_NAME", mandatory=False
        )
        self._read_env(
            env,
            "failed_searches_file_name",
            "FAILED_SEARCHES_FILE_NAME",
            mandatory=False,
        )
        self.playlist_name = self._create_playlist_name()

        self._validate_env()

    def _create_playlist_name(self) -> str:
        now = datetime.datetime.now()
        return f"FIP - {now.strftime('%Y%m%d_%H%M%S')}"

    def _read_env(
        self,
        env: dotenv_values,
        var_string: str,
        env_string: str,
        mandatory: bool = True,
    ) -> None:
        """
        Read environment variables
        """
        try:
            self.__setattr__(var_string, env[env_string])
        except KeyError as e:
            if mandatory:
                raise ValueError(f"{var_string} is not set in the .env file")
            else:
                self.__setattr__(var_string, None)

    @property
    def data_folder(self) -> str:
        return Path(self._data_path).resolve()

    @property
    def tracks_file(self) -> str:
        return (Path(self._data_path) / self.tracks_file_name).resolve()

    @property
    def tracks_id_file(self) -> str:
        return (Path(self._data_path) / self.tracks_id_file_name).resolve()

    @property
    def failed_searches_file(self) -> str:
        return (Path(self._data_path) / self.failed_searches_file_name).resolve()

    def _validate_env(self) -> None:
        """
        Validate environment variables
        """
        if not self.client_id:
            raise ValueError("SPOTIFY_CLIENT_ID is not set in the .env file")

        if not self.client_secret:
            raise ValueError("SPOTIFY_CLIENT_SECRET is not set in the .env file")

        if not self.redirect_uri:
            self.redirect_uri = "http://127.0.0.1"

        if not self._data_path:
            self._data_path = "data/"

        if not Path(self._data_path).exists():
            Path(self._data_path).mkdir(parents=True, exist_ok=True)

        if not self.tracks_file_name:
            self.tracks_file_name = "tracks.csv"

        if not self.tracks_id_file_name:
            self.tracks_id_file_name = "tracks_id.csv"

        if not self.failed_searches_file_name:
            self.failed_searches_file_name = "failed_searches.log"

    def _create_playlist(spotify, name: str) -> str:
        """
        Create a playlist on Spotify
        """
        now = datetime.datetime.now()
        name = f"FIP - {name} - {now.strftime('%Y%m%d')}"


def init_spotify_client(conf: Config) -> spotipy.Spotify:
    """
    Initialize Spotify client
    """
    client_credentials_manager = SpotifyClientCredentials(
        client_id=conf.client_id, client_secret=conf.client_secret
    )
    auth_manager = SpotifyOAuth(
        client_id=conf.client_id,
        client_secret=conf.client_secret,
        redirect_uri=conf.redirect_uri,
        scope=scope,
    )

    return spotipy.Spotify(
        client_credentials_manager=client_credentials_manager, auth_manager=auth_manager
    )
