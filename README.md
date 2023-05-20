# Fip2Spotify


## Description

Fetch about one week of tracks from fip and creates a spotify playlist from them
Personnal project to discover the spotify api


## Usage 

Create a developper app from spotify : 
https://developer.spotify.com/dashboard

Create a .env file at the root of the repo containing : 
```zsh
  cat .env
  SPOTIFY_CLIENT_ID=<ID_CLIENT>
  SPOTIFY_CLIENT_SECRET=<SECRET>
```

Install requirements.txt

```zsh
  pip install -r requirements.txt
```

Run the main file

```txt
Usage: main.py [OPTIONS] COMMAND [ARGS]...

  Trying to find a song from FIP radio ? This program will fetch tracks for about
  the last week and creates a Spotify playlist with them. Limit to songs aired
  between 7am and 0am, cf parse_track.py Some songs that can't be found using
  the spotify search api will be logged in data/failed_searches.log. The
  playlist will be named FIP -  YYYYmmdd_HHMMSS

Options:
  --help  Show this message and exit.

Commands:
  all              Fetch, parse, find ids and create a playlist
  create-playlist  Create a spotify playlist with the tracks found
  fetch-ids        Find track ids on Spotify
  fetch-tracks     Fetch tracks from the site...
  parse-tracks     Parse tracks from the fetched data
```

Run commands in order : 
* Fetch tracks
* Parse tracks
* Fetch ids
* Create playlist

## Links

* https://www.radiofrance.fr/fip
* https://www.playlisteradio.com/fip-radio
