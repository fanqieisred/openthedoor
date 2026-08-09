# openthedoor 部署指南

## 当前状态
- ✓ 代码已推送到 GitHub：fanqieisred/openthedoor
- ✓ 构建配置：vercel.json (Astro)
- ✓ 本地构建：成功 (15 pages, 515ms)
- ⏳ Vercel 部署：需要导入新项目

## 为什么旧 URL 不正确？
`openthedoor.vercel.app` 已绑定到旧项目（Library Website）。
需要在新项目中使用此 URL。

## 步骤：导入新项目

### 1. 访问导入页面
https://vercel.com/new/import/fanqieisred/openthedoor

### 2. 配置项目
| 设置项 | 值 |
|--------|-----|
| Framework Preset | **Astro** |
| Build Command | `astro build` |
| Output Directory | `dist` |
| Install Command | `npm install` |

### 3. 完成部署
点击 **Deploy**，等待 1-2 分钟构建完成。

### 4. 绑定域名（可选）
进入项目 → Settings → Domains → 添加 `www.openthedoor.xin`

## 后续自动部署
绑定 GitHub 仓库后，每次 `git push` 会自动触发构建。

## 本地验证
```bash
cd /home/chen/openthedoor
npm run build
npx astro dev  # 本地预览
```
