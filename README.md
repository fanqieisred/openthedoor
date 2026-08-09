# OpenTheDoor - 医疗AI博客

从 Obsidian 每日文章目录同步文章到网站。

## 使用方法

```bash
# 同步文章
python3 scripts/sync_medical_articles.py

# 构建
npx astro build

# 本地预览
npx astro dev
```

## 目录结构

- 源文件：`/mnt/f/obsidian_hospital/hos_doc/每日文章/`
- 输出：`/home/chen/openthedoor/src/content/posts/`
- 路由：`/home/chen/openthedoor/src/lib/routes.js`

## 分类

| 分类 | 代码 |
|------|------|
| 医疗科研 | medical-research |
| 医疗前瞻 | medical-trends |
| 行业洞察 | medical-insights |
| 技术解析 | medical-tech |
