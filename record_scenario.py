#!/usr/bin/env python3
"""
Playwright 场景录制工具
使用 Playwright codegen 录制用户操作，并自动转换为 POM 结构的 Page 类和测试文件
"""
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def to_snake_case(name: str) -> str:
    """将场景名转换为 snake_case"""
    # 移除特殊字符，保留中文、字母、数字
    name = re.sub(r"[^\w\u4e00-\u9fff]+", "_", name)
    # 将驼峰转换为下划线
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower().strip("_")


def to_pascal_case(name: str) -> str:
    """将场景名转换为 PascalCase"""
    parts = to_snake_case(name).split("_")
    return "".join(word.capitalize() for word in parts if word)


def extract_locators_from_code(code: str) -> List[Tuple[str, str]]:
    """从录制的代码中提取定位器和操作"""
    locators = []
    lines = code.split("\n")
    
    for line in lines:
        line = line.strip()
        # 匹配常见的定位器模式
        if "page.locator(" in line or "page.get_by_" in line:
            # 提取定位器
            match = re.search(r'(page\.(?:locator|get_by_\w+)\([^)]+\))', line)
            if match:
                locator = match.group(1)
                # 提取操作类型
                if ".click()" in line:
                    action = "click"
                elif ".fill(" in line:
                    action = "fill"
                elif ".press(" in line:
                    action = "press"
                else:
                    action = "interact"
                locators.append((locator, action))
    
    return locators


def generate_page_class(scenario_name: str, code: str, url: str = "https://vks_thunder.ktvsky.com/#/") -> str:
    """生成 Page 类代码"""
    class_name = to_pascal_case(scenario_name) + "Page"
    file_name = to_snake_case(scenario_name) + "_page.py"
    
    # 提取定位器
    locators = extract_locators_from_code(code)
    
    # 生成元素定义
    elements = []
    element_names = []
    for i, (locator, action) in enumerate(locators):
        var_name = f"element_{i+1}"
        element_names.append(var_name)
        # 简化定位器，移除 page. 前缀
        clean_locator = locator.replace("page.", "self.page.")
        elements.append(f"        self.{var_name} = {clean_locator}")
    
    elements_code = "\n".join(elements) if elements else "        # 元素定义将根据录制代码自动生成"
    
    page_code = f'''from playwright.sync_api import Page, expect


class {class_name}:
    def __init__(self, page: Page):
        self.page = page
        self.url = "{url}"

{elements_code}

    def navigate(self) -> None:
        """打开网站"""
        self.page.goto(self.url, wait_until="networkidle")
'''
    
    return page_code, class_name, file_name


def generate_test_file(scenario_name: str, class_name: str, page_file_name: str, steps: List[str]) -> str:
    """生成测试文件代码"""
    test_class_name = "Test" + to_pascal_case(scenario_name)
    test_file_name = "test_" + to_snake_case(scenario_name) + ".py"
    page_import_name = page_file_name.replace(".py", "").replace("/", ".")
    
    # 生成步骤代码
    steps_code = []
    for i, step_desc in enumerate(steps, 1):
        steps_code.append(f'        with step("{step_desc}"):')
        steps_code.append(f'            # TODO: 实现步骤 {i}')
    
    steps_code_str = "\n".join(steps_code) if steps_code else "        # 测试步骤将根据录制代码自动生成"
    
    test_code = f'''import pytest
from playwright.sync_api import Page
from pages.{page_import_name} import {class_name}


@pytest.fixture(scope="function")
def {to_snake_case(scenario_name)}_page(page: Page) -> {class_name}:
    """{scenario_name}页面 fixture"""
    return {class_name}(page)


class {test_class_name}:
    """测试{scenario_name}"""

    def test_{to_snake_case(scenario_name)}(self, {to_snake_case(scenario_name)}_page: {class_name}, step) -> None:
        """测试场景：{scenario_name}"""
{steps_code_str}

'''
    
    return test_code, test_file_name


def run_codegen(target_url: str = "https://vks_thunder.ktvsky.com/#/") -> str:
    """运行 Playwright codegen 并返回生成的代码"""
    print(f"正在启动 Playwright 录制工具，目标 URL: {target_url}")
    print("请在浏览器中完成操作，完成后关闭浏览器窗口...")
    
    try:
        # 使用 playwright codegen 录制
        result = subprocess.run(
            ["playwright", "codegen", target_url, "--target", "python"],
            capture_output=True,
            text=True,
            timeout=3600  # 1小时超时
        )
        
        if result.returncode != 0:
            print(f"录制过程出错: {result.stderr}")
            return ""
        
        # codegen 会将代码输出到 stdout，但实际代码在用户操作后才会生成
        # 这里我们需要一个不同的方法
        print("\n注意：Playwright codegen 会打开浏览器窗口，请在该窗口中完成操作。")
        print("操作完成后，代码会显示在终端中，请复制并保存。")
        
        return result.stdout
    except subprocess.TimeoutError:
        print("录制超时")
        return ""
    except FileNotFoundError:
        print("错误：未找到 playwright 命令，请确保已安装 Playwright")
        print("运行: pip install playwright && playwright install")
        return ""


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python record_scenario.py <场景名称> [URL]")
        print("示例: python record_scenario.py '登录场景' 'https://example.com'")
        sys.exit(1)
    
    scenario_name = sys.argv[1]
    target_url = sys.argv[2] if len(sys.argv) > 2 else "https://vks_thunder.ktvsky.com/#/"
    
    print(f"场景名称: {scenario_name}")
    print(f"目标 URL: {target_url}")
    print("\n" + "="*60)
    print("步骤 1: 录制操作")
    print("="*60)
    
    # 运行 codegen（注意：codegen 是交互式的，需要用户操作）
    print("\n正在启动浏览器录制...")
    print("提示：录制完成后，请将生成的代码保存到临时文件，然后运行转换脚本")
    
    # 由于 codegen 是交互式的，我们提供一个替代方案
    print("\n" + "="*60)
    print("替代方案：手动录制")
    print("="*60)
    print("请运行以下命令手动录制：")
    print(f"  playwright codegen {target_url} --target python")
    print("\n录制完成后，将生成的代码保存到文件，然后运行：")
    print(f"  python convert_recorded_code.py <场景名称> <录制代码文件路径>")


if __name__ == "__main__":
    main()

