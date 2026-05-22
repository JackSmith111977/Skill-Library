"""E8-S4: Token 估算器测试"""

from skill_library.loader.token_estimator import estimate_tokens, estimate_tokens_detailed


class TestTokenEstimator:
    def test_estimate_tokens(self):
        text = "a" * 100
        assert estimate_tokens(text) == 25

    def test_estimate_empty(self):
        assert estimate_tokens("") == 0

    def test_estimate_detailed(self):
        result = estimate_tokens_detailed("a" * 40)
        assert result["chars"] == 40
        assert result["estimated_tokens"] == 10
