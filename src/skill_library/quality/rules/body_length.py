"""Rule 4: body 长度校验"""

from ..models import LintWarning

MAX_LINES = 500
MAX_TOKENS_ESTIMATE = 5000
CHARS_PER_TOKEN = 4  # 粗略估算


def check_body_length(body: str) -> list[LintWarning]:
    """校验 body 长度"""
    warnings = []

    if not body:
        return warnings

    lines = body.split("\n")
    if len(lines) > MAX_LINES:
        warnings.append(LintWarning(
            rule="body-length",
            message=f"body 行数 {len(lines)} 超过 {MAX_LINES} 行",
        ))

    # 粗略估算 token
    estimated_tokens = len(body) // CHARS_PER_TOKEN
    if estimated_tokens > MAX_TOKENS_ESTIMATE:
        warnings.append(LintWarning(
            rule="body-length",
            message=f"body 估算 token 数 {estimated_tokens} 超过 {MAX_TOKENS_ESTIMATE}",
        ))

    return warnings


def estimate_tokens(text: str) -> int:
    """粗略估算 token 数"""
    return len(text) // CHARS_PER_TOKEN
