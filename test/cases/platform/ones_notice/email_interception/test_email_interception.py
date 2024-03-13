import random
import pytest
import time
import requests
from allure_commons._allure import story, feature, severity
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install, ability_plugin_enable
from falcons.platform.pluginlifecycle.interface.interface_action import InterfacePlugins
from test.cases.utils.tools import env_clean
from falcons.com.env import EnvContext

from ones_action.act.member import MemberAction
from ones_action.act.pro import PrjAction
from ones_action.act.task import TaskAction
from ones_action.act import IssueAction

@pytest.fixture
def setup_teardown():
    path = "platform/ones_notice/email_interception/1.0.0"
    # 安装插件
    ability_plugin_install(path)
    time.sleep(2)
    ability_plugin_enable(path)
    yield
    # 卸载插件
    env_clean(path=path)

@feature("邮件拦截能力测试用例")
class TestEmailInterception:

    @severity("blocker")
    @story('T248445 邮件拦截：检查启用插件后receiveEmail函数是否调用成功')
    @pytest.mark.flaky(reruns=0, reruns_delay=2)
    def test_emailInterception(self, setup_teardown):
        # 获取url，token, team_uuid, user_uuid
        host = EnvContext.host
        auth_token = EnvContext.user.token
        team_uuid = EnvContext.user.team_uuid
        user_uuid = EnvContext.user.owner_uuid
        # 生成随机字符串
        digits = '023456789'
        random_string = ''.join(random.choice(digits) for _ in range(11))
        # 添加一个成员到团队返回成员信息
        users = MemberAction.new_member(custom_email=random_string + '@163.com')
        member_uuid = getattr(users,'owner_uuid')
        # 创建项目返回项目id
        project_id = PrjAction.new_project(name=random_string)
        # 新增单个成员到项目内
        MemberAction.add_proj_member(member_uuid,project_uuid=project_id)
        # 获取工作项类型的uuid,默认获取任务uuid
        issue_uuids = TaskAction.issue_type_uuid(project_uuid=project_id)
        issue_uuid = issue_uuids[0]
        # 获取通知项列表
        notice_configs_res = IssueAction.get_pro_notice_config(issue_uuid,project_uuid=project_id)
        # 获取指定通知项id
        notice_id = ''
        for item in notice_configs_res.json()['system_configs']:
            if item['name'] == '创建任务':
                notice_id = item['uuid']
        # 勾选邮件通知
        check_email_url = host + f'/project/api/project/team/{team_uuid}/project/{project_id}/issue_type/{issue_uuid}/notice_config/{notice_id}/update_methods'
        check_email_headers = {
            'Content-Type': 'application/json',
            'Ones-Auth-Token': auth_token,
            'Ones-User-Id': user_uuid,
            'cache-control': 'no-cache'
        }
        check_email_payload = {
            "effected_methods": [
                {
                    "type": "notice_center",
                    "enabled": True,
                },
                {
                    "type": "email",
                    "enabled": True,
                },
            ],
        }
        requests.request("POST", check_email_url, headers=check_email_headers, json=check_email_payload)
        # 指定通知项添加通知人
        add_notifier_member_url = host + f'/project/api/project/team/{team_uuid}/project/{project_id}/issue_type/{issue_uuid}/notice_config/{notice_id}/add_subscription'
        add_notifier_member_headers = {
            'Content-Type': 'application/json',
            'Ones-Auth-Token': auth_token,
            'Ones-User-Id': user_uuid,
            'cache-control': 'no-cache'
        }
        add_notifier_member_payload = {
            "roles": [],
            "single_user_uuids": [member_uuid],
            "role_uuids": [],
            "group_uuids": [],
            "department_uuids": [],
            "field_uuids": [],
        }
        requests.request("POST", add_notifier_member_url, headers=add_notifier_member_headers,
                         json=add_notifier_member_payload)
        # 创建工作项
        TaskAction.new_issue(proj_uuid=project_id)
        # 等待能力函数触发，将结果写入数据库
        time.sleep(5)
        # 校验结果
        InterfacePlugins.call_team_ab_external('EmailInterception')