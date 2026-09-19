"""SQLite adapter using only Python's standard library."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from industrial_alarm_manager.domain import (
    AlarmDefinition,
    AlarmEvent,
    AlarmEventType,
    AlarmOccurrence,
    AlarmPriority,
    AlarmState,
    AlarmSuppression,
)


def _dt(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


class SQLiteAlarmRepository:
    def __init__(self, database: str | Path = ":memory:") -> None:
        self.connection = sqlite3.connect(str(database))
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._create_schema()

    def _create_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS alarm_definitions (
                definition_id TEXT PRIMARY KEY, code TEXT NOT NULL, name TEXT NOT NULL,
                description TEXT NOT NULL, source TEXT NOT NULL, priority TEXT NOT NULL,
                category TEXT NOT NULL, ack_required INTEGER NOT NULL,
                reset_required INTEGER NOT NULL, enabled INTEGER NOT NULL,
                created_at TEXT NOT NULL, UNIQUE(code, source)
            );
            CREATE TABLE IF NOT EXISTS alarm_occurrences (
                occurrence_id TEXT PRIMARY KEY, definition_id TEXT NOT NULL, code TEXT NOT NULL,
                source TEXT NOT NULL, priority TEXT NOT NULL, state TEXT NOT NULL,
                first_active_at TEXT, last_active_at TEXT, acknowledged_at TEXT,
                acknowledged_by TEXT, cleared_at TEXT, reset_at TEXT,
                activation_count INTEGER NOT NULL, duplicate_count INTEGER NOT NULL,
                escalation_count INTEGER NOT NULL, is_suppressed INTEGER NOT NULL,
                suppression_reason TEXT, message TEXT, metadata TEXT NOT NULL,
                FOREIGN KEY(definition_id) REFERENCES alarm_definitions(definition_id)
            );
            CREATE INDEX IF NOT EXISTS idx_occurrence_identity_state
                ON alarm_occurrences(code, source, state);
            CREATE TABLE IF NOT EXISTS alarm_events (
                event_id TEXT PRIMARY KEY, occurrence_id TEXT NOT NULL, definition_id TEXT NOT NULL,
                code TEXT NOT NULL, source TEXT NOT NULL, priority TEXT NOT NULL,
                event_type TEXT NOT NULL, state TEXT NOT NULL, timestamp TEXT NOT NULL,
                actor TEXT, details TEXT NOT NULL,
                FOREIGN KEY(occurrence_id) REFERENCES alarm_occurrences(occurrence_id)
            );
            CREATE INDEX IF NOT EXISTS idx_event_time ON alarm_events(timestamp);
            CREATE TABLE IF NOT EXISTS alarm_suppressions (
                suppression_id TEXT PRIMARY KEY, definition_id TEXT NOT NULL,
                reason TEXT NOT NULL, created_by TEXT NOT NULL, created_at TEXT NOT NULL,
                expires_at TEXT, active INTEGER NOT NULL,
                FOREIGN KEY(definition_id) REFERENCES alarm_definitions(definition_id)
            );
            """
        )
        self.connection.commit()

    def save_definition(self, definition: AlarmDefinition) -> None:
        self.connection.execute(
            """INSERT OR REPLACE INTO alarm_definitions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                str(definition.definition_id),
                definition.code,
                definition.name,
                definition.description,
                definition.source,
                definition.default_priority.value,
                definition.category,
                definition.ack_required,
                definition.reset_required,
                definition.enabled,
                _iso(definition.created_at),
            ),
        )
        self.connection.commit()

    def _definition(self, row: sqlite3.Row | None) -> AlarmDefinition | None:
        if row is None:
            return None
        return AlarmDefinition(
            definition_id=UUID(row["definition_id"]),
            code=row["code"],
            name=row["name"],
            description=row["description"],
            source=row["source"],
            default_priority=AlarmPriority(row["priority"]),
            category=row["category"],
            ack_required=bool(row["ack_required"]),
            reset_required=bool(row["reset_required"]),
            enabled=bool(row["enabled"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def get_definition(self, definition_id: UUID) -> AlarmDefinition | None:
        row = self.connection.execute(
            "SELECT * FROM alarm_definitions WHERE definition_id = ?", (str(definition_id),)
        ).fetchone()
        return self._definition(row)

    def find_definition(self, code: str, source: str) -> AlarmDefinition | None:
        row = self.connection.execute(
            "SELECT * FROM alarm_definitions WHERE code = ? AND source = ?", (code, source)
        ).fetchone()
        return self._definition(row)

    def list_definitions(self) -> list[AlarmDefinition]:
        rows = self.connection.execute(
            "SELECT * FROM alarm_definitions ORDER BY code, source"
        ).fetchall()
        return [item for row in rows if (item := self._definition(row)) is not None]

    def save_occurrence(self, occurrence: AlarmOccurrence) -> None:
        values: tuple[Any, ...] = (
            str(occurrence.occurrence_id),
            str(occurrence.definition_id),
            occurrence.code,
            occurrence.source,
            occurrence.priority.value,
            occurrence.state.value,
            _iso(occurrence.first_active_at),
            _iso(occurrence.last_active_at),
            _iso(occurrence.acknowledged_at),
            occurrence.acknowledged_by,
            _iso(occurrence.cleared_at),
            _iso(occurrence.reset_at),
            occurrence.activation_count,
            occurrence.duplicate_count,
            occurrence.escalation_count,
            occurrence.is_suppressed,
            occurrence.suppression_reason,
            occurrence.message,
            json.dumps(occurrence.metadata, sort_keys=True),
        )
        self.connection.execute(
            """INSERT OR REPLACE INTO alarm_occurrences VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            values,
        )
        self.connection.commit()

    def _occurrence(self, row: sqlite3.Row | None) -> AlarmOccurrence | None:
        if row is None:
            return None
        return AlarmOccurrence(
            occurrence_id=UUID(row["occurrence_id"]),
            definition_id=UUID(row["definition_id"]),
            code=row["code"],
            source=row["source"],
            priority=AlarmPriority(row["priority"]),
            state=AlarmState(row["state"]),
            first_active_at=_dt(row["first_active_at"]),
            last_active_at=_dt(row["last_active_at"]),
            acknowledged_at=_dt(row["acknowledged_at"]),
            acknowledged_by=row["acknowledged_by"],
            cleared_at=_dt(row["cleared_at"]),
            reset_at=_dt(row["reset_at"]),
            activation_count=row["activation_count"],
            duplicate_count=row["duplicate_count"],
            escalation_count=row["escalation_count"],
            is_suppressed=bool(row["is_suppressed"]),
            suppression_reason=row["suppression_reason"],
            message=row["message"],
            metadata=json.loads(row["metadata"]),
        )

    def get_occurrence(self, occurrence_id: UUID) -> AlarmOccurrence | None:
        row = self.connection.execute(
            "SELECT * FROM alarm_occurrences WHERE occurrence_id = ?", (str(occurrence_id),)
        ).fetchone()
        return self._occurrence(row)

    def find_open_occurrence(self, code: str, source: str) -> AlarmOccurrence | None:
        row = self.connection.execute(
            """SELECT * FROM alarm_occurrences WHERE code = ? AND source = ?
            AND state IN ('ACTIVE', 'ACKNOWLEDGED', 'CLEARED')
            ORDER BY COALESCE(last_active_at, first_active_at) DESC LIMIT 1""",
            (code, source),
        ).fetchone()
        return self._occurrence(row)

    def list_occurrences(
        self,
        *,
        priority: AlarmPriority | None = None,
        state: AlarmState | None = None,
        code: str | None = None,
        source: str | None = None,
        suppressed: bool | None = None,
    ) -> list[AlarmOccurrence]:
        conditions: list[str] = []
        values: list[Any] = []
        for column, value in (
            ("priority", priority.value if priority else None),
            ("state", state.value if state else None),
            ("code", code),
            ("source", source),
        ):
            if value is not None:
                conditions.append(f"{column} = ?")
                values.append(value)
        if suppressed is not None:
            conditions.append("is_suppressed = ?")
            values.append(suppressed)
        where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        rows = self.connection.execute(
            f"SELECT * FROM alarm_occurrences{where} ORDER BY first_active_at", values
        ).fetchall()
        return [item for row in rows if (item := self._occurrence(row)) is not None]

    def append_event(self, event: AlarmEvent) -> None:
        self.connection.execute(
            "INSERT INTO alarm_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                str(event.event_id),
                str(event.occurrence_id),
                str(event.definition_id),
                event.code,
                event.source,
                event.priority.value,
                event.event_type.value,
                event.state.value,
                _iso(event.timestamp),
                event.actor,
                json.dumps(dict(event.details), sort_keys=True),
            ),
        )
        self.connection.commit()

    def _event(self, row: sqlite3.Row) -> AlarmEvent:
        return AlarmEvent(
            event_id=UUID(row["event_id"]),
            occurrence_id=UUID(row["occurrence_id"]),
            definition_id=UUID(row["definition_id"]),
            code=row["code"],
            source=row["source"],
            priority=AlarmPriority(row["priority"]),
            event_type=AlarmEventType(row["event_type"]),
            state=AlarmState(row["state"]),
            timestamp=datetime.fromisoformat(row["timestamp"]),
            actor=row["actor"],
            details=json.loads(row["details"]),
        )

    def list_events(
        self,
        *,
        occurrence_id: UUID | None = None,
        event_type: str | None = None,
        code: str | None = None,
        source: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[AlarmEvent]:
        conditions: list[str] = []
        values: list[str] = []
        filters = (
            ("occurrence_id", str(occurrence_id) if occurrence_id else None),
            ("event_type", event_type),
            ("code", code),
            ("source", source),
        )
        for column, value in filters:
            if value is not None:
                conditions.append(f"{column} = ?")
                values.append(value)
        if start_time:
            conditions.append("timestamp >= ?")
            values.append(start_time.isoformat())
        if end_time:
            conditions.append("timestamp <= ?")
            values.append(end_time.isoformat())
        where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        rows = self.connection.execute(
            f"SELECT * FROM alarm_events{where} ORDER BY timestamp", values
        ).fetchall()
        return [self._event(row) for row in rows]

    def save_suppression(self, suppression: AlarmSuppression) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO alarm_suppressions VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                str(suppression.suppression_id),
                str(suppression.definition_id),
                suppression.reason,
                suppression.created_by,
                _iso(suppression.created_at),
                _iso(suppression.expires_at),
                suppression.active,
            ),
        )
        self.connection.commit()

    def get_active_suppression(self, definition_id: UUID, at: datetime) -> AlarmSuppression | None:
        row = self.connection.execute(
            """SELECT * FROM alarm_suppressions WHERE definition_id = ? AND active = 1
            AND (expires_at IS NULL OR expires_at > ?) ORDER BY created_at DESC LIMIT 1""",
            (str(definition_id), at.isoformat()),
        ).fetchone()
        if row is None:
            return None
        return AlarmSuppression(
            suppression_id=UUID(row["suppression_id"]),
            definition_id=UUID(row["definition_id"]),
            reason=row["reason"],
            created_by=row["created_by"],
            created_at=datetime.fromisoformat(row["created_at"]),
            expires_at=_dt(row["expires_at"]),
            active=bool(row["active"]),
        )

    def deactivate_suppression(self, suppression_id: UUID) -> None:
        self.connection.execute(
            "UPDATE alarm_suppressions SET active = 0 WHERE suppression_id = ?",
            (str(suppression_id),),
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "SQLiteAlarmRepository":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
