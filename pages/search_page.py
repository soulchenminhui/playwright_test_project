from playwright.sync_api import Page, expect


class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://vks_thunder.ktvsky.com/#/"

        # 1）搜索触发区域：“搜索歌曲、歌手” 文本所在的容器（div.search-input 内的 <p>）
        # 优先用文本 + class，避免依赖 placeholder
        self.search_trigger = page.locator("div.search-input").filter(
            has_text="搜索歌曲、歌手"
        )

        # 2）搜索按钮：<div class="search-btn flex-center">搜索</div>
        # 用 class + 文本双重约束，避免误点其它“搜索”
        self.search_button = page.locator("div.search-btn.flex-center").filter(
            has_text="搜索"
        )

        # 3）Tab：歌手 / 歌曲（页面未声明 role=tab，这里直接用具体 DOM 结构）
        # 歌手 / 歌曲 tab 的结构类似：<div class="item-txt">歌手</div> / <div class="item-txt">歌曲</div>
        self.singer_tab = page.locator("div.item-txt", has_text="歌手")
        self.song_tab = page.locator("div.item-txt", has_text="歌曲")

        # 4）歌曲列表：每一行是 <div class="song-item flex-between list ...">
        # 直接用 class 选择器，避免依赖 role
        self.song_items = page.locator("div.song-item")

    def navigate(self) -> None:
        """打开网站"""
        # 等待页面基本加载完成，避免元素尚未渲染
        self.page.goto(self.url, wait_until="networkidle")

    def search_song(self, keyword: str) -> None:
        """搜索歌曲"""
        # 2）点击“搜索歌曲、歌手”触发搜索输入
        expect(self.search_trigger).to_be_visible()
        self.search_trigger.click()

        # 3）等待真正的输入框出现后再输入
        # 部分站点不会给 input 显式 role，这里直接用常见的 text/search 输入框选择器
        search_input = self.page.locator("input[type='text'], input[type='search']").first
        search_input.click()
        search_input.fill(keyword)

        # 自动等待搜索按钮可点击
        expect(self.search_button).to_be_visible()
        self.search_button.click()

    def click_singer_tab(self) -> None:
        """点击“歌手”tab"""
        expect(self.singer_tab).to_be_visible()
        self.singer_tab.click()

    def click_song_tab(self) -> None:
        """点击“歌曲”tab"""
        expect(self.song_tab).to_be_visible()
        self.song_tab.click()

    def select_first_singer(self) -> None:
        """（保留接口，如后续需要在歌星列表中点歌手）"""
        # 这里暂时不实现具体逻辑，避免依赖未知 DOM
        pass

    def select_first_song(self) -> None:
        """点击任意一首歌曲名称（这里选择第一首）"""
        first_song = self.song_items.first
        expect(first_song).to_be_visible()

        # 歌曲名在内部 <div class="name ellipsis"> 节点中
        song_name = first_song.locator("div.name.ellipsis")
        expect(song_name).to_be_visible()
        song_name.click()

    def verify_search_results(self) -> None:
        """验证搜索结果"""
        expect(self.song_items.first).to_be_visible()

    def verify_singer_page(self) -> None:
        """验证歌手页面（保留接口，视页面实际结构补充）"""
        # 例如可以根据页面上的“歌星”结果列表元素完善
        pass

    def verify_song_playing(self) -> None:
        """验证歌曲正在播放（保留接口，视页面实际结构补充）"""
        pass


