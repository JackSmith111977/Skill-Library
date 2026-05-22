"""register 子命令：扫描目录并注册 skill 到 state.json"""

from pathlib import Path

import click

from ..state.manager import StateManager
from ..registry.indexer import SkillIndexer
from ..registry.scanner import scan_skills
from ..registry.parser import parse_skill_md


@click.command()
@click.argument("skills_dir", type=click.Path(exists=True, file_okay=False))
@click.option("--state", default="state.json", help="state.json 路径")
@click.option("--dry-run", is_flag=True, help="预览不写入")
@click.option("--pack", default=None, help="分配给所有注册技能的技能包")
def register(skills_dir: str, state: str, dry_run: bool, pack: str | None):
    """扫描 skills/ 目录并注册所有 skill 到 state.json"""
    skills_dir = Path(skills_dir)
    found = scan_skills(skills_dir)

    if not found:
        click.echo(f"未发现包含 SKILL.md 的 skill 目录: {skills_dir}")
        raise SystemExit(0)

    click.echo(f"发现 {len(found)} 个 skill:\n")
    for s in found:
        meta = parse_skill_md(s)
        click.echo(f"  [{meta.get('name', '?')}] {s.name}  v{meta.get('version', '0.0.0')}")

    if dry_run:
        click.echo(f"\n--dry-run 模式，未写入 state.json")
        return

    # 注册到 state.json
    sm = StateManager(state)
    indexer = SkillIndexer(sm)
    registered = 0
    for skill_path in found:
        try:
            entry = indexer.register(skill_path)
            if pack:
                state_data = sm.load()
                state_data["skills"][entry["name"]]["pack"] = pack
                sm.save(state_data)
            registered += 1
        except ValueError as e:
            click.echo(f"  跳过 {skill_path.name}: {e}", err=True)

    click.echo(f"\n已注册 {registered}/{len(found)} 个 skill 到 {state}")
