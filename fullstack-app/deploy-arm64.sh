#!/bin/bash

# Flask + React 全栈项目 ARM64 服务器部署脚本
# 适配阿里云 Alibaba Cloud Linux 3.2104 LTS ARM64

set -e

# 配置变量
SERVER_IP="8.140.211.70"
DOMAIN=${1:-$SERVER_IP}
ENV=${2:-"production"}
PROJECT_NAME="flask-react-fullstack"

echo "🚀 ARM64服务器部署 $PROJECT_NAME"
echo "服务器IP: $SERVER_IP"
echo "域名: $DOMAIN"
echo "架构: ARM64"
echo "=" | tr " " "=" | printf "%*s\n" 50 | tr " " "="

# 1. 系统信息检查
echo "📋 检查系统信息..."
uname -a
cat /etc/os-release | head -5

# 2. 更新系统和安装依赖
echo "📦 更新系统并安装依赖..."
sudo yum update -y
sudo yum install -y git curl wget vim python3 python3-pip nodejs npm

# 3. 安装Docker (ARM64版本)
echo "🐳 安装Docker (ARM64)..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $(whoami)
    echo "需要重新登录以使用Docker，或使用sudo"
fi

# 4. 安装Docker Compose
echo "📦 安装Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-linux-aarch64" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 5. 克隆项目
echo "📂 克隆项目代码..."
cd /opt
if [ -d "$PROJECT_NAME" ]; then
    cd $PROJECT_NAME
    sudo git pull origin main
else
    sudo git clone https://github.com/Yanyu779/flask-react-fullstack.git $PROJECT_NAME
    sudo chown -R $(whoami):$(whoami) $PROJECT_NAME
    cd $PROJECT_NAME
fi

# 6. 修改Docker配置以支持ARM64
echo "🔧 配置ARM64兼容的Docker镜像..."
cat > backend/Dockerfile.arm64 << 'EOF'
FROM python:3.9-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
EOF

cat > frontend/Dockerfile.arm64 << 'EOF'
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
EOF

# 7. 创建ARM64优化的docker-compose配置
cat > docker-compose.arm64.yml << 'EOF'
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.arm64
    restart: always
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///app.db
    volumes:
      - ./backend/instance:/app/instance
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/users"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend  
      dockerfile: Dockerfile.arm64
    restart: always
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://$SERVER_IP:5000/api
    depends_on:
      backend:
        condition: service_healthy

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend
EOF

# 8. 创建Nginx配置
cat > nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:5000;
    }
    
    upstream frontend {
        server frontend:3000;
    }

    server {
        listen 80;
        server_name $DOMAIN;

        # API代理
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        }

        # 前端代理
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        }
    }
}
EOF

# 9. 配置环境变量
echo "⚙️ 配置生产环境..."
cat > .env.production << EOF
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///app.db
REACT_APP_API_URL=http://$SERVER_IP/api
EOF

# 10. 启动服务
echo "🚀 启动服务..."
sudo docker-compose -f docker-compose.arm64.yml up --build -d

# 11. 配置防火墙 (阿里云安全组)
echo "🔥 配置本地防火墙..."
if command -v firewall-cmd &> /dev/null; then
    sudo firewall-cmd --permanent --add-port=80/tcp
    sudo firewall-cmd --permanent --add-port=443/tcp
    sudo firewall-cmd --permanent --add-port=3000/tcp
    sudo firewall-cmd --permanent --add-port=5000/tcp
    sudo firewall-cmd --reload
fi

# 12. 等待服务启动并检查
echo "⏳ 等待服务启动..."
sleep 30

echo "✅ 检查服务状态..."
sudo docker-compose -f docker-compose.arm64.yml ps

# 13. 健康检查
echo "🏥 健康检查..."
if curl -f http://localhost:5000/api/users &> /dev/null; then
    echo "✅ 后端API正常"
else
    echo "❌ 后端API异常"
    sudo docker-compose -f docker-compose.arm64.yml logs backend
fi

if curl -f http://localhost:80 &> /dev/null; then
    echo "✅ 前端服务正常"  
else
    echo "❌ 前端服务异常"
    sudo docker-compose -f docker-compose.arm64.yml logs frontend
fi

echo ""
echo "🎉 部署完成!"
echo "🌐 访问地址: http://$SERVER_IP"
echo "📡 API地址: http://$SERVER_IP/api/users"
echo ""
echo "🔧 管理命令:"
echo "  查看状态: sudo docker-compose -f docker-compose.arm64.yml ps"
echo "  查看日志: sudo docker-compose -f docker-compose.arm64.yml logs -f"
echo "  重启服务: sudo docker-compose -f docker-compose.arm64.yml restart"
echo "  停止服务: sudo docker-compose -f docker-compose.arm64.yml down"
echo ""
echo "⚠️ 记得在阿里云控制台的安全组中开放以下端口:"
echo "  - 80 (HTTP)"
echo "  - 443 (HTTPS，如需要)"
echo "  - 22 (SSH)"