#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apollo配置中心Python客户端Demo

这个demo展示了如何使用Apollo配置中心：
1. 连接Apollo服务
2. 获取配置信息
3. 监听配置变更
4. 处理配置更新
"""

import time
import signal
import sys
from apollo_client import ApolloClient, config_change_listener


def custom_config_listener(namespace: str, changed_configs: dict):
    """自定义配置变更监听器"""
    print(f"\n🔔 收到配置变更通知:")
    print(f"   📂 Namespace: {namespace}")
    print(f"   📝 变更内容:")
    for key, value in changed_configs.items():
        print(f"      {key} = {value}")
    print()
    
    # 在这里添加你的业务逻辑
    # 例如：重新加载数据库连接、更新缓存、重启服务等
    if 'database.url' in changed_configs:
        print("   💡 检测到数据库配置变更，建议重新连接数据库")
    
    if 'cache.size' in changed_configs:
        print("   💡 检测到缓存配置变更，建议重新初始化缓存")


def signal_handler(signum, frame):
    """信号处理函数"""
    print("\n👋 接收到退出信号，正在关闭Apollo客户端...")
    sys.exit(0)


def main():
    """主函数"""
    print("🚀 Apollo配置中心Python客户端Demo")
    print("=" * 50)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Apollo配置
    apollo_config = {
        'app_id': 'SampleApp',  # 你的应用ID
        'cluster': 'default',   # 集群名称
        'config_server_url': 'http://localhost:8080',  # Apollo Config Service地址
        'timeout': 90,  # 长轮询超时时间
        # 'ip': '192.168.1.100'  # 可选：指定客户端IP
    }
    
    print(f"📋 配置信息:")
    print(f"   App ID: {apollo_config['app_id']}")
    print(f"   Cluster: {apollo_config['cluster']}")
    print(f"   Config Server: {apollo_config['config_server_url']}")
    print()
    
    try:
        # 创建Apollo客户端
        with ApolloClient(**apollo_config) as client:
            print("✅ Apollo客户端初始化成功")
            
            # 1. 获取默认namespace的配置
            print("\n📥 获取默认namespace配置...")
            default_configs = client.get_config("application")
            print(f"   获取到 {len(default_configs)} 个配置项:")
            for key, value in default_configs.items():
                print(f"      {key} = {value}")
            
            # 2. 获取特定配置值
            print("\n🔍 获取特定配置值...")
            # 这些是示例key，你需要根据实际情况修改
            sample_keys = [
                'server.port',
                'database.url', 
                'redis.host',
                'app.version'
            ]
            
            for key in sample_keys:
                value = client.get_value(key, default="未配置")
                print(f"   {key} = {value}")
            
            # 3. 获取其他namespace的配置（如果有的话）
            print("\n📥 尝试获取其他namespace配置...")
            namespaces = ['application.yml', 'database', 'redis', 'common']
            
            for namespace in namespaces:
                try:
                    configs = client.get_config(namespace)
                    if configs:
                        print(f"   📂 {namespace}: {len(configs)} 个配置项")
                        for key, value in configs.items():
                            print(f"      {key} = {value}")
                    else:
                        print(f"   📂 {namespace}: 无配置或namespace不存在")
                except Exception as e:
                    print(f"   📂 {namespace}: 获取失败 - {e}")
            
            # 4. 添加配置变更监听器
            print("\n👂 添加配置变更监听器...")
            client.add_change_listener("application", custom_config_listener)
            client.add_change_listener("application", config_change_listener)  # 使用默认监听器
            
            # 为其他namespace也添加监听器
            for namespace in ['database', 'redis']:
                client.add_change_listener(namespace, custom_config_listener)
            
            # 5. 开始长轮询监听配置变更
            print("🔄 开始监听配置变更...")
            client.start_polling()
            
            print("\n✨ 系统运行中...")
            print("💡 提示:")
            print("   - 现在可以在Apollo管理界面修改配置")
            print("   - 客户端会自动检测配置变更并触发监听器")
            print("   - 按 Ctrl+C 退出程序")
            print("   - 长轮询超时时间: {}秒".format(apollo_config['timeout']))
            print()
            
            # 6. 定期展示当前配置（可选）
            counter = 0
            while True:
                time.sleep(30)  # 每30秒显示一次状态
                counter += 1
                print(f"⏰ 运行状态检查 #{counter} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # 显示当前缓存的配置数量
                total_configs = sum(len(configs) for configs in client.configs.values())
                print(f"   📊 当前缓存配置总数: {total_configs}")
                print(f"   📂 已缓存的namespace: {list(client.configs.keys())}")
                
                # 可以在这里添加健康检查逻辑
                # 比如检查关键配置是否存在、验证配置格式等
                
    except KeyboardInterrupt:
        print("\n👋 用户中断，正在退出...")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("🔚 Apollo Demo 结束")


if __name__ == "__main__":
    main()