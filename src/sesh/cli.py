from pathlib import Path
import click


from sesh.store import Store
from sesh.tag import TagOption, Tag
from sesh.command.start import StartArg, handle_start
from sesh.command.stop import handle_stop
from sesh.command.status import handle_status


@click.group()
@click.pass_context
def main(ctx):
    ctx.obj = Store(Path.cwd() / ".sesh")
    pass


@main.command()
@click.option(
    "-t", "--tag", "tags", type=TagOption(), help="Tags to be assigned", default=[]
)
@click.argument("arg", nargs=-1, type=StartArg())
@click.pass_obj
def start(store: Store, tags: list[Tag], arg: tuple[str | Tag]):
    """Start a new Sesh

    ARG is a tag-enabled title. It serves as the title for the new Sesh.
    However, if a word is prefixed with a plus (e.g. +tag), it will also be
    treated and included as an inline tag.

    For example, when you run `sesh start do +maths homework`, the title will
    be "do maths homework" and the tag is "maths".
    """
    # check that arg is non-empty
    if not arg:
        click.echo("Error: No argument provided.", err=True)
        return

    handle_start(store, tags, arg)


@main.command()
def stop():
    """Stop the current Sesh"""
    handle_stop()


@main.command()
def status():
    """Show current Sesh's status"""
    handle_status()
