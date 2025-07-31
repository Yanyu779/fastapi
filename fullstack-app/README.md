# 全栈Web应用

这是一个基于Flask后端和React前端的全栈Python Web应用。

## 项目结构

```
fullstack-app/
├── backend/          # Flask后端API
│   ├── app/
│   ├── requirements.txt
│   └── run.py
├── frontend/         # React前端应用
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
```

## 技术栈

### 后端
- Flask - Web框架
- Flask-CORS - 跨域支持
- Flask-SQLAlchemy - ORM
- SQLite - 数据库

### 前端
- React - 前端框架
- Axios - HTTP客户端
- Bootstrap - UI组件库

## 快速开始

### 启动后端
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### 启动前端
```bash
cd frontend
npm install
npm start
```

## API文档

- GET /api/users - 获取所有用户
- POST /api/users - 创建新用户
- GET /api/users/:id - 获取特定用户
- PUT /api/users/:id - 更新用户
- DELETE /api/users/:id - 删除用户

## 贡献

欢迎提交Pull Request或Issue！