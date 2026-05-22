"""CLI 入口"""

import click


@click.group()
@click.version_option(version="0.1.0", prog_name="skill-manager")
def cli():
    """Skill Library 管理工具"""
    pass


# 延迟注册子命令，避免循环导入
def _register_commands():
    from .lint_cmd import lint
    cli.add_command(lint)


_register_commands()
