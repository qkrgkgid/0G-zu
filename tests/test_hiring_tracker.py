import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from hiring_tracker import HiringTracker


class HiringTrackerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = TemporaryDirectory()
        self.db_path = Path(self.tmp_dir.name) / "db.json"
        self.tracker = HiringTracker(self.db_path)
        self.tracker.init_db()

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()

    def test_init_creates_empty_db(self) -> None:
        self.assertEqual(self.tracker.data, {"candidates": {}, "events": []})

    def test_add_and_list_candidate(self) -> None:
        candidate_id = self.tracker.add_candidate(
            "홍길동", "Backend", "hong@example.com", "referral"
        )

        candidates = self.tracker.list_candidates()
        self.assertEqual(len(candidates), 1)
        candidate = candidates[0]
        self.assertEqual(candidate["id"], candidate_id)
        self.assertEqual(candidate["name"], "홍길동")
        self.assertEqual(candidate["role"], "Backend")
        self.assertEqual(candidate["stage"], "applied")
        self.assertIn("updated_at", candidate)

    def test_advance_stage_and_history(self) -> None:
        candidate_id = self.tracker.add_candidate(
            "홍길동", "Backend", "hong@example.com", "referral"
        )

        self.tracker.advance_stage(candidate_id, "onsite", note="과제 제출")

        candidate = self.tracker.list_candidates()[0]
        self.assertEqual(candidate["stage"], "onsite")

        history = self.tracker.candidate_history(candidate_id)
        self.assertEqual(len(history), 2)  # 추가 + 단계 이동
        self.assertEqual(history[-1]["summary"], "applied -> onsite")
        self.assertEqual(history[-1]["note"], "과제 제출")

    def test_add_note_records_event(self) -> None:
        candidate_id = self.tracker.add_candidate(
            "홍길동", "Backend", "hong@example.com", "referral"
        )

        self.tracker.add_note(candidate_id, "연락 예정")

        history = self.tracker.candidate_history(candidate_id)
        self.assertTrue(
            any(event["type"] == "note" and event["note"] == "연락 예정" for event in history)
        )

    def test_invalid_json_recovers(self) -> None:
        # 손상된 JSON을 작성한 뒤 새 인스턴스를 만들어 복구 여부를 확인합니다.
        self.db_path.write_text("not-json")

        tracker = HiringTracker(self.db_path)
        self.assertEqual(tracker.data, {"candidates": {}, "events": []})


if __name__ == "__main__":
    unittest.main()
