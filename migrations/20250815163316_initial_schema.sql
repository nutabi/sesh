-- Add migration script here

--------------------------------------------------------------------
-- Sessions
--------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sesh (
    sesh_id         INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT,
    sesh_uid        TEXT        NOT NULL UNIQUE DEFAULT (lower(hex(randomblob(16)))),
    title           TEXT        NOT NULL CHECK (length(title) <= 100),
    details         TEXT        NOT NULL CHECK (length(details) <= 1000),
    start_time      TIMESTAMP   NOT NULL,
    end_time        TIMESTAMP   NOT NULL CHECK (end_time >= start_time),
    created_at      TIMESTAMP   NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    updated_at      TIMESTAMP   NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- Auto-update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS trg_sesh_touch
AFTER UPDATE ON sesh FOR EACH ROW
BEGIN
    UPDATE sesh SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ','now') WHERE sesh_id = NEW.sesh_id;
END;

--------------------------------------------------------------------
-- Tags
--------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tag (
    tag_id          INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT,
    tag_name        TEXT        NOT NULL UNIQUE CHECK (tag_name = trim(lower(tag_name)) AND length(tag_name) <= 20),
    is_builtin      BOOLEAN     NOT NULL DEFAULT 0 CHECK (is_builtin IN (0, 1)),
    created_at      TIMESTAMP   NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    updated_at      TIMESTAMP   NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- Add built-in tags
INSERT INTO tag (tag_name, is_builtin)
VALUES
    ('edited', 1),
    ('manual', 1);

-- Reject additional built-in tags
CREATE TRIGGER IF NOT EXISTS trg_tag_reject_additional_builtin
BEFORE INSERT ON tag
FOR EACH ROW
WHEN NEW.is_builtin = 1
BEGIN
    SELECT RAISE(ABORT, 'Only predefined built-in tags are allowed');
END;

-- Prevent deletion of built-in tags
CREATE TRIGGER IF NOT EXISTS trg_tag_prevent_builtin_deletion
BEFORE DELETE ON tag
FOR EACH ROW
WHEN OLD.is_builtin = 1
BEGIN
    SELECT RAISE(ABORT, 'Built-in tags cannot be deleted');
END;

-- Prevent modification of built-in tags
CREATE TRIGGER IF NOT EXISTS trg_tag_prevent_builtin_update
BEFORE UPDATE ON tag
FOR EACH ROW
WHEN OLD.is_builtin = 1 AND (NEW.tag_name != OLD.tag_name OR NEW.is_builtin != OLD.is_builtin)
BEGIN
    SELECT RAISE(ABORT, 'Built-in tags cannot be modified');
END;

-- Auto-update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS trg_tag_touch
AFTER UPDATE ON tag FOR EACH ROW
BEGIN
    UPDATE tag SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ','now') WHERE tag_id = NEW.tag_id;
END;

-- Auto-add 'edited' tag to sesh_tag if sesh start or end time is changed
CREATE TRIGGER IF NOT EXISTS trg_sesh_tag_edited
AFTER UPDATE ON sesh
FOR EACH ROW
WHEN OLD.start_time != NEW.start_time OR OLD.end_time != NEW.end_time
BEGIN
    INSERT OR IGNORE INTO sesh_tag (sesh_id, tag_id)
    SELECT NEW.sesh_id, tag_id FROM tag WHERE tag_name = 'edited';
END;

--------------------------------------------------------------------
-- Session-Tag (many-to-many)
--------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sesh_tag (
    sesh_id         INTEGER     NOT NULL REFERENCES sesh (sesh_id) ON DELETE CASCADE,
    tag_id          INTEGER     NOT NULL REFERENCES tag (tag_id) ON DELETE CASCADE,
    created_at      TIMESTAMP   NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    PRIMARY KEY (sesh_id, tag_id)
);

--------------------------------------------------------------------
-- Indexes for performance
--------------------------------------------------------------------
-- Index for time-based queries on Sesh
CREATE INDEX IF NOT EXISTS idx_sesh_start_time ON sesh (start_time);
CREATE INDEX IF NOT EXISTS idx_sesh_end_time ON sesh (end_time);
CREATE INDEX IF NOT EXISTS idx_sesh_time_range ON sesh (start_time, end_time);
CREATE INDEX IF NOT EXISTS idx_sesh_created_at ON sesh (created_at);

-- Index for UUID lookups
CREATE INDEX IF NOT EXISTS idx_sesh_uid ON sesh (sesh_uid);

-- Index for short UID lookups (last 6 characters)
CREATE INDEX IF NOT EXISTS idx_sesh_uid_short ON sesh (substr(sesh_uid, -6));

-- Index for tag lookups (tag_name already has unique index)
-- Index for Sesh-tag relationships (composite primary key already creates index)
CREATE INDEX IF NOT EXISTS idx_sesh_tag_tag_id ON sesh_tag (tag_id);
