#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apollo配置中心简单示例
"""

import time
from config import ApolloConfig
from apollo_client import ApolloClient

def simple_demo():
    """简单示例"""
    print("🚀 Apollo配置中心简单示例")
    print("=" * 40)
    
    # 1. 创建配置
    config = ApolloConfig()
    print("✅ 配置创建完成")
    
    # 2. 创建客户端
    client = ApolloClient(config)
    print("✅ 客户端创建完成")
    
    # 3. 获取配置示例
    print("\n📋 获取配置示例:")
    print("-" * 20)
    
    # 获取单个配置
    db_url = client.get_config('database.url', 'localhost:3306')
    print(f"数据库URL: {db_url}")
    
    redis_host = client.get_config('redis.host', 'localhost')
    print(f"Redis主机: {redis_host}")
    
    app_name = client.get_config('app.name', 'demo-app')
    print(f"应用名称: {app_name}")
    
    # 获取所有配置
    print("\n📋 所有配置:")
    print("-" * 20)
    all_configs = client.get_all_configs()
    for key, value in all_configs.items():
        print(f"{key}: {value}")
    
    # 4. 配置变更监听示例
    print("\n👂 配置变更监听示例:")
    print("-" * 20)
    
    def on_config_change(key, old_value, new_value):
        print(f"🎯 配置变更: {key} = {old_value} -> {new_value}")
    
    # 添加监听器
    client.add_listener('database.url', on_config_change)
    client.add_listener('redis.host', on_config_change)
    client.add_listener('app.name', on_config_change)
    
    # 开始监听
    print("开始监听配置变更...")
    client.start_long_polling()
    
    # 运行一段时间
    print("运行30秒，期间可以在Apollo控制台修改配置...")
    time.sleep(30)
    
    # 停止监听
    client.stop_long_polling()
    print("✅ 示例完成")

def quick_start():
    """快速开始示例"""
    print("⚡ 快速开始示例")
    print("=" * 30)
    
    # 最简单的使用方式
    config = ApolloConfig()
    client = ApolloClient(config)
    
    # 获取配置
    value = client.get_config('test.key', 'default_value')
    print(f"配置值: {value}")
    
    # 获取所有配置
    configs = client.get_all_configs()
    print(f"所有配置: {configs}")
    
    print("✅ 快速开始完成")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_start()
    else:
        simple_demo()