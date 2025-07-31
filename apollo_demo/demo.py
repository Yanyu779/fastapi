#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apollo配置中心Python客户端Demo
"""

import time
import signal
import sys
from config import ApolloConfig
from apollo_client import ApolloClient

def config_change_handler(key: str, old_value, new_value):
    """配置变更处理函数"""
    print(f"🎯 配置变更通知: {key}")
    print(f"   旧值: {old_value}")
    print(f"   新值: {new_value}")
    print(f"   时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

def signal_handler(signum, frame):
    """信号处理函数"""
    print("\n正在退出...")
    sys.exit(0)

def main():
    """主函数"""
    print("🚀 Apollo配置中心Python客户端Demo")
    print("=" * 50)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 创建配置对象
    config = ApolloConfig()
    config.print_config()
    
    # 创建Apollo客户端
    with ApolloClient(config) as client:
        print("\n📋 获取配置示例:")
        print("-" * 30)
        
        # 获取单个配置
        db_url = client.get_config('database.url', 'localhost:3306')
        print(f"数据库URL: {db_url}")
        
        redis_host = client.get_config('redis.host', 'localhost')
        print(f"Redis主机: {redis_host}")
        
        app_name = client.get_config('app.name', 'demo-app')
        print(f"应用名称: {app_name}")
        
        # 获取所有配置
        print("\n📋 所有配置:")
        print("-" * 30)
        all_configs = client.get_all_configs()
        for key, value in all_configs.items():
            print(f"{key}: {value}")
        
        # 添加配置变更监听器
        print("\n👂 添加配置变更监听器...")
        client.add_listener('database.url', config_change_handler)
        client.add_listener('redis.host', config_change_handler)
        client.add_listener('app.name', config_change_handler)
        
        # 开始长轮询监听配置变更
        print("\n🔄 开始监听配置变更...")
        client.start_long_polling()
        
        # 模拟应用运行
        print("\n⏰ 应用运行中，按Ctrl+C退出...")
        print("💡 提示: 在Apollo控制台修改配置，这里会收到变更通知")
        
        try:
            while True:
                # 模拟定期获取配置
                current_db_url = client.get_config('database.url', 'localhost:3306')
                current_redis_host = client.get_config('redis.host', 'localhost')
                
                print(f"\r当前配置 - DB: {current_db_url}, Redis: {current_redis_host}", end='')
                time.sleep(10)  # 每10秒更新一次显示
                
        except KeyboardInterrupt:
            print("\n\n正在退出...")
        finally:
            client.stop_long_polling()

def demo_basic_usage():
    """基础使用示例"""
    print("🔧 基础使用示例:")
    print("-" * 30)
    
    # 创建配置
    config = ApolloConfig()
    
    # 创建客户端
    client = ApolloClient(config)
    
    # 获取配置
    value = client.get_config('test.key', 'default_value')
    print(f"配置值: {value}")
    
    # 获取所有配置
    all_configs = client.get_all_configs()
    print(f"所有配置: {all_configs}")
    
    # 添加监听器
    def on_config_change(key, old_value, new_value):
        print(f"配置 {key} 从 {old_value} 变更为 {new_value}")
    
    client.add_listener('test.key', on_config_change)
    
    # 开始监听
    client.start_long_polling()
    
    # 运行一段时间
    time.sleep(30)
    
    # 停止监听
    client.stop_long_polling()

def demo_context_manager():
    """上下文管理器示例"""
    print("🔧 上下文管理器示例:")
    print("-" * 30)
    
    config = ApolloConfig()
    
    with ApolloClient(config) as client:
        # 在上下文管理器中使用客户端
        value = client.get_config('test.key', 'default_value')
        print(f"配置值: {value}")
        
        # 上下文管理器会自动处理资源清理
        print("客户端将在退出时自动清理资源")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "basic":
            demo_basic_usage()
        elif sys.argv[1] == "context":
            demo_context_manager()
        else:
            print("用法: python demo.py [basic|context]")
            print("  basic  - 基础使用示例")
            print("  context - 上下文管理器示例")
            print("  无参数 - 完整交互式demo")
    else:
        main()