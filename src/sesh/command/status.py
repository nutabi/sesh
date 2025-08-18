import click
from whenever import Instant, TimeDelta

from sesh.error import SessionStorageError
from sesh.store import Store


def format_start_time(start_time: Instant) -> str:
    return (
        start_time.to_system_tz().round().py_datetime().strftime("%A, %d %B, %H:%M:%S")
    )


def format_elapsed_time(duration: TimeDelta) -> str:
    (h, m, s, _) = duration.in_hrs_mins_secs_nanos()
    if h == 0:
        if m == 0:
            return f"{s}s"
        return f"{m}m {s}s"
    return f"{h}h {m}m {s}s"


def handle_status(store: Store) -> None:
    try:
        current = store.current_manager.read()
        if current is None:
            click.echo("No active Sesh")
        else:
            click.echo(f"Active Sesh: {current.title}")
            click.echo(f"Tags: {', '.join(str(tag) for tag in current.tags)}")
            click.echo(f"Start time: {format_start_time(current.start_time)}")
            click.echo(
                f"Elapsed time: {format_elapsed_time(Instant.now() - current.start_time)}"
            )
    except SessionStorageError as e:
        click.echo(f"Error: Failed to read session data ({e})", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: An unexpected error occurred while reading status ({e})", err=True)
        raise click.Abort()
