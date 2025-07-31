# Apollo配置中心Python客户端Demo

这是一个完整的Apollo配置中心Python客户端示例，展示了如何连接Apollo配置中心、获取配置、监听配置变更等功能。

## 功能特性

- ✅ 连接Apollo配置中心
- ✅ 获取单个配置和所有配置
- ✅ 配置变更监听（长轮询）
- ✅ 本地配置缓存
- ✅ 上下文管理器支持
- ✅ 环境变量配置
- ✅ 异常处理和重试机制

## 项目结构

```
apollo_demo/
├── requirements.txt      # 依赖包
├── config.py            # 配置管理
├── apollo_client.py     # Apollo客户端核心
├── demo.py              # 示例程序
├── .env.example         # 环境变量示例
└── README.md           # 说明文档
```

## 安装依赖

```bash
cd apollo_demo
pip install -r requirements.txt
```

## 配置说明

1. 复制环境变量文件：
```bash
cp .env.example .env
```

2. 修改 `.env` 文件中的配置：
```bash
# Apollo服务器地址
APOLLO_SERVER_URL=http://your-apollo-server:8080

# 应用ID
APOLLO_APP_ID=your-app-id

# 集群名称
APOLLO_CLUSTER=default

# 命名空间
APOLLO_NAMESPACE=application
```

## 使用方法

### 1. 完整交互式Demo

```bash
python demo.py
```

这个命令会启动一个完整的交互式demo，包括：
- 显示当前配置
- 获取配置示例
- 监听配置变更
- 实时显示配置状态

### 2. 基础使用示例

```bash
python demo.py basic
```

展示基础的使用方法，包括：
- 创建客户端
- 获取配置
- 添加监听器
- 开始监听

### 3. 上下文管理器示例

```bash
python demo.py context
```

展示如何使用上下文管理器，自动处理资源清理。

## 代码示例

### 基础使用

```python
from config import ApolloConfig
from apollo_client import ApolloClient

# 创建配置
config = ApolloConfig()

# 创建客户端
client = ApolloClient(config)

# 获取配置
value = client.get_config('database.url', 'localhost:3306')
print(f"数据库URL: {value}")

# 获取所有配置
all_configs = client.get_all_configs()
print(f"所有配置: {all_configs}")
```

### 配置变更监听

```python
def on_config_change(key, old_value, new_value):
    print(f"配置 {key} 从 {old_value} 变更为 {new_value}")

# 添加监听器
client.add_listener('database.url', on_config_change)

# 开始监听
client.start_long_polling()

# 停止监听
client.stop_long_polling()
```

### 上下文管理器

```python
with ApolloClient(config) as client:
    # 在上下文管理器中使用客户端
    value = client.get_config('test.key', 'default_value')
    print(f"配置值: {value}")
    # 退出时自动清理资源
```

## 配置参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `APOLLO_SERVER_URL` | Apollo服务器地址 | `http://localhost:8080` |
| `APOLLO_APP_ID` | 应用ID | `demo-app` |
| `APOLLO_CLUSTER` | 集群名称 | `default` |
| `APOLLO_NAMESPACE` | 命名空间 | `application` |
| `APOLLO_ENABLE_LONG_POLLING` | 是否启用长轮询 | `true` |
| `APOLLO_POLLING_INTERVAL` | 轮询间隔（秒） | `30` |
| `APOLLO_TIMEOUT` | 超时时间（秒） | `30` |
| `APOLLO_ENABLE_CACHE` | 是否启用缓存 | `true` |
| `APOLLO_CACHE_DIR` | 缓存目录 | `./apollo_cache` |

## Apollo服务器设置

### 1. 使用Docker快速启动Apollo

```bash
# 克隆Apollo项目
git clone https://github.com/apolloconfig/apollo.git
cd apollo

# 启动Apollo
docker-compose up -d
```

### 2. 访问Apollo控制台

- 地址：http://localhost:8070
- 用户名：apollo
- 密码：admin

### 3. 创建应用和配置

1. 登录Apollo控制台
2. 创建应用（AppId: demo-app）
3. 在application命名空间添加配置：
   - `database.url`: `localhost:3306`
   - `redis.host`: `localhost`
   - `app.name`: `demo-app`

## 注意事项

1. **网络连接**：确保Python客户端能够访问Apollo服务器
2. **配置权限**：确保应用有读取配置的权限
3. **缓存清理**：如果配置有问题，可以删除缓存目录重新获取
4. **长轮询**：长轮询会占用一个线程，注意在应用退出时停止

## 故障排除

### 1. 连接失败

- 检查Apollo服务器地址是否正确
- 检查网络连接是否正常
- 检查防火墙设置

### 2. 配置获取失败

- 检查AppId是否正确
- 检查命名空间是否存在
- 检查配置项是否已创建

### 3. 监听器不工作

- 检查长轮询是否已启动
- 检查监听器是否正确注册
- 检查Apollo服务器是否支持长轮询

## 扩展功能

### 1. 添加更多配置类型支持

```python
# 支持JSON配置
json_config = client.get_config('app.settings', '{}')
settings = json.loads(json_config)

# 支持数字配置
max_connections = int(client.get_config('database.max_connections', '10'))
```

### 2. 添加配置验证

```python
def validate_config(key, value):
    if key == 'database.url' and not value.startswith('jdbc:'):
        raise ValueError(f"Invalid database URL: {value}")
    return value

# 在获取配置时进行验证
value = client.get_config('database.url')
validated_value = validate_config('database.url', value)
```

### 3. 添加配置加密支持

```python
import base64

def decrypt_config(value):
    # 实现配置解密逻辑
    return base64.b64decode(value).decode('utf-8')

# 获取加密配置
encrypted_value = client.get_config('secret.key')
decrypted_value = decrypt_config(encrypted_value)
```

## 许可证

MIT License