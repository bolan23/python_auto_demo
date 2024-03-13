import pytest
import requests
import time
from allure_commons._allure import story,feature,severity
from falcons.com.env import EnvContext
from falcons.com.page import Browser
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install,ability_plugin_enable
from falcons.platform.pluginlifecycle.interface.interface_action import InterfacePlugins
from test.cases.utils.tools import env_clean


@feature("插件侧边栏能力测试用例")
class TestSidebarMenu:
    path = "/platform/sidebar_menu/1.0.0"
    #

    @story("清理环境")
    def teardown_method(self):
        env_clean(path=self.path)

    @story("安装插件")
    def setup_method(self):
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)

    @severity("blocker")
    @story('T182275开放平台提供插件应用能力-业务场景：能力配置与实际效果一致（团队级别插件）')
    def test_sidebar_menu_functionality(self, pw: Browser):
        team_uuid = EnvContext.user.team_uuid
        pw.refresh()
        time.sleep(1)
        pw.click_link('icon newSidebarMenu')
        time.sleep(1)
        # 校验插槽SDK
        pw.check_checkbox(elem=f"//*[contains(@class, 'test-team')][contains(text(), '{team_uuid}')]")





