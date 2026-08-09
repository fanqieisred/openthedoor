# openthedoor 自动部署配置

## 已配置
- `vercel.json` - 构建配置
- GitHub 仓库已推送所有代码

## 完成自动部署的步骤

1. 访问 https://vercel.com/new/import/fanqieisred/openthedoor
2. 点击 **Import**
3. 框架会自动识别为 **Astro**
4. 点击 **Deploy**
5. 等待构建完成

之后每次 `git push` 会自动触发 Vercel 重新构建部署。

## 手动验证构建
```bash
cd /home/chen/openthedoor
npm run build
```

## 访问地址
- 预览：https://openthedoor.vercel.app
- 域名：https://www.openthedoor.xin（已配置）
