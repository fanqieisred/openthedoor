# OpenTheDoor 医疗AI博客 - 上线报告

## 项目概述
医疗AI领域的科研成果与发展前瞻博客网站

## 技术栈
- **框架**: Astro 4.x
- **样式**: Tailwind CSS
- **部署**: Vercel
- **内容源**: Obsidian 每日文章目录

## 已完成工作

### 1. 内容同步系统
- 脚本: `scripts/sync_medical_articles.py`
- 源目录: `/mnt/f/obsidian_hospital/hos_doc/每日文章/`
- 功能: 自动读取文章、提取分类、生成路由

### 2. 文章内容渲染
- 使用 `marked` 库将 Markdown 转换为 HTML
- 从源文件读取文章内容
- 保留原始格式（标题、列表、表格等）

### 3. 网站结构
```
/dist/
├── index.html           # 首页
├── about/index.html     # 关于页
├── categories/index.html          # 分类列表
├── categories/medical-research/   # 医疗科研 (6篇)
├── categories/medical-trends/     # 医疗前瞻 (1篇)
├── posts/00-每日文章汇总-2026-08-09/
├── posts/01-大语言模型.../
└── ... (共7篇文章)
```

### 4. 配置优化
- `vercel.json`: 自动构建配置
- `astro.config.mjs`: Astro + Tailwind 集成

## 构建验证
```
13 page(s) built in 517ms
```

## 文章内容验证 ✓
```html
<h2>研究背景</h2>
<p>随着ChatGPT等大语言模型在医疗咨询场景的普及...</p>
<h2>主要结果</h2>
<p><strong>高使用率、低信任度并存</strong>：超七成患者...</p>
```

## 部署状态
- GitHub: fanqieisred/openthedoor ✓
- 本地构建: 成功 ✓
- Vercel: 等待导入

## 下一步
1. 在 Vercel Dashboard 导入项目
   https://vercel.com/new/import/fanqieisred/openthedoor
2. 设置自定义域名 www.openthedoor.xin
3. 配置自动部署（每次 git push 触发）

## 使用方式
```bash
# 同步新文章
python3 scripts/sync_medical_articles.py

# 构建
npm run build

# 推送部署
git add -A && git commit -m "sync articles" && git push
```
