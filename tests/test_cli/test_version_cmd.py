"""E13-S4: 版本命令测试"""

from click.testing import CliRunner
from skill_library.cli.main import cli


class TestVersionCommand:

    def test_version_subcommand(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "version" in result.output

    def test_version_option(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output or "skill-manager" in result.output
