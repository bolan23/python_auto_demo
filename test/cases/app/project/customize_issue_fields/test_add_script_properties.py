#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/3/6 15:01
# @Author   : lanbo
# @File     :test_add_script_properties.py
import os.path
import shutil
import sys
import time
from glob import glob
import requests
from allure_commons._allure import story, feature, severity
from falcons.platform.pluginlifecycle import helper
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install, ability_plugin_enable
from falcons.platform.pluginlifecycle.interface.interface_action import InterfacePlugins
from falcons.com.env import EnvContext

from test.cases.utils.tools import env_clean


@feature("自定义工作项属性：添加单选/多选菜单属性")
class TestAddScriptProperties:
    path = "/app/project/customize_issue_fields/1.0.0"

    @story("清理环境")
    def teardown_method(self):
        env_clean(path=self.path)

    @story("安装插件")
    def setup_method(self):
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)


    @severity("blocker")
    @story("添加工作项单选/多选菜单属性")
    def test_add_issue_fields(self):
        time.sleep(2)
        team_uuid = EnvContext.user.team_uuid
        user_uuid = EnvContext.user.owner_uuid
        instance_uuid = helper.get_plugin_instanceUUID()
        create_issue_url = f'{EnvContext.host}/project/api/project/creatScriptField'
        create_issue_headers = {
            'Content-Type': 'application/json',
            'Ones-Check-Point': 'team',
            'Ones-User-Id': user_uuid,
            'Ones-Check-Id': team_uuid,
            'Ones-Plugin-Id': instance_uuid,
        }
        create_issue_response = requests.request(method='POST', url=create_issue_url, headers=create_issue_headers)
        create_issue_response.raise_for_status()  # 检查请求
        # 校验结果
        time.sleep(1)
        InterfacePlugins.call_team_ab_external('CustomizeIssueFields')

    @severity("blocker")
    @story("添加产品层单选/多选菜单属性")
    def test_add_product_fields(self):
        time.sleep(2)
        team_uuid = EnvContext.user.team_uuid
        user_uuid = EnvContext.user.owner_uuid
        instance_uuid = helper.get_plugin_instanceUUID()
        create_issue_url = f'{EnvContext.host}/project/api/project/creatProductField'
        create_issue_headers = {
            'Content-Type': 'application/json',
            'Ones-Check-Point': 'team',
            'Ones-User-Id': user_uuid,
            'Ones-Check-Id': team_uuid,
            'Ones-Plugin-Id': instance_uuid,
        }
        create_issue_response = requests.request(method='POST', url=create_issue_url, headers=create_issue_headers)
        create_issue_response.raise_for_status()  # 检查请求
        # 校验结果
        time.sleep(1)
        InterfacePlugins.call_team_ab_external('CustomizeIssueFields')

    @severity("blocker")
    @story("添加项目层单选/多选菜单属性")
    def test_add_project_fields(self):
        time.sleep(2)
        team_uuid = EnvContext.user.team_uuid
        user_uuid = EnvContext.user.owner_uuid
        instance_uuid = helper.get_plugin_instanceUUID()
        create_issue_url = f'{EnvContext.host}/project/api/project/creatProjectField'
        create_issue_headers = {
            'Content-Type': 'application/json',
            'Ones-Check-Point': 'team',
            'Ones-User-Id': user_uuid,
            'Ones-Check-Id': team_uuid,
            'Ones-Plugin-Id': instance_uuid,
        }
        create_issue_response = requests.request(method='POST', url=create_issue_url, headers=create_issue_headers)
        create_issue_response.raise_for_status()  # 检查请求
        # 校验结果
        time.sleep(1)
        InterfacePlugins.call_team_ab_external('CustomizeIssueFields')

    @severity("blocker")
    @story("添加工作项属性组")
    def test_add_issue_group(self):
        time.sleep(2)
        team_uuid = EnvContext.user.team_uuid
        user_uuid = EnvContext.user.owner_uuid
        instance_uuid = helper.get_plugin_instanceUUID()
        create_issue_url = f'{EnvContext.host}/project/api/project/creatScriptFieldGroup'
        create_issue_headers = {
            'Content-Type': 'application/json',
            'Ones-Check-Point': 'team',
            'Ones-User-Id': user_uuid,
            'Ones-Check-Id': team_uuid,
            'Ones-Plugin-Id': instance_uuid,
        }
        create_issue_response = requests.request(method='POST', url=create_issue_url, headers=create_issue_headers)
        create_issue_response.raise_for_status()  # 检查请求
        # 校验结果
        time.sleep(1)
        InterfacePlugins.call_team_ab_external('CustomizeIssueFields')

    @severity("blocker")
    @story("添加产品层属性组")
    def test_add_product_group(self):
        time.sleep(2)
        team_uuid = EnvContext.user.team_uuid
        user_uuid = EnvContext.user.owner_uuid
        instance_uuid = helper.get_plugin_instanceUUID()
        create_issue_url = f'{EnvContext.host}/project/api/project/createProductFieldGroup'
        create_issue_headers = {
            'Content-Type': 'application/json',
            'Ones-Check-Point': 'team',
            'Ones-User-Id': user_uuid,
            'Ones-Check-Id': team_uuid,
            'Ones-Plugin-Id': instance_uuid,
        }
        create_issue_response = requests.request(method='POST', url=create_issue_url, headers=create_issue_headers)
        create_issue_response.raise_for_status()  # 检查请求
        # 校验结果
        time.sleep(1)
        InterfacePlugins.call_team_ab_external('CustomizeIssueFields')

    @severity("blocker")
    @story("添加项目层属性组")
    def test_add_project_group(self):
        time.sleep(2)
        team_uuid = EnvContext.user.team_uuid
        user_uuid = EnvContext.user.owner_uuid
        instance_uuid = helper.get_plugin_instanceUUID()
        create_issue_url = f'{EnvContext.host}/project/api/project/createProjectFieldGroup'
        create_issue_headers = {
            'Content-Type': 'application/json',
            'Ones-Check-Point': 'team',
            'Ones-User-Id': user_uuid,
            'Ones-Check-Id': team_uuid,
            'Ones-Plugin-Id': instance_uuid,
        }
        create_issue_response = requests.request(method='POST', url=create_issue_url, headers=create_issue_headers)
        create_issue_response.raise_for_status()  # 检查请求
        # 校验结果
        time.sleep(1)
        InterfacePlugins.call_team_ab_external('CustomizeIssueFields')