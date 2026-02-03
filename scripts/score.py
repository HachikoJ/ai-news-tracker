#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI 新闻智能过滤和评分系统
多维度评估新闻重要性
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


class AINewsScorer:
    """AI 新闻评分器"""
    
    # 极重要关键词
    BREAKTHROUGH_KEYWORDS = [
        'GPT-5', 'Claude-4', 'Gemini 2', 'DeepSeek',
        'AGI', 'artificial general intelligence',
        'breakthrough', 'revolutionary', 'groundbreaking',
        'state-of-the-art', 'SOTA',
        'human-level', 'superhuman'
    ]
    
    # 大模型发布关键词
    MODEL_KEYWORDS = [
        'new model', 'model release', 'launch',
        'parameter', 'billion', 'trillion',
        'open source', 'closed source'
    ]
    
    # 研究突破关键词
    RESEARCH_KEYWORDS = [
        'paper', 'research', 'arxiv',
        'architecture', 'algorithm',
        'novel', 'innovative'
    ]
    
    # 可信来源（加分）
    TRUSTED_SOURCES = [
        'openai.com', 'anthropic.com', 'deepmind.google',
        'arxiv.org', 'nature.com', 'science.org',
        'mit.edu', 'stanford.edu'
    ]
    
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
    
    def load_config(self, config_path):
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def score_news(self, news_item):
        """单条新闻评分"""
        score = 0
        details = {}
        
        title = news_item.get('title', '').lower()
        summary = news_item.get('summary', '')[:500].lower()
        url = news_item.get('url', '')
        source = news_item.get('source', '')
        combined_text = f"{title} {summary}"
        
        # 1. 技术创新性 (0-5分，权重2x)
        innovation = self.score_innovation(combined_text, news_item)
        score += innovation * 2
        details['innovation'] = innovation
        
        # 2. 行业影响力 (0-5分，权重1.5x)
        impact = self.score_impact(combined_text, news_item)
        score += impact * 1.5
        details['impact'] = impact
        
        # 3. 可验证性 (0-5分，权重1x)
        verifiability = self.score_verifiability(news_item)
        score += verifiability
        details['verifiability'] = verifiability
        
        # 4. 关注度 (0-5分，权重1x)
        attention = self.score_attention(news_item)
        score += attention
        details['attention'] = attention
        
        # 5. 时效性 (0-5分，权重0.5x)
        timeliness = self.score_timeliness(news_item)
        score += timeliness * 0.5
        details['timeliness'] = timeliness
        
        return round(score, 2), details
    
    def score_innovation(self, text, news_item):
        """评分：技术创新性"""
        score = 0
        
        # 跨时代突破 (5分)
        for kw in self.BREAKTHROUGH_KEYWORDS:
            if kw.lower() in text:
                return 5
        
        # 大模型发布 (4分)
        for kw in self.MODEL_KEYWORDS:
            if kw in text:
                score = 4
                break
        
        # 研究突破 (3分)
        for kw in self.RESEARCH_KEYWORDS:
            if kw in text:
                score = max(score, 3)
                break
        
        # arXiv 论文 (基础2分)
        if news_item.get('source') == 'arXiv':
            score = max(score, 2)
        
        return min(score, 5)
    
    def score_impact(self, text, news_item):
        """评分：行业影响力"""
        score = 0
        
        # 开源突破 (5分)
        if any(kw in text for kw in ['open source', '开源', 'weights released']):
            score = 5
        
        # 性能数量级提升 (4分)
        elif any(kw in text for kw in ['10x', '100x', 'order of magnitude']):
            score = 4
        
        # 新能力涌现 (3分)
        elif any(kw in text for kw in ['emergent', 'new capability', 'first']):
            score = 3
        
        # 普通改进 (2分)
        elif any(kw in text for kw in ['improve', 'better', 'faster']):
            score = 2
        
        return min(score, 5)
    
    def score_verifiability(self, news_item):
        """评分：可验证性"""
        score = 0
        
        url = news_item.get('url', '')
        source = news_item.get('source', '')
        
        # 官方来源 (5分)
        for trusted in self.TRUSTED_SOURCES:
            if trusted in url or trusted == source:
                score = 5
                break
        
        # arXiv 论文 (5分)
        elif source == 'arXiv':
            score = 5
        
        # 有代码仓库 (4分)
        elif any(kw in url for kw in ['github.com', 'huggingface.co']):
            score = 4
        
        # 有详细报告 (3分)
        elif news_item.get('summary'):
            score = 3
        
        # 仅宣传 (1分)
        else:
            score = 1
        
        return score
    
    def score_attention(self, news_item):
        """评分：关注度"""
        score = 0
        
        # Hacker News 评分
        if news_item.get('source') == 'Hacker News':
            hn_score = news_item.get('score', 0)
            comments = news_item.get('comments', 0)
            
            if hn_score > 500 or comments > 200:
                score = 5
            elif hn_score > 200 or comments > 100:
                score = 4
            elif hn_score > 100 or comments > 50:
                score = 3
            elif hn_score > 50 or comments > 20:
                score = 2
            else:
                score = 1
        
        # 社区热议（模拟）
        # 这里可以接入真实的社交数据
        else:
            # 默认中等分数
            score = 2
        
        return score
    
    def score_timeliness(self, news_item):
        """评分：时效性"""
        published = news_item.get('published')
        
        if not published:
            return 1
        
        try:
            pub_time = datetime.fromisoformat(published.replace('Z', '+00:00'))
            age = datetime.now(pub_time.tzinfo) - pub_time
            
            if age < timedelta(minutes=30):
                return 5
            elif age < timedelta(hours=1):
                return 4
            elif age < timedelta(hours=6):
                return 3
            elif age < timedelta(hours=24):
                return 2
            else:
                return 1
        except:
            return 1
    
    def classify_news(self, score, news_item):
        """分类新闻"""
        if score >= 15:
            return '🔴 极重要'
        elif score >= 10:
            return '🟡 重要'
        else:
            return '🟢 一般'
    
    def filter_and_score(self, input_path, output_path, threshold=10):
        """过滤并评分所有新闻"""
        print(f"[{datetime.now()}] 开始评分和过滤...")
        
        # 加载原始新闻
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        news_list = data.get('news', [])
        
        filtered_news = []
        
        for news_item in news_list:
            # 评分
            score, details = self.score_news(news_item)
            news_item['importance_score'] = score
            news_item['score_details'] = details
            
            # 分类
            news_item['category'] = self.classify_news(score, news_item)
            
            # 过滤
            if score >= threshold:
                filtered_news.append(news_item)
        
        # 按分数排序
        filtered_news.sort(key=lambda x: x['importance_score'], reverse=True)
        
        # 保存结果
        result = {
            'processed_at': datetime.now().isoformat(),
            'threshold': threshold,
            'total_raw': len(news_list),
            'total_filtered': len(filtered_news),
            'news': filtered_news
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 过滤完成：{len(news_list)} → {len(filtered_news)}")
        print(f"  🔴 极重要: {len([n for n in filtered_news if n['category'] == '🔴 极重要'])}")
        print(f"  🟡 重要: {len([n for n in filtered_news if n['category'] == '🟡 重要'])}")
        print(f"✓ 结果已保存到: {output_path}\n")
        
        return filtered_news


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI 新闻评分和过滤')
    parser.add_argument('--input', default='data/news_raw.json',
                       help='原始新闻文件')
    parser.add_argument('--output', default='data/news_scored.json',
                       help='评分后文件')
    parser.add_argument('--config', default='config/sources.json',
                       help='配置文件')
    parser.add_argument('--threshold', type=int, default=10,
                       help='重要性阈值 (默认: 10)')
    
    args = parser.parse_args()
    
    # 创建输出目录
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    # 初始化评分器
    scorer = AINewsScorer(args.config)
    
    # 过滤和评分
    news = scorer.filter_and_score(args.input, args.output, args.threshold)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
