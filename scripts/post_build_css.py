#!/usr/bin/env python3
"""Post-build CSS injection script.
Injects CSS directly into dist/posts/*/index.html files
to fix Astro prerender discarding <style> tags."""

import os
import re

dist_posts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dist', 'posts')

if not os.path.exists(dist_posts_dir):
    print("No posts directory found, skipping CSS injection")
    exit(0)

css = """
<style>
  article { line-height: 1.8; }
  article h1, article h2, article h3 { margin-top: 2em; margin-bottom: 1em; }
  article p { margin-bottom: 1.5em; }
  article ul, article ol { margin-bottom: 1.5em; padding-left: 1.5em; }
  article pre { background: #f5f5f5; padding: 1em; border-radius: 8px; overflow-x: auto; }
  article code { background: #f5f5f5; padding: 0.2em 0.4em; border-radius: 4px; }
  article blockquote { border-left: 4px solid #3b82f6; padding-left: 1em; margin: 1em 0; color: #666; }
  article table { width: 100%; border-collapse: collapse; margin: 1.5em 0; }
  article th, article td { border: 1px solid #e5e7eb; padding: 0.75em; text-align: left; }
  article th { background: #f9fafb; font-weight: 600; }
  .sidebar-nav a { display: block; padding: 0.5em 1em; border-radius: 6px; color: #374151; }
  .sidebar-nav a:hover { background: #f3f4f6; }
  .sidebar-nav a.active { background: #dbeafe; color: #1d4ed8; font-weight: 500; }
</style>
"""

count = 0
for root, dirs, files in os.walk(dist_posts_dir):
    for f in files:
        if f == 'index.html':
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            if '<style>' not in content and '</head>' in content:
                content = content.replace('</head>', css + '</head>')
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                count += 1

print(f"Injected CSS into {count} article files")
