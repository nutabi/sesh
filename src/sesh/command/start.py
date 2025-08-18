import click
from sesh.store import Store
from sesh.tag import Tag


class StartArg(click.ParamType):
    name = "start-arg"

    def convert(self, value, param, ctx):
        if isinstance(value, Tag):
            return value

        if value.startswith("+"):
            if Tag.validate_tag_name(value[1:]):
                return Tag(value[1:])
            self.fail(f"Invalid tag: {value}")

        return value


def handle_start(store: Store, tags: list[Tag], arg: tuple[str | Tag]) -> None:
    # combine tags
    tags += [t for t in arg if isinstance(t, Tag)]

    # make title
    title = " ".join(map(str, arg))

    # delegate work to store
    store.start_sesh(title, tags)
