"""load 子命令"""

import click

from ..loader.lifecycle import LoadManager

load_manager = LoadManager()


@click.command()
@click.argument("name")
@click.option("--level", default="L1", type=click.Choice(["L1", "L2", "L3"]),
              help="加载级别")
@click.option("--path", default=None, help="skill 目录路径")
def load(name, level, path):
    """加载 skill 到指定级别"""
    if not path:
        # 尝试从 state.json 查找
        from ..state.manager import StateManager
        sm = StateManager("state.json")
        state = sm.load()
        skill_info = state.get("skills", {}).get(name)
        if skill_info:
            path = skill_info.get("path")
        else:
            click.echo(f"skill 未找到: {name}", err=True)
            raise SystemExit(1)

    try:
        result = load_manager.load(name, path, level)
        click.echo(f"Loaded {name} at {level}: {result.get('name')} v{result.get('version', '0.0.0')}")
    except Exception as e:
        click.echo(f"加载失败: {e}", err=True)
        raise SystemExit(1)
