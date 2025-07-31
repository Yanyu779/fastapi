#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的Apollo配置中心使用示例

这是一个最简化的例子，展示Apollo客户端的基本用法。
"""

from apollo_client import ApolloClient
import time


def simple_example():
    """简单使用示例"""
    print("🚀 简单Apollo示例")
    print("-" * 30)
    
    # 创建Apollo客户端
    client = ApolloClient(
        app_id='SampleApp',  # 替换为你的应用ID
        config_server_url='http://localhost:8080'  # 替换为你的Apollo地址
    )
    
    try:
        # 1. 获取配置
        print("📥 获取配置...")
        configs = client.get_config('application')
        print(f"获取到配置: {configs}")
        
        # 2. 获取特定配置值
        port = client.get_value('server.port', default=8080)
        print(f"服务端口: {port}")
        
        # 3. 添加配置变更监听
        def on_config_change(namespace, changed_configs):
            print(f"⚡ 配置变更: {namespace} -> {changed_configs}")
        
        client.add_change_listener('application', on_config_change)
        
        # 4. 开始监听（可选）
        print("👂 开始监听配置变更...")
        client.start_polling()
        
        # 5. 模拟业务运行
        print("✨ 系统运行中，按Ctrl+C退出")
        for i in range(10):
            print(f"业务循环 {i+1}/10")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("👋 用户中断")
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        client.stop_polling()
        print("🔚 示例结束")


if __name__ == "__main__":
    simple_example()