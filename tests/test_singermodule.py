import pytest
from playwright.sync_api import Page
from pages.singermodule_page import SingermodulePage


@pytest.fixture(scope="function")
def singermodule_page(page: Page) -> SingermodulePage:
    """singermodule页面 fixture"""
    return SingermodulePage(page)


class TestSingermodule:
    """测试singermodule"""

    def test_singermodule(self, singermodule_page: SingermodulePage, step) -> None:
        """测试场景：singermodule"""
        with step("打开页面"):
            singermodule_page.navigate()
        with step("点击已阅读且同意"):
            singermodule_page.step_2()
        with step("执行操作"):
            singermodule_page.step_3()
        with step("点击大陆女歌手"):
            singermodule_page.step_4()
        with step("点击中国组合"):
            singermodule_page.step_5()
        with step("点击大陆男歌手"):
            singermodule_page.step_6()
        with step("执行操作"):
            singermodule_page.step_7()
        with step("执行操作"):
            singermodule_page.step_8()
        with step("点击热门歌手"):
            singermodule_page.step_9()
        with step("执行操作"):
            singermodule_page.step_10()
        with step("点击搁浅(B)(HD)"):
            singermodule_page.step_11()
        with step("执行操作"):
            singermodule_page.step_12()
        with step("执行操作"):
            singermodule_page.step_13()

