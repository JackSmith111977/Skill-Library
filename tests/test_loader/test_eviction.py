"""E11: LRU 淘汰策略测试"""

import pytest
from datetime import datetime, timezone

from skill_library.loader.eviction import LRUEvictor
from skill_library.loader.lifecycle import LoadManager


class TestLRUEvictor:
    """E11-S2: LRU 淘汰器"""

    def test_evict_when_over_limit(self):
        evictor = LRUEvictor(max_loaded=2)
        state = {
            "skills": {
                "s1": {"load-level": "L2", "last-used": "2020-01-01T00:00:00"},
                "s2": {"load-level": "L2", "last-used": "2020-01-02T00:00:00"},
                "s3": {"load-level": "L2", "last-used": "2020-01-03T00:00:00"},
            }
        }
        evicted = evictor.evict_if_needed(state)
        assert len(evicted) == 1
        # s1 has oldest last-used
        assert evicted[0]["skill"] == "s1"
        assert state["skills"]["s1"]["load-level"] == "L1"

    def test_evict_multiple(self):
        evictor = LRUEvictor(max_loaded=1)
        state = {
            "skills": {
                "s1": {"load-level": "L2", "last-used": "2020-01-01T00:00:00"},
                "s2": {"load-level": "L2", "last-used": "2020-01-02T00:00:00"},
                "s3": {"load-level": "L2", "last-used": "2020-01-03T00:00:00"},
            }
        }
        evicted = evictor.evict_if_needed(state)
        assert len(evicted) == 2
        assert evicted[0]["skill"] == "s1"
        assert evicted[1]["skill"] == "s2"

    def test_no_evict_when_under_limit(self):
        evictor = LRUEvictor(max_loaded=5)
        state = {"skills": {"s1": {"load-level": "L2"}, "s2": {"load-level": "L1"}}}
        evicted = evictor.evict_if_needed(state)
        assert evicted == []

    def test_empty_state(self):
        evictor = LRUEvictor(max_loaded=10)
        assert evictor.evict_if_needed({"skills": {}}) == []

    def test_invalid_max_loaded(self):
        with pytest.raises(ValueError):
            LRUEvictor(max_loaded=0)

    def test_record_access(self):
        evictor = LRUEvictor()
        state = {"skills": {"s1": {"load-level": "L2"}}}
        evictor.record_access("s1", state)
        assert "last-used" in state["skills"]["s1"]

    def test_record_access_agent_skills(self):
        evictor = LRUEvictor()
        state = {
            "skills": {"s1": {"load-level": "L2"}},
            "agents": {"a1": {"skills": {"s1": {"status": "mounted"}}}},
        }
        evictor.record_access("s1", state)
        assert "last-used" in state["agents"]["a1"]["skills"]["s1"]


class TestLastUsedTimestamp:
    """E11-S3: last-used 时间戳更新"""

    def test_load_updates_timestamp(self, tmp_path):
        mgr = LoadManager()
        skill = tmp_path / "test"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\nBody")
        mgr.load("test", skill, "L2")
        entry = mgr._cache["test"]
        assert "last-used" in entry["data"]

    def test_get_updates_timestamp(self, tmp_path):
        mgr = LoadManager()
        skill = tmp_path / "test"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: test\ndescription: test\n---\nBody")
        mgr.load("test", skill, "L1")
        ts1 = mgr._cache["test"]["data"].get("last-used", "")
        mgr.get("test")
        assert mgr._cache["test"]["data"]["last-used"] >= ts1

    def test_newly_loaded_not_evicted(self, tmp_path):
        """刚加载的 skill 不应被立即淘汰（如果在限额内）"""
        evictor = LRUEvictor(max_loaded=3)
        mgr = LoadManager()
        mgr.set_evictor(evictor)
        skills = []
        for i in range(3):
            s = tmp_path / f"skill-{i}"
            s.mkdir()
            (s / "SKILL.md").write_text(f"---\nname: skill-{i}\ndescription: s\n---\nBody")
            mgr.load(f"skill-{i}", s, "L2")
            skills.append(s)
        assert len(mgr.loaded()) == 3


class TestEvictionEvents:
    """E11-S4: 淘汰事件日志"""

    def test_events_recorded(self):
        evictor = LRUEvictor(max_loaded=2)
        state = {
            "skills": {
                "s1": {"load-level": "L2", "last-used": "2020-01-01"},
                "s2": {"load-level": "L2", "last-used": "2020-01-02"},
                "s3": {"load-level": "L2", "last-used": "2020-01-03"},
            }
        }
        evictor.evict_if_needed(state)
        events = evictor.get_events()
        assert len(events) == 1
        assert events[0]["skill"] == "s1"
        assert "evicted-at" in events[0]
        assert "last-used" in events[0]

    def test_clear_events(self):
        evictor = LRUEvictor(max_loaded=1)
        state = {
            "skills": {
                "s1": {"load-level": "L2", "last-used": "2020-01-01"},
                "s2": {"load-level": "L2", "last-used": "2020-01-02"},
            }
        }
        evictor.evict_if_needed(state)
        assert len(evictor.get_events()) == 1
        evictor.clear_events()
        assert evictor.get_events() == []

    def test_integration_with_load_manager(self, tmp_path):
        """集成：LoadManager + LRUEvictor 联动"""
        evictor = LRUEvictor(max_loaded=2)
        mgr = LoadManager()
        mgr.set_evictor(evictor)
        skills = []
        for i in range(3):
            s = tmp_path / f"skill-{i}"
            s.mkdir()
            (s / "SKILL.md").write_text(f"---\nname: skill-{i}\ndescription: s\n---\nBody")
            mgr.load(f"skill-{i}", s, "L2")
            skills.append(s)
        # 只有 2 个 slot，第 3 个加载时触发淘汰
        loaded = mgr.loaded()
        assert len(loaded) <= 3
        # oldest skill (skill-0) should be evicted to L1
        s0 = mgr.get("skill-0")
        assert s0["level"] == "L1"
        assert "body" not in s0
