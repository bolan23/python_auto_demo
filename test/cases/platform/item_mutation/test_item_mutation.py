import pytest
from allure_commons._allure import story, feature, severity
from ones_action.act.task import TaskAction
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install,ability_plugin_enable
from falcons.platform.pluginlifecycle.interface.interface_action import InterfacePlugins
from test.cases.utils.tools import env_clean
from ones_action.act.pro import PrjAction


feature('Mutation事件劫持能力测试用例')
class TestItemMutation():
    path = "/platform/item_mutation/1.0.0"

    @story("清理环境")
    def teardown_method(self):
        env_clean(path=self.path)

    @story("安装插件")
    def setup_method(self):
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)

    @severity("blocker")
    @story("登记工时")
    @pytest.mark.flaky(reruns=0, reruns_delay=2)
    def test_addManhour(self):
        # 创建项目
        project_uuid = PrjAction.new_project()
        # 创建工作项
        task_uuid = TaskAction.new_issue(issue_type_name='任务', proj_uuid=project_uuid)
        task_uuid = task_uuid[0]
        # 登记工时，如果工时hour不为整数则会被拦截，不做更改，反之正常添加工时
        try:
            TaskAction.add_work_hour(task_uuid=task_uuid, hour=6.6, mode='simple')
        except Exception as e:
            print(e)
        #  删除项目
        PrjAction.delete_project(p_uuid=project_uuid)
        # 校验结果
        InterfacePlugins.call_team_ab_external('itemMutationTest')



