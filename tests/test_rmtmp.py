from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

import pytest
from click.testing import CliRunner

from shuncommands import rmtmp


@pytest.fixture
def init_tmpdir():
    """
    tmpdir
        - .rmtmpignore
        - testfile
        - testdir
            - testfile2
        - ignorefile
        - ignoredir
            - testfile3
    """
    tmpdir = mkdtemp()
    mkdir_dirs = ["testdir", "ignoredir"]
    touch_files = ["testfile", "testdir/testfile2", "ignorefile", "ignoredir/testfile3"]
    for d in mkdir_dirs:
        Path(tmpdir, d).mkdir()
    for f in touch_files:
        Path(tmpdir, f).touch()
    with Path(tmpdir, ".rmtmpignore").open("w") as fd:
        fd.write("ignorefile\n")
        fd.write("ignoredir\n")
    yield tmpdir
    rmtree(tmpdir)


class TestRmTmp:
    def test_run_help(self):
        runner = CliRunner()
        res = runner.invoke(rmtmp.ctx, ["--help"])
        assert res.exit_code == 0

        res = runner.invoke(rmtmp.ctx, ["-h"])
        assert res.exit_code == 0

    def test_run_version(self):
        runner = CliRunner()
        res = runner.invoke(rmtmp.ctx, ["--version"])
        assert res.exit_code == 0

        res = runner.invoke(rmtmp.ctx, ["-v"])
        assert res.exit_code == 0

    def test_run(self, init_tmpdir):
        tmpdir = init_tmpdir
        runner = CliRunner()
        res = runner.invoke(rmtmp.ctx, ["-d", "0", tmpdir])
        assert res.exit_code == 0

        files = [f for f in Path(tmpdir).iterdir()]
        assert set(files) == set(
            [
                Path(tmpdir, ".rmtmpignore"),
                Path(tmpdir, "ignorefile"),
                Path(tmpdir, "ignoredir"),
            ]
        )

    def test_get_files(self, init_tmpdir):
        tmpdir = init_tmpdir
        files = rmtmp.get_files(Path(tmpdir))
        expect_paths = [
            Path(tmpdir, ".rmtmpignore"),
            Path(tmpdir, "testfile"),
            Path(tmpdir, "ignorefile"),
            Path(tmpdir, "testdir"),
            Path(tmpdir, "ignoredir"),
        ]
        assert set(files) == set(expect_paths)

    def test_filter_files(self, init_tmpdir):
        tmpdir = init_tmpdir
        target_paths = [
            Path(tmpdir, ".rmtmpignore"),
            Path(tmpdir, "testfile"),
            Path(tmpdir, "ignorefile"),
            Path(tmpdir, "testdir"),
            Path(tmpdir, "ignoredir"),
        ]
        filter_paths = rmtmp.filter_files(target_paths)
        assert filter_paths == []

        filter_paths = rmtmp.filter_files(target_paths, day=0)
        assert set(filter_paths) == set(target_paths)

        filter_paths = rmtmp.filter_files(
            target_paths, day=0, rmtmpignore=Path(tmpdir, ".rmtmpignore")
        )
        assert set(filter_paths) == set(
            [Path(tmpdir, "testfile"), Path(tmpdir, "testdir")]
        )

    def test_rm_files(self, init_tmpdir):
        tmpdir = init_tmpdir
        rmtmp.rm_files([Path(tmpdir, "testfile"), Path(tmpdir, "testdir")])
        files = [f for f in Path(tmpdir).iterdir()]
        assert set(files) == set(
            [
                Path(tmpdir, ".rmtmpignore"),
                Path(tmpdir, "ignorefile"),
                Path(tmpdir, "ignoredir"),
            ]
        )
