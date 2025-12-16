import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://vks_thunder.ktvsky.com/#/")
    page.get_by_text("《雷石KTV用户协议》").click()
    page.locator("div").filter(has_text=re.compile(r"^雷石 KTV 用户服务协议 搜索 搜索歌曲、歌手已点$")).locator("use").first.click()
    page.get_by_text("《雷石KTV隐私权政策》").click()
    page.locator(".svg-icon").first.click()
    page.get_by_text("已阅读且同意").click()
    page.get_by_text("换一批").click()
    page.get_by_text("换一批").click()
    page.get_by_text("爱一个人好难").click()
    page.locator(".mic-operation > img").click()
    page.get_by_label("Loading").locator("use").click()
    page.get_by_text("说不出口的话都唱给你听").click()
    page.get_by_text("人人都会唱").click()
    page.get_by_text("难以抗拒的千面魅力").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
