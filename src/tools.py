from __future__ import annotations

import json
import platform
import socket
import sqlite3
import uuid
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


DB_PATH = Path("data/helpdesk.db")


def _ensure_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id TEXT PRIMARY KEY,
                issue TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def check_internet_connection() -> dict[str, Any]:
    """Checks whether this computer can reach a public HTTPS endpoint."""
    try:
        request = Request(
            "https://www.google.com/generate_204",
            headers={"User-Agent": "AI-IT-Helpdesk-Agent/1.0"},
            method="GET",
        )
        with urlopen(request, timeout=4) as response:
            return {
                "connected": True,
                "http_status": response.status,
                "message": "Internet connectivity is available.",
            }
    except Exception as exc:
        return {
            "connected": False,
            "message": "Internet connectivity check failed.",
            "error": str(exc),
        }


def get_system_info() -> dict[str, Any]:
    """Returns non-sensitive basic information about the local computer."""
    try:
        import psutil

        memory_gb = round(psutil.virtual_memory().total / (1024**3), 1)
        cpu_count = psutil.cpu_count(logical=True)
        disk = psutil.disk_usage("/")
        free_disk_gb = round(disk.free / (1024**3), 1)
    except Exception:
        memory_gb = None
        cpu_count = None
        free_disk_gb = None

    return {
        "operating_system": platform.platform(),
        "processor": platform.processor() or "Unknown",
        "logical_cpu_count": cpu_count,
        "ram_gb": memory_gb,
        "free_disk_gb": free_disk_gb,
        "hostname": socket.gethostname(),
    }


def create_support_ticket(issue: str, priority: str = "Medium") -> dict[str, Any]:
    """Creates a local support ticket after the user explicitly requests escalation."""
    _ensure_db()

    allowed = {"Low", "Medium", "High", "Critical"}
    priority = priority if priority in allowed else "Medium"

    ticket_id = f"IT-{uuid.uuid4().hex[:6].upper()}"

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO tickets(ticket_id, issue, priority, status)
            VALUES (?, ?, ?, ?)
            """,
            (ticket_id, issue, priority, "Open"),
        )
        conn.commit()

    return {
        "ticket_id": ticket_id,
        "issue": issue,
        "priority": priority,
        "status": "Open",
        "message": "Support ticket created successfully.",
    }
