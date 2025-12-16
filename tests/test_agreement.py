import pytest
from playwright.sync_api import Page
from pages.agreement_page import AgreementPage


@pytest.fixture(scope="function")
def agreement_page(page: Page) -> AgreementPage:
    """agreement页面 fixture"""
    return AgreementPage(page)


class TestAgreement:
    """测试agreement"""

    def test_agreement(self, agreement_page: AgreementPage, step) -> None:
        """测试场景：agreement"""
        with step("打开页面"):
            agreement_page.navigate()
        with step("点击《雷石KTV用户协议》"):
            agreement_page.step_2()
        with step("执行操作"):
            agreement_page.step_3()
        with step("点击《雷石KTV隐私权政策》"):
            agreement_page.step_4()
        with step("执行操作"):
            agreement_page.step_5()
        with step("点击已阅读且同意"):
            agreement_page.step_6()
        with step("点击换一批"):
            agreement_page.step_7()
        with step("点击换一批"):
            agreement_page.step_8()
        with step("点击爱一个人好难"):
            agreement_page.step_9()
        with step("执行操作"):
            agreement_page.step_10()
        with step("执行操作"):
            agreement_page.step_11()
        with step("点击说不出口的话都唱给你听"):
            agreement_page.step_12()
        with step("点击人人都会唱"):
            agreement_page.step_13()
        with step("点击难以抗拒的千面魅力"):
            agreement_page.step_14()

