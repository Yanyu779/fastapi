#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apollo客户端测试
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import tempfile
import os
from config import ApolloConfig
from apollo_client import ApolloClient

class TestApolloConfig(unittest.TestCase):
    """测试Apollo配置类"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = ApolloConfig()
        
        self.assertEqual(config.apollo_server_url, 'http://localhost:8080')
        self.assertEqual(config.app_id, 'demo-app')
        self.assertEqual(config.cluster, 'default')
        self.assertEqual(config.namespace, 'application')
        self.assertTrue(config.enable_long_polling)
        self.assertEqual(config.polling_interval, 30)
        self.assertEqual(config.timeout, 30)
        self.assertTrue(config.enable_cache)
        self.assertEqual(config.cache_dir, './apollo_cache')
    
    def test_config_dict(self):
        """测试配置字典"""
        config = ApolloConfig()
        config_dict = config.get_config_dict()
        
        self.assertIn('apollo_server_url', config_dict)
        self.assertIn('app_id', config_dict)
        self.assertIn('cluster', config_dict)
        self.assertIn('namespace', config_dict)

class TestApolloClient(unittest.TestCase):
    """测试Apollo客户端类"""
    
    def setUp(self):
        """设置测试环境"""
        self.config = ApolloConfig()
        self.client = ApolloClient(self.config)
    
    def tearDown(self):
        """清理测试环境"""
        if hasattr(self, 'client'):
            self.client.stop_long_polling()
    
    @patch('requests.get')
    def test_get_config_success(self, mock_get):
        """测试成功获取配置"""
        # 模拟响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'configurations': {
                'database.url': 'localhost:3306',
                'redis.host': 'localhost'
            }
        }
        mock_get.return_value = mock_response
        
        # 测试获取配置
        value = self.client.get_config('database.url', 'default')
        self.assertEqual(value, 'localhost:3306')
        
        # 测试默认值
        value = self.client.get_config('nonexistent.key', 'default_value')
        self.assertEqual(value, 'default_value')
    
    @patch('requests.get')
    def test_get_config_failure(self, mock_get):
        """测试获取配置失败"""
        # 模拟失败响应
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # 测试失败时返回默认值
        value = self.client.get_config('database.url', 'default')
        self.assertEqual(value, 'default')
    
    @patch('requests.get')
    def test_get_all_configs(self, mock_get):
        """测试获取所有配置"""
        # 模拟响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'configurations': {
                'database.url': 'localhost:3306',
                'redis.host': 'localhost',
                'app.name': 'demo-app'
            }
        }
        mock_get.return_value = mock_response
        
        # 测试获取所有配置
        configs = self.client.get_all_configs()
        self.assertEqual(len(configs), 3)
        self.assertEqual(configs['database.url'], 'localhost:3306')
        self.assertEqual(configs['redis.host'], 'localhost')
        self.assertEqual(configs['app.name'], 'demo-app')
    
    def test_listener_management(self):
        """测试监听器管理"""
        # 测试添加监听器
        def test_callback(key, old_value, new_value):
            pass
        
        self.client.add_listener('test.key', test_callback)
        self.assertIn('test.key', self.client._listeners)
        
        # 测试移除监听器
        self.client.remove_listener('test.key')
        self.assertNotIn('test.key', self.client._listeners)
    
    def test_context_manager(self):
        """测试上下文管理器"""
        with ApolloClient(self.config) as client:
            self.assertIsInstance(client, ApolloClient)
            # 上下文管理器应该正常工作
    
    def test_cache_operations(self):
        """测试缓存操作"""
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 修改配置使用临时目录
            self.config.cache_dir = temp_dir
            self.config.enable_cache = True
            
            client = ApolloClient(self.config)
            
            # 测试保存缓存
            client._config_cache = {'test.key': 'test.value'}
            client._save_cache()
            
            # 验证缓存文件存在
            cache_file = os.path.join(temp_dir, f"{self.config.app_id}_{self.config.namespace}.json")
            self.assertTrue(os.path.exists(cache_file))
            
            # 测试加载缓存
            client._config_cache = {}
            client._load_cache()
            self.assertEqual(client._config_cache.get('test.key'), 'test.value')

class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        config = ApolloConfig()
        client = ApolloClient(config)
        
        # 测试基本功能
        self.assertIsNotNone(client)
        self.assertEqual(client.app_id, 'demo-app')
        self.assertEqual(client.cluster, 'default')
        self.assertEqual(client.namespace, 'application')

def run_tests():
    """运行测试"""
    print("🧪 运行Apollo客户端测试...")
    
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 添加测试用例
    suite.addTest(unittest.makeSuite(TestApolloConfig))
    suite.addTest(unittest.makeSuite(TestApolloClient))
    suite.addTest(unittest.makeSuite(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果
    if result.wasSuccessful():
        print("✅ 所有测试通过!")
    else:
        print("❌ 部分测试失败!")
        print(f"失败: {len(result.failures)}")
        print(f"错误: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_tests()