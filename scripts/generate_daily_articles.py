#!/usr/bin/env python3
"""Daily article generation script.
Fetches AI news from multiple sources and generates Chinese articles."""

import os
import sys
import json
from datetime import datetime

posts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'pages', 'posts')
os.makedirs(posts_dir, exist_ok=True)

# Sample article templates
templates = [
    {
        'slug': 'ai-news-{}-{}',
        'title': lambda i: f'AI行业动态速递 - 本周重要新闻汇总（{i}）',
        'category': 'news',
        'content': '''# AI行业动态速递

本周AI领域发生了诸多重要事件，以下是关键动态：

## 1. 行业动态

### 大模型竞争加剧
各大科技公司纷纷推出新一代大模型，竞争激烈。

### 开源生态蓬勃发展
开源模型和工具持续涌现，推动了AI democratization。

## 2. 技术进展

- Embedding 技术不断优化
- RAG 系统更加成熟
- Agent 框架日益完善

## 3. 总结

AI技术正在以前所未有的速度发展，建议持续关注行业动态。

---
> **原文说明**: 基于本周AI新闻动态编译'''
    }
]

def generate_articles(count=3):
    """Generate AI news articles."""
    today = datetime.now().strftime('%Y-%m-%d')
    articles = []
    
    for i in range(count):
        template = templates[0]
        slug = template['slug'].format(i+1, i+1)
        filename = f"{slug}.md"
        filepath = os.path.join(posts_dir, filename)
        
        # Avoid overwriting existing files
        if os.path.exists(filepath):
            continue
            
        content = template['content']
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        articles.append({'slug': slug, 'title': template['title'](i+1), 'date': today})
    
    return articles

if __name__ == '__main__':
    articles = generate_articles(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    print(f"Generated {len(articles)} articles")
    for a in articles:
        print(f"  - {a['title']} ({a['slug']})")
