import sqlite3
from pathlib import Path
from ip_checker.storage import load_records

DB_FILE = Path(__file__).resolve().parent.parent / "ip_records.db"


def connect_db():
    return sqlite3.connect(DB_FILE)


def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    # Existing table: stores unique IP addresses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ip_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE NOT NULL,
            flagged INTEGER DEFAULT 0
        )
    """)

    # New table: stores every IP-checking attempt
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            status TEXT NOT NULL,
            ip_version TEXT NOT NULL,
            checked_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def insert_ip(ip, flagged=0):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO ip_records
        (ip_address, flagged)
        VALUES (?, ?)
        """,
        (ip, flagged)
    )

    connection.commit()
    connection.close()


def record_activity(ip, status, ip_version="N/A"):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO activity_history
        (ip_address, status, ip_version)
        VALUES (?, ?, ?)
        """,
        (ip, status, ip_version)
    )

    connection.commit()
    connection.close()


def get_all_records():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM ip_records")
    records = cursor.fetchall()

    connection.close()
    return records


def get_activity_history(status=None):
    connection = connect_db()
    cursor = connection.cursor()

    if status in ("Valid", "Invalid"):
        cursor.execute(
            """
            SELECT * FROM activity_history
            WHERE status = ?
            ORDER BY id DESC
            """,
            (status,)
        )
    else:
        cursor.execute("""
            SELECT * FROM activity_history
            ORDER BY id DESC
        """)

    records = cursor.fetchall()
    connection.close()

    return records


def get_dashboard_stats():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM activity_history
    """)
    total_ips = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM activity_history
        WHERE status = 'Valid'
    """)
    valid_ips = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM ip_records
        WHERE flagged = 1
    """)
    flagged_ips = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM ip_records
    """)
    unique_ips = cursor.fetchone()[0]

    connection.close()

    return {
        "total_checks": total_ips,
        "valid_checks": valid_ips,
        "flagged_ips": flagged_ips,
        "unique_ips": unique_ips
    }


def update_flag(ip, flagged):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE ip_records
        SET flagged = ?
        WHERE ip_address = ?
        """,
        (flagged, ip)
    )

    connection.commit()
    connection.close()


def delete_ip(ip):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM ip_records WHERE ip_address = ?",
        (ip,)
    )

    connection.commit()
    connection.close()


def migrate_json_to_db():
    ips, flagged_ips = load_records()

    for ip in set(ips) | set(flagged_ips):
        flagged = 1 if ip in flagged_ips else 0
        insert_ip(ip, flagged)


if __name__ == "__main__":
    create_table()
    migrate_json_to_db()

    print("Database tables are ready.")
    print(get_all_records())