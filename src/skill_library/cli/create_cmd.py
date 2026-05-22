"""create 子命令"""

import click

from ..templates.engine import create_skill


@click.command()
@click.argument("name")
@click.option("--type", "skill_type", default="atomic", type=click.Choice(["atomic", "workflow"]),
              help="Skill 类型")
@click.option("--pack", default="default", help="所属 pack")
@click.option("--description", default="", help="Skill 描述")
@click.option("--version", default="0.1.0", help="版本号")
@click.option("--design-pattern", default=None,
              type=click.Choice(["tool-wrapper", "pipeline", "inversion", "reviewer", "generator"]),
              help="设计模式（workflow 类型必选）")
@click.option("--output-dir", default=".", help="输出目录")
def create(name, skill_type, pack, description, version, design_pattern, output_dir):
    """创建新 skill"""
    try:
        skill_path = create_skill(
            name=name,
            output_dir=output_dir,
            skill_type=skill_type,
            description=description,
            pack=pack,
            version=version,
            design_pattern=design_pattern,
        )
        click.echo(f"Skill 已创建: {skill_path}")
    except (ValueError, Exception) as e:
        click.echo(f"创建失败: {e}", err=True)
        raise SystemExit(1)
