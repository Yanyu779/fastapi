# 🚀 Flask + React 全栈项目文件包

这个文件包包含了完整的全栈项目文件，你可以直接上传到服务器使用。

## 📁 文件结构

```
flask-react-fullstack/
├── backend/                 # Flask后端
│   ├── app/
│   │   ├── __init__.py     # Flask应用工厂
│   │   ├── models.py       # 数据库模型
│   │   └── routes.py       # API路由
│   ├── requirements.txt    # Python依赖
│   ├── run.py             # 启动文件
│   └── Dockerfile         # Docker配置
├── frontend/               # 前端文件
│   ├── public/
│   │   └── index.html     # 主页面
│   ├── src/
│   │   ├── App.js         # 主应用组件
│   │   └── index.js       # 入口文件
│   └── package.json       # Node.js依赖
├── simple-frontend/        # 简单HTML版本
│   └── index.html         # 纯HTML+JS版本
└── deploy-scripts/         # 部署脚本
    ├── deploy.sh          # 完整部署脚本
    └── start-services.sh  # 启动服务脚本
```

## 🚀 部署步骤

### 方式1: 使用简单HTML版本 (推荐)
1. 上传 `simple-frontend/index.html` 到服务器
2. 上传 `backend/` 目录到服务器
3. 在服务器上运行部署脚本

### 方式2: 使用React版本
1. 上传整个项目到服务器 `/opt/flask-react-fullstack/`
2. 运行 `deploy-scripts/deploy.sh`

## 💡 快速命令

```bash
# 上传到服务器后执行
cd /opt/flask-react-fullstack
chmod +x deploy-scripts/*.sh
./deploy-scripts/deploy.sh
```

## 🌐 访问地址
- 前端: http://你的服务器IP:3000
- API: http://你的服务器IP:5000/api/users