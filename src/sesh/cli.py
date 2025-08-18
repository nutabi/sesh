from pathlib import Path
import click

from sesh.command.reset import handle_reset
from sesh.error import DatabaseError, MigrationError, SessionStorageError, SeshInProgressError
from sesh.store import Store
from sesh.tag import TagOption, Tag
from sesh.command.start import StartArg, handle_start
from sesh.command.stop import handle_stop
from sesh.command.status import handle_status


@click.group()
@click.pass_context
def main(ctx):
    try:
        ctx.obj = Store(Path.cwd() / ".sesh")
    except (DatabaseError, MigrationError) as e:
        click.echo(f"Error: Failed to initialize store ({e})", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: An unexpected error occurred during initialization ({e})", err=True)
        raise click.Abort()


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
        click.echo("Error: No argument provided for start command.", err=True)
        raise click.Abort()

    try:
        handle_start(store, tags, arg)
        click.echo("Sesh started successfully.")
    except SeshInProgressError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
    except DatabaseError as e:
        click.echo(f"Error: Database error while starting Sesh ({e})", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: An unexpected error occurred while starting the Sesh ({e})", err=True)
        raise click.Abort()


@main.command()
@click.option(
    "-t", "--tag", "tags", type=TagOption(), help="Tags to be assigned", default=[]
)
@click.argument("details", default="")
@click.pass_obj
def stop(store: Store, tags: list[Tag], details: str):
    """Stop the current Sesh"""
    handle_stop(store, tags, details)


@main.command()
@click.pass_obj
def status(store: Store):
    """Show current Sesh's status"""
    handle_status(store)


@main.command()
@click.option("--yes", "-y", is_flag=True, help="Confirm reset", prompt=True)
@click.pass_obj
def reset(store: Store, yes: bool):
    """Reset the current Sesh"""
    if not yes:
        click.echo("Reset cancelled.")
        return
    
    try:
        handle_reset(store)
        click.echo("Reset completed successfully.")
    except SessionStorageError as e:
        click.echo(f"Error: Failed to clear current session ({e})", err=True)
        raise click.Abort()
    except DatabaseError as e:
        click.echo(f"Error: Database error during reset ({e})", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: An unexpected error occurred during reset ({e})", err=True)
        raise click.Abort()
