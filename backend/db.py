import sqlite3
import json
import time
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "sentinel.db"
CACHE_TTL_SECONDS = 7 * 24 * 3600


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS reviews (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            game TEXT NOT NULL,
            riot_id TEXT NOT NULL,
            region TEXT NOT NULL,
            data_mode TEXT NOT NULL,
            decision TEXT NOT NULL,
            full_payload_json TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS riot_cache (
            endpoint TEXT NOT NULL,
            key TEXT NOT NULL,
            response_json TEXT NOT NULL,
            fetched_at REAL NOT NULL,
            PRIMARY KEY (endpoint, key)
        );
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            input_json TEXT NOT NULL,
            output_json TEXT NOT NULL,
            latency_ms REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (review_id) REFERENCES reviews(id)
        );
    """)
    conn.commit()
    conn.close()


def cache_get(endpoint: str, key: str) -> dict | None:
    conn = get_conn()
    row = conn.execute(
        "SELECT response_json, fetched_at FROM riot_cache WHERE endpoint = ? AND key = ?",
        (endpoint, key),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    age = time.time() - row["fetched_at"]
    if age > CACHE_TTL_SECONDS:
        return None
    return {"data": json.loads(row["response_json"]), "age_seconds": age}


def cache_set(endpoint: str, key: str, response: dict):
    conn = get_conn()
    conn.execute(
        "INSERT OR REPLACE INTO riot_cache (endpoint, key, response_json, fetched_at) VALUES (?, ?, ?, ?)",
        (endpoint, key, json.dumps(response), time.time()),
    )
    conn.commit()
    conn.close()


def save_review(review: dict):
    conn = get_conn()
    conn.execute(
        "INSERT INTO reviews (id, timestamp, game, riot_id, region, data_mode, decision, full_payload_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            review["id"],
            review["timestamp"],
            review["game"],
            review["riot_id"],
            review["region"],
            review["data_mode"],
            review["orchestrator"]["decision"],
            json.dumps(review),
        ),
    )
    conn.commit()
    conn.close()


def save_audit(review_id: str, agent_name: str, input_data: dict, output_data: dict, latency_ms: float, timestamp: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO audit_log (review_id, agent_name, input_json, output_json, latency_ms, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (review_id, agent_name, json.dumps(input_data), json.dumps(output_data), latency_ms, timestamp),
    )
    conn.commit()
    conn.close()


def get_history(limit: int = 20) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, timestamp, game, riot_id, region, data_mode, decision FROM reviews ORDER BY timestamp DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_review(review_id: str) -> dict | None:
    conn = get_conn()
    row = conn.execute(
        "SELECT full_payload_json FROM reviews WHERE id = ?",
        (review_id,),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return json.loads(row["full_payload_json"])
