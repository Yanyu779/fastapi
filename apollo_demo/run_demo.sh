#!/bin/bash

# Apollo配置中心Python客户端Demo启动脚本

echo "🚀 Apollo配置中心Python客户端Demo"
echo "=================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误: 请在apollo_demo目录下运行此脚本"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量文件..."
    cp .env.example .env
    echo "✅ 已创建.env文件，请根据需要修改配置"
fi

# 显示菜单
echo ""
echo "请选择要运行的示例:"
echo "1) 完整交互式Demo"
echo "2) 简单示例"
echo "3) 快速开始"
echo "4) 基础使用示例"
echo "5) 上下文管理器示例"
echo "6) 退出"
echo ""

read -p "请输入选择 (1-6): " choice

case $choice in
    1)
        echo "🎯 运行完整交互式Demo..."
        python demo.py
        ;;
    2)
        echo "🎯 运行简单示例..."
        python simple_demo.py
        ;;
    3)
        echo "🎯 运行快速开始示例..."
        python simple_demo.py quick
        ;;
    4)
        echo "🎯 运行基础使用示例..."
        python demo.py basic
        ;;
    5)
        echo "🎯 运行上下文管理器示例..."
        python demo.py context
        ;;
    6)
        echo "👋 再见!"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "✅ Demo运行完成!"