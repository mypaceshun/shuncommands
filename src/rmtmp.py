#!/usr/bin/env python3

from datetime import datetime, timedelta
from pathlib import Path
from shutil import rmtree

import click
from gitignore_parser import parse_gitignore


@click.command(no_args_is_help=True)
@click.option('-q', '--quiet',
              is_flag=True,
              help='quiet output')
@click.option('--dry-run',
              is_flag=True)
@click.option('-d', '--day',
              type=int,
              default=3,
              help='削除対象となる期日',
              show_default=True)
@click.argument('targetdir',
                type=click.Path(exists=True))
def ctx(targetdir, day, dry_run, quiet):
    '''
    tmpディレクトリの中身お掃除君

    \b
    <TARGETDIR>で指定されたディレクトリの中身をせっせとお掃除してくれるかわいいやつ。
    自分がよく ~/document/tmp/ とか雑にディレクトリ作ってしまうので、それのお掃除用に生まれた

    <TARGETDIR>/.rmtmpignore のファイルに gitignore と同様の書式でファイルを指定することで、
    削除対象から明示的に外すことができる。
    '''
    target = Path(targetdir).expanduser()
    if not quiet:
        click.echo(f'target is [{target}]')
    rmtmpignore = Path(target, '.rmtmpignore')
    target_files = get_files(target, day)
    if rmtmpignore.exists():
        if not quiet:
            click.echo(f'find [{rmtmpignore}]')
        target_files.pop(target_files.index(rmtmpignore))
        target_files = filter_files(target_files, rmtmpignore)
    rm_files(target_files, dry_run, quiet)


def get_files(target, day):
    files = []
    for file in target.iterdir():
        mtime = datetime.fromtimestamp(file.stat().st_mtime)
        today = datetime.now()
        if mtime + timedelta(days=day) < today:
            files.append(file)
    return files


def filter_files(target_files, rmtmpignore):
    files = []
    matches = parse_gitignore(rmtmpignore)
    for file in target_files:
        if not matches(file):
            files.append(file)
    return files


def rm_files(target_files, dry_run, quiet):
    for file in target_files:
        if dry_run is True:
            click.echo(file)
        else:
            try:
                if not quiet:
                    click.echo(f'rm [{file}]')
                if file.is_dir():
                    rmtree(file)
                else:
                    file.unlink()
            except Exception as error:
                msg = f'{file} remove failur [{error}]'
                click.echo(msg, err=True)
