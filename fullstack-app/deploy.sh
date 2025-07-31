#!/bin/bash

# Flask + React 全栈项目自动部署脚本
# 使用方法: ./deploy.sh [域名] [环境]

set -e

# 配置变量
DOMAIN=${1:-"localhost"}
ENV=${2:-"production"}
PROJECT_NAME="flask-react-fullstack"
USER=$(whoami)

echo "🚀 开始部署 $PROJECT_NAME 到 $DOMAIN"
echo "环境: $ENV"
echo "用户: $USER"
echo "=" | tr " " "=" | printf "%*s\n" 50 | tr " " "="

# 1. 系统依赖检查和安装
echo "📦 检查系统依赖..."
if command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx git curl
elif command -v yum &> /dev/null; then
    sudo yum install -y python3 python3-pip nodejs npm nginx git curl
elif command -v dnf &> /dev/null; then
    sudo dnf install -y python3 python3-pip nodejs npm nginx git curl
fi

# 2. Docker安装 (可选)
echo "🐳 检查Docker..."
if ! command -v docker &> /dev/null; then
    echo "安装Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
fi

if ! command -v docker-compose &> /dev/null; then
    echo "安装Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 3. 项目部署
echo "📂 部署项目代码..."
cd /opt
if [ -d "$PROJECT_NAME" ]; then
    cd $PROJECT_NAME
    git pull origin main
else
    sudo git clone https://github.com/Yanyu779/flask-react-fullstack.git $PROJECT_NAME
    sudo chown -R $USER:$USER $PROJECT_NAME
    cd $PROJECT_NAME
fi

# 4. 环境配置
echo "⚙️ 配置环境变量..."
cat > .env.production << EOF
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=sqlite:///app.db
DOMAIN=$DOMAIN
EOF

# 5. Docker部署
echo "🐳 使用Docker部署..."
if [ "$ENV" = "production" ]; then
    # 生产环境配置
    cat > docker-compose.prod.yml << EOF
version: '3.8'
services:
  backend:
    build: ./backend
    restart: always
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
    
  frontend:
    build: ./frontend
    restart: always
    ports:
      - "3000:3000"
    depends_on:
      - backend
      
  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
EOF

    docker-compose -f docker-compose.prod.yml up -d
else
    docker-compose up -d
fi

# 6. Nginx配置
echo "🌐 配置Nginx..."
sudo tee /etc/nginx/sites-available/$PROJECT_NAME << EOF
server {
    listen 80;
    server_name $DOMAIN;
    
    # 前端静态文件
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
    
    # 后端API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 7. 防火墙配置
echo "🔥 配置防火墙..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 80
    sudo ufw allow 443
    sudo ufw allow 22
fi

# 8. 服务状态检查
echo "✅ 检查服务状态..."
sleep 10
if curl -f http://localhost:5000/api/users > /dev/null 2>&1; then
    echo "✅ 后端API正常"
else
    echo "❌ 后端API异常"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ 前端服务正常"
else
    echo "❌ 前端服务异常"
fi

echo ""
echo "🎉 部署完成!"
echo "🌐 访问地址: http://$DOMAIN"
echo "📡 API地址: http://$DOMAIN/api"
echo "🔧 管理命令:"
echo "  查看日志: docker-compose logs -f"
echo "  重启服务: docker-compose restart"
echo "  停止服务: docker-compose down"