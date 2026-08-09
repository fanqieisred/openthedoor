# OpenTheDoor 部署问题说明

## 问题原因
Vercel CLI 无法认证，无法链接到现有项目。

## 解决方案

### 方案 1：获取新的 Personal Access Token（推荐）
1. 访问 https://vercel.com/account/tokens
2. 点击 **Create Token**
3. 复制新生成的 Token
4. 运行以下命令：
   ```bash
   cd /home/chen/openthedoor
   npx vercel@48.0.0 login --token <YOUR_TOKEN>
   ```

### 方案 2：使用 Vercel Dashboard 直接部署
1. 访问 https://vercel.com/new/import/fanqieisred/openthedoor
2. 选择 **Import**
3. 框架会自动识别为 **Astro**
4. 点击 **Deploy**

### 方案 3：使用 GitHub Integration
1. 在 Vercel Dashboard 导入 GitHub 仓库
2. 启用自动部署
3. 每次 `git push` 自动触发构建

## 当前状态
- ✅ 代码已推送到 GitHub
- ✅ 本地构建成功（13 页面）
- ✅ 文章内容已渲染
- ⏳ Vercel 部署：需要认证
