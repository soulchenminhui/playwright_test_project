import os
import re
import sys
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import allure
import pytest

# ---- Allure 与 pytest 高版本兼容性修复 ----
# 部分 allure-pytest 版本在配合 pytest 8.x 时，对 _test_fixtures 的实现与
# 新版 pytest FixtureManager.getfixturedefs 签名不兼容，会导致：
# AttributeError: 'str' object has no attribute 'iter_parents'
#
# 这里通过 monkey patch 方式修复，让 allure 使用兼容新版 pytest 的实现。
try:
    import allure_pytest.listener as _allure_listener

    def _patched_test_fixtures(item: pytest.Item):
        """兼容 pytest 8.x 的 _test_fixtures 实现."""
        fixturemanager = item.session._fixturemanager
        fixturedefs = []

        if hasattr(item, "_request") and hasattr(item._request, "fixturenames"):
            for name in item._request.fixturenames:
                try:
                    # pytest 8.x: 需要传 Node 对象
                    fixturedefs_pytest = fixturemanager.getfixturedefs(name, item)
                except TypeError:
                    # 兼容旧版 pytest / allure 的签名（传 nodeid 字符串）
                    fixturedefs_pytest = fixturemanager.getfixturedefs(name, item.nodeid)
                if fixturedefs_pytest:
                    fixturedefs.extend(fixturedefs_pytest)

        return fixturedefs

    # 覆盖 allure 内部的 _test_fixtures，实现兼容
    _allure_listener._test_fixtures = _patched_test_fixtures  # type: ignore[attr-defined]
except Exception:
    # 任何异常都不应阻止测试运行，只是不进行该兼容修复
    pass


# 当前项目根目录（即包含本 conftest.py 的目录）
ROOT_DIR = os.path.dirname(__file__)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


REPORT_DIR = Path(ROOT_DIR) / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def _get_scenario_name(item: pytest.Item) -> str:
    """优先使用用例的 docstring 作为场景名，其次是测试函数名。"""
    doc: Optional[str] = getattr(getattr(item, "obj", None), "__doc__", None)
    if doc:
        return doc.strip().splitlines()[0]
    return item.name


def _safe_filename(name: str) -> str:
    """将场景名转换成适合作为文件名的形式。"""
    # 保留中文和数字字母，其它字符转为下划线
    safe = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "_", name).strip("_")
    return safe or "scenario"


@pytest.fixture
def step(request):
    """
    用于在测试用例中记录每个业务步骤的耗时，并集成 Allure 报告：

        def test_xxx(step):
            with step("1. 打开页面"):
                ...
    """
    steps: List[dict] = []
    setattr(request.node, "_steps", steps)

    @contextmanager
    def _step(name: str):
        start = time.time()
        status = "PASSED"
        # 使用 Allure 的 step 装饰器记录步骤
        with allure.step(name):
            try:
                yield
            except Exception as e:
                status = "FAILED"
                # 在 Allure 中附加异常信息
                allure.attach(
                    str(e),
                    name="异常详情",
                    attachment_type=allure.attachment_type.TEXT,
                )
                raise
            finally:
                duration = time.time() - start
                steps.append(
                    {
                        "name": name,
                        "duration": duration,
                        "status": status,
                    }
                )

    return _step


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """集成 Allure 报告，记录测试结果和步骤信息。"""
    outcome = yield
    report: pytest.TestReport = outcome.get_result()

    # 只在用例执行阶段（call）结束后处理
    if report.when != "call":
        return

    try:
        scenario_name = _get_scenario_name(item)
        
        # 为 Allure 报告添加场景名称作为标签
        allure.dynamic.label("scenario", scenario_name)
        
        # 获取步骤信息
        steps: List[dict] = getattr(item, "_steps", [])
        
        # 如果测试失败，在 Allure 中附加失败详情
        if report.failed:
            allure.attach(
                report.longreprtext,
                name="失败详情",
                attachment_type=allure.attachment_type.TEXT,
            )
            
            # 如果 Playwright 页面可用，尝试附加截图
            try:
                # 使用更安全的方式获取 page fixture
                if hasattr(item, "_request") and hasattr(item._request, "fixturenames"):
                    if "page" in item._request.fixturenames:
                        page = item._request.getfixturevalue("page")
                        if hasattr(page, "screenshot"):
                            screenshot = page.screenshot()
                            allure.attach(
                                screenshot,
                                name="失败截图",
                                attachment_type=allure.attachment_type.PNG,
                            )
            except Exception:
                pass  # 截图失败不影响报告生成
        
        # 在 Allure 中附加步骤统计信息
        if steps:
            steps_summary = "\n".join(
                [
                    f"{idx}. {s['name']} - {s['status']} ({s['duration']:.3f}s)"
                    for idx, s in enumerate(steps, start=1)
                ]
            )
            allure.attach(
                steps_summary,
                name="步骤明细",
                attachment_type=allure.attachment_type.TEXT,
            )
    except Exception as e:
        # 如果 Allure 相关操作失败，不影响测试执行
        pass

