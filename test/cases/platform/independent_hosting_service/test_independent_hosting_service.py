import time
import pytest
import requests
from allure_commons._allure import story, feature, severity
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install, ability_plugin_enable
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_disable, ability_plugin_uninstall
from falcons.platform.pluginlifecycle.ab_helper import get_ability_plugin_path
from falcons.platform.pluginlifecycle.lifecycle import plugin_status
from falcons.platform.pluginlifecycle.helper import read_yaml
from falcons.platform.pluginlifecycle.msg_code import Msg
from falcons.com.env import EnvContext


@pytest.fixture
def setup_teardown():
    path = "platform/independent_hosting_service/1.0.0"
    # 安装插件
    ability_plugin_install(path, scope='org')
    time.sleep(2)
    ability_plugin_enable(path, scope='org')
    yield
    # 停用插件，卸载插件
    # env_clean(path=path, scope='org')
    paths = get_ability_plugin_path(path)
    lifecycle_path = paths['lifecycle_path']
    plugin = read_yaml(lifecycle_path)
    if plugin:
        if plugin_status(plugin['instance_uuid']) in [Msg.DisableSuccess, Msg.InstallSuccess]:
            ability_plugin_uninstall(path, scope='org')
        if plugin_status(plugin['instance_uuid']) == Msg.EnableSuccess:
            time.sleep(1)
            ability_plugin_disable(path, scope='org')
            time.sleep(2)
            ability_plugin_uninstall(path, scope='org')
        if plugin_status(plugin['instance_uuid']) in [Msg.EnableFail]:
            ability_plugin_uninstall(path, scope='org')

@feature("托管独立应用")
class TestIndependentHostingService:

    @severity("blocker")
    @story('T160803 托管独立应用能力：外部访问开启 & 外部访问关闭')
    @pytest.mark.flaky(reruns=0, reruns_delay=2)
    def test_independentHostingService(self, setup_teardown):
        # 获取url
        host = EnvContext.host
        # 请求开启外部访问独立应用服务
        time.sleep(4)
        try:
            accessible_url = host + '/plugin_service/Accessible'
            accessible_res = requests.get(accessible_url, verify=True)
            accessible_res_str = accessible_res.text.strip()
            # 请求禁用外部访问独立应用服务
            not_accessible_url = host + '/plugin_service/notAccessible'
            not_accessible_res = requests.get(not_accessible_url, verify=True)
            if not_accessible_res.text == '':
                time.sleep(1)
                not_accessible_res = requests.get(not_accessible_url, verify=True)
            not_accessible_res_str = not_accessible_res.text.strip()
            print('打印禁用外部访问的独立应用服务返回结果===================================', not_accessible_res_str)
            if 'Hello World!' != accessible_res_str:
                raise AssertionError('未能访问到开启外部访问的独立应用服务')
            if '"Forbidden"' != not_accessible_res_str:
                raise AssertionError('未能访问到禁用外部访问的独立应用服务')
        except Exception:
            raise AssertionError('访问独立服务应用异常')
        return None
