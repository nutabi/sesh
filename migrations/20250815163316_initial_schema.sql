-- Add migration script here

--------------------------------------------------------------------
-- Sessions
--------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sesh (
    sesh_id         INTEGER     NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    sesh_uid        TEXT        NOT NULL UNIQUE DEFAULT (lower(hex(randomblob(16)))),
    title           TEXT        NOT NULL CHECK (length(title) <= 100),
    details         TEXT        NOT NULL,
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
    tag_id          INTEGER    NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    tag_name        TEXT       NOT NULL UNIQUE CHECK (tag_name = trim(lower(tag_name)) AND length(tag_name) <= 20),
    created_at      TIMESTAMP  NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
    updated_at      TIMESTAMP  NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);

-- Auto-update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS trg_tag_touch
AFTER UPDATE ON tag FOR EACH ROW
BEGIN
    UPDATE tag SET updated_at = strftime('%Y-%m-%dT%H:%M:%SZ','now') WHERE tag_id = NEW.tag_id;
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

-- Index for tag lookups (tag_name already has unique index)
-- Index for Sesh-tag relationships (composite primary key already creates index)
CREATE INDEX IF NOT EXISTS idx_sesh_tag_tag_id ON sesh_tag (tag_id);
