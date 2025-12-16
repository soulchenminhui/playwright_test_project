from playwright.sync_api import Page, expect


class PlaylistPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://vks_thunder.ktvsky.com/#/"

        # 定制歌单元素
        # DOM 结构：<div class="nav-list-item"><img alt="定制歌单" ... /></div>
        # 先找到 img，再回到父级容器点击，保证点击区域正确
        self.custom_playlist_icon = page.locator("div.nav-list-item img[alt='定制歌单']")
        self.custom_playlist = self.custom_playlist_icon.locator("xpath=..")

        # 歌曲元素：每一行歌曲条目
        self.song_items = page.locator(".song-item, [data-v-ae97f2ee].song-item")

        # 已点模块元素
        # 已点 DOM 示例：
        # <div class="already-order flex-center">
        #   <svg ...></svg>
        #   <span class="flex-center">2</span>
        #   <p>已点</p>
        # </div>
        self.played_tab = page.locator("div.already-order.flex-center")

        # 已点歌曲列表 DOM 示例：
        # <div class="order-item song-item flex-between playing">...</div>
        self.played_songs = page.locator("div.order-item.song-item")

        # 关闭按钮 DOM 示例：
        # <div class="close">
        #   <svg class="svg-icon" ...><use xlink:href="#icon-close"></use></svg>
        # </div>
        # 直接点击包裹关闭图标的 svg
        self.close_button = page.locator("div.close svg.svg-icon").first

    def navigate(self) -> None:
        """打开网站"""
        self.page.goto(self.url, wait_until="networkidle")

    def open_custom_playlist(self) -> None:
        """打开定制歌单"""
        expect(self.custom_playlist_icon).to_be_visible()
        self.custom_playlist.click()

    def add_first_song_to_playlist(self) -> None:
        """添加第一首歌曲到歌单（点击第一条歌曲行）"""
        first_song = self.song_items.first
        expect(first_song).to_be_visible()
        first_song.click()

    def click_played_tab(self) -> None:
        """点击已点标签"""
        self.played_tab.click()

    def close_playlist(self) -> None:
        """关闭歌单"""
        expect(self.close_button).to_be_visible()
        self.close_button.click()

    def verify_playlist_opened(self) -> None:
        """验证歌单已打开"""
        expect(self.played_tab).to_be_visible()

    def verify_song_added(self) -> None:
        """验证歌曲已添加"""
        expect(self.played_songs.first).to_be_visible()



