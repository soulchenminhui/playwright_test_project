# 快速开始：录制新场景

## 三步添加新测试场景

### 步骤 1: 录制操作

```bash
playwright codegen https://vks_thunder.ktvsky.com/#/ --target python
```

在打开的浏览器中完成你的操作，完成后关闭浏览器，将终端中显示的代码保存到文件，例如 `my_recorded_code.py`

### 步骤 2: 转换为 POM 结构

```bash
python convert_recorded_code.py "场景名称" my_recorded_code.py
```

示例：
```bash
python convert_recorded_code.py "用户登录" my_recorded_code.py
python convert_recorded_code.py "播放控制" my_recorded_code.py
```

### 步骤 3: 运行测试

```bash
# 单独运行新场景
pytest tests/test_场景名称.py -v

# 或运行所有测试
pytest -v
```

## 完整示例

假设你要录制一个"播放控制"场景：

```bash
# 1. 录制
playwright codegen https://vks_thunder.ktvsky.com/#/ --target python
# 在浏览器中：点击播放按钮、暂停、下一首等操作
# 完成后，复制代码保存为 recorded_playback.py

# 2. 转换
python convert_recorded_code.py "播放控制" recorded_playback.py

# 3. 运行
pytest tests/test_播放控制.py -v
```

## 生成的文件

转换后会生成两个文件：

1. **`pages/<场景名>_page.py`** - Page Object 类
2. **`tests/test_<场景名>.py`** - 测试用例文件

## 注意事项

- 生成的代码包含 TODO 注释，需要根据实际 DOM 结构优化定位器
- 可以参考现有的 `search_page.py` 和 `playlist_page.py` 的实现方式
- 每个场景的测试都可以独立运行

