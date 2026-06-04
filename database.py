"""
database.py — SQLite persistence layer for ZenEnglish Bot.

Tables:
  users       — chat_id, bedtime, waketime, timezone_offset
  sleep_logs  — id, chat_id, date, hours_slept, mood
"""

import sqlite3
import os
from datetime import date, datetime
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "zenbot.db")


# ──────────────────────────────────────────────────
#  Connection helper
# ──────────────────────────────────────────────────
def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ──────────────────────────────────────────────────
#  Initialisation — create tables if they don't exist
# ──────────────────────────────────────────────────
def init_db() -> None:
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                chat_id         INTEGER PRIMARY KEY,
                bedtime         TEXT NOT NULL,          -- "HH:MM" (24h, UTC)
                waketime        TEXT NOT NULL,          -- "HH:MM" (24h, UTC)
                blackout_sent   INTEGER DEFAULT 0,      -- flag: blackout sent today?
                created_at      TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS sleep_logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id     INTEGER NOT NULL,
                log_date    TEXT NOT NULL,              -- ISO date YYYY-MM-DD
                hours_slept REAL,
                mood        TEXT,
                created_at  TEXT DEFAULT (datetime('now')),
                UNIQUE(chat_id, log_date)
            );
            """
        )


# ──────────────────────────────────────────────────
#  Users
# ──────────────────────────────────────────────────
def upsert_user(chat_id: int, bedtime: str, waketime: str) -> None:
    """Insert or replace the user's schedule."""
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO users (chat_id, bedtime, waketime)
            VALUES (?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET
                bedtime  = excluded.bedtime,
                waketime = excluded.waketime,
                blackout_sent = 0
            """,
            (chat_id, bedtime, waketime),
        )


def get_user(chat_id: int) -> Optional[sqlite3.Row]:
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE chat_id = ?", (chat_id,)
        ).fetchone()


def get_all_users() -> list[sqlite3.Row]:
    with _connect() as conn:
        return conn.execute("SELECT * FROM users").fetchall()


def mark_blackout_sent(chat_id: int, sent: bool = True) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE users SET blackout_sent = ? WHERE chat_id = ?",
            (1 if sent else 0, chat_id),
        )


def reset_daily_flags() -> None:
    """Called at midnight to clear the daily blackout flag."""
    with _connect() as conn:
        conn.execute("UPDATE users SET blackout_sent = 0")


# ──────────────────────────────────────────────────
#  Sleep logs
# ──────────────────────────────────────────────────
def upsert_sleep_log(chat_id: int, log_date: str, hours_slept: float, mood: str) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO sleep_logs (chat_id, log_date, hours_slept, mood)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(chat_id, log_date) DO UPDATE SET
                hours_slept = excluded.hours_slept,
                mood        = excluded.mood
            """,
            (chat_id, log_date, hours_slept, mood),
        )


def get_weekly_logs(chat_id: int, weeks: int = 1) -> list[sqlite3.Row]:
    """Return up to 7 * weeks recent log rows, newest first."""
    with _connect() as conn:
        return conn.execute(
            """
            SELECT log_date, hours_slept, mood
            FROM sleep_logs
            WHERE chat_id = ?
            ORDER BY log_date DESC
            LIMIT ?
            """,
            (chat_id, 7 * weeks),
        ).fetchall()


def get_today_log(chat_id: int) -> Optional[sqlite3.Row]:
    today = date.today().isoformat()
    with _connect() as conn:
        return conn.execute(
            "SELECT * FROM sleep_logs WHERE chat_id = ? AND log_date = ?",
            (chat_id, today),
        ).fetchone()
