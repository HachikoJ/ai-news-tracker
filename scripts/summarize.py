#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI 新闻摘要生成器
使用模板生成可读性强的新闻摘要
"""

import json
import sys
from datetime import datetime
from pathlib import Path


class AINewsSummarizer:
    """AI 新闻摘要生成器"""
    
    def __init__(self):
        pass
    
    def summarize_single(self, news_item):
        """生成单条新闻摘要"""
        title = news_item.get('title', '')
        url = news_item.get('url', '')
        source = news_item.get('source', '')
        score = news_item.get('importance_score', 0)
        category = news_item.get('category', '')
        
        # 生成摘要
        summary_parts = []
        
        # 标题
        summary_parts.append(f"【{category}】{title}")
        
        # 来源
        summary_parts.append(f"📍 来源：{source}")
        
        # 重要性
        summary_parts.append(f"⭐ 评分：{score}/20")
        
        # 链接
        summary_parts.append(f"🔗 链接：{url}")
        
        # 额外信息
        if news_item.get('authors'):
            authors = ', '.join(news_item['authors'][:3])
            if len(news_item['authors']) > 3:
                authors += f" 等{len(news_item['authors'])}人"
            summary_parts.append(f"👤 作者：{authors}")
        
        if news_item.get('abstract'):
            abstract = news_item['abstract'][:200]
            if len(news_item['abstract']) > 200:
                abstract += "..."
            summary_parts.append(f"📝 摘要：{abstract}")
        
        return '\n'.join(summary_parts)
    
    def generate_digest(self, news_list, title="AI 新闻速递"):
        """生成新闻汇总"""
        if not news_list:
            return f"# {title}\n\n暂无重要新闻。\n"
        
        digest = f"# {title}\n"
        digest += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        digest += f"📊 共 {len(news_list)} 条重要新闻\n\n"
        
        # 极重要新闻
        critical_news = [n for n in news_list if n['category'] == '🔴 极重要']
        if critical_news:
            digest += "## 🔴 极重要新闻\n\n"
            for news in critical_news:
                digest += self.summarize_single(news)
                digest += "\n\n---\n\n"
        
        # 重要新闻
        important_news = [n for n in news_list if n['category'] == '🟡 重要']
        if important_news:
            digest += "## 🟡 重要新闻\n\n"
            for news in important_news[:10]:  # 最多10条
                digest += self.summarize_single(news)
                digest += "\n\n"
        
        return digest
    
    def generate_notification(self, news_item):
        """生成推送通知（适合 IM/邮件）"""
        title = news_item.get('title', '')
        url = news_item.get('url', '')
        category = news_item.get('category', '')
        score = news_item.get('importance_score', 0)
        
        # 简短通知
        notification = f"{category} | 评分: {score}\n"
        notification += f"{title}\n"
        notification += f"{url}"
        
        return notification


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI 新闻摘要生成')
    parser.add_argument('--input', default='data/news_scored.json',
                       help='评分后的新闻文件')
    parser.add_argument('--output', default='data/news_digest.md',
                       help='输出摘要文件')
    parser.add_argument('--format', default='digest',
                       choices=['digest', 'single'],
                       help='输出格式')
    
    args = parser.parse_args()
    
    # 创建输出目录
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    # 加载新闻
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    news_list = data.get('news', [])
    
    # 生成摘要
    summarizer = AINewsSummarizer()
    
    if args.format == 'digest':
        content = summarizer.generate_digest(news_list)
    else:
        content = ''
        for news in news_list:
            content += summarizer.summarize_single(news)
            content += "\n\n---\n\n"
    
    # 保存
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 摘要已保存到: {args.output}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
