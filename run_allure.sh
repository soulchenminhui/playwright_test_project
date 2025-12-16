#!/bin/bash
# Allure 报告启动脚本
# 自动设置环境变量并启动 Allure 服务

export ALLURE_HOME="$HOME/.allure"
export PATH="$ALLURE_HOME/bin:$PATH"

if [ ! -d "allure-results" ]; then
    echo "错误: 找不到 allure-results 目录"
    echo "请先运行测试生成报告数据: pytest"
    exit 1
fi

echo "正在启动 Allure 报告服务..."
echo "提示: 如果无法访问自动打开的 URL，请使用 http://localhost:随机端口"
echo ""

# 使用 --host 参数指定使用 localhost
allure serve allure-results --host localhost

