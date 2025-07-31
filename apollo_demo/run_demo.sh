#!/bin/bash

# Apollo配置中心演示启动脚本

echo "=== Apollo配置中心Python演示 ==="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "apollo_client.py" ]; then
    echo "错误: 请在apollo_demo目录下运行此脚本"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip3 install -r requirements.txt

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "未找到.env文件，正在创建..."
    cp .env.example .env
    echo "请编辑.env文件配置您的Apollo服务器信息"
    echo
fi

echo "选择运行模式:"
echo "1) 基础演示 (demo.py)"
echo "2) FastAPI Web应用 (fastapi_example.py)"
echo "3) 客户端测试 (test_client.py)"
echo "4) 退出"
echo

read -p "请输入选择 (1-4): " choice

case $choice in
    1)
        echo "启动基础演示..."
        python3 demo.py
        ;;
    2)
        echo "启动FastAPI Web应用..."
        echo "访问 http://localhost:8000/docs 查看API文档"
        python3 fastapi_example.py
        ;;
    3)
        echo "运行客户端测试..."
        python3 test_client.py
        ;;
    4)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac