#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/2/4 14:20
# @Author : lishiguang
# @File : test_item_handler.py
import pytest
from falcons.check import go
from allure_commons._allure import story, feature, severity
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install, ability_plugin_enable
from falcons.platform.pluginlifecycle.interface.interface_action import InterfacePlugins
from test.cases.utils.tools import env_clean
from falcons.com.env import EnvContext
from ones_action.act import pro


@feature("Item处理器测试用例")
class TestItemHandler:
    path = "app/project/intercept_item_actions/1.0.0"

    @story("清理环境")
    def teardown_method(self):
        env_clean(path=self.path)

    @story("安装插件")
    def setup_method(self):
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)

    @story('Item处理器能力创建项目')
    @pytest.mark.flaky(reruns=0, reruns_delay=3)
    def test_item_handler_pro(self):
        header_param = {
            'Ones-Check-Point': 'team',
            'Ones-Check-Id': EnvContext.user.team_uuid,
            'Ones-User-Id': EnvContext.user.member_uuid,
            'Ones-Auth-Token': EnvContext.user.token
        }
        proj_uuid = pro.PrjAction.new_project()
        InterfacePlugins.call_team_external('validateItemHandler', header=header_param)
        pro.PrjAction.delete_project(proj_uuid)

    # @story('Item处理器能力创建任务')
    # @pytest.mark.flaky(reruns=0, reruns_delay=3)
    # def test_item_handle_task(self):
    #     header_param = {
    #         'Ones-Check-Point': 'team',
    #         'Ones-Check-Id': EnvContext.user.team_uuid,
    #         'Ones-User-Id': EnvContext.user.member_uuid,
    #         'Ones-Auth-Token': EnvContext.user.token
    #     }
    #
    #     # 创建任务
    #     proj_uuid, proj_name = pro.PrjAction.new_project()
    #     task.TaskAction.new_issue(proj_uuid)
    #     InterfacePlugins.call_team_external('validateItemHandler', header=header_param)
    #     pro.PrjAction.delete_project(proj_uuid)

    # @story('Item处理器能力添加工时')
    # @pytest.mark.flaky(reruns=0, reruns_delay=3)
    # def test_item_handle_hour(self):
    #     header_param = {
    #         'Ones-Check-Point': 'team',
    #         'Ones-Check-Id': EnvContext.user.team_uuid,
    #         'Ones-User-Id': EnvContext.user.member_uuid,
    #         'Ones-Auth-Token': EnvContext.user.token
    #     }
    #     res1 = pro.PrjAction.new_project()
    #     res = task.TaskAction.new_issue(res1)
    #     task.TaskAction.add_work_hour(res)
    #     InterfacePlugins.call_team_external('validateItemHandler', header=header_param)
    #     task.TaskAction.del_task(res)
    #
    # @story('Item处理器能力更新剩余工时')
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    # def test_item_handle_remaining_hour(self):
    #     header_param = {
    #         'Ones-Check-Point': 'team',
    #         'Ones-Check-Id': EnvContext.user.team_uuid,
    #         'Ones-User-Id': EnvContext.user.member_uuid,
    #         'Ones-Auth-Token': EnvContext.user.token
    #     }
    #     # 创建任务
    #     res = task.TaskAction.new_issue()
    #     # 修改预估工时
    #     task.TaskAction.add_assess_hour(res)
    #     InterfacePlugins.call_team_external('validateItemHandler', header=header_param)
    #     task.TaskAction.del_task(res)
    #
    # @story('Item处理器能力创建项目计划')
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    # def test_item_handle_remaining_hour(self):
    #     header_param = {
    #         'Ones-Check-Point': 'team',
    #         'Ones-Check-Id': EnvContext.user.team_uuid,
    #         'Ones-User-Id': EnvContext.user.member_uuid,
    #         'Ones-Auth-Token': EnvContext.user.token
    #     }
    #     # 创建项目
    #     res = pro.PrjAction.new_project()
    #     # 添加项目计划
    #     res1 = pro.PrjAction.add_prj_plan_component()
    #     # 创建项目计划
    #     res = pro.PrjSettingAction.add_gattdata()
    #     InterfacePlugins.call_team_external('validateItemHandler', header=header_param)
