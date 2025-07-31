import requests
import json
import time
import threading
from typing import Dict, Any, Optional, Callable
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApolloClient:
    """Apollo配置中心客户端"""
    
    def __init__(self, 
                 app_id: str,
                 cluster: str = "default",
                 config_server_url: str = "http://localhost:8080",
                 timeout: int = 90,
                 ip: Optional[str] = None):
        """
        初始化Apollo客户端
        
        Args:
            app_id: 应用ID
            cluster: 集群名称，默认为default
            config_server_url: Apollo配置服务URL
            timeout: 长轮询超时时间（秒）
            ip: 客户端IP地址
        """
        self.app_id = app_id
        self.cluster = cluster
        self.config_server_url = config_server_url.rstrip('/')
        self.timeout = timeout
        self.ip = ip
        
        # 存储配置信息
        self.configs: Dict[str, Dict[str, Any]] = {}
        self.notifications: Dict[str, int] = {}
        
        # 监听器
        self.listeners: Dict[str, list] = {}
        
        # 控制长轮询的标志
        self._stop_event = threading.Event()
        self._polling_thread = None
        
    def get_config(self, namespace: str = "application") -> Dict[str, Any]:
        """
        获取指定namespace的配置
        
        Args:
            namespace: 命名空间，默认为application
            
        Returns:
            配置字典
        """
        url = f"{self.config_server_url}/configs/{self.app_id}/{self.cluster}/{namespace}"
        
        params = {}
        if self.ip:
            params['ip'] = self.ip
            
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            configurations = data.get('configurations', {})
            
            # 更新本地缓存
            self.configs[namespace] = configurations
            
            # 更新notification ID
            self.notifications[namespace] = data.get('releaseKey', 0)
            
            logger.info(f"成功获取namespace '{namespace}' 的配置")
            return configurations
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取配置失败: {e}")
            return self.configs.get(namespace, {})
    
    def get_value(self, key: str, namespace: str = "application", default: Any = None) -> Any:
        """
        获取指定key的配置值
        
        Args:
            key: 配置key
            namespace: 命名空间
            default: 默认值
            
        Returns:
            配置值
        """
        if namespace not in self.configs:
            self.get_config(namespace)
            
        return self.configs.get(namespace, {}).get(key, default)
    
    def add_change_listener(self, namespace: str, listener: Callable[[str, Dict[str, Any]], None]):
        """
        添加配置变更监听器
        
        Args:
            namespace: 命名空间
            listener: 监听器函数，参数为(namespace, changed_configs)
        """
        if namespace not in self.listeners:
            self.listeners[namespace] = []
        self.listeners[namespace].append(listener)
        logger.info(f"为namespace '{namespace}' 添加了变更监听器")
    
    def start_polling(self):
        """开始长轮询监听配置变更"""
        if self._polling_thread and self._polling_thread.is_alive():
            logger.warning("长轮询已经在运行中")
            return
            
        self._stop_event.clear()
        self._polling_thread = threading.Thread(target=self._polling_loop, daemon=True)
        self._polling_thread.start()
        logger.info("开始长轮询监听配置变更")
    
    def stop_polling(self):
        """停止长轮询"""
        self._stop_event.set()
        if self._polling_thread:
            self._polling_thread.join(timeout=5)
        logger.info("停止长轮询")
    
    def _polling_loop(self):
        """长轮询循环"""
        while not self._stop_event.is_set():
            try:
                # 构建notifications参数
                notifications = []
                for namespace, notification_id in self.notifications.items():
                    notifications.append({
                        "namespaceName": namespace,
                        "notificationId": notification_id
                    })
                
                if not notifications:
                    # 如果没有namespace，先获取默认配置
                    self.get_config()
                    time.sleep(1)
                    continue
                
                # 发起长轮询请求
                url = f"{self.config_server_url}/notifications/v2"
                params = {
                    'appId': self.app_id,
                    'cluster': self.cluster,
                    'notifications': json.dumps(notifications)
                }
                
                if self.ip:
                    params['ip'] = self.ip
                
                response = requests.get(url, params=params, timeout=self.timeout + 5)
                
                if response.status_code == 200:
                    # 有配置变更
                    changed_namespaces = response.json()
                    for change in changed_namespaces:
                        namespace = change['namespaceName']
                        old_config = self.configs.get(namespace, {}).copy()
                        
                        # 重新获取配置
                        new_config = self.get_config(namespace)
                        
                        # 找出变更的配置项
                        changed_configs = {}
                        for key, value in new_config.items():
                            if key not in old_config or old_config[key] != value:
                                changed_configs[key] = value
                        
                        # 通知监听器
                        for listener in self.listeners.get(namespace, []):
                            try:
                                listener(namespace, changed_configs)
                            except Exception as e:
                                logger.error(f"监听器执行失败: {e}")
                        
                        logger.info(f"检测到namespace '{namespace}' 配置变更: {changed_configs}")
                
                elif response.status_code == 304:
                    # 没有变更，继续轮询
                    pass
                else:
                    logger.warning(f"长轮询请求失败: {response.status_code}")
                    time.sleep(5)
                    
            except requests.exceptions.Timeout:
                # 超时是正常的，继续下一次轮询
                pass
            except Exception as e:
                logger.error(f"长轮询异常: {e}")
                time.sleep(5)
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop_polling()


# 示例监听器函数
def config_change_listener(namespace: str, changed_configs: Dict[str, Any]):
    """配置变更监听器示例"""
    print(f"配置变更通知:")
    print(f"  Namespace: {namespace}")
    print(f"  变更的配置: {changed_configs}")
    
    # 这里可以添加你的业务逻辑
    # 比如重新加载应用配置、更新缓存等