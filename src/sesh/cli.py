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
    handle_start(tags, description)


@main.command()
def stop():
    """Stop the current session"""


@main.command()
def status():
    """Show current session's status"""
