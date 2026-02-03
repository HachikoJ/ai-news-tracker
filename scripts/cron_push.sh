#!/bin/bash

# AI 新闻自动推送脚本
# 每 30 分钟运行一次

PROJECT_DIR="/root/.openclaw/workspace/skills/ai-news-tracker"
cd "$PROJECT_DIR" || exit 1

# 1. 运行监控
bash scripts/monitor.sh > /dev/null 2>&1

# 2. 检查是否有重要新闻并生成报告
python3 scripts/auto_push.py > /tmp/ai_news_report.txt 2>&1

# 3. 将报告输出到标准输出（会被 cron 发送）
if [ -s /tmp/ai_news_report.txt ]; then
    cat /tmp/ai_news_report.txt
fi
