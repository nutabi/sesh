import click


class Tag:
    def __init__(self, name: str, display_name: str | None = None):
        if Tag.validate_tag_name(name):
            self.name = name
        else:
            raise ValueError(f"Invalid tag: {name}")

        if display_name is None:
            self.display_name = Tag.make_display_name(name)
        else:
            self.display_name = display_name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.display_name

    @staticmethod
    def make_display_name(name):
        return " ".join(name.split("_"))

    @staticmethod
    def validate_tag_name(tag):
        return (
            len(tag) >= 1
            and all(c.isdigit() or c == "-" or ("a" <= c <= "z") for c in tag)
            and tag[0] != "-"
            and tag[-1] != "-"
        )


class TagOption(click.ParamType):
    name = "tag"

    def convert(self, value, param, ctx):
        if isinstance(value, list):
            return value

        tags = []
        for tag in value.lower().split(","):
            tag = tag.strip()
            if Tag.validate_tag_name(tag):
                tags.append(Tag(tag))
            else:
                self.fail(f"{tag} is not a valid tag", param, ctx)
        return tags
