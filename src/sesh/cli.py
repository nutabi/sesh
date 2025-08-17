import click


from sesh.tag import TagOption, Tag
from sesh.command.start import StartArg, handle_start
from sesh.command.stop import handle_stop
from sesh.command.status import handle_status


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
    handle_stop()


@main.command()
def status():
    """Show current session's status"""
    handle_status()
