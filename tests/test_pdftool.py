from click.testing import CliRunner

from shuncommands import pdftool


class TestPdfTool():
    def test_run(self):
        runner = CliRunner()
        res = runner.invoke(pdftool.ctx, ['--help'])
        assert res.exit_code == 0

    def test_run_unlock(self):
        runner = CliRunner()
        res = runner.invoke(pdftool.ctx, ['unlock', '--help'])
        assert res.exit_code == 0
