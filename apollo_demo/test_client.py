#!/usr/bin/env python3
"""
Apollo客户端测试脚本
"""

import os
import sys
from apollo_client import ApolloClient

def test_apollo_client():
    """测试Apollo客户端基本功能"""
    print("=== Apollo客户端测试 ===")
    
    # 创建客户端
    client = ApolloClient(
        app_id='test-app',
        apollo_url='http://localhost:8080'
    )
    
    print(f"客户端创建成功:")
    print(f"  应用ID: {client.app_id}")
    print(f"  集群: {client.cluster}")
    print(f"  命名空间: {client.namespace}")
    print(f"  服务器地址: {client.apollo_url}")
    print()
    
    # 测试获取配置
    print("测试获取配置...")
    try:
        # 尝试获取一个不存在的配置，应该返回默认值
        test_value = client.get_config('test.key', 'default_value')
        print(f"  测试配置 'test.key': {test_value}")
        
        # 获取所有配置
        all_configs = client.get_all_configs()
        print(f"  当前配置数量: {len(all_configs)}")
        
        if all_configs:
            print("  当前配置:")
            for key, value in all_configs.items():
                print(f"    {key}: {value}")
        else:
            print("  没有找到配置，这可能是正常的（如果Apollo服务器没有运行或没有配置）")
            
    except Exception as e:
        print(f"  测试失败: {e}")
        print("  这可能是正常的，如果Apollo服务器没有运行")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_apollo_client()