import re
from playwright.sync_api import Page, expect


class AgreementPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://vks_thunder.ktvsky.com/#/"

        # 元素定义
        self.element_1 = self.page.get_by_text("《雷石KTV用户协议》")
        self.element_2 = self.page.locator("div").filter(has_text=re.compile(r"^雷石 KTV 用户服务协议 搜索 搜索歌曲、歌手已点$")).locator("use").first
        self.element_3 = self.page.get_by_text("《雷石KTV隐私权政策》")
        self.element_4 = self.page.locator(".svg-icon").first
        self.element_5 = self.page.get_by_text("已阅读且同意")
        self.element_6 = self.page.get_by_text("换一批")
        self.element_7 = self.page.get_by_text("换一批")
        self.element_8 = self.page.get_by_text("爱一个人好难")
        self.element_9 = self.page.locator(".mic-operation > img")
        self.element_10 = self.page.get_by_label("Loading").locator("use")
        self.element_11 = self.page.get_by_text("说不出口的话都唱给你听")
        self.element_12 = self.page.get_by_text("人人都会唱")
        self.element_13 = self.page.get_by_text("难以抗拒的千面魅力")

    def navigate(self) -> None:
        """打开网站"""
        self.page.goto(self.url, wait_until="networkidle")

    def navigate(self) -> None:
        """打开页面"""
        self.page.goto(self.url, wait_until="networkidle")

    def step_2(self) -> None:
        """点击《雷石KTV用户协议》"""
        expect(self.element_1).to_be_visible()
        self.element_1.click()

    def step_3(self) -> None:
        """执行操作"""
        expect(self.element_2).to_be_visible()
        self.element_2.click()

    def step_4(self) -> None:
        """点击《雷石KTV隐私权政策》"""
        expect(self.element_3).to_be_visible()
        self.element_3.click()

    def step_5(self) -> None:
        """执行操作"""
        expect(self.element_4).to_be_visible()
        self.element_4.click()

    def step_6(self) -> None:
        """点击已阅读且同意"""
        expect(self.element_5).to_be_visible()
        self.element_5.click()

    def step_7(self) -> None:
        """点击换一批"""
        expect(self.element_6).to_be_visible()
        self.element_6.click()

    def step_8(self) -> None:
        """点击换一批"""
        expect(self.element_6).to_be_visible()
        self.element_6.click()

    def step_9(self) -> None:
        """点击爱一个人好难"""
        expect(self.element_8).to_be_visible()
        self.element_8.click()

    def step_10(self) -> None:
        """执行操作"""
        expect(self.element_9).to_be_visible()
        self.element_9.click()

    def step_11(self) -> None:
        """执行操作"""
        expect(self.element_10).to_be_visible()
        self.element_10.click()

    def step_12(self) -> None:
        """点击说不出口的话都唱给你听"""
        expect(self.element_11).to_be_visible()
        self.element_11.click()

    def step_13(self) -> None:
        """点击人人都会唱"""
        expect(self.element_12).to_be_visible()
        self.element_12.click()

    def step_14(self) -> None:
        """点击难以抗拒的千面魅力"""
        expect(self.element_13).to_be_visible()
        self.element_13.click()

