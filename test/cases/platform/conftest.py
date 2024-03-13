#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：conftest.py
@Author  ：Zeno
@Email   ：zhangyongjun@ones.cn
@Date    ：2021/11/25 
@Desc    ：
"""

import pytest
from falcons.com.nick import fixture
from falcons.com.pw import SinglePlay
from falcons.pages import Browser
from ones_action.act.team import TeamAction

# from ones_action.

GLOBAL_DRIVER = None


@fixture(scope='session', name='pw')
def my_driver() -> Browser:
    """"""
    TeamAction.update_team_name()

    with SinglePlay() as p:
        page = Browser()
        page.sync_page(p)

        global GLOBAL_DRIVER
        GLOBAL_DRIVER = page

        # print(f'Now UI project name is :[{page.env.proj_name}]')
        yield page

        page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """当用例失败后，会执行刷新页面操作，防止弹窗未关闭"""
    out = yield
    report = out.get_result()
    if (report.when == "call" or report.when == "setup") and report.outcome == 'failed':
        if report.outcome == 'failed':
            # 刷新页面
            global GLOBAL_DRIVER
            # GLOBAL_DRIVER.refresh()
            print(f'\nRefresh page when case [{item.name}] failed\n')
