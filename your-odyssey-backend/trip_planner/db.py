import os
import sqlite3
from typing import Any, Dict, List
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3')

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS saved_trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        created_at TEXT NOT NULL,
        itinerary_json TEXT NOT NULL
    )
    ''')
    # table to track follows: follower follows followed (both are user sub identifiers)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS follows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        follower_id TEXT NOT NULL,
        followed_id TEXT NOT NULL,
        name TEXT,
        username TEXT,
        bio TEXT,
        picture TEXT,
        created_at TEXT NOT NULL
    )
    ''')
    # simple profiles table for storing editable user bios and lightweight profile info
    cur.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
        user_id TEXT PRIMARY KEY,
        bio TEXT,
        updated_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

def save_itinerary(user_id: str, itinerary_json: str) -> int:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO saved_trips (user_id, created_at, itinerary_json) VALUES (?, ?, ?)',
                (user_id, datetime.utcnow().isoformat(), itinerary_json))
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid

def list_itineraries(user_id: str) -> List[Dict[str, Any]]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, user_id, created_at, itinerary_json FROM saved_trips WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_follows(follower_id: str) -> List[Dict[str, Any]]:
    """Return list of followed people for a given follower_id."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, follower_id, followed_id, name, username, bio, picture, created_at FROM follows WHERE follower_id = ? ORDER BY created_at DESC', (follower_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_followed_profile(followed_id: str) -> Dict[str, Any] | None:
    """Return stored profile info for a followed_id if available."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('SELECT followed_id as id, name, username, bio, picture, created_at FROM follows WHERE followed_id = ? LIMIT 1', (followed_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def save_follow(follower_id: str, followed_id: str, name: str | None = None, username: str | None = None, bio: str | None = None, picture: str | None = None) -> int:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO follows (follower_id, followed_id, name, username, bio, picture, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (follower_id, followed_id, name, username, bio, picture, datetime.utcnow().isoformat()))
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid


def get_profile(user_id: str) -> dict | None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute('SELECT user_id as id, bio, updated_at FROM profiles WHERE user_id = ? LIMIT 1', (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def save_profile(user_id: str, bio: str) -> int:
    conn = _get_conn()
    cur = conn.cursor()
    # upsert: insert or update existing
    cur.execute('INSERT INTO profiles (user_id, bio, updated_at) VALUES (?, ?, ?) '
                'ON CONFLICT(user_id) DO UPDATE SET bio=excluded.bio, updated_at=excluded.updated_at',
                (user_id, bio, datetime.utcnow().isoformat()))
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid
