from pathlib import Path
import sqlite3

from whenever import Instant

from sesh.current import CurrentManager, CurrentSesh
from sesh.error import MigrationError, NoActiveSeshError, SeshInProgressError
from sesh.tag import Tag


DATA_SQLITE = "store.db"
CURRENT_SESSION_JSON = "current.json"


class Store:
    def __init__(self, root: Path) -> None:
        self.db_path = root / DATA_SQLITE
        self.current_path = root / CURRENT_SESSION_JSON

        self.init_root(root)

        self.db_conn = sqlite3.connect(self.db_path)
        self.current_manager = CurrentManager(self.current_path)

    def init_root(self, root: Path) -> None:
        # create directories and empty file
        root.mkdir(parents=True, exist_ok=True)
        self.db_path.touch(exist_ok=True)

        # run migration
        self.migrate()

    def migrate(self) -> None:
        """Run all migration scripts in alphabetical order from the migrations folder."""
        migrations_dir = Path.cwd() / "migrations"

        if not migrations_dir.exists():
            return  # No migrations directory, skip

        # get all .sql files in migrations directory
        migration_files = sorted(migrations_dir.glob("*.sql"))

        # open database connection
        db_conn = sqlite3.connect(self.db_path)

        # execute each migration file
        for migration_file in migration_files:
            try:
                with open(migration_file, "r") as f:
                    migration_sql = f.read()

                # Execute the migration SQL
                db_conn.executescript(migration_sql)
                db_conn.commit()
            except Exception:
                raise MigrationError()

    def start_sesh(
        self,
        title: str,
        tags: list[Tag],
    ) -> None:
        # check that no active Sesh
        if self.current_manager.read() is not None:
            raise SeshInProgressError()

        # create new Sesh
        current = CurrentSesh(title, tags, Instant.now())

        # write Sesh to file
        self.current_manager.write(current)

    def end_sesh(self, details: str, tags: list[Tag]) -> str:
        # pop current Sesh
        current_sesh = self.current_manager.pop()

        # error when no active Sesh
        if current_sesh is None:
            raise NoActiveSeshError()

        # merge tags
        current_sesh.tags = list(set(tags).union(current_sesh.tags))

        # insert tags and get tag ids
        cur = self.db_conn.cursor()
        tag_ids = []
        if current_sesh.tags:  # Only insert tags if the list is not empty
            cur.executemany(
                "INSERT OR IGNORE INTO tag (tag_name) VALUES (?)",
                [(str(tag),) for tag in current_sesh.tags],
            )
            cur.execute(
                "SELECT tag_id FROM tag WHERE tag_name IN ({})".format(
                    ",".join("?" * len(current_sesh.tags))
                ),
                [str(tag) for tag in current_sesh.tags],
            )
            tag_ids = [row[0] for row in cur.fetchall()]
            self.db_conn.commit()

        # insert Sesh
        cur.execute(
            "INSERT INTO sesh (title, details, start_time, end_time) VALUES (?, ?, ?, ?)",
            (
                current_sesh.title,
                details,
                current_sesh.start_time.round().format_common_iso(),
                Instant.now().round().format_common_iso(),
            ),
        )
        self.db_conn.commit()

        # get sesh id
        cur.execute("SELECT last_insert_rowid()")
        result = cur.fetchone()
        if not result:
            raise RuntimeError("Failed to get sesh ID after insertion")
        sesh_id = result[0]

        # insert sesh-tag relationships
        if tag_ids:  # Only insert relationships if we have tag IDs
            cur.executemany(
                "INSERT INTO sesh_tag (sesh_id, tag_id) VALUES (?, ?)",
                [(sesh_id, tag_id) for tag_id in tag_ids],
            )
            self.db_conn.commit()

        # fetch sesh uid
        cur.execute("SELECT sesh_uid FROM sesh WHERE sesh_id = ?", (sesh_id,))
        result = cur.fetchone()
        if not result:
            raise RuntimeError("Failed to fetch sesh UID")
        sesh_uid = result[0]

        return sesh_uid[:6]

    def load(self) -> None:
        pass

    def save(self) -> None:
        pass
