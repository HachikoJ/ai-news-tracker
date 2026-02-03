#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI 新闻实时采集器
支持多平台：X/Twitter, arXiv, 官方博客, 新闻网站
"""

import os
import sys
import json
import time
import feedparser
import requests
from datetime import datetime, timedelta
from pathlib import Path

class AINewsCollector:
    """AI 新闻实时采集器"""
    
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.collected_news = []
        self.seen_urls = set()
        
    def load_config(self, config_path):
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def collect_all(self):
        """采集所有信息源"""
        print(f"[{datetime.now()}] 开始采集 AI 新闻...")
        
        # 采集 arXiv 论文
        print("→ 采集 arXiv...")
        self.collect_arxiv()
        
        # 采集官方博客（RSS）
        print("→ 采集官方博客...")
        self.collect_blogs()
        
        # 采集新闻网站
        print("→ 采集新闻网站...")
        self.collect_news_sites()
        
        # 采集 X/Twitter（如果有 API）
        print("→ 采集 X/Twitter...")
        self.collect_twitter()
        
        # 采集 Hacker News
        print("→ 采集 Hacker News...")
        self.collect_hackernews()
        
        print(f"✓ 采集完成，共收集 {len(self.collected_news)} 条新闻\n")
        
        return self.collected_news
    
    def collect_arxiv(self):
        """采集 arXiv AI 论文"""
        base_url = "http://export.arxiv.org/api/query?"
        
        categories = self.config.get('arxiv_categories', [
            'cs.AI',   # Artificial Intelligence
            'cs.CL',   # Computation and Language
            'cs.CV',   # Computer Vision
            'cs.LG',   # Machine Learning
            'cs.NE'    # Neural and Evolutionary Computing
        ])
        
        # 查询最近 24 小时的论文
        for cat in categories:
            try:
                # 构建查询：指定类别 + 最近时间
                query = f"cat:{cat}"
                
                params = {
                    'search_query': query,
                    'start': 0,
                    'max_results': 50,
                    'sortBy': 'submittedDate',
                    'sortOrder': 'descending'
                }
                
                response = requests.get(base_url, params=params, timeout=30)
                response.raise_for_status()
                
                feed = feedparser.parse(response.content)
                
                for entry in feed.entries:
                    # 检查是否在 1 小时内
                    published = datetime(*entry.published_parsed[:6])
                    if datetime.now() - published > timedelta(hours=1):
                        continue
                    
                    # 去重
                    if entry.link in self.seen_urls:
                        continue
                    
                    self.seen_urls.add(entry.link)
                    
                    self.collected_news.append({
                        'source': 'arXiv',
                        'category': cat,
                        'title': entry.title,
                        'url': entry.link,
                        'authors': [author.name for author in entry.authors],
                        'abstract': entry.summary,
                        'published': published.isoformat(),
                        'importance_score': 0  # 后续计算
                    })
                    
            except Exception as e:
                print(f"  ✗ arXiv {cat} 采集失败: {e}")
    
    def collect_blogs(self):
        """采集官方博客 RSS"""
        blogs = self.config.get('blogs', [])
        
        for blog in blogs:
            try:
                feed = feedparser.parse(blog['url'])
                
                for entry in feed.entries[:20]:  # 每个源最多 20 条
                    # 检查时效（1 小时内）
                    if hasattr(entry, 'published_parsed'):
                        published = datetime(*entry.published_parsed[:6])
                    else:
                        published = datetime.now() - timedelta(minutes=30)
                    
                    if datetime.now() - published > timedelta(hours=1):
                        continue
                    
                    # 去重
                    if entry.link in self.seen_urls:
                        continue
                    
                    self.seen_urls.add(entry.link)
                    
                    self.collected_news.append({
                        'source': blog['name'],
                        'title': entry.title,
                        'url': entry.link,
                        'summary': entry.get('summary', '')[:500],
                        'published': published.isoformat(),
                        'importance_score': 0
                    })
                    
            except Exception as e:
                print(f"  ✗ {blog['name']} 采集失败: {e}")
    
    def collect_news_sites(self):
        """采集新闻网站"""
        # 这里可以用爬虫或 API
        # 暂时跳过，需要定制化实现
        pass
    
    def collect_twitter(self):
        """采集 X/Twitter"""
        # 需要 Twitter API v2
        # 暂时跳过，需要 API 密钥
        pass
    
    def collect_hackernews(self):
        """采集 Hacker News AI 相关"""
        try:
            # 获取最新 stories
            api_url = "https://hacker-news.firebaseio.com/v0/newstories.json"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            
            story_ids = response.json()[:100]  # 最新 100 条
            
            for story_id in story_ids:
                try:
                    # 获取 story 详情
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_resp = requests.get(story_url, timeout=5)
                    story_resp.raise_for_status()
                    story = story_resp.json()
                    
                    # 检查时间（1 小时内）
                    if story.get('time'):
                        published = datetime.fromtimestamp(story['time'])
                        if datetime.now() - published > timedelta(hours=1):
                            continue
                    
                    # 检查是否是 AI 相关（标题或 URL）
                    title = story.get('title', '').lower()
                    url = story.get('url', '')
                    
                    ai_keywords = ['ai', 'machine learning', 'deep learning', 
                                  'neural network', 'gpt', 'llm', 'model',
                                  'openai', 'anthropic', 'google gemini']
                    
                    if not any(kw in title for kw in ai_keywords):
                        continue
                    
                    # 去重
                    if url in self.seen_urls:
                        continue
                    
                    self.seen_urls.add(url)
                    
                    self.collected_news.append({
                        'source': 'Hacker News',
                        'title': story.get('title'),
                        'url': url,
                        'score': story.get('score', 0),
                        'comments': story.get('descendants', 0),
                        'published': datetime.fromtimestamp(story['time']).isoformat(),
                        'importance_score': 0
                    })
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"  ✗ Hacker News 采集失败: {e}")
    
    def save_results(self, output_path):
        """保存采集结果"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'collected_at': datetime.now().isoformat(),
                'total': len(self.collected_news),
                'news': self.collected_news
            }, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 结果已保存到: {output_path}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI 新闻实时采集器')
    parser.add_argument('--config', default='config/sources.json',
                       help='配置文件路径')
    parser.add_argument('--output', default='data/news_raw.json',
                       help='输出文件路径')
    
    args = parser.parse_args()
    
    # 创建配置目录（如果不存在）
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    # 初始化采集器
    collector = AINewsCollector(args.config)
    
    # 采集所有源
    news = collector.collect_all()
    
    # 保存结果
    collector.save_results(args.output)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
