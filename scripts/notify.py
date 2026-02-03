#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI 新闻实时推送脚本
将重要新闻推送到 OpenClaw 会话
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def load_news(file_path):
    """加载评分后的新闻"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('news', [])

def format_news_message(news_list):
    """格式化新闻消息"""
    if not news_list:
        return None

    # 按重要性排序
    news_list.sort(key=lambda x: x.get('importance_score', 0), reverse=True)

    lines = []
    lines.append("🤖 **AI 新闻监控报告**")
    lines.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"📊 发现 {len(news_list)} 条重要新闻\n")

    # 极重要新闻
    critical = [n for n in news_list if n.get('category') == '🔴 极重要']
    important = [n for n in news_list if n.get('category') == '🟡 重要']

    if critical:
        lines.append("## 🔴 极重要新闻")
        for i, news in enumerate(critical, 1):
            lines.append(f"\n{i}. **{news.get('title')}**")
            lines.append(f"   📍 来源: {news.get('source')}")
            lines.append(f"   ⭐ 评分: {news.get('importance_score')}/20")
            lines.append(f"   🔗 {news.get('url')}")

    if important:
        lines.append("\n## 🟡 重要新闻")
        for i, news in enumerate(important, 1):
            lines.append(f"\n{i}. **{news.get('title')}**")
            lines.append(f"   📍 来源: {news.get('source')}")
            lines.append(f"   ⭐ 评分: {news.get('importance_score')}/20")
            if news.get('summary'):
                summary = news.get('summary')[:100]
                lines.append(f"   📝 {summary}...")
            lines.append(f"   🔗 {news.get('url')}")

    return "\n".join(lines)

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='AI 新闻推送')
    parser.add_argument('--input', default='data/news_scored.json',
                       help='评分后的新闻文件')
    parser.add_argument('--output', default='logs/news_message.txt',
                       help='输出的消息文件')

    args = parser.parse_args()

    # 加载新闻
    news_list = load_news(args.input)

    if not news_list:
        print("✓ 无需推送的新闻")
        return 0

    # 格式化消息
    message = format_news_message(news_list)

    if not message:
        print("✓ 无需推送的新闻")
        return 0

    # 保存消息
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(message)

    print(f"✓ 消息已保存到: {output_path}")
    print(f"\n{message}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
