import click
from .tag import Tag


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


def handle_start(tags: list[Tag], description: tuple[str | Tag]) -> None:
    click.echo("with explicit tags: " + " ".join(map(lambda t: str(t), tags)))
    click.echo(
        "with inline tags: "
        + " ".join(
            map(lambda x: str(x), filter(lambda x: isinstance(x, Tag), description))
        )
    )
    click.echo("with description: " + " ".join(map(lambda x: str(x), description)))
