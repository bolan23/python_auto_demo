import pytest
from allure_commons._allure import story, feature, severity
from ones_action.act.task import TaskAction
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install,ability_plugin_enable
from falcons.platform.pluginlifecycle.interface.interface_action import InterfacePlugins
from test.cases.utils.tools import env_clean
from ones_action.act.pro import PrjAction
from falcons.com.env import EnvContext

feature('获取插件能力配置测试用例')
class TestGetPluginAbilityConfig():
    path = "/platform/get_plugin_ability_config/1.0.0"
    #
    @story("清理环境")
    def teardown_method(self):
        env_clean(path=self.path)

    @story("安装插件")
    def setup_method(self):
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)

    @severity("blocker")
    @story("校验获取插件能力配置与实际效果一致")
    @pytest.mark.flaky(reruns=0, reruns_delay=2)
    def test_get_plugin_ability_cfg(self):
        team_uuid = EnvContext.user.team_uuid
        data = {
            "abilityID":"2XINIy4H",
            "teamUUID": team_uuid
        }
        # 校验结果
        InterfacePlugins.call_team_ab_external('GetPluginAbility',data=data)