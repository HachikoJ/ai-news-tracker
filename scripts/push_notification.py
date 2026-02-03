#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
推送重要新闻到当前会话
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def check_and_push_news():
    """检查并推送重要新闻"""
    
    data_file = Path("/root/.openclaw/workspace/skills/ai-news-tracker/data/news_scored.json")
    
    if not data_file.exists():
        return None
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    news_list = data.get('news', [])
    
    if not news_list:
        return "✅ 监控运行正常，暂无重要新闻"
    
    # 按重要性排序
    news_list.sort(key=lambda x: x.get('importance_score', 0), reverse=True)
    
    critical = [n for n in news_list if n.get('category') == '🔴 极重要']
    important = [n for n in news_list if n.get('category') == '🟡 重要']
    
    if not critical and not important:
        return "✅ 监控运行正常，暂无重要新闻"
    
    lines = []
    lines.append("🤖 **AI 新闻监控报告**")
    lines.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    
    if critical:
        lines.append(f"🚨 **发现 {len(critical)} 条极重要新闻！**\n")
        for i, news in enumerate(critical, 1):
            lines.append(f"**{i}. {news.get('title')}**")
            lines.append(f"📍 {news.get('source')} | ⭐ {news.get('importance_score')}/20")
            lines.append(f"🔗 {news.get('url')}\n")
    
    if important:
        lines.append(f"📊 **发现 {len(important)} 条重要新闻**\n")
        for i, news in enumerate(important[:3], 1):
            lines.append(f"**{i}. {news.get('title')}**")
            lines.append(f"📍 {news.get('source')} | ⭐ {news.get('importance_score')}/20")
            lines.append(f"🔗 {news.get('url')}\n")
    
    return "\n".join(lines)

if __name__ == '__main__':
    message = check_and_push_news()
    if message and not message.startswith("✅"):
        print(message)
        sys.exit(0)
    else:
        # 无重要新闻时静默
        sys.exit(0)
