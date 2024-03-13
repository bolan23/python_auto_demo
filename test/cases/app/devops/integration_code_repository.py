#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/3/12 16:59
# @Author   : lanbo
# @File     :integration_code_repository.py
import time
from allure_commons._allure import story,feature,severity
from falcons.com.env import EnvContext
from falcons.com.page import Browser
from falcons.platform.pluginlifecycle import helper
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install,ability_plugin_enable
from test.cases.utils.tools import env_clean

org_uuid = EnvContext.user.org_uuid
team_uuid = EnvContext.user.team_uuid
secret_value = ''  # secret值
callback_url = ''  # 回调url


@feature("关联代码仓_测试用例")
class TestIntegrationCodeRepository:
    path = "/app/devops/integration_code_repository/1.0.0"

    @story("清理环境")
    def teardown_method(self):
        env_clean(path=self.path)

    @story("安装插件")
    def setup_method(self):
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)

    @story("前置操作：进入gitlab-获取-Application消息")
    def pre_get_gitlab_ApplicationInfo(self, pw: Browser):
        global secret_value, callback_url
        callback_url = f'{EnvContext.host}/plugin/{org_uuid}/{team_uuid}/2IMpOmW61/1.0.1/modules/about-blank-BE8t/index.html'
        pw.go_to("http://47.112.50.166:7991/oauth/applications/37/")
        time.sleep(1)
        # 登录root账号
        pw.find_element("//input[@autocomplete='username']").type('root')
        pw.find_element("//input[@autocomplete='current-password']").type("Test1234")
        pw.click_button("Sign in")
        # 更新secret url
        pw.click_link("Edit")
        pw.find_element("//textarea[@name='doorkeeper_application[redirect_uri]']").clear()
        pw.find_element("//textarea[@name='doorkeeper_application[redirect_uri]']").type(callback_url)
        pw.find_element("//button[@class='gl-button btn btn-md btn-confirm ']").scroll_into_view_if_needed()
        pw.click_button("Save application")
        # 获取secret
        pw.click_button("Renew secret")
        pw.action_click("//button[@class='btn js-modal-action-primary btn-confirm btn-md gl-button']")
        pw.action_click("//button[@aria-label='Click to reveal']")
        time.sleep(2)
        # 获取secret值
        secret_value = pw.page.evaluate('''() => {
            const element = document.evaluate('//button[@id="clipboard-button-42"]/@data-clipboard-text', 
                                              document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            return element ? element.value : null;
        }''')
        print(secret_value)

    @story("关联代码仓：添加代码仓库/删除代码仓库")
    def test_add_codeRepository(self, pw: Browser):
        # 前置操作：通过gitlab创建Application 获取secret、appID
        TestIntegrationCodeRepository.pre_get_gitlab_ApplicationInfo(self, pw)
        time.sleep(1)
        repo_manage_url = f'{EnvContext.host}/project/#/team/{team_uuid}/do_code/configuration/repo_manage'
        pw.go_to(repo_manage_url)
        time.sleep(1)
        pw.click_button("关联代码仓")
        pw.find_element("//div[@class='ones-modal-body']/div[6]").scroll_into_view_if_needed()
        pw.find_element("//div[@class='ones-modal-body']/div[6]").click()
        pw.click_button('下一步')
        # 输入secret
        input_secret = pw.find_element("//input[@id='secret']")
        input_secret.type(secret_value)
        # 输入 redirect_url
        input_redirect_url = pw.find_element("//input[@id='redirectUrl']")
        input_redirect_url.type(callback_url)
        # 跳转tabs进行Authorize认证
        try:
            pw.click_button("认证")
            time.sleep(2)
            pages = pw.context.pages  # 获取所以页面
            pages[1].bring_to_front()  # 切换至认证页面
            time.sleep(1)
            # 点击Authorize按钮
            pages[1].evaluate('''(selector) => {
                const element = document.querySelector(selector);
                if (element) {
                    element.click();
                    return true;  // 表示元素存在并且被成功点击
                } else {
                    return false;  // 表示元素不存在或者点击失败
                }
            }''', "#commit-changes")
            time.sleep(1)
            pages[0].bring_to_front()  # 切换为默认测试页面
        except Exception as e:
            print('已操作过认证,注意：',e)
            pass
        # code选项
        pw.action_click("//div[@class='ones-select-selection-overflow']")
        time.sleep(1)
        # 添加3个代码仓
        pw.action_click("//div[@class='rc-virtual-list-holder-inner']/div[1]")
        time.sleep(0.5)
        pw.action_click("//input[@id='secret']")
        pw.click_button("确定")
        time.sleep(5)
        # 断言添加成功
        pw.has_text("已激活", exact=True)
        # 删除关联代码仓
        pw.action_click("//button[@type='button']",nth=2)
        pw.action_click("//div[@class='ones-dropdown-menu']")
        time.sleep(3)
        # pw.input_v2("输入“移除关联代码仓”，以完成后续操作","移除代码仓")
        pw.find_element("//div[@class='ones-form-item-control-input-content']/input").type("移除关联代码仓")
        pw.click_button("移除")
        time.sleep(0.5)
        # 断言删除成功
        pw.element_is_exist("//tr[@class='art-table-row first even']/td[7]/span/button",is_exist=False,wait_time=5)




