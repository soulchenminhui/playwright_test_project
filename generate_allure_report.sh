#!/bin/bash
# 生成静态 Allure 报告脚本
# 生成 HTML 报告，可以直接在浏览器中打开

export ALLURE_HOME="$HOME/.allure"
export PATH="$ALLURE_HOME/bin:$PATH"

if [ ! -d "allure-results" ]; then
    echo "错误: 找不到 allure-results 目录"
    echo "请先运行测试生成报告数据: pytest"
    exit 1
fi

echo "正在生成 Allure 静态报告..."
allure generate allure-results -o allure-report --clean

if [ $? -eq 0 ]; then
    echo ""
    echo "报告生成成功！"
    echo "在浏览器中打开: file://$(pwd)/allure-report/index.html"
    echo ""
    echo "或者运行: open allure-report/index.html"
    
    # macOS 自动打开
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open allure-report/index.html
    fi
else
    echo "报告生成失败"
    exit 1
fi

