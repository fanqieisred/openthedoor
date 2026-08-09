#!/usr/bin/env python3
"""Regenerate routes.js from all .md files in posts directory."""

import os
import re

posts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'pages', 'posts')
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'lib', 'routes.js')

# Known title mappings
title_map = {
    'top-10-ai-tools-2026': '2026年最值得关注的10个AI工具',
    'ai-art-tools-comparison': 'AI绘画工具对比：Midjourney vs DALL-E vs Stable Diffusion',
    'openai-function-calling-guide': 'OpenAI Function Calling 完全指南',
    'openai-assistants-api-guide': 'OpenAI Assistants API 实战',
    'openai-structured-outputs-guide': 'OpenAI Structured Outputs',
    'openai-developing-hallucination-guardrails': 'OpenAI 幻觉防护',
    'openai-moderation-api-guide': 'OpenAI Moderation API 指南',
    'openai-guardrails-best-practices': 'Guardrails 最佳实践',
    'openai-function-calling-complete-guide': 'Function Calling 完整指南',
    'openai-assistants-overview': 'Assistants API 概览',
    'python-automation-beginner': 'Python自动化入门',
    'llm-lora-finetune-guide': '大模型微调指南：LoRA实战',
    'openai-function-calling-tutorial': '教程：Function Calling 智能工具调用',
    'openai-rag-tutorial': '教程：Embeddings 和 RAG 问答系统',
    'openai-fine-tuning-tutorial': '教程：OpenAI Fine-Tuning 定制模型',
    'openai-agents-orchestration-tutorial': '教程：OpenAI Agents 编排多Agent系统',
    'embedding-deployment-guide': 'Embedding 模型部署完全指南',
    'embedding-finetuning-guide': 'Embedding 模型微调',
    'embedding-evaluation-mteb': 'Embedding 模型评分：MTEB 基准测试',
    'embedding-rag-retrieval': 'Embedding 在 RAG 中的核心作用',
    'embedding-long-text-chunking': 'Embedding 长文本处理：分块策略',
    'embedding-cross-encoder-reranking': 'Embedding 进阶：交叉编码器重排序',
    'openai-customizing-embeddings': 'OpenAI 自定义 Embedding',
    'openai-entity-extraction-long-documents': 'OpenAI 长文档实体抽取',
    'openai-data-extraction-gpt4o': 'OpenAI GPT-4o 数据提取与转换',
    'openai-code-search-embeddings': 'OpenAI Embedding 代码语义搜索',
    'openai-rag-question-answering': 'RAG 问答系统',
    'openai-parse-pdf-rag': '从 PDF 文档提取数据用于 RAG',
    'openai-streaming-completions': '流式输出',
    'openai-tiktoken-guide': 'TikToken 使用指南',
    'openai-rate-limit-guide': '处理 API 速率限制',
    'openai-format-chat-inputs': 'Chat 模型输入格式',
    'openai-function-finetuning': 'Function Calling 微调指南',
    'openai-chat-finetuning-guide': 'Chat 模型微调完全指南',
    'openai-visualizing-embeddings': 'Embedding 可视化',
    'openai-embedding-long-inputs': '处理长输入 Embedding',
    'openai-user-product-embeddings': '用户和产品 Embedding',
    'openai-zero-shot-classification': '零样本分类',
    'openai-embedding-wikipedia': '维基百科文章 Embedding 搜索',
    'openai-get-embeddings-from-dataset': '批量生成 Embedding',
    'openai-embedding-semantic-search': '语义文本搜索',
    'openai-whisper-processing': 'Whisper 音频转录处理',
    'openai-summarizing-long-docs': '长文档摘要',
    'openai-named-entity-recognition': '命名实体识别',
    'ai-trends-2026': '2026年AI行业趋势预测',
    'openai-july-2026-updates': 'OpenAI 2026年7月重大更新',
    'ai-industry-july-2026-roundup': '2026年7月 AI 行业周报',
    'openai-optimizing-prompts-guide': '提示词优化指南',
    'openai-prompt-caching-101': '提示词缓存入门',
    'openai-function-calling-faq': 'Function Calling FAQ',
    'openai-rag-faq': 'RAG 技术 FAQ',
    'openai-multi-agent-faq': '多 Agent 系统 FAQ',
    'openai-logprobs-guide': '使用 LogProbs 评估置信度',
    'openai-seed-parameter': '使用 Seed 参数保证可复现性',
    'openai-batch-processing': '批处理 API',
    'openai-completions-usage': 'Completions API 使用量统计',
    'openai-unit-test-writing': '单元测试编写',
    'openai-reproducible-outputs': '可复现输出',
    'openai-api-key-security-1': 'OpenAI API进阶实战 - API Key安全管理与权限控制（一）',
    'weekly-ai-news-1': 'AI行业动态速递 - 本周AI重要新闻汇总（一）',
    'openai-production-client-1': 'OpenAI API进阶实战 - 构建生产级API客户端（一）',
    'llm-tuning-faq-1': 'AI技术问答精选 - 大模型调优常见问题（1）',
    'langchain-vs-llamaindex-1': 'AI开发工具评测 - LangChain vs LlamaIndex对比（1）',
    'embedding-faq-1': 'AI技术问答精选 - Embedding应用实战问答（1）',
    'langgraph-overview-tutorial': 'LangGraph 概述',
    'langgraph-quickstart-tutorial': 'LangGraph 快速开始',
    'langgraph-install-tutorial': 'LangGraph 安装配置',
    'langgraph-graph-api-tutorial': 'LangGraph 图 API',
    'langgraph-functional-api-tutorial': 'LangGraph 函数式 API',
    'langgraph-thinking-in-langgraph-tutorial': 'LangGraph 思维模式',
    'langgraph-checkpointers-tutorial': 'LangGraph 检查点机制',
    'langgraph-memory-tutorial': 'LangGraph 记忆系统',
    'langgraph-streaming-tutorial': 'LangGraph 流式处理',
    'langgraph-human-in-the-loop-tutorial': 'LangGraph 人机协作',
    'langgraph-interrupts-tutorial': 'LangGraph 中断机制',
    'langgraph-deploy-tutorial': 'LangGraph 部署指南',
    'langgraph-observability-tutorial': 'LangGraph 可观测性',
    'langgraph-agentic-rag-tutorial': 'LangGraph 智能 RAG',
    'langgraph-application-structure-tutorial': 'LangGraph 应用架构',
    'langgraph-pregel-tutorial': 'LangGraph Pregel 运行时',
    'langgraph-fault-tolerance-tutorial': 'LangGraph 容错机制',
    'langgraph-persistence-tutorial': 'LangGraph 持久化存储',
    'langgraph-stores-tutorial': 'LangGraph 存储系统',
    'ai-news-anthropics-landmark-15b-copyright-settlement-is-ap-1': 'Anthropic 里程碑式版权和解',
    'ai-news-trumps-latest-ai-czar-has-already-resigned-2': '特朗普最新 AI 特使已辞职',
    'ai-news-google-is-working-on-a-new-ai-chip-designed-to-mak-3': 'Google 研发新一代 AI 芯片',
    'ai-news-ais-most-important-protocol-is-getting-a-little-bi-4': 'AI 最重要协议迎来更新',
    'ai-news-x-relaunches-a-rebuilt-android-app-after-year-long-5': 'X 重新发布 Android 应用',
}

