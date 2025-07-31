# 使用说明

## 项目概述

这是一个Flask + React的全栈Web应用，实现了基本的用户管理功能。

## 项目结构

```
fullstack-app/
├── backend/          # Flask后端
│   ├── app/          
│   │   ├── __init__.py      # Flask应用工厂
│   │   ├── models.py        # 数据库模型
│   │   └── routes.py        # API路由
│   ├── requirements.txt     # Python依赖
│   ├── run.py              # 后端启动文件
│   ├── .env                # 后端环境变量
│   └── Dockerfile          # 后端Docker配置
├── frontend/         # React前端
│   ├── src/
│   │   ├── components/      # React组件
│   │   ├── services/        # API服务
│   │   ├── types/          # TypeScript类型
│   │   └── App.tsx         # 主应用组件
│   ├── package.json        # Node.js依赖
│   ├── .env               # 前端环境变量
│   └── Dockerfile         # 前端Docker配置
├── docker-compose.yml      # Docker编排配置
├── start-dev.sh           # 开发环境启动脚本
└── README.md              # 项目说明
```

## 启动方式

### 方式1: 手动启动

#### 启动后端
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

#### 启动前端
```bash
cd frontend
npm install
npm start
```

### 方式2: 使用启动脚本
```bash
./start-dev.sh
```

### 方式3: 使用Docker
```bash
docker-compose up
```

## 功能特性

- ✅ 用户列表显示
- ✅ 添加新用户
- ✅ 编辑用户信息
- ✅ 删除用户
- ✅ 响应式UI设计
- ✅ 错误处理
- ✅ 数据验证

## API端点

- `GET /api/users` - 获取所有用户
- `POST /api/users` - 创建新用户
- `GET /api/users/:id` - 获取特定用户
- `PUT /api/users/:id` - 更新用户
- `DELETE /api/users/:id` - 删除用户

## 访问地址

- 前端: http://localhost:3000
- 后端API: http://localhost:5000/api

## 注意事项

1. 确保Python 3.9+和Node.js 16+已安装
2. 后端使用SQLite数据库，数据文件会自动创建
3. 首次运行前端时需要执行`npm install`安装依赖
4. 开发环境下，前端和后端都支持热重载