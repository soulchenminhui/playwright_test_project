import pytest
from playwright.sync_api import Page
from pages.search_page import SearchPage


@pytest.fixture(scope="function")
def search_page(page: Page) -> SearchPage:
    """搜索页面 fixture"""
    return SearchPage(page)


class TestSearchFunction:
    """测试搜索功能"""

    def test_search_song_and_play(self, search_page: SearchPage, step) -> None:
        """测试搜索场景：搜索歌手、歌曲"""
        with step("1. 打开页面"):
            search_page.navigate()

        with step("2. 搜索“周杰伦”"):
            search_page.search_song("周杰伦")

        with step("3. 验证搜索结果已出现"):
            search_page.verify_search_results()

        with step("4. 点击“歌手”tab"):
            search_page.click_singer_tab()

        with step("5. 点击“歌曲”tab"):
            search_page.click_song_tab()

        with step("6. 点击任意一首歌曲名称（这里选第一首）"):
            search_page.select_first_song()

        with step("7. 验证歌曲点击后的结果（视实际页面行为，当前保留接口）"):
            search_page.verify_song_playing()


