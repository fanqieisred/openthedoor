# OpenTheDoor 部署指南

## 当前状态
- ✅ GitHub 仓库：fanqieisred/openthedoor
- ✅ 本地构建：13 页面，544ms
- ✅ 文章内容：Markdown 渲染正常

## 部署步骤

### 1. 导入项目
访问：**https://vercel.com/new/import/fanqieisred/openthedoor**

### 2. 配置（自动识别）
- Framework: **Astro** ✓
- Build Command: `astro build`
- Output Directory: `dist`
- Install Command: `npm install`

### 3. 点击 Deploy
等待构建完成（约 1-2 分钟）

### 4. 绑定域名（可选）
在 Project Settings → Domains 添加：
- `www.openthedoor.xin`

### 5. 验证
访问：`https://openthedoor.vercel.app`

## 后续使用

```bash
# 1. 同步新文章
python3 scripts/sync_medical_articles.py

# 2. 构建验证
npm run build

# 3. 推送触发自动部署
git add -A
git commit -m "sync articles"
git push origin master
```

## 访问地址
- 预览：https://openthedoor.vercel.app
- 主域名：https://www.openthedoor.xin（已配置）
