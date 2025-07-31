#!/bin/bash

echo "启动全栈开发环境..."

# 启动后端服务器
echo "启动Flask后端服务器..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端服务器
echo "启动React前端服务器..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "开发环境已启动！"
echo "后端服务器: http://localhost:5000"
echo "前端服务器: http://localhost:3000"
echo ""
echo "按 Ctrl+C 停止所有服务器"

# 等待用户按Ctrl+C
trap "echo '正在停止服务器...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait