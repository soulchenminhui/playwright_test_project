#!/usr/bin/env python3
"""
将 Playwright 录制的代码转换为 POM 结构的 Page 类和测试文件
"""
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict


def to_snake_case(name: str) -> str:
    """将场景名转换为 snake_case"""
    name = re.sub(r"[^\w\u4e00-\u9fff]+", "_", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower().strip("_")


def to_pascal_case(name: str) -> str:
    """将场景名转换为 PascalCase"""
    parts = to_snake_case(name).split("_")
    return "".join(word.capitalize() for word in parts if word)


def parse_recorded_code(code: str) -> Dict:
    """解析录制的代码，提取操作步骤和定位器"""
    lines = code.split("\n")
    steps = []
    locators_map = {}
    operations = []  # 存储操作序列：[(locator, action, value), ...]
    url = "https://vks_thunder.ktvsky.com/#/"
    
    # 提取 URL
    url_match = re.search(r'page\.goto\(["\']([^"\']+)["\']', code)
    if url_match:
        url = url_match.group(1)
    
    # 提取操作步骤
    step_counter = 0
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # 检测 goto 操作
        if "page.goto(" in line:
            step_counter += 1
            steps.append(f"{step_counter}. 打开页面")
            operations.append(("navigate", None, None))
        
        # 检测 locator + 操作（可能在同一行，也可能跨多行）
        elif "page.locator(" in line or "page.get_by_" in line:
            # 当前行是否已经包含操作（codegen 默认是 page.xxx().click() 这种写法）
            inline_action = any(op in line for op in [".click()", ".fill(", ".press(", ".select_option("])

            # 收集完整的定位器代码（可能跨多行，但不包括后续纯操作行）
            locator_lines = [line]
            j = i + 1
            if not inline_action:
                while j < len(lines) and not any(
                    op in lines[j] for op in [".click()", ".fill(", ".press(", ".select_option("]
                ):
                    if lines[j].strip() and not lines[j].strip().startswith("#"):
                        locator_lines.append(lines[j].strip())
                    j += 1
            locator_full = " ".join(locator_lines)
            
            # 查找对应的操作
            if inline_action:
                action_line = line
            else:
                action_line = ""
                if j < len(lines):
                    action_line = lines[j].strip()
            
            # 提取定位器
            if inline_action:
                # 对于一行形式，直接截取到 .click() / .fill() / .press() 之前，保留完整链式调用
                base = locator_full
                for op in [".click()", ".fill(", ".press(", ".select_option("]:
                    if op in base:
                        base = base.split(op)[0]
                        break
                locator_code = base.replace("\n", " ").strip()
            else:
                locator_match = re.search(r'(page\.(?:locator|get_by_\w+)\([^)]+\))', locator_full)
                if not locator_match:
                    # 尝试匹配多行定位器
                    locator_match = re.search(
                        r'(page\.(?:locator|get_by_\w+)\([^)]*(?:\n[^)]*)*?\))',
                        locator_full,
                        re.MULTILINE,
                    )
                if not locator_match:
                    i += 1
                    continue
                locator_code = locator_match.group(1).replace("\n", " ").strip()
            
            # 到这里，无论是否 inline_action 都已经得到 locator_code
            if ".click()" in action_line:
                step_counter += 1
                desc = extract_action_description(locator_full + " " + action_line)
                steps.append(f"{step_counter}. {desc}")
                operations.append(("click", locator_code, None))
            elif ".fill(" in action_line:
                step_counter += 1
                fill_match = re.search(r'\.fill\(["\']([^"\']+)["\']', action_line)
                value = fill_match.group(1) if fill_match else "输入内容"
                desc = extract_action_description(locator_full)
                steps.append(f"{step_counter}. {desc}：{value}")
                operations.append(("fill", locator_code, value))
            elif ".press(" in action_line:
                step_counter += 1
                press_match = re.search(r'\.press\(["\']([^"\']+)["\']', action_line)
                key = press_match.group(1) if press_match else "按键"
                steps.append(f"{step_counter}. 按下 {key}")
                operations.append(("press", locator_code, key))
            
            # 存储定位器
            var_name = f"element_{len(locators_map) + 1}"
            locators_map[var_name] = locator_code

            # 如果操作在下一行，i 需要跳过到 j；如果在同一行，仅前进一行
            if inline_action:
                i += 1
            else:
                i = j
            continue
        
        i += 1
    
    return {
        "url": url,
        "steps": steps,
        "locators": locators_map,
        "operations": operations,
        "raw_code": code
    }


def extract_action_description(line: str) -> str:
    """从代码行中提取操作描述"""
    # 尝试从定位器中提取文本
    text_match = re.search(r'has_text\(["\']([^"\']+)["\']', line)
    if text_match:
        return f"点击{text_match.group(1)}"
    
    # 尝试从 get_by_text 中提取
    text_match = re.search(r'get_by_text\(["\']([^"\']+)["\']', line)
    if text_match:
        return f"点击{text_match.group(1)}"
    
    # 尝试从 get_by_role 中提取
    role_match = re.search(r'get_by_role\(["\'](\w+)["\'].*name=["\']([^"\']+)["\']', line)
    if role_match:
        return f"点击{role_match.group(2)}"
    
    # 尝试从 get_by_placeholder 中提取
    placeholder_match = re.search(r'get_by_placeholder\(["\']([^"\']+)["\']', line)
    if placeholder_match:
        return f"在{placeholder_match.group(1)}中输入"
    
    return "执行操作"


def generate_page_class(scenario_name: str, parsed: Dict) -> Tuple[str, str, str]:
    """生成 Page 类代码"""
    class_name = to_pascal_case(scenario_name) + "Page"
    file_name = to_snake_case(scenario_name) + "_page.py"
    
    # 生成元素定义
    elements = []
    methods = []
    
    element_index = 0
    for var_name, locator_code in parsed["locators"].items():
        element_index += 1
        # 清理定位器代码
        clean_locator = locator_code.replace("page.", "self.page.")
        elements.append(f"        self.{var_name} = {clean_locator}")
    
    # 根据步骤生成方法
    method_names = []
    operations = parsed.get("operations", [])
    
    for i, step in enumerate(parsed["steps"], 1):
        step_desc = step.split(". ", 1)[1] if ". " in step else step
        method_name = f"step_{i}"
        
        # 根据操作类型生成方法
        if i <= len(operations):
            op_type, locator, value = operations[i-1]
            
            # 生成方法实现
            if op_type == "navigate":
                method_name = "navigate"
                method_body = '''        self.page.goto(self.url, wait_until="networkidle")'''
            elif op_type == "click":
                # 找到对应的元素变量
                element_var = None
                for var, loc in parsed["locators"].items():
                    if loc in locator or locator in loc:
                        element_var = var
                        break
                
                if element_var:
                    method_body = f'''        expect(self.{element_var}).to_be_visible()
        self.{element_var}.click()'''
                else:
                    method_body = f'''        # TODO: 实现点击操作
        # 定位器: {locator}'''
            elif op_type == "fill":
                element_var = None
                for var, loc in parsed["locators"].items():
                    if loc in locator or locator in loc:
                        element_var = var
                        break
                
                if element_var:
                    method_body = f'''        expect(self.{element_var}).to_be_visible()
        self.{element_var}.fill("{value}")'''
                else:
                    method_body = f'''        # TODO: 实现输入操作
        # 定位器: {locator}
        # 值: {value}'''
            elif op_type == "press":
                method_body = f'''        self.page.keyboard.press("{value}")'''
            else:
                method_body = f'''        # TODO: 实现操作
        # 类型: {op_type}'''
        else:
            method_body = '''        # TODO: 根据录制代码实现具体逻辑
        pass'''
        
        methods.append(f'''    def {method_name}(self) -> None:
        """{step_desc}"""
{method_body}
''')
    
    elements_code = "\n".join(elements) if elements else "        # 元素定义将根据录制代码自动生成"
    methods_code = "\n".join(methods) if methods else "    # 方法将根据录制代码自动生成"
    
    page_code = f'''import re
from playwright.sync_api import Page, expect


class {class_name}:
    def __init__(self, page: Page):
        self.page = page
        self.url = "{parsed['url']}"

        # 元素定义
{elements_code}

    def navigate(self) -> None:
        """打开网站"""
        self.page.goto(self.url, wait_until="networkidle")

{methods_code}
'''
    
    return page_code, class_name, file_name


def generate_test_file(scenario_name: str, class_name: str, page_file_name: str, steps: List[str]) -> Tuple[str, str]:
    """生成测试文件代码"""
    test_class_name = "Test" + to_pascal_case(scenario_name)
    test_file_name = "test_" + to_snake_case(scenario_name) + ".py"
    page_import_name = page_file_name.replace(".py", "").replace("/", ".")
    page_var_name = to_snake_case(scenario_name) + "_page"
    
    # 生成步骤代码
    steps_code = []
    method_index = 0
    for i, step in enumerate(steps, 1):
        step_desc = step.split(". ", 1)[1] if ". " in step else step
        method_index += 1
        
        # 确定调用的方法名
        if "打开" in step_desc or "navigate" in step_desc.lower():
            method_call = f"{page_var_name}.navigate()"
        else:
            method_call = f"{page_var_name}.step_{method_index}()"
        
        steps_code.append(f'        with step("{step_desc}"):')
        steps_code.append(f"            {method_call}")
    
    # 如果没有步骤，至少添加导航
    if not steps_code:
        steps_code.append(f'        with step("1. 打开页面"):')
        steps_code.append(f"            {page_var_name}.navigate()")
    
    steps_code_str = "\n".join(steps_code) if steps_code else f"        {page_var_name}.navigate()"
    
    test_code = f'''import pytest
from playwright.sync_api import Page
from pages.{page_import_name} import {class_name}


@pytest.fixture(scope="function")
def {page_var_name}(page: Page) -> {class_name}:
    """{scenario_name}页面 fixture"""
    return {class_name}(page)


class {test_class_name}:
    """测试{scenario_name}"""

    def test_{to_snake_case(scenario_name)}(self, {page_var_name}: {class_name}, step) -> None:
        """测试场景：{scenario_name}"""
{steps_code_str}

'''
    
    return test_code, test_file_name


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python convert_recorded_code.py <场景名称> <录制代码文件路径>")
        print("示例: python convert_recorded_code.py '登录场景' recorded_code.py")
        sys.exit(1)
    
    scenario_name = sys.argv[1]
    code_file_path = sys.argv[2]
    
    # 读取录制的代码
    try:
        with open(code_file_path, "r", encoding="utf-8") as f:
            recorded_code = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {code_file_path}")
        sys.exit(1)
    
    print(f"场景名称: {scenario_name}")
    print(f"读取录制代码: {code_file_path}")
    
    # 解析代码
    print("\n正在解析录制代码...")
    parsed = parse_recorded_code(recorded_code)
    
    print(f"提取到 {len(parsed['steps'])} 个步骤")
    print(f"提取到 {len(parsed['locators'])} 个定位器")
    print(f"目标 URL: {parsed['url']}")
    
    # 生成 Page 类
    print("\n正在生成 Page 类...")
    page_code, class_name, page_file_name = generate_page_class(scenario_name, parsed)
    
    # 生成测试文件
    print("正在生成测试文件...")
    test_code, test_file_name = generate_test_file(scenario_name, class_name, page_file_name, parsed["steps"])
    
    # 保存文件
    pages_dir = Path("pages")
    tests_dir = Path("tests")
    pages_dir.mkdir(exist_ok=True)
    tests_dir.mkdir(exist_ok=True)
    
    page_file_path = pages_dir / page_file_name
    test_file_path = tests_dir / test_file_name
    
    print(f"\n保存 Page 类到: {page_file_path}")
    with open(page_file_path, "w", encoding="utf-8") as f:
        f.write(page_code)
    
    print(f"保存测试文件到: {test_file_path}")
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_code)
    
    print("\n" + "="*60)
    print("生成完成！")
    print("="*60)
    print(f"\nPage 类: {page_file_path}")
    print(f"测试文件: {test_file_path}")
    print(f"\n可以单独运行测试:")
    print(f"  pytest {test_file_path} -v")
    print("\n注意：生成的代码包含 TODO 注释，需要根据实际页面结构完善定位器和方法实现。")


if __name__ == "__main__":
    main()

