"""version 子命令"""

import importlib.metadata
import click


@click.command(name="version")
def version():
    """显示版本信息"""
    try:
        ver = importlib.metadata.version("skill-library")
    except importlib.metadata.PackageNotFoundError:
        ver = "0.1.0 (dev)"
    click.echo(f"skill-manager version {ver}")
