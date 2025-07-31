import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ApolloConfig:
    """Apollo配置类"""
    
    def __init__(self):
        # Apollo服务器地址
        self.apollo_server_url = os.getenv('APOLLO_SERVER_URL', 'http://localhost:8080')
        
        # 应用ID
        self.app_id = os.getenv('APOLLO_APP_ID', 'demo-app')
        
        # 集群名称
        self.cluster = os.getenv('APOLLO_CLUSTER', 'default')
        
        # 命名空间
        self.namespace = os.getenv('APOLLO_NAMESPACE', 'application')
        
        # 是否启用长轮询
        self.enable_long_polling = os.getenv('APOLLO_ENABLE_LONG_POLLING', 'true').lower() == 'true'
        
        # 轮询间隔（秒）
        self.polling_interval = int(os.getenv('APOLLO_POLLING_INTERVAL', '30'))
        
        # 超时时间（秒）
        self.timeout = int(os.getenv('APOLLO_TIMEOUT', '30'))
        
        # 是否启用缓存
        self.enable_cache = os.getenv('APOLLO_ENABLE_CACHE', 'true').lower() == 'true'
        
        # 缓存目录
        self.cache_dir = os.getenv('APOLLO_CACHE_DIR', './apollo_cache')
    
    def get_config_dict(self):
        """获取配置字典"""
        return {
            'apollo_server_url': self.apollo_server_url,
            'app_id': self.app_id,
            'cluster': self.cluster,
            'namespace': self.namespace,
            'enable_long_polling': self.enable_long_polling,
            'polling_interval': self.polling_interval,
            'timeout': self.timeout,
            'enable_cache': self.enable_cache,
            'cache_dir': self.cache_dir
        }
    
    def print_config(self):
        """打印配置信息"""
        print("=== Apollo配置信息 ===")
        for key, value in self.get_config_dict().items():
            print(f"{key}: {value}")
        print("=====================")