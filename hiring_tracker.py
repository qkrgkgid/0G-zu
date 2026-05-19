"""
Simple CLI tool to track hiring pipeline data.
"""

import argparse
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

DEFAULT_DB_PATH = Path("hiring_data.json")


class HiringTracker:
    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.data: Dict[str, Any] = {"candidates": {}, "events": []}
        if db_path.exists():
            try:
                self.data = json.loads(db_path.read_text())
            except json.JSONDecodeError:
                # 손상된 파일을 감지하면 새 데이터로 복구합니다.
                self.data = {"candidates": {}, "events": []}

    def save(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False))

    def init_db(self) -> None:
        self.data = {"candidates": {}, "events": []}
        self.save()

    def add_candidate(self, name: str, role: str, email: str, source: str) -> str:
        candidate_id = str(uuid.uuid4())
        candidate = {
            "id": candidate_id,
            "name": name,
            "role": role,
            "email": email,
            "source": source,
            "stage": "applied",
            "created_at": self._timestamp(),
            "updated_at": self._timestamp(),
        }
        self.data["candidates"][candidate_id] = candidate
        self._add_event(candidate_id, "candidate_added", f"Added candidate from {source}")
        self.save()
        return candidate_id

    def advance_stage(self, candidate_id: str, stage: str, note: str | None = None) -> None:
        candidate = self._get_candidate(candidate_id)
        previous_stage = candidate.get("stage", "unknown")
        candidate["stage"] = stage
        candidate["updated_at"] = self._timestamp()
        self._add_event(candidate_id, "stage_changed", f"{previous_stage} -> {stage}", note)
        self.save()

    def add_note(self, candidate_id: str, note: str) -> None:
        self._get_candidate(candidate_id)
        self._add_event(candidate_id, "note", "note", note)
        self.save()

    def list_candidates(self) -> list[Dict[str, Any]]:
        return list(self.data.get("candidates", {}).values())

    def candidate_history(self, candidate_id: str) -> list[Dict[str, Any]]:
        self._get_candidate(candidate_id)
        return [e for e in self.data.get("events", []) if e["candidate_id"] == candidate_id]

    def _get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        try:
            return self.data["candidates"][candidate_id]
        except KeyError as exc:
            raise SystemExit(f"Unknown candidate id: {candidate_id}") from exc

    def _add_event(self, candidate_id: str, event_type: str, summary: str, note: str | None = None) -> None:
        event = {
            "candidate_id": candidate_id,
            "type": event_type,
            "summary": summary,
            "note": note,
            "timestamp": self._timestamp(),
        }
        self.data.setdefault("events", []).append(event)

    @staticmethod
    def _timestamp() -> str:
        return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hiring pipeline tracker")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH, help="Path to JSON database file")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize a new empty database")

    add_parser = subparsers.add_parser("add", help="Add a new candidate")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--role", required=True)
    add_parser.add_argument("--email", required=True)
    add_parser.add_argument("--source", default="unknown")

    advance_parser = subparsers.add_parser("advance", help="Move a candidate to a new stage")
    advance_parser.add_argument("id", help="Candidate ID")
    advance_parser.add_argument("--stage", required=True, help="New stage name")
    advance_parser.add_argument("--note", help="Optional note for the transition")

    note_parser = subparsers.add_parser("note", help="Add a note for a candidate")
    note_parser.add_argument("id", help="Candidate ID")
    note_parser.add_argument("--note", required=True, help="Note text")

    subparsers.add_parser("list", help="List all candidates")

    history_parser = subparsers.add_parser("history", help="Show activity for a candidate")
    history_parser.add_argument("id", help="Candidate ID")

    return parser


def main(args: list[str] | None = None) -> None:
    parser = build_parser()
    parsed = parser.parse_args(args)
    tracker = HiringTracker(parsed.db)

    if parsed.command == "init":
        tracker.init_db()
        print(f"Initialized database at {tracker.db_path}")
    elif parsed.command == "add":
        candidate_id = tracker.add_candidate(parsed.name, parsed.role, parsed.email, parsed.source)
        print(f"Created candidate {candidate_id}")
    elif parsed.command == "advance":
        tracker.advance_stage(parsed.id, parsed.stage, parsed.note)
        print(f"Candidate {parsed.id} advanced to {parsed.stage}")
    elif parsed.command == "note":
        tracker.add_note(parsed.id, parsed.note)
        print(f"Added note for candidate {parsed.id}")
    elif parsed.command == "list":
        candidates = tracker.list_candidates()
        for c in candidates:
            print(f"{c['id']} | {c['name']} | {c['role']} | {c['stage']} | {c.get('source', '')}")
    elif parsed.command == "history":
        events = tracker.candidate_history(parsed.id)
        for event in events:
            note_text = f" | note: {event['note']}" if event.get("note") else ""
            print(f"{event['timestamp']} | {event['type']} | {event['summary']}{note_text}")


if __name__ == "__main__":
    main()
