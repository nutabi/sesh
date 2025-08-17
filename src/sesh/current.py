from dataclasses import dataclass
import json
from pathlib import Path
from whenever import Instant

from sesh.error import InvalidSeshDataError
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
            self.current_path.unlink()
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
        except (json.JSONDecodeError, ValueError):
            raise InvalidSeshDataError("Invalid session format.")

    def write(self, sesh: CurrentSesh) -> None:
        with self.current_path.open("w") as f:
            json.dump(sesh, f, default=CurrentManager.encode_session)

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
