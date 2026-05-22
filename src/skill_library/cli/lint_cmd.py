"""lint 子命令"""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from ..quality.lint import QualityEngine


console = Console()


@click.command()
@click.argument("skill_path", type=click.Path(exists=True, file_okay=False))
@click.option("--json", "output_json", is_flag=True, help="输出 JSON 格式")
def lint(skill_path: str, output_json: bool):
    """检测 skill 质量"""
    engine = QualityEngine()
    result = engine.lint_atomic(Path(skill_path))

    if output_json:
        import json
        click.echo(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_report(result)

    raise SystemExit(0 if result.passed else 1)


def _print_report(result):
    """输出可读报告"""
    # 标题
    status = "[green]PASSED[/green]" if result.passed else "[red]FAILED[/red]"
    console.print(f"\nLint Result: {status}  Score: {result.score}/100\n")

    if not result.errors and not result.warnings:
        console.print("[green]No issues found.[/green]\n")
        return

    # 错误表格
    if result.errors:
        table = Table(title="Errors", title_style="red bold")
        table.add_column("Rule", style="red")
        table.add_column("Message")
        for err in result.errors:
            table.add_row(err.rule, err.message)
        console.print(table)

    # 警告表格
    if result.warnings:
        table = Table(title="Warnings", title_style="yellow bold")
        table.add_column("Rule", style="yellow")
        table.add_column("Message")
        for warn in result.warnings:
            table.add_row(warn.rule, warn.message)
        console.print(table)

    console.print()
