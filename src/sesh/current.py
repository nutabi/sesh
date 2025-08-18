from dataclasses import dataclass
import json
from pathlib import Path
from whenever import Instant

from sesh.error import InvalidSeshDataError, SessionStorageError
from sesh.tag import Tag


@dataclass
class CurrentSesh:
    title: str
    tags: list[Tag]
    start_time: Instant


class CurrentManager:
    def __init__(self, current_path: Path) -> None:
        self.current_path = current_path

    def pop(self) -> None | CurrentSesh:
        current_session = self.read()
        if current_session is not None:
            try:
                self.current_path.unlink()
            except (OSError, IOError) as e:
                raise SessionStorageError(f"Failed to remove session file: {e}")
        return current_session

    def read(self) -> None | CurrentSesh:
        try:
            with self.current_path.open("r") as f:
                data = json.load(f)

            # Ensure the root object is a dict
            if not isinstance(data, dict):
                raise ValueError("Data must be a JSON object.")

            return CurrentManager.decode_session(data)
        except FileNotFoundError:
            return None
        except (OSError, IOError) as e:
            raise SessionStorageError(f"Failed to read session file: {e}")
        except json.JSONDecodeError as e:
            raise SessionStorageError(f"Invalid JSON in session file: {e}")
        except ValueError as e:
            raise SessionStorageError(f"Invalid session file format: {e}")
        except InvalidSeshDataError:
            # Re-raise this specific error
            raise
        except Exception as e:
            raise SessionStorageError(f"Unexpected error reading session file: {e}")

    def write(self, sesh: CurrentSesh) -> None:
        try:
            with self.current_path.open("w") as f:
                json.dump(sesh, f, default=CurrentManager.encode_session)
        except (OSError, IOError) as e:
            raise SessionStorageError(f"Failed to write session file: {e}")
        except (TypeError, ValueError) as e:
            raise SessionStorageError(f"Failed to serialize session data: {e}")

    @staticmethod
    def encode_session(obj: CurrentSesh) -> dict:
        return {
            "title": obj.title,
            "tags": [str(t) for t in obj.tags],
            "start_time": obj.start_time.round().format_common_iso(),
        }

    @staticmethod
    def decode_session(data: dict) -> None | CurrentSesh:
        # No active current Sesh
        if not data:
            return None

        # Invalid Sesh data
        if "title" not in data or "tags" not in data or "start_time" not in data:
            raise InvalidSeshDataError()

        return CurrentSesh(
            title=data["title"],
            tags=[Tag(name) for name in data["tags"]],
            start_time=Instant.parse_common_iso(data["start_time"]),
        )
