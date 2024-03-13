#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/2/5 14:23
# @Author : lishiguang
# @File : test_project_components.py
import time

import pytest
from allure_commons._allure import story, feature, severity
from falcons.com.nick import fixture
from falcons.pages import Browser
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install, ability_plugin_enable
from falcons.platform.pluginlifecycle.interface.interface_action import InterfacePlugins
from test.cases.utils.tools import env_clean
from falcons.com.env import EnvContext
from ones_action.act import pro, task


@feature("自定义项目组件测试用例")
class TestProjectComponents:
    path = "app/project/customize_project_components/1.0.0"

    @story("清理环境")
    def teardown_method(self):
        """
        后置
        """
        env_clean(path=self.path)

    @story("安装插件")
    def setup_method(self):
        """前置
        """
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)

    @story('在项目中安装自定义组件并复制项目')
    @pytest.mark.flaky(reruns=0, reruns_delay=0)
    def test_project_components(self, pw: Browser):
        pw.go_to(EnvContext.host + '/project/#/home/project')
        # 创建项目
        proj_uuid = pro.PrjAction.new_project(name="tester01")
        # 添加自定义项目组件
        pro.PrjAction.add_component(component_name='project_custom_component', project_uuid=proj_uuid)
        pw.click_link('项目管理')
        time.sleep(1)
        # 点击项目名称
        pw.action_click('//div[text()="tester01"]')
        # 点击导航栏自定义组件
        pw.action_click('//span[text()="project_custom_component"]')
        # 验证项目信息
        pw.click_button('Show TeamInfo')
        # 数据校验
        project_uuid_slot = pw.find_element('//*[@id="ones-mf-root"]').inner_text()
        assert project_uuid_slot == proj_uuid
        # 点击设置 验证复制
        pw.action_click('//span[text()="设置"]')
        pw.action_click('//span[text()="项目操作"]')
        pw.action_click('//span[text()="复制项目"]')
        time.sleep(1)
        pw.click_button('确定')
        pw.action_click(f'(//*[text()="确定"])[2]')
        pw.click_link('项目管理')
        time.sleep(2)
        # 校验复制成功的项目
        pw.action_click('//div[text()="tester01 (复制)"]')
        pw.click_button('Show TeamInfo')
        # 删除项目
        pro.PrjAction.delete_project(proj_uuid)

