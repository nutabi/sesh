from dataclasses import dataclass
import json
from pathlib import Path
from whenever import Instant

from sesh.error import InvalidSeshDataError


@dataclass
class CurrentSesh:
    title: str
    tags: list[str]
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
        return json.load(
            self.current_path.open("r"), object_hook=CurrentManager.decode_session
        )

    def write(self, sesh: CurrentSesh) -> None:
        with self.current_path.open("w") as f:
            json.dump(sesh, f, default=CurrentManager.encode_session)

    @staticmethod
    def encode_session(obj: CurrentSesh) -> dict:
        if not isinstance(obj, CurrentSesh):
            raise TypeError("Expected CurrentSesh instance")

        return {
            "title": obj.title,
            "tags": obj.tags,
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
            tags=data["tags"],
            start_time=Instant.parse_common_iso(data["start_time"]),
        )
