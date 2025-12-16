import re
from playwright.sync_api import Page, expect


class SingermodulePage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://vks_thunder.ktvsky.com/#/"

        # 元素定义
        self.element_1 = self.page.get_by_text("已阅读且同意")
        self.element_2 = self.page.get_by_alt_text("全部歌手")
        self.element_3 = self.page.get_by_text("大陆女歌手")
        self.element_4 = self.page.get_by_text("中国组合")
        self.element_5 = self.page.get_by_text("大陆男歌手")
        self.element_6 = self.page.locator("div").filter(has_text=re.compile(r"^高安$")).locator("div").nth(1)
        self.element_7 = self.page.locator(".svg-icon").first
        # 热门歌手 Tab：<div class="item-txt active">热门歌手</div>
        self.element_8 = self.page.locator("div.item-txt", has_text="热门歌手")
        self.element_9 = self.page.locator("div").filter(has_text=re.compile(r"^周杰伦$")).locator("div").nth(1)
        self.element_10 = self.page.get_by_text("搁浅(B)(HD)")
        self.element_11 = self.page.locator(".svg-icon").first
        self.element_12 = self.page.locator(".svg-icon").first

    def navigate(self) -> None:
        """打开网站"""
        self.page.goto(self.url, wait_until="networkidle")

    def navigate(self) -> None:
        """打开页面"""
        self.page.goto(self.url, wait_until="networkidle")

    def step_2(self) -> None:
        """点击已阅读且同意"""
        expect(self.element_1).to_be_visible()
        self.element_1.click()

    def step_3(self) -> None:
        """执行操作"""
        expect(self.element_2).to_be_visible()
        self.element_2.click()

    def step_4(self) -> None:
        """点击大陆女歌手"""
        expect(self.element_3).to_be_visible()
        self.element_3.click()

    def step_5(self) -> None:
        """点击中国组合"""
        expect(self.element_4).to_be_visible()
        self.element_4.click()

    def step_6(self) -> None:
        """点击大陆男歌手"""
        expect(self.element_5).to_be_visible()
        self.element_5.click()

    def step_7(self) -> None:
        """执行操作"""
        expect(self.element_6).to_be_visible()
        self.element_6.click()

    def step_8(self) -> None:
        """执行操作"""
        expect(self.element_7).to_be_visible()
        self.element_7.click()

    def step_9(self) -> None:
        """点击热门歌手"""
        expect(self.element_8).to_be_visible()
        self.element_8.click()

    def step_10(self) -> None:
        """执行操作"""
        expect(self.element_9).to_be_visible()
        self.element_9.click()

    def step_11(self) -> None:
        """点击搁浅(B)(HD)"""
        expect(self.element_10).to_be_visible()
        self.element_10.click()

    def step_12(self) -> None:
        """执行操作"""
        expect(self.element_7).to_be_visible()
        self.element_7.click()

    def step_13(self) -> None:
        """执行操作"""
        expect(self.element_7).to_be_visible()
        self.element_7.click()

