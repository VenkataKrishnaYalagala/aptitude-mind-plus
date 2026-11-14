-- For an existing Cloudflare D1 database that already ran schema/schema.sql.
-- Apply once. Safe to retry because the objects use IF NOT EXISTS.
CREATE TABLE IF NOT EXISTS student_doubts (
 id TEXT PRIMARY KEY,
 exam TEXT NOT NULL CHECK (exam IN ('upsc','gate','ssc','bank','state','rail')),
 topic TEXT NOT NULL,
 question TEXT NOT NULL,
 student_name TEXT NOT NULL,
 student_email TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new','answered','archived')),
 private_notes TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL DEFAULT (datetime('now')),
 reviewed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_student_doubts_recent ON student_doubts(status,created_at DESC);
