# openthedoor Vercel 部署流程

## 配置状态
- GitHub 仓库：fanqieisred/openthedoor ✓
- 框架：Astro ✓
- 构建命令：astro build ✓
- 输出目录：dist/ ✓
- Vercel 配置：vercel.json ✓

## 手动部署步骤

### 方法一：Vercel Dashboard（推荐）
1. 访问 https://vercel.com/new
2. 导入 `fanqieisred/openthedoor` 仓库
3. 框架选 Astro（自动识别）
4. 点击 Deploy
5. 等待构建完成（约 1-2 分钟）

### 方法二：获取有效 Token
1. 访问 https://vercel.com/dashboard/tokens
2. 点击 Create Token
3. Token 名称：hermes-deploy
4. 类型：Personal
5. 复制 Token 给我

### 方法三：浏览器登录（无需 Token）
运行以下命令，在浏览器完成授权：
```bash
cd /home/chen/openthedoor
npx vercel login
```

## 推送后自动部署
绑定 GitHub 仓库后，每次 `git push` 会自动触发 Vercel 构建。

## 当前状态
- 构建：✓ 成功 (15 pages, 512ms)
- Git：✓ 已推送
- Vercel：⏳ 等待授权
