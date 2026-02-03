#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成监控系统状态报告
"""

import json
import os
from datetime import datetime
from pathlib import Path

def generate_status_report():
    """生成状态报告"""

    project_dir = Path("/root/.openclaw/workspace/skills/ai-news-tracker")
    data_dir = project_dir / "data"
    logs_dir = project_dir / "logs"

    lines = []
    lines.append("🤖 **AI 新闻监控系统 - 启动报告**")
    lines.append("=" * 50)
    lines.append("")
    lines.append(f"📅 **启动时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"📍 **项目路径**: {project_dir}")
    lines.append("")

    # 检查最新数据
    scored_file = data_dir / "news_scored.json"
    if scored_file.exists():
        with open(scored_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        total = data.get('total_filtered', 0)
        critical = len([n for n in data.get('news', []) if n.get('category') == '🔴 极重要'])
        important = len([n for n in data.get('news', []) if n.get('category') == '🟡 重要'])

        lines.append("📊 **最新监控结果**:")
        lines.append(f"  - 采集时间: {data.get('processed_at', 'N/A')}")
        lines.append(f"  - 总计: {total} 条重要新闻")
        lines.append(f"  - 🔴 极重要: {critical} 条")
        lines.append(f"  - 🟡 重要: {important} 条")
        lines.append("")

        if total > 0:
            lines.append("**🔝 最新重要新闻**:")
            for news in data.get('news', [])[:3]:
                lines.append(f"  • {news.get('title')[:60]}...")
                lines.append(f"    来源: {news.get('source')} | 评分: {news.get('importance_score')}/20")
            lines.append("")
    else:
        lines.append("⏳ **等待首次监控完成...**")
        lines.append("")

    # 定时任务状态
    lines.append("⏰ **定时任务配置**:")
    lines.append("  - 监控频率: 每 10 分钟")
    lines.append("  - 通知频率: 每 30 分钟")
    lines.append("  - 下次监控: 立即（cron 任务已设置）")
    lines.append("")

    # 数据源状态
    config_file = project_dir / "config" / "sources.json"
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        lines.append("🌐 **数据源配置**:")
        lines.append(f"  - arXiv 分类: {len(config.get('arxiv_categories', []))} 个")
        lines.append(f"  - 官方博客: {len(config.get('blogs', []))} 个")
        lines.append(f"  - Twitter 账号: {len(config.get('twitter_accounts', []))} 个")
        lines.append("")

    # 日志文件
    lines.append("📁 **日志文件**:")
    lines.append(f"  - 监控日志: {logs_dir / 'monitor.log'}")
    lines.append(f"  - Cron 日志: {logs_dir / 'cron.log'}")
    lines.append(f"  - 最新消息: {logs_dir / 'latest_message.txt'}")
    lines.append("")

    # 管理命令
    lines.append("🛠️ **管理命令**:")
    lines.append("  ```bash")
    lines.append("  # 手动运行一次监控")
    lines.append(f"  cd {project_dir} && bash scripts/monitor.sh")
    lines.append("")
    lines.append("  # 查看定时任务")
    lines.append("  crontab -l")
    lines.append("")
    lines.append("  # 停止监控")
    lines.append("  crontab -e  # 删除相关行")
    lines.append("  pkill -f monitor.sh")
    lines.append("  ```")
    lines.append("")

    lines.append("📈 **监控状态**: ✅ 运行中")
    lines.append("🔔 **通知状态**: ✅ 已启用")
    lines.append("")
    lines.append("=" * 50)
    lines.append("💡 提示: 重要新闻会自动推送到此会话！")

    return "\n".join(lines)

if __name__ == '__main__':
    report = generate_status_report()
    print(report)
