from pathlib import Path
import click

from sesh.command.reset import handle_reset
from sesh.error import (
    DatabaseError,
    MigrationError,
    SessionStorageError,
    SeshInProgressError,
)
from sesh.store import Store
from sesh.tag import TagOption, Tag
from sesh.command.start import StartArg, handle_start
from sesh.command.stop import handle_stop
from sesh.command.status import handle_status


@click.group()
@click.pass_context
def main(ctx):
    """Sesh - A simple session tracking CLI application.

    Track your work sessions with titles, tags, and timing. Start a session,
    work on your task, then stop to record your progress. Use tags to organize
    and categorize your sessions for better productivity insights.

    \b
    Examples:
        sesh start working on +python +cli project
        sesh status
        sesh stop "completed the feature"
    """
    try:
        ctx.obj = Store(Path.cwd() / ".sesh")
    except (DatabaseError, MigrationError) as e:
        click.echo(f"Error: Failed to initialize store ({e})", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(
            f"Error: An unexpected error occurred during initialization ({e})", err=True
        )
        raise click.Abort()


@main.command()
@click.option(
    "-t",
    "--tag",
    "tags",
    type=TagOption(),
    help="Additional tags to assign (comma-separated)",
    default=[],
)
@click.argument("arg", nargs=-1, type=StartArg())
@click.pass_obj
def start(store: Store, tags: list[Tag], arg: tuple[str | Tag]):
    """Start a new work session.

    Begin tracking a new session with a descriptive title. Words in the title
    can include inline tags by prefixing them with '+' (e.g., +python, +bug-fix).
    These tagged words will be extracted as tags while remaining part of the title.

    ARG: The session title with optional inline tags

    \b
    Examples:
        sesh start working on documentation
        sesh start fix +bug in authentication system
        sesh start +python +web-dev building new API
        sesh start -t urgent,review code review session

    Tags help organize and categorize your sessions for better tracking.
    Use lowercase letters, numbers, and hyphens only in tag names.
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
        click.echo(
            f"Error: An unexpected error occurred while starting the Sesh ({e})",
            err=True,
        )
        raise click.Abort()


@main.command()
@click.option(
    "-t",
    "--tag",
    "tags",
    type=TagOption(),
    help="Additional tags to add when stopping (comma-separated)",
    default=[],
)
@click.argument("details", default="")
@click.pass_obj
def stop(store: Store, tags: list[Tag], details: str):
    """Stop the current work session.

    End the currently active session and save it to your session history.
    Optionally provide completion details and additional tags to better
    categorize and document what was accomplished.

    DETAILS: Optional description of what was completed or achieved

    \b
    Examples:
        sesh stop
        sesh stop "completed user authentication feature"
        sesh stop -t completed,tested "finished API endpoints"
        sesh stop "need to continue tomorrow" -t incomplete

    Additional tags specified with -t will be merged with any existing
    tags from when the session was started.
    """
    handle_stop(store, tags, details)


@main.command()
@click.pass_obj
def status(store: Store):
    """Display information about the current work session.

    Shows details about the currently active session including title,
    assigned tags, start time, and elapsed duration. If no session is
    active, displays a helpful message.

    \b
    Examples:
        sesh status

    \b
    Output includes:
        - Session title
        - Assigned tags
        - Start time (formatted for your timezone)
        - Elapsed time (human-readable format)

    Use this command to quickly check your current session progress
    or verify that a session is running as expected.
    """
    handle_status(store)


@main.command()
@click.option(
    "--yes",
    "-y",
    is_flag=True,
    help="Skip confirmation prompt",
    prompt="Are you sure you want to reset all data?",
)
@click.pass_obj
def reset(store: Store, yes: bool):
    """Reset all session data and clear current session.

    WARNING: This is a destructive operation that will permanently delete
    ALL session history and stop any currently active session.

    \b
    This command will:
        - Stop the current session (if active) without saving
        - Delete all completed session records
        - Clear all tag data
        - Reset the database to empty state

    \b
    Examples:
        sesh reset          # Prompts for confirmation
        sesh reset -y       # Skip confirmation prompt

    Use this when you want to start fresh or clear out test data.
    There is no way to recover deleted data after reset.
    """
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
