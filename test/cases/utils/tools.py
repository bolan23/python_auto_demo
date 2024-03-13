from falcons.platform.pluginlifecycle.ab_helper import get_ability_plugin_path
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_uninstall, \
    ability_plugin_disable

from falcons.platform.pluginlifecycle.lifecycle import plugin_status

from falcons.platform.pluginlifecycle.helper import read_yaml
from falcons.platform.pluginlifecycle.msg_code import Msg


def env_clean(path, scope="team"):
    paths = get_ability_plugin_path(path)
    lifecycle_path = paths['lifecycle_path']
    plugin = read_yaml(lifecycle_path)
    if plugin:
        if plugin_status(plugin['instance_uuid']) in [Msg.DisableSuccess, Msg.InstallSuccess]:
            ability_plugin_uninstall(path, scope=scope)
        if plugin_status(plugin['instance_uuid']) == Msg.EnableSuccess:
            ability_plugin_disable(path, scope=scope)
            ability_plugin_uninstall(path, scope=scope)
        if plugin_status(plugin['instance_uuid']) in [Msg.EnableFail]:
            ability_plugin_uninstall(path, scope=scope)
