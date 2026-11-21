import sqlite3
from datetime import datetime, timedelta

DB_PATH = "data/recruiters.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recruiters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            title TEXT,
            url TEXT UNIQUE,
            description TEXT,
            relevance_score INTEGER,
            email TEXT,
            company TEXT,
            status TEXT DEFAULT 'New',
            date_added TEXT,
            last_contacted TEXT,
            follow_up_count INTEGER DEFAULT 0,
            follow_up_due TEXT
        )
    """)

    # Migration for existing databases
    cursor.execute("PRAGMA table_info(recruiters)")
    columns = [column[1] for column in cursor.fetchall()]

    if "follow_up_due" not in columns:
        cursor.execute(
            "ALTER TABLE recruiters ADD COLUMN follow_up_due TEXT"
        )

    conn.commit()
    conn.close()


def save_recruiter(recruiter):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT OR IGNORE INTO recruiters (
                name,
                title,
                url,
                description,
                relevance_score,
                email,
                company,
                status,
                date_added,
                last_contacted,
                follow_up_count,
                follow_up_due
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            recruiter.get("name", ""),
            recruiter.get("title", ""),
            recruiter.get("url", ""),
            recruiter.get("snippet", recruiter.get("description", "")),
            recruiter.get("relevance_score", 0),
            recruiter.get("email", ""),
            recruiter.get("company", ""),
            "New",
            datetime.now().strftime("%Y-%m-%d"),
            None,
            0,
            None
        ))

        inserted = cursor.rowcount > 0

        conn.commit()

        return inserted

    except sqlite3.Error as e:

        print(f"Database error: {e}")
        return False

    finally:

        conn.close()


def get_all_recruiters():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM recruiters
        ORDER BY date_added DESC
    """)

    recruiters = cursor.fetchall()

    conn.close()

    return recruiters


def update_recruiter_status(recruiter_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE recruiters
        SET status = ?
        WHERE id = ?
    """, (status, recruiter_id))

    conn.commit()
    conn.close()


def mark_contacted(recruiter_id):

    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    cursor.execute("""
        UPDATE recruiters
        SET status = 'Contacted',
            last_contacted = ?,
            follow_up_due = ?,
            follow_up_count = 0
        WHERE id = ?
    """, (today, due_date, recruiter_id))

    conn.commit()
    conn.close()


def record_follow_up(recruiter_id):

    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    cursor.execute("""
        UPDATE recruiters
        SET follow_up_count = follow_up_count + 1,
            last_contacted = ?,
            follow_up_due = ?
        WHERE id = ?
    """, (today, due_date, recruiter_id))

    conn.commit()
    conn.close()


def update_recruiter_email(recruiter_id, email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE recruiters
        SET email = ?
        WHERE id = ?
    """, (email, recruiter_id))

    conn.commit()
    conn.close()


def get_follow_up_stats():

    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT COUNT(*)
        FROM recruiters
        WHERE follow_up_due IS NOT NULL
          AND follow_up_due < ?
          AND status NOT IN ('Replied', 'Interview', 'Rejected')
          AND follow_up_count < 2
    """, (today,))

    overdue = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM recruiters
        WHERE follow_up_due IS NOT NULL
          AND follow_up_due = ?
          AND status NOT IN ('Replied', 'Interview', 'Rejected')
          AND follow_up_count < 2
    """, (today,))

    due_today = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM recruiters
        WHERE follow_up_due IS NOT NULL
          AND follow_up_due > ?
          AND follow_up_due <= ?
          AND status NOT IN ('Replied', 'Interview', 'Rejected')
          AND follow_up_count < 2
    """, (
        today,
        (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    ))

    due_soon = cursor.fetchone()[0]

    conn.close()

    return overdue, due_today, due_soon