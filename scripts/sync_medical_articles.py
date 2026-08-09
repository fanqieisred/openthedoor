#!/usr/bin/env python3
"""从 Obsidian 每日文章目录生成网站 posts 和 routes.js"""

import os
import re
from pathlib import Path
import json

SOURCE_DIR = Path("/mnt/f/obsidian_hospital/hos_doc/每日文章")
CONTENT_DIR = Path("/home/chen/openthedoor/src/content/posts")
ROUTES_FILE = Path("/home/chen/openthedoor/src/lib/routes.js")
META_FILE = Path("/home/chen/openthedoor/src/lib/articles_meta.json")

# 分类映射
CATEGORY_MAP = {
    '科研成果': 'medical-research',
    '发展前瞻': 'medical-trends',
    '行业洞察': 'medical-insights',
    '技术解析': 'medical-tech',
}

CATEGORY_DISPLAY = {
    'medical-research': '医疗科研',
    'medical-trends': '医疗前瞻',
    'medical-insights': '行业洞察',
    'medical-tech': '技术解析',
}

COLORS = {
    'medical-research': 'blue',
    'medical-trends': 'purple',
    'medical-insights': 'green',
    'medical-tech': 'orange',
}

EMOJIS = {
    'medical-research': '🔬',
    'medical-trends': '🔮',
    'medical-insights': '💡',
    'medical-tech': '⚙️',
}


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """提取 frontmatter 和正文"""
    match = re.match(r'---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return {}, content
    
    fm = {}
    lines = match.group(1).split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip().strip('"')
            
            # 检查是否是列表
            if val == '' and i + 1 < len(lines) and lines[i + 1].strip().startswith('-'):
                # 列表形式
                items = []
                while i + 1 < len(lines) and lines[i + 1].strip().startswith('-'):
                    item = lines[i + 1].strip()[1:].strip().strip('"')
                    if item:
                        items.append(item)
                    i += 1
                fm[key] = items
            else:
                fm[key] = val
        i += 1
    
    return fm, match.group(2)


def process_article(filepath: Path, content_dir: Path):
    """处理单个文章文件"""
    content = filepath.read_text(encoding='utf-8')
    
    fm, body = extract_frontmatter(content)
    
    # 提取标题（第一个 H1）
    title = ''
    for line in body.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break
    if not title:
        title = filepath.stem
    
    # 提取日期
    date = fm.get('created', '') or fm.get('updated', '') or '2026-08-09'
    
    # 提取分类
    raw_category = fm.get('分类', '科研成果')
    category = CATEGORY_MAP.get(raw_category, 'medical-research')
    
    # 提取标签
    tags = fm.get('tags', [])
    if not tags:
        tags = ['医疗AI', raw_category]
    # 清理标签
    tags = [t.strip() for t in tags if t.strip()]
    if not tags:
        tags = ['医疗AI', raw_category]
    
    # 生成 slug
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    
    num_match = re.match(r'^(\d+)-', filepath.stem)
    if num_match:
        slug = f"{num_match.group(1)}-{slug}"
    
    # 构建新的 frontmatter
    new_fm = f"""---
title: {title}
date: {date}
tags:
  - {'\n  - '.join(tags)}
category: {category}
emoji: {EMOJIS.get(category, '📄')}
---"""
    
    # 写入新 frontmatter
    new_content = new_fm + '\n\n' + body
    
    # 保存文件
    content_dir.mkdir(parents=True, exist_ok=True)
    output_path = content_dir / f"{slug}.md"
    output_path.write_text(new_content, encoding='utf-8')
    
    return {
        'slug': slug,
        'title': title,
        'category': category,
        'date': date,
        'raw_category': raw_category,
        'tags': tags,
    }


def update_routes_js(articles: list, routes_file: Path, meta_file: Path):
    slugs = sorted([a['slug'] for a in articles])
    
    # 构建 meta JSON
    meta_json = {}
    for a in articles:
        meta_json[a['slug']] = {
            'title': a['title'],
            'tags': a['tags'],
            'date': a['date'],
            'emoji': EMOJIS.get(a['category'], '📄'),
            'color': COLORS.get(a['category'], 'blue'),
            'category': a['category'],
        }
    
    meta_file.write_text(json.dumps(meta_json, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # 构建 JS 数组
    slugs_json = json.dumps(slugs, ensure_ascii=False)
    
    meta_lines = []
    for slug in slugs:
        a = next(x for x in articles if x['slug'] == slug)
        meta_lines.append(f'  "{a["slug"]}": {json.dumps(meta_json[slug], ensure_ascii=False)}')
    
    meta_json_str = '{\n' + ',\n'.join(meta_lines) + '\n}'
    
    category_entries = []
    for cat, display in CATEGORY_DISPLAY.items():
        category_entries.append(f'  "{cat}": "{display}"')
    
    categories_json = '{\n' + ',\n'.join(category_entries) + '\n}'
    
    content = f"""export const allSlugs = {slugs_json};

export const articleMeta = {meta_json_str};

export const categoryMap = {categories_json};

export const colorMap = {{
  blue: 'from-blue-600 to-purple-600',
  green: 'from-green-600 to-teal-600',
  orange: 'from-orange-500 to-red-500',
  pink: 'from-pink-500 to-rose-500',
  indigo: 'from-indigo-600 to-blue-700',
  purple: 'from-purple-500 to-pink-600'
}};

export const tagBgMap = {{
  blue: 'bg-blue-100 text-blue-700',
  green: 'bg-green-100 text-green-700',
  orange: 'bg-orange-100 text-orange-700',
  pink: 'bg-pink-100 text-pink-700',
  indigo: 'bg-indigo-100 text-indigo-700',
  purple: 'bg-purple-100 text-purple-700'
}};
"""
    routes_file.write_text(content, encoding='utf-8')
    
    return len(slugs)


def main():
    md_files = []
    for date_dir in sorted(SOURCE_DIR.iterdir()):
        if date_dir.is_dir() and date_dir.name.startswith('20'):
            for f in sorted(date_dir.glob('*.md')):
                if f.name != 'README.md':
                    md_files.append(f)
    
    print(f"找到 {len(md_files)} 篇文章")
    
    articles = []
    for f in md_files:
        result = process_article(f, CONTENT_DIR)
        articles.append(result)
        print(f"  ✓ {result['title'][:40]}... -> /posts/{result['slug']}")
    
    count = update_routes_js(articles, ROUTES_FILE, META_FILE)
    print(f"\n已更新 routes.js 和 articles_meta.json，共 {count} 篇文章")
    
    from collections import Counter
    cat_counts = Counter(a['category'] for a in articles)
    print("\n分类统计:")
    for cat, count in cat_counts.items():
        display = CATEGORY_DISPLAY.get(cat, cat)
        print(f"  {display}: {count} 篇")


if __name__ == '__main__':
    main()