files = sorted([f[:-3] for f in os.listdir(posts_dir) if f.endswith('.md')])

def get_category(slug):
    if slug.startswith('langgraph-'): return 'tutorials'
    if slug.startswith('ai-news-'): return 'news'
    if slug.startswith('openai-') or slug.startswith('embedding-'): return 'tutorials'
    if 'faq' in slug: return 'qanda'
    if slug.startswith('top-') or slug.startswith('langchain-vs'): return 'ai-tools'
    if 'news' in slug or 'trend' in slug: return 'news'
    return 'tutorials'

def get_tags(slug):
    if slug.startswith('langgraph-'): return ['LangGraph', 'AI']
    if slug.startswith('ai-news-'): return ['AI', '科技动态']
    if slug.startswith('openai-'): return ['OpenAI', '教程']
    if slug.startswith('embedding-'): return ['Embedding', '教程']
    if slug.startswith('top-') or slug.startswith('langchain-vs'): return ['AI工具', '评测']
    if 'faq' in slug: return ['FAQ', '答疑']
    return ['AI', '技术']

def get_emoji(slug):
    if slug.startswith('langgraph-'): return '🔗'
    if slug.startswith('ai-news-'): return '📰'
    if slug.startswith('top-'): return '🤖'
    if 'faq' in slug: return '💡'
    if 'news' in slug or 'trend' in slug: return '📰'
    return '📚'

colors = {'ai-tools': 'blue', 'tutorials': 'green', 'news': 'purple', 'qanda': 'orange'}
meta_lines = []
for slug in files:
    title = title_map.get(slug, slug.replace('-', ' ').title())
    cat = get_category(slug)
    meta_lines.append(f"  '{slug}': {{ title: '{title}', tags: {get_tags(slug)}, date: '2026-07-21', emoji: '{get_emoji(slug)}', color: '{colors[cat]}', category: '{cat}' }}")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("export const allSlugs = [\n")
    for i in range(0, len(files), 10):
        f.write("  " + ", ".join(f"'{s}'" for s in files[i:i+10]) + ",\n")
    f.write("];\n\n")
    f.write("export const articleMeta = {\n")
    for line in meta_lines:
        f.write(line + ",\n")
    f.write("};\n\n")
    f.write("export const categoryMap = { 'ai-tools': 'AI 工具', 'tutorials': '技术教程', 'news': '行业资讯', 'qanda': '问答合集' };\n\n")
    f.write("export const colorMap = {\n  blue: 'from-blue-600 to-purple-600',\n  green: 'from-green-600 to-teal-600',\n  orange: 'from-orange-500 to-red-500',\n  pink: 'from-pink-500 to-rose-500',\n  indigo: 'from-indigo-600 to-blue-700',\n  purple: 'from-purple-500 to-pink-600'\n};\n\n")
    f.write("export const tagBgMap = {\n  blue: 'bg-blue-100 text-blue-700',\n  green: 'bg-green-100 text-green-700',\n  orange: 'bg-orange-100 text-orange-700',\n  pink: 'bg-pink-100 text-pink-700',\n  indigo: 'bg-indigo-100 text-indigo-700',\n  purple: 'bg-purple-100 text-purple-700'\n};\n")

print(f"Generated routes.js with {len(files)} slugs")
