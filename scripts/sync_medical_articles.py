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


def quote_yaml_value(val: str) -> str:
    """如果值包含冒号或特殊字符，加上引号"""
    if val and (':' in val or '"' in val or "'" in val or val.strip() == ''):
        escaped = val.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return val


def process_frontmatter(content: str) -> str:
    """修复 frontmatter 中的 YAML 问题"""
    if not content.startswith('---'):
        return content

    match = re.match(r'^(---\n)(.*?)(\n---\n)(.*)', content, re.DOTALL)
    if not match:
        return content

    header = match.group(1)
    fm_content = match.group(2)
    footer = match.group(3)
    body = match.group(4)

    fixed_lines = []
    for line in fm_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            fixed_lines.append(line)
            continue
        if ':' in line:
            key, _, val = line.partition(':')
            val = val.strip()
            if val:
                fixed_lines.append(f"{key}: {quote_yaml_value(val)}")
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return header + '\n'.join(fixed_lines) + footer + body


def process_article(filepath: Path, content_dir: Path):
    """处理单个文章文件"""
    content = filepath.read_text(encoding='utf-8')
    content = process_frontmatter(content)

    # 提取元数据
    fm_match = re.match(r'---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    fm = {}
    if fm_match:
        for line in fm_match.group(1).split('\n'):
            line = line.strip()
            if ':' in line:
                key, _, val = line.partition(':')
                val = val.strip().strip('"')
                fm[key.strip()] = val

    raw_category = fm.get('分类', '科研成果')
    category = CATEGORY_MAP.get(raw_category, 'medical-research')

    body = fm_match.group(2) if fm_match else content
    title = ''
    for line in body.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break
    if not title:
        title = filepath.stem

    date = fm.get('created', '') or fm.get('updated', '')

    # 生成 slug
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')

    num_match = re.match(r'^(\d+)-', filepath.stem)
    if num_match:
        slug = f"{num_match.group(1)}-{slug}"

    content_dir.mkdir(parents=True, exist_ok=True)
    output_path = content_dir / f"{slug}.md"
    output_path.write_text(content, encoding='utf-8')

    return {
        'slug': slug,
        'title': title,
        'category': category,
        'date': date,
        'raw_category': raw_category,
    }


def update_routes_js(articles: list, routes_file: Path, meta_file: Path):
    slugs = sorted([a['slug'] for a in articles])

    # 构建 meta JSON
    meta_json = {}
    for a in articles:
        meta_json[a['slug']] = {
            'title': a['title'],
            'tags': ['医疗AI', a['raw_category']],
            'date': a['date'],
            'emoji': EMOJIS.get(a['category'], '📄'),
            'color': COLORS.get(a['category'], 'blue'),
            'category': a['category'],
        }
    
    meta_file.write_text(json.dumps(meta_json, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # 构建 JS 数组 - 使用 JSON.stringify 确保正确转义
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
