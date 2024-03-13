import pytest
import time
import requests
from allure_commons._allure import story, feature, severity
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install, ability_plugin_enable
from falcons.platform.pluginlifecycle.interface.interface_action import InterfacePlugins
from ones_action.act.pro import PrjAction
from ones_action.act.task import TaskAction

from falcons.com.env import Account, EnvContext

from test.cases.utils.tools import env_clean


@feature("工作项属性拦截测试用例")
class TestTaskEventHandler:
    path = "/app/project/task_event_handler/1.0.0"

    @story("清理环境")
    def teardown_method(self):
         env_clean(path=self.path)

    @story("安装插件")
    def setup_method(self):
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)

    @severity("blocker")
    @story('T161634-接口update_issuetype：触发点验证（变更工作项状态）')
    def test_update_work_item_status(self):
        # 创建项目
        project_uuid = PrjAction.new_project()
        # 创建工作项
        task_uuid = TaskAction.new_issue(issue_type_name='任务', proj_uuid=project_uuid)
        task_uuid = task_uuid[0]
        # transition_uuid = TaskAction.task_status_uuid('进行中')
        team_uuid = EnvContext.user.team_uuid
        token = EnvContext.user.token
        user_uuid = EnvContext.user.owner_uuid
        # 获取工作项更改状态的uuid
        transition_uuid_url = f'{EnvContext.host}/project/api/project/team/{team_uuid}/task/{task_uuid}/transitions'
        transition_uuid_headers = {
            'Content-Type': 'application/json',
            'Ones-Auth-Token': token,
            'Ones-User-Id': user_uuid,
            'cache-control': 'no-cache'

        }

        transition_uuid_response = requests.request("Get", transition_uuid_url,
                                                            headers=transition_uuid_headers)
        # 在返回值中取进行中状态的uuid
        transition_uuid = transition_uuid_response.json()['transitions'][0]['uuid']
        # 更改工作项状态
        TaskAction.transit_task_status(transition_uuid=transition_uuid, tasks_uuid=task_uuid)

        time.sleep(5)
        # # 删除项目
        PrjAction.delete_project(p_uuid=project_uuid)
        # 校验结果
        InterfacePlugins.call_team_ab_external('validateTaskEventHandler')



