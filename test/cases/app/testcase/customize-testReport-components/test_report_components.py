#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/2/23 14:29
# @Author : lishiguang
# @File : test_report_components.py
import time

from falcons.com.env import EnvContext
from falcons.com.nick import story, feature
from falcons.pages import Browser
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install, ability_plugin_enable

from test.cases.utils.tools import env_clean
from test.utils.ui import UiPluginPath


@feature("自定义测试报告组件")
class TestReportComponents:
    path = UiPluginPath.test

    @story("清理环境")
    def teardown_method(self):
        """
        清理环境
        """
        env_clean(path=self.path)

    @story("安装启用插件")
    def setup_method(self):
        """
        安装启动插件
        """
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)

    @story('自定义测试报告组件')
    def test_report_components(self, pw: Browser):
        # plan_uuid = case.CaseAction.add_testcase_plan('test')
        pw.go_to(EnvContext.host + '/project/#/testcase/team/' + EnvContext.team_uuid + '/report')
        pw.refresh()
        # 创建测试报告
        pw.click_link('测试报告')
        pw.click_button('新建测试报告')
        pw.send_key('//input[@placeholder="请输入测试报告名称"]', 'test')
        pw.click_button('下一步')
        pw.action_click("//*//span[@title='【示例】敏捷式研发管理']")
        pw.action_click('//*//input[@type="checkbox"]')
        pw.click_button('完成')
        # 编辑测试报告
        time.sleep(2)
        pw.action_click('//span[text()="编辑组件"]')
        # 校验自定义组件存在
        pw.check_checkbox(elem="//*[contains(text(), 'Test report custom component name')]")
        # 拖动组件
        source = pw.page.locator(".ComponentItem:has-text('Test report custom component name')")
        target = pw.page.locator('div.report-components')
        source.drag_to(target)
        # 输入组件名称
        time.sleep(2)
        pw.send_key('//*//input[@id="name"]', 'autotest')
        pw.click_button('确定')
        pw.click_button('保存')
        # 验证数据组件uuid
        component_uuid = pw.page.get_by_text('//*[contains(text()"测试报告ID")]')
        if component_uuid != 'undefined':
            pass
        else:
            raise AssertionError('未能获取到component_uuid')



