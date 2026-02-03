#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI 新闻自动推送脚本
定期检查并推送重要新闻到用户会话
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def get_latest_news():
    """获取最新重要新闻"""

    data_file = Path("/root/.openclaw/workspace/skills/ai-news-tracker/data/news_scored.json")

    if not data_file.exists():
        return None

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        news_list = data.get('news', [])

        if not news_list:
            return None

        # 按重要性排序
        news_list.sort(key=lambda x: x.get('importance_score', 0), reverse=True)

        critical = [n for n in news_list if n.get('category') == '🔴 极重要']
        important = [n for n in news_list if n.get('category') == '🟡 重要']

        if not critical and not important:
            return None

        lines = []
        lines.append("🤖 **AI 新闻监控报告**")
        lines.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")

        if critical:
            lines.append(f"🚨 **发现 {len(critical)} 条极重要新闻！**\n")
            for i, news in enumerate(critical[:3], 1):
                lines.append(f"**{i}. {news.get('title')}**")
                lines.append(f"📍 {news.get('source')} | ⭐ {news.get('importance_score')}/20")
                lines.append(f"🔗 {news.get('url')}\n")

        if important:
            lines.append(f"📊 **发现 {len(important)} 条重要新闻**\n")
            for i, news in enumerate(important[:3], 1):
                lines.append(f"**{i}. {news.get('title')}**")
                lines.append(f"📍 {news.get('source')} | ⭐ {news.get('importance_score')}/20")
                if news.get('summary'):
                    summary = news.get('summary')[:80]
                    lines.append(f"📝 {summary}...")
                lines.append(f"🔗 {news.get('url')}\n")

        return "\n".join(lines)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

if __name__ == '__main__':
    message = get_latest_news()

    if message:
        print(message)
        sys.exit(0)
    else:
        print("✅ AI 新闻监控正常运行，暂无重要新闻")
        sys.exit(0)
