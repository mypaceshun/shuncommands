from click.testing import CliRunner

from shuncommands import pdftool


class TestPdfTool:
    def test_run_help(self):
        runner = CliRunner()
        res = runner.invoke(pdftool.ctx, ["--help"])
        assert res.exit_code == 0

        res = runner.invoke(pdftool.ctx, ["-h"])
        assert res.exit_code == 0

    def test_run_version(self):
        runner = CliRunner()
        res = runner.invoke(pdftool.ctx, ["--version"])
        assert res.exit_code == 0

        res = runner.invoke(pdftool.ctx, ["-v"])
        assert res.exit_code == 0

    def test_run_unlock(self):
        runner = CliRunner()
        res = runner.invoke(pdftool.ctx, ["unlock", "--help"])
        assert res.exit_code == 0

        res = runner.invoke(pdftool.ctx, ["unlock", "-h"])
        assert res.exit_code == 0

    def test_run_text(self):
        runner = CliRunner()
        res = runner.invoke(pdftool.ctx, ["text", "--help"])
        assert res.exit_code == 0

        res = runner.invoke(pdftool.ctx, ["text", "-h"])
        assert res.exit_code == 0
