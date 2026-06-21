# modules/storage.py — SQLite scan history storage

import sqlite3
import json
from datetime import datetime
from config import DB_PATH


def init_db():
    """
    Create tables if not exist.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            project     TEXT,
            target      TEXT,
            scan_type   TEXT,
            timestamp   TEXT,
            findings    TEXT,
            report_path TEXT,
            notes       TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("[DB] Database initialized.")


def save_scan(project: str, target: str, scan_type: str,
              findings: list, report_path: str, notes: str = ""):
    """
    Save scan result to DB.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        INSERT INTO scans (project, target, scan_type, timestamp, findings, report_path, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        project,
        target,
        scan_type,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        json.dumps(findings),
        report_path,
        notes
    ))

    conn.commit()
    conn.close()
    print("[DB] Scan saved.")


def get_all_scans() -> list:
    """
    Fetch all past scans.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT id, project, target, scan_type, timestamp, report_path FROM scans ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    scans = []
    for row in rows:
        scans.append({
            "id":          row[0],
            "project":     row[1],
            "target":      row[2],
            "scan_type":   row[3],
            "timestamp":   row[4],
            "report_path": row[5]
        })

    return scans


def get_scan_by_id(scan_id: int) -> dict:
    """
    Fetch single scan by ID.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
    row = c.fetchone()
    conn.close()

    if not row:
        return {}

    return {
        "id":          row[0],
        "project":     row[1],
        "target":      row[2],
        "scan_type":   row[3],
        "timestamp":   row[4],
        "findings":    json.loads(row[5]),
        "report_path": row[6],
        "notes":       row[7]
    }
