import requests
import json
import time
import threading
import os
from typing import Dict, Any, Optional, Callable
from config import ApolloConfig

class ApolloClient:
    """Apollo配置中心客户端"""
    
    def __init__(self, config: ApolloConfig):
        self.config = config
        self.base_url = config.apollo_server_url
        self.app_id = config.app_id
        self.cluster = config.cluster
        self.namespace = config.namespace
        self.timeout = config.timeout
        
        # 配置缓存
        self._config_cache: Dict[str, Any] = {}
        self._notification_id = -1
        
        # 监听器列表
        self._listeners: Dict[str, Callable] = {}
        
        # 长轮询线程
        self._polling_thread = None
        self._stop_polling = False
        
        # 确保缓存目录存在
        if config.enable_cache:
            os.makedirs(config.cache_dir, exist_ok=True)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        # 先从缓存获取
        if key in self._config_cache:
            return self._config_cache[key]
        
        # 从Apollo服务器获取
        try:
            url = f"{self.base_url}/configs/{self.app_id}/{self.cluster}/{self.namespace}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                configs = data.get('configurations', {})
                
                # 更新缓存
                self._config_cache.update(configs)
                
                # 保存到本地缓存文件
                if self.config.enable_cache:
                    self._save_cache()
                
                return configs.get(key, default)
            else:
                print(f"获取配置失败: {response.status_code}")
                return default
                
        except Exception as e:
            print(f"获取配置异常: {e}")
            return default
    
    def get_all_configs(self) -> Dict[str, Any]:
        """获取所有配置"""
        try:
            url = f"{self.base_url}/configs/{self.app_id}/{self.cluster}/{self.namespace}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                configs = data.get('configurations', {})
                
                # 更新缓存
                self._config_cache.update(configs)
                
                # 保存到本地缓存文件
                if self.config.enable_cache:
                    self._save_cache()
                
                return configs
            else:
                print(f"获取所有配置失败: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"获取所有配置异常: {e}")
            return {}
    
    def add_listener(self, key: str, callback: Callable[[str, Any, Any], None]):
        """添加配置变更监听器"""
        self._listeners[key] = callback
    
    def remove_listener(self, key: str):
        """移除配置变更监听器"""
        if key in self._listeners:
            del self._listeners[key]
    
    def start_long_polling(self):
        """开始长轮询监听配置变更"""
        if not self.config.enable_long_polling:
            print("长轮询未启用")
            return
        
        self._stop_polling = False
        self._polling_thread = threading.Thread(target=self._polling_worker)
        self._polling_thread.daemon = True
        self._polling_thread.start()
        print("开始长轮询监听配置变更...")
    
    def stop_long_polling(self):
        """停止长轮询"""
        self._stop_polling = True
        if self._polling_thread:
            self._polling_thread.join()
        print("停止长轮询监听")
    
    def _polling_worker(self):
        """长轮询工作线程"""
        while not self._stop_polling:
            try:
                # 获取通知ID
                if self._notification_id == -1:
                    self._notification_id = self._get_notification_id()
                
                # 长轮询检查配置变更
                url = f"{self.base_url}/notifications/v2"
                params = {
                    'appId': self.app_id,
                    'cluster': self.cluster,
                    'notifications': json.dumps([{
                        'namespaceName': self.namespace,
                        'notificationId': self._notification_id
                    }])
                }
                
                response = requests.get(url, params=params, timeout=self.timeout + 10)
                
                if response.status_code == 200:
                    notifications = response.json()
                    
                    for notification in notifications:
                        if notification.get('notificationId') > self._notification_id:
                            self._notification_id = notification.get('notificationId')
                            
                            # 重新获取配置
                            old_configs = self._config_cache.copy()
                            new_configs = self.get_all_configs()
                            
                            # 检查配置变更并触发监听器
                            self._check_config_changes(old_configs, new_configs)
                
            except Exception as e:
                print(f"长轮询异常: {e}")
                time.sleep(5)  # 异常时等待5秒后重试
    
    def _get_notification_id(self) -> int:
        """获取通知ID"""
        try:
            url = f"{self.base_url}/notifications/v2"
            params = {
                'appId': self.app_id,
                'cluster': self.cluster,
                'notifications': json.dumps([{
                    'namespaceName': self.namespace,
                    'notificationId': -1
                }])
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                notifications = response.json()
                if notifications:
                    return notifications[0].get('notificationId', -1)
            
            return -1
            
        except Exception as e:
            print(f"获取通知ID异常: {e}")
            return -1
    
    def _check_config_changes(self, old_configs: Dict[str, Any], new_configs: Dict[str, Any]):
        """检查配置变更"""
        all_keys = set(old_configs.keys()) | set(new_configs.keys())
        
        for key in all_keys:
            old_value = old_configs.get(key)
            new_value = new_configs.get(key)
            
            if old_value != new_value:
                print(f"配置变更: {key} = {old_value} -> {new_value}")
                
                # 触发监听器
                if key in self._listeners:
                    try:
                        self._listeners[key](key, old_value, new_value)
                    except Exception as e:
                        print(f"监听器执行异常: {e}")
    
    def _save_cache(self):
        """保存配置到本地缓存"""
        try:
            cache_file = os.path.join(self.config.cache_dir, f"{self.app_id}_{self.namespace}.json")
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self._config_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存缓存异常: {e}")
    
    def _load_cache(self):
        """从本地缓存加载配置"""
        try:
            cache_file = os.path.join(self.config.cache_dir, f"{self.app_id}_{self.namespace}.json")
            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self._config_cache = json.load(f)
        except Exception as e:
            print(f"加载缓存异常: {e}")
    
    def __enter__(self):
        """上下文管理器入口"""
        if self.config.enable_cache:
            self._load_cache()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop_long_polling()