#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/3/6 15:18
# @Author   : lanbo
# @File     :test_modify_script_properties.py
import os.path
import shutil
import sys
import time
import uuid
from glob import glob
import requests
from allure_commons._allure import story, feature, severity
from falcons.platform.pluginlifecycle import helper
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install, ability_plugin_enable
from falcons.platform.pluginlifecycle.interface.interface_action import InterfacePlugins
from falcons.com.env import EnvContext

from test.cases.utils.tools import env_clean


@feature("自定义工作项属性：修改菜单属性")
class TestModifyScriptProperties:
    path = "/app/project/customize_issue_fields/1.0.0"

    @story("清理环境")
    def teardown_method(self):
        env_clean(path=self.path)

    @story("安装插件")
    def setup_method(self):
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)

    @severity("blocker")
    @story("修改工作项菜单属性：选项名称")
    def test_modify_issue_fields(self):
        time.sleep(2)
        team_uuid = EnvContext.user.team_uuid
        user_uuid = EnvContext.user.owner_uuid
        instance_uuid = helper.get_plugin_instanceUUID()
        # 新建菜单选项
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
        field_uuid = create_issue_response.json()['data']['message'][0]
        # 修改属性组
        new_name = str(uuid.uuid4())
        update_issue_response = f'{EnvContext.host}/project/api/project/UpdateName'
        update_issue_body = {
            'name': '自动化测试修改属性组名称{}'.format(new_name),
            'team_uuid': team_uuid,
            'field_uuid': field_uuid,
            'pool': "Task"
        }
        update_issue_response = requests.request(method='POST', url=update_issue_response, headers=create_issue_headers, json=update_issue_body)
        update_issue_response.raise_for_status()
        time.sleep(2)
        # 校验结果
        InterfacePlugins.call_team_ab_external('CustomizeUpdateName')

    @severity("blocker")
    @story("修改工作项属性组属性：随机修改组名称")
    def test_modify_issue_group(self):
        time.sleep(2)
        team_uuid = EnvContext.user.team_uuid
        user_uuid = EnvContext.user.owner_uuid
        instance_uuid = helper.get_plugin_instanceUUID()
        create_group_url = f'{EnvContext.host}/project/api/project/creatScriptFieldGroup'
        create_group_headers = {
            'Content-Type': 'application/json',
            'Ones-Check-Point': 'team',
            'Ones-User-Id': user_uuid,
            'Ones-Check-Id': team_uuid,
            'Ones-Plugin-Id': instance_uuid,
        }
        create_issue_response = requests.request(method='POST', url=create_group_url, headers=create_group_headers)
        create_issue_response.raise_for_status()  # 检查请求
        # 校验结果
        time.sleep(1)
        field_uuid1 = create_issue_response.json()['data']['message'][0]
        field_uuid2 = create_issue_response.json()['data']['message'][1]
        field_uuid3 = create_issue_response.json()['data']['message'][2]
        field_group = create_issue_response.json()['data']['message'][3][0]
        # 修改属性组
        new_name = str(uuid.uuid4())
        update_issue_response = f'{EnvContext.host}/project/api/project/UpdateGroupName'
        update_issue_body = {
            'name': '自动化测试修改属性组名称{}'.format(new_name[:4]),
            'team_uuid': team_uuid,
            'relations': [field_uuid1, field_uuid2, field_uuid3],
            'group_uuid': field_group,
            'pool': "Task"
        }
        update_issue_response = requests.request(method='POST', url=update_issue_response, headers=create_group_headers, json=update_issue_body)
        update_issue_response.raise_for_status()
        time.sleep(2)
        # 校验结果
        InterfacePlugins.call_team_ab_external('CustomizeUpdateName')