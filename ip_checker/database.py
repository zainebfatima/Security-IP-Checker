import sqlite3
from pathlib import Path
from ip_checker.storage import load_records
DB_FILE = Path(__file__).resolve().parent.parent / "ip_records.db"

def connect_db():
    conn = sqlite3.connect(DB_FILE)
    return conn

def create_table():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ip_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE NOT NULL,
            flagged INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()

def insert_ip(ip, flagged=0):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO ip_records (ip_address, flagged) VALUES (?, ?)",
        (ip, flagged)
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

def update_flag(ip, flagged):
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE ip_records SET flagged = ? WHERE ip_address = ?",
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

    records = get_all_records()
    print(records)
    