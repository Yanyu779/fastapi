#!/usr/bin/env python3
"""
Apollo配置中心演示脚本
"""

import os
import time
import json
from apollo_client import ApolloClient

def config_change_callback(configs):
    """
    配置变化回调函数
    """
    print(f"\n配置发生变化: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("新的配置:")
    for key, value in configs.items():
        print(f"  {key}: {value}")

def main():
    """
    主函数
    """
    print("=== Apollo配置中心演示 ===")
    
    # 从环境变量获取配置，如果没有则使用默认值
    app_id = os.getenv('APOLLO_APP_ID', 'demo-app')
    apollo_url = os.getenv('APOLLO_URL', 'http://localhost:8080')
    cluster = os.getenv('APOLLO_CLUSTER', 'default')
    namespace = os.getenv('APOLLO_NAMESPACE', 'application')
    
    print(f"应用ID: {app_id}")
    print(f"Apollo服务器: {apollo_url}")
    print(f"集群: {cluster}")
    print(f"命名空间: {namespace}")
    print()
    
    # 创建Apollo客户端
    client = ApolloClient(
        app_id=app_id,
        cluster=cluster,
        namespace=namespace,
        apollo_url=apollo_url
    )
    
    # 获取单个配置
    print("=== 获取单个配置 ===")
    db_url = client.get_config('database.url', 'mysql://localhost:3306/demo')
    print(f"数据库URL: {db_url}")
    
    redis_host = client.get_config('redis.host', 'localhost')
    print(f"Redis主机: {redis_host}")
    
    max_connections = client.get_config('database.max_connections', 10)
    print(f"最大连接数: {max_connections}")
    
    # 获取所有配置
    print("\n=== 获取所有配置 ===")
    all_configs = client.get_all_configs()
    if all_configs:
        print("当前所有配置:")
        for key, value in all_configs.items():
            print(f"  {key}: {value}")
    else:
        print("没有找到任何配置，可能Apollo服务器未运行或配置为空")
    
    # 演示配置监听
    print("\n=== 开始监听配置变化 ===")
    print("配置监听已启动，每5秒检查一次配置变化...")
    print("您可以在Apollo管理界面修改配置来测试监听功能")
    print("按 Ctrl+C 停止监听")
    
    # 启动配置监听
    watch_thread = client.watch_config(config_change_callback, interval=5)
    
    try:
        # 保持程序运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序已停止")

if __name__ == "__main__":
    main()