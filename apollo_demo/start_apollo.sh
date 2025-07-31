#!/bin/bash

# 启动Apollo服务器脚本

echo "=== 启动Apollo配置中心服务器 ==="
echo

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: 未找到Docker，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: 未找到Docker Compose，请先安装Docker Compose"
    exit 1
fi

# 创建配置目录
mkdir -p apollo-config

echo "正在启动Apollo服务器..."
echo "这可能需要几分钟时间，请耐心等待..."
echo

# 启动服务
docker-compose up -d

echo
echo "Apollo服务器启动中..."
echo "等待服务完全启动..."

# 等待服务启动
sleep 30

echo
echo "Apollo服务器已启动!"
echo
echo "服务地址:"
echo "  - Apollo Portal (管理界面): http://localhost:8070"
echo "  - Apollo Config Service: http://localhost:8080"
echo "  - Apollo Admin Service: http://localhost:8090"
echo "  - MySQL数据库: localhost:3306"
echo
echo "默认登录信息:"
echo "  - 用户名: apollo"
echo "  - 密码: admin"
echo
echo "请在管理界面中创建应用和配置，然后运行Python演示程序"
echo
echo "要停止服务器，请运行: docker-compose down"