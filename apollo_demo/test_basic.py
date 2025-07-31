#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础测试脚本 - 不依赖外部包
"""

import os
import sys

def test_basic_import():
    """测试基础导入"""
    print("🧪 测试基础导入...")
    
    # 模拟dotenv功能
    class MockDotenv:
        def load_dotenv(self):
            pass
    
    # 临时替换dotenv模块
    sys.modules['dotenv'] = MockDotenv()
    
    try:
        from config import ApolloConfig
        print("✅ config.py 导入成功")
        
        config = ApolloConfig()
        print("✅ ApolloConfig 实例化成功")
        
        print(f"服务器地址: {config.apollo_server_url}")
        print(f"应用ID: {config.app_id}")
        print(f"集群: {config.cluster}")
        print(f"命名空间: {config.namespace}")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_client_import():
    """测试客户端导入"""
    print("\n🧪 测试客户端导入...")
    
    try:
        from apollo_client import ApolloClient
        print("✅ apollo_client.py 导入成功")
        
        # 创建配置（使用模拟的dotenv）
        from config import ApolloConfig
        config = ApolloConfig()
        
        client = ApolloClient(config)
        print("✅ ApolloClient 实例化成功")
        
        print(f"客户端AppId: {client.app_id}")
        print(f"客户端集群: {client.cluster}")
        print(f"客户端命名空间: {client.namespace}")
        
        return True
        
    except Exception as e:
        print(f"❌ 客户端导入失败: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("\n🧪 测试文件结构...")
    
    required_files = [
        'requirements.txt',
        'config.py',
        'apollo_client.py',
        'demo.py',
        'simple_demo.py',
        'test_apollo.py',
        'run_demo.sh',
        '.env.example',
        'README.md',
        '项目总览.md'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - 缺失")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  缺失文件: {missing_files}")
        return False
    else:
        print("\n✅ 所有必需文件都存在")
        return True

def main():
    """主测试函数"""
    print("🚀 Apollo配置中心Python客户端 - 基础测试")
    print("=" * 50)
    
    # 测试文件结构
    structure_ok = test_file_structure()
    
    # 测试基础导入
    import_ok = test_basic_import()
    
    # 测试客户端导入
    client_ok = test_client_import()
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"文件结构: {'✅ 通过' if structure_ok else '❌ 失败'}")
    print(f"基础导入: {'✅ 通过' if import_ok else '❌ 失败'}")
    print(f"客户端导入: {'✅ 通过' if client_ok else '❌ 失败'}")
    
    if all([structure_ok, import_ok, client_ok]):
        print("\n🎉 所有基础测试通过！")
        print("💡 下一步: 安装依赖包并运行完整测试")
        print("   pip install -r requirements.txt")
        print("   python test_apollo.py")
    else:
        print("\n⚠️  部分测试失败，请检查代码")
    
    return all([structure_ok, import_ok, client_ok])

if __name__ == "__main__":
    main()