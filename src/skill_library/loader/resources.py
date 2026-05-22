"""L3 资源加载器"""

from pathlib import Path


def load_references(skill_path: str | Path) -> dict[str, str]:
    """加载 references/ 下所有文件。"""
    ref_dir = Path(skill_path) / "references"
    if not ref_dir.is_dir():
        return {}

    result: dict[str, str] = {}
    for f in sorted(ref_dir.iterdir()):
        if f.is_file():
            try:
                result[f.name] = f.read_text(encoding="utf-8")
            except Exception:
                result[f.name] = ""
    return result


def load_assets(skill_path: str | Path) -> list[str]:
    """列出 assets/ 下文件名称。"""
    assets_dir = Path(skill_path) / "assets"
    if not assets_dir.is_dir():
        return []

    return sorted(f.name for f in assets_dir.iterdir() if f.is_file())


def load_all_resources(skill_path: str | Path) -> dict[str, dict[str, str] | list[str]]:
    """加载所有 L3 资源。"""
    return {
        "references": load_references(skill_path),
        "assets": load_assets(skill_path),
    }
