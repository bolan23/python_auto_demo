import pytest
from allure_commons._allure import story, feature, severity
from falcons.platform.pluginlifecycle.ab_lifecycle import ability_plugin_install, ability_plugin_enable
from falcons.com.page import Browser
from falcons.com.env import EnvContext
from test.cases.utils.tools import env_clean

@pytest.fixture
def setup_teardown():
    path = "/app/project/dashboard_card/1.0.0"
    # 安装插件
    ability_plugin_install(path)
    ability_plugin_enable(path)
    yield
    # 停用插件，卸载插件
    env_clean(path=path)

@feature("仪表盘卡片")
class TestDashboardCard:

    @severity("blocker")
    @story('T207064 插件自定义卡片-业务场景：添加插件自定义卡片')
    @pytest.mark.flaky(reruns=0, reruns_delay=2)
    def test_dashboard_card(self, setup_teardown, pw: Browser):
        # 获取url，teamUUID
        host = EnvContext.host
        team_uuid = EnvContext.user.team_uuid
        # 进入测试页面 https://p8000-pzc2.dev.myones.net/project/#/workspace/team/dGQi9Bdt/dashboard
        url = host + f'/project/#/workspace/team/{team_uuid}/dashboard'
        pw.go_to(url)
        # 新建仪表盘
        pw.page.locator('.dashboard_head').locator('.head-top_left').get_by_text('仪表盘').click()
        pw.find_element('.ones-select-custom-menu').get_by_text('新建仪表盘').click()
        pw.page.locator('.ones-modal-content').locator('.ones-input').fill('test1')
        pw.click_button('确定')
        # 编辑仪表盘
        pw.click_button('编辑仪表盘')
        # 添加卡片
        pw.click_button('添加卡片')
        pw.page.locator('.ones-modal-content').locator('.dashboard-dialog-select-card-navlist').get_by_text('自定义').click()
        pw.click_button('添加')
        pw.find_element('id=cardName').fill('自定义卡片1')
        pw.click_button('完成')
        # 完成编辑
        pw.click_button('完成编辑')
        # 校验数据
        # 确认值不为undefined, 0, '', null, false, NaN
        card_uuid = pw.find_element('id=card-uuid').inner_text()
        if card_uuid != 'undefined':
            if card_uuid:
                # 删除仪表盘
                pw.click_button('更多')
                pw.click_span_precise('删除仪表盘')
                pw.click_button('确定')
            else:
                raise AssertionError('未能获取到cardUUID')
        else:
            raise AssertionError('获取到的值为undefined')
