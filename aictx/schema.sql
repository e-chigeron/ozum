PRAGMA foreign_keys = ON;

BEGIN;

CREATE TABLE meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
) STRICT;

CREATE TABLE sources (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    uri TEXT NOT NULL,
    revision TEXT,
    digest TEXT
) STRICT;

CREATE TABLE nodes (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL,
    body TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'active',
    priority INTEGER NOT NULL DEFAULT 0,
    source_id TEXT REFERENCES sources(id),
    payload TEXT CHECK (payload IS NULL OR json_valid(payload))
) STRICT;

CREATE TABLE edges (
    src TEXT NOT NULL REFERENCES nodes(id),
    rel TEXT NOT NULL,
    dst TEXT NOT NULL REFERENCES nodes(id),
    payload TEXT CHECK (payload IS NULL OR json_valid(payload)),
    PRIMARY KEY (src, rel, dst)
) STRICT;

CREATE TABLE entrypoints (
    node_id TEXT PRIMARY KEY REFERENCES nodes(id),
    rank INTEGER NOT NULL UNIQUE CHECK (rank > 0)
) STRICT;

CREATE TABLE artifacts (
    id TEXT PRIMARY KEY,
    media_type TEXT NOT NULL,
    source_id TEXT REFERENCES sources(id),
    uri TEXT,
    content BLOB,
    digest TEXT,
    CHECK (uri IS NOT NULL OR content IS NOT NULL)
) STRICT;

INSERT INTO meta (key, value) VALUES
    ('format', 'aictx'),
    ('schema_version', '0'),
    ('canonical', 'false');

COMMIT;
