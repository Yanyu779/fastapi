#!/bin/bash

echo "🚀 Flask + React 全栈项目一键部署脚本"
echo "适用于阿里云服务器 (8.140.211.70)"

# 配置中国镜像源
echo "🇨🇳 配置中国镜像源..."
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
trusted-host = mirrors.aliyun.com
timeout = 120
EOF

# 安装Python依赖
echo "📦 安装Python依赖..."
cd backend
python3 -m pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 启动后端服务
echo "🚀 启动后端服务..."
pkill -f "python3 run.py" || true
nohup python3 run.py > ../backend.log 2>&1 &
echo $! > ../backend.pid

echo "⏳ 等待后端启动..."
sleep 5

# 测试后端API
if curl -f http://localhost:5000/api/users &> /dev/null; then
    echo "✅ 后端API启动成功"
else
    echo "❌ 后端启动失败，查看日志: tail -f backend.log"
    exit 1
fi

# 启动前端服务 (简单HTTP服务器)
echo "🌐 启动前端服务..."
cd ..
pkill -f "python.*http.server" || true
nohup python3 -m http.server 3000 > frontend.log 2>&1 &
echo $! > frontend.pid

echo "⏳ 等待前端启动..."
sleep 3

echo ""
echo "🎉 部署完成!"
echo "📊 服务状态:"
ps aux | grep -E "(python3 run.py|http.server)" | grep -v grep

echo ""
echo "🌐 访问地址:"
echo "  前端应用: http://8.140.211.70:3000"
echo "  后端API: http://8.140.211.70:5000/api/users"

echo ""
echo "🔧 管理命令:"
echo "  查看后端日志: tail -f backend.log"
echo "  查看前端日志: tail -f frontend.log"
echo "  停止服务: kill \$(cat *.pid)"

echo ""
echo "⚠️ 提醒: 请确保阿里云安全组已开放端口 3000 和 5000"