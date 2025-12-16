import pytest
from playwright.sync_api import Page, expect
from pages.playlist_page import PlaylistPage


@pytest.fixture(scope="function")
def playlist_page(page: Page) -> PlaylistPage:
    """歌单页面 fixture"""
    return PlaylistPage(page)


class TestPlaylistModule:
    """测试已点模块"""

    def test_playlist_operations(self, playlist_page: PlaylistPage) -> None:
        """测试歌单操作流程"""
        # 1. 打开网址
        playlist_page.navigate()

        # 2. 点击定制歌单
        playlist_page.open_custom_playlist()

        # 验证歌单已打开
        playlist_page.verify_playlist_opened()

        # 3. 点击任意一首歌曲（添加歌曲）
        playlist_page.add_first_song_to_playlist()

        # 4. 点击已点
        playlist_page.click_played_tab()

        # 验证歌曲已添加
        playlist_page.verify_song_added()

        # 5. 点击关闭
        playlist_page.close_playlist()

