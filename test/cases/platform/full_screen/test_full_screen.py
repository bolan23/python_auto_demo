import time
import pytest
from allure_commons._allure import story,feature,severity
from falcons.com.env import EnvContext
from falcons.com.page import Browser


@feature("全屏展示测试用例")
class TestSidebarMenu:
    @severity("blocker")
    @story('T196837 url参数控制布局-业务场景：设置页面全屏展示')
    def test_full_screen(self, pw: Browser):
        team_uuid = EnvContext.user.team_uuid
        # 构造测试用例计划的URL，并指定允许全屏模式
        testcase_plan_url = f'{EnvContext.host}/project/#/testcase/team/{team_uuid}/plan?allow=fullscreen'
        pw.go_to(testcase_plan_url)
        pw.refresh()
        xpath_expression = '//*[@class="test-plan-group-list"]'
        element = pw.page.locator(xpath_expression).first
        # 获取测试计划页面的像素尺寸（边界框）
        bounding_box = element.bounding_box()
        width = bounding_box["width"]
        # 设置期望的全屏模式下的元素宽度和高度
        expected_width = 1440
        # 断言页面元素是否真正进入了全屏模式，即其宽度是否与预期值一致
        assert expected_width == width

