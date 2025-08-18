import click

from sesh.error import DatabaseError, NoActiveSeshError
from sesh.parser.tag import Tag
from sesh.store import Store


def handle_stop(store: Store, tags: list[Tag], details: str) -> None:
    """Handle the stop command to end the current Sesh."""
    try:
        uid = store.end_sesh(details, tags)
        click.echo(f"Sesh stopped successfully ({uid})")
    except NoActiveSeshError:
        click.echo("Error: No active Sesh to stop", err=True)
        raise click.Abort()
    except DatabaseError as e:
        click.echo(f"Error: Database error while stopping Sesh ({e})", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(
            f"Error: An unexpected error occurred while stopping the Sesh ({e})",
            err=True,
        )
        raise click.Abort()
