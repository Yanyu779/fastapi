# Apollo配置中心Python客户端演示

这是一个Python连接Apollo配置中心的完整演示项目，包含了基本的配置获取、监听配置变化等功能。

## 功能特性

- ✅ 连接Apollo配置中心
- ✅ 获取单个配置项
- ✅ 获取所有配置
- ✅ 配置变化监听
- ✅ 支持默认值
- ✅ 自动JSON解析
- ✅ 环境变量配置

## 项目结构

```
apollo_demo/
├── apollo_client.py    # Apollo客户端核心类
├── demo.py            # 演示脚本
├── requirements.txt   # 依赖包
├── .env.example      # 环境变量示例
└── README.md         # 说明文档
```

## 安装依赖

```bash
cd apollo_demo
pip install -r requirements.txt
```

## 配置环境变量

1. 复制环境变量示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，设置您的Apollo配置：
```bash
# 应用ID
APOLLO_APP_ID=your-app-id

# Apollo服务器地址
APOLLO_URL=http://your-apollo-server:8080

# 集群名称
APOLLO_CLUSTER=default

# 命名空间
APOLLO_NAMESPACE=application
```

## 使用方法

### 基本使用

```python
from apollo_client import ApolloClient

# 创建客户端
client = ApolloClient(
    app_id='your-app-id',
    apollo_url='http://localhost:8080'
)

# 获取配置
db_url = client.get_config('database.url', 'mysql://localhost:3306/demo')
redis_host = client.get_config('redis.host', 'localhost')

# 获取所有配置
all_configs = client.get_all_configs()
```

### 配置监听

```python
def config_change_callback(configs):
    print("配置发生变化:", configs)

# 启动配置监听
client.watch_config(config_change_callback, interval=5)
```

### 运行演示

```bash
python demo.py
```

## Apollo服务器设置

### 使用Docker快速启动Apollo

```bash
# 克隆Apollo项目
git clone https://github.com/apolloconfig/apollo.git
cd apollo

# 启动Apollo
docker-compose up -d
```

### 手动安装Apollo

1. 下载Apollo二进制包
2. 配置数据库
3. 启动Apollo服务

详细安装步骤请参考：[Apollo官方文档](https://github.com/apolloconfig/apollo)

## 在Apollo管理界面创建配置

1. 访问Apollo管理界面：`http://localhost:8070`
2. 创建应用：`demo-app`
3. 在`application`命名空间下添加配置：

```
database.url=mysql://localhost:3306/demo
redis.host=localhost
database.max_connections=20
app.name=Apollo Demo
```

## API文档

### ApolloClient类

#### 初始化参数

- `app_id` (str): 应用ID
- `cluster` (str): 集群名称，默认为"default"
- `namespace` (str): 命名空间，默认为"application"
- `apollo_url` (str): Apollo服务器地址
- `timeout` (int): 请求超时时间

#### 方法

- `get_config(key, default=None)`: 获取单个配置
- `get_all_configs()`: 获取所有配置
- `watch_config(callback, interval=5)`: 监听配置变化

## 错误处理

客户端会自动处理以下情况：

- 网络连接失败
- 服务器不可用
- 配置解析错误
- 超时异常

## 注意事项

1. 确保Apollo服务器正在运行
2. 检查网络连接和防火墙设置
3. 验证应用ID、集群和命名空间配置
4. 配置监听功能会持续运行，记得在适当时候停止

## 故障排除

### 常见问题

1. **连接失败**
   - 检查Apollo服务器地址是否正确
   - 确认服务器是否正在运行
   - 检查网络连接

2. **获取不到配置**
   - 验证应用ID是否正确
   - 检查命名空间是否存在
   - 确认配置是否已发布

3. **监听不工作**
   - 检查回调函数是否正确
   - 确认监听间隔设置合理

## 许可证

MIT License