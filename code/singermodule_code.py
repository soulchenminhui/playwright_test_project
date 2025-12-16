import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://vks_thunder.ktvsky.com/#/")
    page.get_by_text("已阅读且同意").click()
    page.get_by_alt_text("全部歌手").click()
    page.get_by_text("大陆女歌手").click()
    page.get_by_text("中国组合").click()
    page.get_by_text("大陆男歌手").click()
    page.locator("div").filter(has_text=re.compile(r"^高安$")).locator("div").nth(1).click()
    page.locator(".svg-icon").first.click()
    page.get_by_text("热门歌手").click()
    page.locator("div").filter(has_text=re.compile(r"^周杰伦$")).locator("div").nth(1).click()
    page.get_by_text("搁浅(B)(HD)").click()
    page.locator(".svg-icon").first.click()
    page.locator(".svg-icon").first.click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
