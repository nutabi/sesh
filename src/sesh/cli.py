# File: src/sesh/cli.py
#
# Description: This file contains the main CLI application. It handles
# user input, processes it and passes it on to the appropriate handlers.

import click

from .command_utils.tag import TagOption, Tag
from .command_utils.start import StartArg, handle_start


@click.group()
def main():
    pass


@main.command()
@click.option("-t", "--tag", "tags", type=TagOption(), help="Tags to be assigned")
@click.argument("description", nargs=-1, type=StartArg())
def start(tags: list[Tag], description: tuple[str | Tag]):
    """Start a new session"""
    click.echo("start sesh")
    handle_start(tags, description)


@main.command(help="Stop the current session")
def stop():
    click.echo("stop sesh")


@main.command(help="Show current session's status")
def status():
    click.echo("show sesh status")
