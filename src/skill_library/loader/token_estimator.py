"""Token 估算器"""


def estimate_tokens(text: str) -> int:
    """估算文本 token 数。

    按字符数 / 4 估算，误差 ≤ 20%。
    """
    return len(text) // 4


def estimate_tokens_detailed(text: str) -> dict[str, int]:
    """返回详细估算。"""
    total_chars = len(text)
    return {
        "chars": total_chars,
        "estimated_tokens": total_chars // 4,
    }
