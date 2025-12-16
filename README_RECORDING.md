# Playwright 场景录制指南

本工具支持通过 Playwright 录制功能添加新的测试场景，并自动生成符合 POM 结构的代码。

## 使用步骤

### 1. 录制操作

运行 Playwright codegen 录制你的操作：

```bash
playwright codegen https://vks_thunder.ktvsky.com/#/ --target python
```

或者指定其他 URL：

```bash
playwright codegen <你的URL> --target python
```

### 2. 完成操作

在打开的浏览器窗口中：
1. 完成你想要测试的所有操作（点击、输入、导航等）
2. 操作完成后，关闭浏览器窗口
3. 在终端中会显示生成的 Python 代码
4. **将生成的代码复制并保存到文件**，例如 `recorded_code.py`

### 3. 转换为 POM 结构

使用转换脚本将录制的代码转换为 POM 结构：

```bash
python convert_recorded_code.py <场景名称> <录制代码文件路径>
```

示例：

```bash
python convert_recorded_code.py "登录场景" recorded_code.py
python convert_recorded_code.py "播放歌曲" recorded_code.py
```

### 4. 完善生成的代码

转换脚本会生成两个文件：

1. **Page 类** (`pages/<场景名>_page.py`)
   - 包含元素定位器定义
   - 包含基础方法框架
   - 需要根据实际 DOM 结构完善定位器和方法实现

2. **测试文件** (`tests/test_<场景名>.py`)
   - 包含测试用例框架
   - 使用 `step` fixture 记录每个步骤
   - 可以单独运行

### 5. 运行测试

单独运行新场景的测试：

```bash
# 运行特定场景
pytest tests/test_<场景名>.py -v

# 运行所有测试
pytest -v
```

## 命名规则

- **Page 类**: `XxxPage` (PascalCase)
- **Page 文件**: `xxx_page.py` (snake_case)
- **测试类**: `TestXxx` (PascalCase)
- **测试文件**: `test_xxx.py` (snake_case)

## 注意事项

1. **定位器优化**: 生成的定位器可能需要根据实际 DOM 结构优化
2. **等待机制**: 确保在关键操作前添加适当的等待（`expect(...).to_be_visible()`）
3. **步骤描述**: 测试中的步骤描述会自动从录制代码中提取，可以手动优化
4. **独立运行**: 每个场景的测试文件都可以独立运行，不依赖其他场景

## 示例

### 录制新场景

```bash
# 1. 录制
playwright codegen https://vks_thunder.ktvsky.com/#/ --target python
# 完成操作后，保存代码到 recorded_login.py

# 2. 转换
python convert_recorded_code.py "用户登录" recorded_login.py

# 3. 运行
pytest tests/test_用户登录.py -v
```

## 故障排除

### 问题：找不到 playwright 命令

```bash
pip install playwright
playwright install
```

### 问题：生成的定位器不准确

这是正常的，需要根据实际 DOM 结构手动优化定位器。可以参考现有的 `search_page.py` 和 `playlist_page.py` 的实现方式。

### 问题：测试无法单独运行

确保：
1. `conftest.py` 在项目根目录
2. `pages` 目录有 `__init__.py`
3. 导入路径正确

