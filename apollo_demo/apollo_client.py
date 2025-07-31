import os
import time
import json
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ApolloClient:
    """
    Apollo配置中心客户端
    """
    
    def __init__(self, 
                 app_id: str,
                 cluster: str = "default",
                 namespace: str = "application",
                 apollo_url: str = "http://localhost:8080",
                 timeout: int = 30):
        """
        初始化Apollo客户端
        
        Args:
            app_id: 应用ID
            cluster: 集群名称，默认为default
            namespace: 命名空间，默认为application
            apollo_url: Apollo服务器地址
            timeout: 请求超时时间
        """
        self.app_id = app_id
        self.cluster = cluster
        self.namespace = namespace
        self.apollo_url = apollo_url.rstrip('/')
        self.timeout = timeout
        self.config_cache = {}
        self.last_update_time = 0
        self.notification_id = -1
        
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值或默认值
        """
        # 确保配置已加载
        self._load_config()
        
        # 从缓存中获取配置
        value = self.config_cache.get(key, default)
        
        # 尝试解析JSON
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                pass
                
        return value
    
    def get_all_configs(self) -> Dict[str, Any]:
        """
        获取所有配置
        
        Returns:
            所有配置的字典
        """
        self._load_config()
        return self.config_cache.copy()
    
    def _load_config(self):
        """
        从Apollo服务器加载配置
        """
        try:
            # 构建请求URL
            url = f"{self.apollo_url}/configs/{self.app_id}/{self.cluster}/{self.namespace}"
            
            # 添加通知ID参数
            params = {
                'ip': self._get_local_ip(),
                'notifications': json.dumps([{
                    'namespaceName': self.namespace,
                    'notificationId': self.notification_id
                }])
            }
            
            # 发送请求
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # 更新配置缓存
            if 'configurations' in data:
                self.config_cache.update(data['configurations'])
                self.last_update_time = time.time()
            
            # 更新通知ID
            if 'notificationId' in data:
                self.notification_id = data['notificationId']
                
        except requests.RequestException as e:
            print(f"加载配置失败: {e}")
            # 如果请求失败，使用缓存中的配置（如果有的话）
            if not self.config_cache:
                print("无法加载配置，请检查Apollo服务器是否运行")
    
    def _get_local_ip(self) -> str:
        """
        获取本地IP地址
        """
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def watch_config(self, callback, interval: int = 5):
        """
        监听配置变化
        
        Args:
            callback: 配置变化时的回调函数
            interval: 检查间隔（秒）
        """
        import threading
        
        def watch_loop():
            while True:
                try:
                    old_config = self.config_cache.copy()
                    self._load_config()
                    
                    # 检查配置是否有变化
                    if old_config != self.config_cache:
                        callback(self.config_cache)
                        
                except Exception as e:
                    print(f"监听配置变化时出错: {e}")
                
                time.sleep(interval)
        
        # 启动监听线程
        thread = threading.Thread(target=watch_loop, daemon=True)
        thread.start()
        return thread