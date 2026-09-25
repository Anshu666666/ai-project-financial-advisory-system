"""
================================================================================
FINWISE AI – SQLITE PERSISTENCE LAYER
Author: Anshuman (Core Backend & API Orchestration Lead)
================================================================================
Lightweight, thread-safe SQLite database manager for saving user financial
profiles, generated expert plans, and contextual chat conversation history.
================================================================================
"""

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Database storage path (defaults to finwise.db in workspace root)
DB_PATH = os.getenv("FINWISE_DB_PATH", str(Path(__file__).parent.parent.parent / "finwise.db"))


def get_db_connection() -> sqlite3.Connection:
    """Creates a thread-safe connection to the SQLite database with dict row factory."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes tables for financial sessions and conversational chat history."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Sessions table: Stores user profile and evaluated plan
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS financial_sessions (
                session_id TEXT PRIMARY KEY,
                user_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                profile_json TEXT NOT NULL,
                fuzzy_json TEXT NOT NULL,
                expert_plan_json TEXT NOT NULL,
                advisory_report TEXT NOT NULL
            )
            """
        )

        # 2. Chat messages table: Stores conversational memory for each session
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                rules_json TEXT,
                citations_json TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES financial_sessions (session_id)
            )
            """
        )
        conn.commit()


def save_session(
    session_id: str,
    user_name: str,
    profile: Dict[str, Any],
    fuzzy_res: Dict[str, Any],
    expert_plan: Dict[str, Any],
    advisory_report: str,
):
    """Saves or updates a complete evaluated financial session."""
    now_iso = datetime.now(timezone.utc).isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO financial_sessions (
                session_id, user_name, created_at, profile_json, fuzzy_json, expert_plan_json, advisory_report
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                user_name,
                now_iso,
                json.dumps(profile, default=str),
                json.dumps(fuzzy_res, default=str),
                json.dumps(expert_plan, default=str),
                advisory_report,
            ),
        )
        conn.commit()


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves an evaluated session by session_id."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM financial_sessions WHERE session_id = ?",
            (session_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None

        return {
            "session_id": row["session_id"],
            "user_name": row["user_name"],
            "created_at": row["created_at"],
            "profile": json.loads(row["profile_json"]),
            "fuzzy_assessment": json.loads(row["fuzzy_json"]),
            "expert_plan": json.loads(row["expert_plan_json"]),
            "advisory_report": row["advisory_report"],
        }


def list_sessions(limit: int = 50) -> List[Dict[str, Any]]:
    """Lists recent financial sessions for dashboard overview."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT session_id, user_name, created_at, fuzzy_json FROM financial_sessions ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        rows = cursor.fetchall()
        results = []
        for r in rows:
            fuzzy = json.loads(r["fuzzy_json"])
            results.append({
                "session_id": r["session_id"],
                "user_name": r["user_name"],
                "risk_category": fuzzy.get("category", "Moderate"),
                "created_at": r["created_at"],
            })
        return results


def add_chat_message(
    session_id: str,
    role: str,
    message: str,
    rules: Optional[List[str]] = None,
    citations: Optional[List[Dict[str, Any]]] = None,
):
    """Appends a new conversational message to the session's chat history."""
    now_iso = datetime.now(timezone.utc).isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO chat_messages (
                session_id, role, message, rules_json, citations_json, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                role,
                message,
                json.dumps(rules or []),
                json.dumps(citations or []),
                now_iso,
            ),
        )
        conn.commit()


def get_chat_history(session_id: str) -> List[Dict[str, Any]]:
    """Retrieves all chat messages for a specific session in chronological order."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, session_id, role, message, rules_json, citations_json, timestamp FROM chat_messages WHERE session_id = ? ORDER BY id ASC",
            (session_id,),
        )
        rows = cursor.fetchall()
        history = []
        for r in rows:
            history.append({
                "id": r["id"],
                "session_id": r["session_id"],
                "role": r["role"],
                "message": r["message"],
                "rules": json.loads(r["rules_json"]) if r["rules_json"] else [],
                "citations": json.loads(r["citations_json"]) if r["citations_json"] else [],
                "timestamp": r["timestamp"],
            })
        return history


# Automatically ensure tables exist on module load
init_db()
