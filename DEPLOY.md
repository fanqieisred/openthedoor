部署 openthedoor 到 Vercel 的步骤：

1. 在浏览器完成授权：
   https://vercel.com/oauth/device?user_code=QVKQ-BMMT

2. 授权完成后，运行以下命令部署：
   cd /home/chen/openthedoor
   npx -p vercel@48.0.0 vercel --prod --yes

项目配置：
- Framework: Astro
- Build: astro build
- Output: dist/
- GitHub: fanqieisred/openthedoor
