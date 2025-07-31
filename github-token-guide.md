# 🔑 GitHub Personal Access Token 详细指南

## 📱 手机端生成步骤

### 第一步：访问GitHub设置
1. 手机浏览器打开：https://github.com/settings/tokens
2. 登录你的GitHub账号

### 第二步：创建新token
1. 点击 "Generate new token" 
2. 选择 "Generate new token (classic)"

### 第三步：配置token
```
Note (备注): Flask-React-Fullstack-Project
Expiration (过期): 30 days

Select scopes (权限选择):
✅ repo                    # 完整仓库权限
  ✅ repo:status           # 仓库状态
  ✅ repo_deployment       # 部署权限  
  ✅ public_repo           # 公开仓库
  ✅ repo:invite          # 邀请权限
  ✅ security_events       # 安全事件

可选权限:
□ workflow               # GitHub Actions (如需要)
□ write:packages         # 包发布 (如需要)
```

### 第四步：生成并保存
1. 滚动到底部，点击 "Generate token"
2. **立即复制token** (格式: ghp_xxxxxxxxxxxxxxxxx)
3. ⚠️ **警告**: Token只显示一次，必须立即保存！

## 🚀 使用Token推送代码

### 方法1: 直接在URL中使用
```bash
cd /workspace/fullstack-app
git remote set-url origin https://YOUR_TOKEN@github.com/Yanyu779/flask-react-fullstack.git
git push -u origin main
```

### 方法2: 使用用户名和token
```bash
git remote set-url origin https://Yanyu779:YOUR_TOKEN@github.com/Yanyu779/flask-react-fullstack.git
git push -u origin main
```

## 🔒 Token安全提示

1. **保存位置**: 保存在安全的地方（密码管理器）
2. **权限最小化**: 只勾选必要权限
3. **定期更新**: 建议30-90天更新一次
4. **不要分享**: 绝不要在代码或公开场所分享token

## 📋 常见问题

**Q: Token在哪里显示？**
A: 生成后立即显示，只显示一次

**Q: 忘记复制怎么办？**  
A: 只能删除重新生成

**Q: Token格式是什么？**
A: 以 `ghp_` 开头，后跟40个字符

**Q: 权限选择错了怎么办？**
A: 可以编辑已有token或重新生成

## 🎯 快速链接

- 生成token: https://github.com/settings/tokens/new
- 管理tokens: https://github.com/settings/tokens
- GitHub文档: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token