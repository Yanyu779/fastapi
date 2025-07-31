# Apollo配置中心Python客户端Demo

这是一个用Python连接Apollo配置中心的完整示例，展示了如何获取配置、监听配置变更等功能。

## 📋 项目结构

```
.
├── apollo_client.py        # Apollo客户端核心模块
├── apollo_demo.py         # 完整的Demo示例
├── apollo_requirements.txt # 项目依赖
└── apollo_README.md       # 使用说明（本文件）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r apollo_requirements.txt
```

或者手动安装：

```bash
pip install requests typing-extensions
```

### 2. 配置Apollo服务信息

编辑 `apollo_demo.py` 文件中的配置：

```python
apollo_config = {
    'app_id': 'YourAppId',                    # 改为你的应用ID
    'cluster': 'default',                     # 集群名称
    'config_server_url': 'http://localhost:8080',  # Apollo Config Service地址
    'timeout': 90,                            # 长轮询超时时间
    # 'ip': '192.168.1.100'                  # 可选：指定客户端IP
}
```

### 3. 运行Demo

```bash
python apollo_demo.py
```

## 🔧 功能特性

### ✅ 支持的功能

- ✅ 获取指定namespace的配置
- ✅ 获取单个配置项的值
- ✅ 实时监听配置变更（长轮询）
- ✅ 支持多个namespace
- ✅ 支持自定义配置变更监听器
- ✅ 自动重连和错误处理
- ✅ 上下文管理器支持
- ✅ 线程安全的长轮询
- ✅ 配置本地缓存

### 📝 API使用示例

#### 基本使用

```python
from apollo_client import ApolloClient

# 创建客户端
client = ApolloClient(
    app_id='SampleApp',
    config_server_url='http://localhost:8080'
)

# 获取配置
configs = client.get_config('application')
print(configs)

# 获取单个配置值
port = client.get_value('server.port', default=8080)
print(f"服务端口: {port}")
```

#### 配置变更监听

```python
def my_config_listener(namespace: str, changed_configs: dict):
    print(f"配置变更: {namespace} -> {changed_configs}")
    # 添加你的业务逻辑
    if 'database.url' in changed_configs:
        # 重新连接数据库
        reconnect_database()

# 添加监听器
client.add_change_listener('application', my_config_listener)

# 开始监听
client.start_polling()
```

#### 使用上下文管理器

```python
with ApolloClient(app_id='SampleApp', config_server_url='http://localhost:8080') as client:
    client.add_change_listener('application', my_config_listener)
    client.start_polling()
    
    # 你的业务代码
    while True:
        # 处理业务逻辑
        time.sleep(10)
# 自动清理资源
```

## 🛠️ 高级配置

### 环境变量配置

你也可以通过环境变量来配置Apollo连接信息：

```bash
export APOLLO_APP_ID=SampleApp
export APOLLO_CLUSTER=default
export APOLLO_CONFIG_SERVER_URL=http://localhost:8080
export APOLLO_TIMEOUT=90
```

### 多环境支持

```python
import os

def get_apollo_config():
    env = os.getenv('ENV', 'dev')
    
    config_map = {
        'dev': {
            'app_id': 'SampleApp',
            'config_server_url': 'http://dev-apollo:8080'
        },
        'test': {
            'app_id': 'SampleApp',
            'config_server_url': 'http://test-apollo:8080'
        },
        'prod': {
            'app_id': 'SampleApp',
            'config_server_url': 'http://prod-apollo:8080'
        }
    }
    
    return config_map.get(env, config_map['dev'])
```

## 🔍 常见问题

### Q: 连接Apollo失败怎么办？

A: 检查以下几点：
1. Apollo Config Service是否正常运行
2. 网络连接是否正常
3. app_id是否正确
4. 防火墙是否阻止了连接

### Q: 获取不到配置怎么办？

A: 检查以下几点：
1. namespace是否存在
2. 应用是否已经在Apollo中创建
3. 配置是否已经发布
4. 客户端IP是否有权限访问

### Q: 长轮询不工作怎么办？

A: 检查以下几点：
1. 网络是否稳定
2. 超时时间设置是否合理
3. Apollo服务是否支持长轮询
4. 查看日志输出排查问题

### Q: 如何处理配置格式？

A: Apollo支持多种配置格式：

```python
# 处理JSON格式配置
import json
json_config = client.get_value('app.config')
if json_config:
    config_dict = json.loads(json_config)

# 处理YAML格式配置
import yaml
yaml_config = client.get_value('app.yaml')
if yaml_config:
    config_dict = yaml.safe_load(yaml_config)
```

## 📚 相关资源

- [Apollo官方文档](https://www.apolloconfig.com/)
- [Apollo GitHub](https://github.com/apolloconfig/apollo)
- [Apollo Java客户端](https://github.com/apolloconfig/apollo-java)

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个Demo！

## 📄 许可证

本项目采用MIT许可证。