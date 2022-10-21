# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxy_pool
   Description :   proxy pool 启动入口
   Author :        JHao
   date：          2020/6/19
-------------------------------------------------
   Change Activity:
                   2020/6/19:
-------------------------------------------------
"""
__author__ = 'JHao'

import time
from datetime import timedelta

import click
from timeloop import Timeloop
from schedule import every, repeat, run_pending

tl = Timeloop()
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """ProxyPool cli工具"""


def _init():
    print('init')


@cli.command(name="init")
def init():
    """ 启动调度程序 """
    _init()


@repeat(every(10).seconds)
def _check():
    print('check')


@cli.command(name="check")
def check():
    """ 启动api服务 """
    _check()
    while True:
        run_pending()
        time.sleep(1)


if __name__ == '__main__':
    cli()
