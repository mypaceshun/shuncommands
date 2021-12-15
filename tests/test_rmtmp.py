from click.testing import CliRunner

from shuncommands import rmtmp


class TestRmTmp():
    def test_run(self):
        runner = CliRunner()
        res = runner.invoke(rmtmp.ctx, ['--help'])
        assert res.exit_code == 0

    def test_get_files(self):
        pass

    def test_filter_files(self):
        pass

    def test_rm_files(self):
        pass
