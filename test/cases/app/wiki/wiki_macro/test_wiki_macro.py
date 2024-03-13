#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/2/29 11:22
# @Author   : lanbo
# @File     :test_wiki_macro.py

import time
from allure_commons._allure import story,feature,severity
from falcons.com.page import Browser
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install,ability_plugin_enable
from test.cases.utils.tools import env_clean





@feature("wiki_宏测试用例")
class TestWikiMacro:
    path = "/app/wiki/wiki_macro/1.0.0"

    @story("清理环境")
    def teardown_method(self):
         env_clean(path=self.path)

    @story("安装插件")
    def setup_method(self):
        ability_plugin_install(self.path)
        ability_plugin_enable(self.path)

    @story("前置操作：进入wiki-页面组-协同页面")
    def pre_goto_wikiPage(self, pw: Browser):
        pw.click_link("知识库管理")
        time.sleep(5)
        pw.click_link("页面组")
        # 点击默认页面组第一个知识库
        pw.action_click("//div[@class='oac-overflow-hidden oac-ml-xs']/span")
        # 点击默认wiki_page“主页"
        pw.action_click("//div[@class='ones-tree-list-holder']/div/div/div[1]")
        time.sleep(0.5)
        pw.click_button("编辑")

    @severity("blocker")
    @story("通过快捷指令插入block元素")
    def test_insert_block(self, pw: Browser):
        # 前置操作：进入wiki-页面组-协同页面
        TestWikiMacro.pre_goto_wikiPage(self, pw)
        time.sleep(5)
        pw.find_element("//div[@class='text-block focused']/div[@data-type='block-content']").click()
        time.sleep(0.5)
        # 点击菜单按钮
        pw.action_click("//button[@class='block-button']")
        # 点击“从上方插入”选项
        pw.move_to_element("在上方插入")
        pw.move_to_element("正文")
        # 滚动弹框页面至插件选项名
        pw.page.locator("//*[@data-command-bar-id='quick-menu']/div/div/div/div/div[39]").scroll_into_view_if_needed()
        # 添加插件选项tabs
        pw.action_click("//*[@data-command-bar-id='quick-menu']/div/div/div/div/div[39]/div[2]")
        time.sleep(0.5)
        # 点击插件内置block-tabs选项
        pw.find_element("//div[@class='ones-tabs-items-container']/div[1]/span").click()
        time.sleep(0.5)
        pw.has_text("tabs", exact=True)
        time.sleep(0.5)
        # 后置操作： 删除插件选项
        try:
            pw.action_click("//button[@class='block-button']")
            pw.action_click("//div[@class='tippy-content']/div/div/div[3]")
            pw.click_button("返回")
        except Exception as e:
            raise ValueError("删除失败，错误原因:", e)


    @severity("blocker")
    @story("通过快捷指令插入embed元素")
    def test_insert_embed(self, pw: Browser):
        TestWikiMacro.pre_goto_wikiPage(self, pw)
        pw.find_element("//div[@class='text-block focused']/div[@data-type='block-content']").click()
        time.sleep(0.5)
        pw.action_click("//button[@class='block-button']")
        pw.move_to_element("在上方插入")
        pw.move_to_element("正文")
        pw.page.locator("//*[@data-command-bar-id='quick-menu']/div/div/div/div/div[40]").scroll_into_view_if_needed()
        # 添加插件选项embed
        pw.action_click("//*[@data-command-bar-id='quick-menu']/div/div/div/div/div[40]/div[2]")
        time.sleep(0.5)
        pw.has_text("数据保存错误", exact=True)
        time.sleep(0.5)
        try:
            pw.action_click("//div[@class='wiz-mf-plugin-decorator-container']")
            pw.action_click("//button[@class='block-button']")
            pw.action_click("//div[@class='tippy-content']/div/div/div[3]")
            pw.click_button("返回")
        except Exception as e:
            pw.click_button("返回")
            raise ValueError("删除失败，错误原因:", e)


    @severity("blocker")
    @story("通过快捷指令插入box元素")
    def test_insert_box(self, pw: Browser):
        TestWikiMacro.pre_goto_wikiPage(self, pw)
        pw.find_element("//div[@class='text-block focused']/div[@data-type='block-content']").click()
        time.sleep(0.5)
        pw.action_click("//button[@class='block-button']")
        pw.move_to_element("在上方插入")
        pw.move_to_element("正文")
        pw.page.locator("//*[@data-command-bar-id='quick-menu']/div/div/div/div/div[42]").scroll_into_view_if_needed()
        # 添加插件选项box
        pw.action_click("//*[@data-command-bar-id='quick-menu']/div/div/div/div/div[42]/div[2]")
        time.sleep(0.5)
        pw.has_text("box-from-insert", exact=True)
        time.sleep(0.5)
        try:
            pw.action_click("//span[@data-type='box-content']")
            pw.click_button("取消")
            pw.action_click("//button[@class='block-button']")
            pw.action_click("//div[@class='tippy-content']/div/div/div[3]")
            pw.click_button("返回")
        except Exception as e:
            raise ValueError("删除失败，错误原因:", e)

    @severity("blocker")
    @story("通过快捷指令插入upload-img元素")
    def test_insert_uploadImg(self, pw: Browser):
        TestWikiMacro.pre_goto_wikiPage(self, pw)
        pw.find_element("//div[@class='text-block focused']/div[@data-type='block-content']").click()
        time.sleep(0.5)
        pw.action_click("//button[@class='block-button']")
        pw.move_to_element("在上方插入")
        pw.move_to_element("正文")
        pw.page.locator("//*[@data-command-bar-id='quick-menu']/div/div/div/div/div[41]").scroll_into_view_if_needed()
        # 添加插件选项box
        pw.action_click("//*[@data-command-bar-id='quick-menu']/div/div/div/div/div[41]/div[2]")
        time.sleep(0.5)
        pw.has_location("//div[@class='ones-upload ones-upload-select ones-upload-select-picture-card']/span/button")
        time.sleep(0.5)
        try:
            pw.action_click("//div[@class='wiz-mf-plugin-decorator-container']")
            pw.action_click("//button[@class='block-button']")
            pw.action_click("//div[@class='tippy-content']/div/div/div[3]")
            pw.click_button("返回")
        except Exception as e:
            raise ValueError("删除失败，错误原因:", e)