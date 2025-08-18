import click

from sesh.error import DatabaseError, SeshInProgressError, SessionStorageError
from sesh.parser.tag import Tag
from sesh.store import Store


class StartArg(click.ParamType):
    name = "start-arg"

    def convert(self, value, param, ctx):
        if isinstance(value, Tag):
            return value

        if value.startswith("+"):
            if Tag.validate_tag_name(value[1:]):
                return Tag(value[1:])
            # Use UsageError for cleaner error messages
            raise click.UsageError(f"Invalid inline tag ({value[1:]})")

        return value


def handle_start(store: Store, tags: list[Tag], arg: tuple[str | Tag]) -> None:
    try:
        # combine tags
        tags += [t for t in arg if isinstance(t, Tag)]

        # make title
        title = " ".join(map(str, arg))

        # delegate work to store
        store.start_sesh(title, tags)
    except SeshInProgressError:
        # Re-raise this specific error to be handled by CLI
        raise
    except (DatabaseError, SessionStorageError):
        # Re-raise these errors to be handled by CLI
        raise
    except Exception as e:
        # Convert any unexpected errors to DatabaseError for consistency
        raise DatabaseError(f"Failed to start session: {e}")
