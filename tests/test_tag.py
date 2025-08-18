import pytest
import click
from click.testing import CliRunner
from sesh.error import InvalidTagError
from sesh.tag import Tag, TagOption


class TestTag:
    """Test cases for the Tag class."""

    def test_valid_tag_creation(self):
        """Test creating valid tags."""
        tag = Tag("python")
        assert tag.name == "python"
        assert tag.display_name == "python"

    def test_tag_with_hyphens(self):
        """Test tag creation with hyphens."""
        tag = Tag("machine-learning")
        assert tag.name == "machine-learning"
        assert tag.display_name == "machine learning"

    def test_tag_with_digits(self):
        """Test tag creation with digits."""
        tag = Tag("python3")
        assert tag.name == "python3"
        assert tag.display_name == "python3"

    def test_tag_with_multiple_hyphens(self):
        """Test tag with multiple hyphens creates proper display name."""
        tag = Tag("web-api-development")
        assert tag.name == "web-api-development"
        assert tag.display_name == "web api development"

    def test_custom_display_name(self):
        """Test tag creation with custom display name."""
        tag = Tag("ml", "Machine Learning")
        assert tag.name == "ml"
        assert tag.display_name == "Machine Learning"

    def test_str_representation(self):
        """Test string representation returns internal name."""
        tag = Tag("web-dev")
        assert str(tag) == "web-dev"

    def test_repr_representation(self):
        """Test repr returns display name."""
        tag = Tag("web-dev")
        assert repr(tag) == "web dev"

    def test_invalid_tag_empty_string(self):
        """Test that empty string raises InvalidTagError."""
        with pytest.raises(InvalidTagError, match="Invalid tag provided"):
            Tag("")

    def test_invalid_tag_starts_with_hyphen(self):
        """Test that tag starting with hyphen raises InvalidTagError."""
        with pytest.raises(InvalidTagError, match="Invalid tag: -python"):
            Tag("-python")

    def test_invalid_tag_ends_with_hyphen(self):
        """Test that tag ending with hyphen raises InvalidTagError."""
        with pytest.raises(InvalidTagError, match="Invalid tag: python-"):
            Tag("python-")

    def test_invalid_tag_uppercase_letters(self):
        """Test that uppercase letters raise InvalidTagError."""
        with pytest.raises(InvalidTagError, match="Invalid tag: Python"):
            Tag("Python")

    def test_invalid_tag_special_characters(self):
        """Test that special characters raise InvalidTagError."""
        with pytest.raises(InvalidTagError, match="Invalid tag: python!"):
            Tag("python!")

    def test_invalid_tag_underscore(self):
        """Test that underscores raise InvalidTagError."""
        with pytest.raises(InvalidTagError, match="Invalid tag: python_web"):
            Tag("python_web")

    def test_invalid_tag_spaces(self):
        """Test that spaces raise InvalidTagError."""
        with pytest.raises(InvalidTagError, match="Invalid tag: web dev"):
            Tag("web dev")

    def test_validate_tag_name_valid_cases(self):
        """Test validate_tag_name static method with valid inputs."""
        assert Tag.validate_tag_name("python") is True
        assert Tag.validate_tag_name("python3") is True
        assert Tag.validate_tag_name("web-dev") is True
        assert Tag.validate_tag_name("a") is True
        assert Tag.validate_tag_name("123") is True

    def test_validate_tag_name_invalid_cases(self):
        """Test validate_tag_name static method with invalid inputs."""
        assert Tag.validate_tag_name("") is False
        assert Tag.validate_tag_name("-python") is False
        assert Tag.validate_tag_name("python-") is False
        assert Tag.validate_tag_name("Python") is False
        assert Tag.validate_tag_name("python!") is False
        assert Tag.validate_tag_name("python_web") is False
        assert Tag.validate_tag_name("web dev") is False

    def test_make_display_name(self):
        """Test make_display_name static method."""
        assert Tag.make_display_name("python") == "python"
        assert Tag.make_display_name("web-dev") == "web dev"
        assert Tag.make_display_name("machine-learning-ai") == "machine learning ai"


