#!/usr/bin/env python3
"""
FastAPI + Apollo配置中心示例
"""

import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from apollo_client import ApolloClient

# 创建FastAPI应用
app = FastAPI(title="Apollo配置中心演示", version="1.0.0")

# 创建Apollo客户端
apollo_client = ApolloClient(
    app_id=os.getenv('APOLLO_APP_ID', 'demo-app'),
    apollo_url=os.getenv('APOLLO_URL', 'http://localhost:8080'),
    cluster=os.getenv('APOLLO_CLUSTER', 'default'),
    namespace=os.getenv('APOLLO_NAMESPACE', 'application')
)

# 配置变化回调函数
def on_config_change(configs):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 配置发生变化:")
    for key, value in configs.items():
        print(f"  {key}: {value}")

# 启动配置监听
apollo_client.watch_config(on_config_change, interval=10)

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Apollo配置中心演示",
        "timestamp": time.time(),
        "app_id": apollo_client.app_id
    }

@app.get("/config/{key}")
async def get_config(key: str):
    """获取指定配置项"""
    try:
        value = apollo_client.get_config(key)
        return {
            "key": key,
            "value": value,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取配置失败: {str(e)}")

@app.get("/configs")
async def get_all_configs():
    """获取所有配置"""
    try:
        configs = apollo_client.get_all_configs()
        return {
            "configs": configs,
            "count": len(configs),
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取所有配置失败: {str(e)}")

@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 尝试获取一个配置来检查连接
        apollo_client.get_config("test", "default")
        return {
            "status": "healthy",
            "apollo_connected": True,
            "timestamp": time.time()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "apollo_connected": False,
                "error": str(e),
                "timestamp": time.time()
            }
        )

@app.get("/info")
async def get_info():
    """获取应用信息"""
    return {
        "app_id": apollo_client.app_id,
        "cluster": apollo_client.cluster,
        "namespace": apollo_client.namespace,
        "apollo_url": apollo_client.apollo_url,
        "config_count": len(apollo_client.config_cache),
        "last_update": apollo_client.last_update_time
    }

if __name__ == "__main__":
    import uvicorn
    
    print("启动FastAPI + Apollo演示应用...")
    print(f"Apollo服务器: {apollo_client.apollo_url}")
    print(f"应用ID: {apollo_client.app_id}")
    print("访问 http://localhost:8000/docs 查看API文档")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)