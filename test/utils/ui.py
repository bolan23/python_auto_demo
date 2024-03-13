#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/2/26 16:16
# @Author : lishiguang
# @File : ui.py
import subprocess
from string import Template


class UiPluginPath:
    """UI 测试用例配置"""

    account = 'businessAbility/account/1.0.0'
    plugin_log = '/ability/baseAbility/pluginLog/1.0.0'
    test = 'app/testcase/1.0.0'

    @classmethod
    def get_paths(cls, keys):
        """
        Get all ui path config values
        """
        paths = []
        for key in keys:
            try:
                paths.append(getattr(cls, key))
            except KeyError as _:
                pass

        return paths

    @classmethod
    def download_ui_plugin(cls, name):
        """Download Plugin"""
        import pathlib
        cpath = pathlib.Path(__file__).parent.parent
        base_dir = cpath.parent.absolute()
        name = [n + '.yaml' for n in name]
        plugins = ' '.join(name)
        cmd = Template(f"""cd $dir; pwd ; python plugin_init.py $plug""")
        p = subprocess.Popen(cmd.substitute(dir=base_dir, plug=plugins), stdout=subprocess.PIPE, shell=True)
        std_out = p.communicate()[0]
        print('Plugin Download log:', std_out.decode())
