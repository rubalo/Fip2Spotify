import click

from config import Config
from create_playlist import populate_playlist
from fetch_ids import fetch_tracks_ids
from fetch_tracks import fetch_tracks_info
from parse_tracks import parse_tracks_info


@click.group()
@click.pass_context
def cli(ctx) -> None:
    """
    Trying to find a song from FIP ? This program will fetch tracks for about the last week and creates a Spotify playlist with them.
    Limit to songs aired between 7am and 0am, cf parse_track.py
    Some songs that can't be found using the spotify search api will be logged in data/failed_searches.log.
    The playlist will be named FIP -  YYYYmmdd_HHMMSS
    """
    ctx.ensure_object(dict)
    ctx.obj["CONF"] = Config()


@cli.command(help="Fetch tracks from the site https://www.playlisteradio.com/fip-radio")
@click.pass_context
def fetch_tracks(ctx) -> None:
    """
    Fetch tracks from the site https://www.playlisteradio.com/fip-radio

    :param ctx: Context object
    :type ctx: click.Context
    """
    conf = ctx.obj["CONF"]
    fetch_tracks_info(conf.data_folder)


@cli.command(help="Parse tracks from the fetched data")
@click.pass_context
def parse_tracks(ctx) -> None:
    """
    Parse tracks from the fetched data

    :param ctx: Context object
    :type ctx: click.Context
    """
    conf = ctx.obj["CONF"]
    parse_tracks_info(conf)


@cli.command(help="Find track ids on Spotify")
@click.pass_context
def fetch_ids(ctx) -> None:
    """
    Find track ids on Spotify

    :param ctx: Context object
    :type ctx: click.Context
    """
    conf = ctx.obj["CONF"]
    fetch_tracks_ids(conf)


@cli.command(help="Create a spotify playlist with the tracks found")
@click.pass_context
def create_playlist(ctx) -> None:
    """
    Create a spotify playlist with the tracks found

    :param ctx: Context object
    :type ctx: click.Context
    """
    conf = ctx.obj["CONF"]
    populate_playlist(conf)


@cli.command(help="Fetch, parse, find ids and create a playlist")
@click.pass_context
def all(ctx) -> None:
    """
    Fetch, parse, find ids and create a playlist

    :param ctx: Context object
    :type ctx: click.Context
    """
    conf = ctx.obj["CONF"]
    fetch_tracks_info(conf.data_folder)
    parse_tracks_info(conf)
    fetch_tracks_ids(conf)
    populate_playlist(conf)


if __name__ == "__main__":
    cli(obj={})
