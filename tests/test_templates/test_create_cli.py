"""E6-S3: create CLI 测试"""

from click.testing import CliRunner
import pytest

from skill_library.cli.main import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestCreateCLI:
    def test_create_atomic(self, runner, tmp_path):
        """创建原子 skill"""
        result = runner.invoke(cli, ["create", "test-skill",
                                      "--output-dir", str(tmp_path),
                                      "--description", "test skill"])
        assert result.exit_code == 0
        assert "已创建" in result.output
        assert (tmp_path / "default" / "test-skill" / "SKILL.md").exists()

    def test_create_workflow(self, runner, tmp_path):
        """创建工作流 skill"""
        result = runner.invoke(cli, ["create", "test-workflow",
                                      "--type", "workflow",
                                      "--output-dir", str(tmp_path),
                                      "--description", "test workflow",
                                      "--design-pattern", "pipeline"])
        assert result.exit_code == 0
        assert (tmp_path / "default" / "test-workflow" / "SKILL.md").exists()

    def test_create_with_pack(self, runner, tmp_path):
        """指定 pack"""
        result = runner.invoke(cli, ["create", "packed-skill",
                                      "--pack", "my-pack",
                                      "--output-dir", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / "my-pack" / "packed-skill" / "SKILL.md").exists()

    def test_create_fails_invalid_type(self, runner, tmp_path):
        """非法类型返回非零"""
        result = runner.invoke(cli, ["create", "test",
                                      "--type", "invalid",
                                      "--output-dir", str(tmp_path)])
        assert result.exit_code != 0
