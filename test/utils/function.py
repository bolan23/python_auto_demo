from falcons.platform.pluginlifecycle.ab_helper import get_ability_plugin_path
from falcons.platform.pluginlifecycle.helper import read_yaml


def getMinSystemVersion(path):
    """"get ability min system version"""
    try:
        release = read_yaml(get_ability_plugin_path(path)['release_path'])
        if release is not None:
            return release['min_system_version']
    except (Exception,):
        return None
    return None

