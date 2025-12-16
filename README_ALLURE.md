# Allure 测试报告使用指南

项目已集成 Allure Reports，提供更美观、功能更强大的测试报告。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试并生成 Allure 报告

### 1. 运行测试（生成原始数据）

```bash
# 运行所有测试
pytest

# 运行特定场景
pytest tests/test_search_function.py -v

# 运行并显示浏览器（调试用）
pytest tests/test_search_function.py -v --headed
```

测试运行后，会在 `allure-results/` 目录下生成原始报告数据。

### 2. 生成并查看 Allure 报告

#### 方式一：生成静态 HTML 报告

```bash
# 生成报告
allure generate allure-results -o allure-report --clean

# 打开报告（macOS）
open allure-report/index.html

# 或使用 Python 内置服务器
cd allure-report && python -m http.server 8080
# 然后访问 http://localhost:8080
```

#### 方式二：使用 Allure 服务（推荐）

```bash
# 启动 Allure 服务（实时查看报告）
allure serve allure-results
```

这会自动打开浏览器显示报告。

## Allure 报告特性

### 1. 步骤记录

测试用例中使用 `step` fixture 记录的步骤会自动显示在 Allure 报告中：

```python
def test_xxx(step):
    with step("1. 打开页面"):
        page.navigate()
    with step("2. 搜索歌曲"):
        page.search_song("周杰伦")
```

每个步骤会显示：
- 步骤名称
- 执行状态（PASSED/FAILED）
- 执行耗时

### 2. 失败截图

测试失败时，会自动附加页面截图到报告中（如果 Playwright page 可用）。

### 3. 场景标签

每个测试用例会自动添加场景名称标签，方便在报告中筛选。

### 4. 步骤明细

在测试详情页面可以看到完整的步骤执行明细。

## 常用命令

```bash
# 运行测试并生成报告数据
pytest -v

# 查看最新报告
allure serve allure-results

# 生成静态报告
allure generate allure-results -o allure-report --clean

# 清理旧的报告数据
rm -rf allure-results/*

# 清理生成的报告
rm -rf allure-report
```

## 报告目录说明

- `allure-results/` - Allure 原始数据目录（由 pytest 生成）
- `allure-report/` - 生成的静态 HTML 报告目录（由 allure generate 生成）
- `reports/` - 保留的旧版 HTML 报告目录（可选，可删除）

## 注意事项

1. **首次使用需要安装 Allure 命令行工具**：
   ```bash
   # macOS (使用 Homebrew)
   brew install allure
   
   # 或下载安装包
   # https://github.com/allure-framework/allure2/releases
   ```

2. **Allure 报告数据会累积**：每次运行测试都会在 `allure-results/` 中追加数据，可以使用 `--clean` 参数清理旧数据。

3. **步骤记录**：确保测试用例中使用了 `step` fixture，步骤才会显示在报告中。

4. **截图功能**：失败截图需要 Playwright page 对象可用，某些情况下可能无法截图。

## 与旧版报告的区别

- **旧版**：每个场景生成一个独立的 HTML 文件
- **Allure**：统一的报告界面，支持历史趋势、分类筛选等功能

如果需要同时保留两种报告格式，可以保留 `conftest.py` 中的旧版报告生成逻辑。