class TestTagOption:
    """Test cases for the TagOption class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.tag_option = TagOption()

    def test_single_tag_conversion(self):
        """Test converting single tag string."""
        result = self.tag_option.convert("python", None, None)
        assert len(result) == 1
        assert isinstance(result[0], Tag)
        assert result[0].name == "python"

    def test_multiple_tags_conversion(self):
        """Test converting comma-separated tags."""
        result = self.tag_option.convert("python,web-dev,api", None, None)
        assert len(result) == 3
        assert all(isinstance(tag, Tag) for tag in result)
        assert result[0].name == "python"
        assert result[1].name == "web-dev"
        assert result[2].name == "api"

    def test_tags_with_spaces_stripped(self):
        """Test that whitespace around tags is stripped."""
        result = self.tag_option.convert("python, web-dev , api", None, None)
        assert len(result) == 3
        assert result[0].name == "python"
        assert result[1].name == "web-dev"
        assert result[2].name == "api"

    def test_uppercase_converted_to_lowercase(self):
        """Test that uppercase input is converted to lowercase."""
        result = self.tag_option.convert("PYTHON,Web-Dev", None, None)
        assert len(result) == 2
        assert result[0].name == "python"
        assert result[1].name == "web-dev"

    def test_list_input_returned_as_is(self):
        """Test that list input is returned unchanged."""
        input_tags = [Tag("python"), Tag("web-dev")]
        result = self.tag_option.convert(input_tags, None, None)
        assert result is input_tags

    def test_invalid_tag_raises_error(self):
        """Test that invalid tag names raise click.BadParameter via self.fail()."""
        # Test by using Click's testing framework
        from click.testing import CliRunner

        @click.command()
        @click.option("--tags", type=TagOption())
        def test_cmd(tags):
            pass

        runner = CliRunner()
        result = runner.invoke(test_cmd, ["--tags", "invalid-tag-"])
        assert result.exit_code != 0
        assert "Invalid tag (invalid-tag-)" in result.output

    def test_empty_tag_skipped(self):
        """Test that empty tags are skipped gracefully."""
        result = self.tag_option.convert("python,,web-dev", None, None)
        assert len(result) == 2
        assert result[0].name == "python"
        assert result[1].name == "web-dev"

    def test_multiple_empty_tags_skipped(self):
        """Test that multiple empty tags are all skipped."""
        result = self.tag_option.convert("python,,,web-dev,,", None, None)
        assert len(result) == 2
        assert result[0].name == "python"
        assert result[1].name == "web-dev"

    def test_all_empty_tags_returns_empty_list(self):
        """Test that input with only empty tags returns empty list."""
        result = self.tag_option.convert(",,", None, None)
        assert len(result) == 0

    def test_mixed_valid_invalid_tags(self):
        """Test behavior with mix of valid and invalid tags."""
        from click.testing import CliRunner

        @click.command()
        @click.option("--tags", type=TagOption())
        def test_cmd(tags):
            pass

        runner = CliRunner()
        result = runner.invoke(test_cmd, ["--tags", "python,Invalid_Tag,web-dev"])
        assert result.exit_code != 0

    def test_name_attribute(self):
        """Test that TagOption has correct name attribute."""
        assert self.tag_option.name == "tag"


class TestTagOptionIntegration:
    """Integration tests for TagOption with Click commands."""

    def test_click_command_integration(self):
        """Test TagOption integration with Click commands."""

        @click.command()
        @click.option("--tags", type=TagOption())
        def test_command(tags):
            click.echo(f"Tags: {[str(tag) for tag in tags]}")

        runner = CliRunner()
        result = runner.invoke(test_command, ["--tags", "python,web-dev"])

        assert result.exit_code == 0
        assert "Tags: ['python', 'web-dev']" in result.output

    def test_click_command_invalid_tag(self):
        """Test TagOption error handling in Click commands."""

        @click.command()
        @click.option("--tags", type=TagOption())
        def test_command(tags):
            click.echo(f"Tags: {[str(tag) for tag in tags]}")

        runner = CliRunner()
        result = runner.invoke(test_command, ["--tags", "python,invalid-tag-"])

        assert result.exit_code != 0
        assert "Invalid tag (invalid-tag-)" in result.output
