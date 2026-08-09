# openthedoor 部署指南

## 快速部署
访问 https://vercel.com/new/import/fanqieisred/openthedoor 导入项目。

框架会自动识别为 Astro，点击 Deploy 即可。

## 自动部署
导入后，每次 `git push` 自动触发 Vercel 构建。

## 本地构建验证
```bash
cd /home/chen/openthedoor
npm run build
```

输出: 15 pages in ~500ms
