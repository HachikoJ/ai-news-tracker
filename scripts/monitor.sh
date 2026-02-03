#!/bin/bash

# AI 新闻实时监控主脚本
# 每 5-10 分钟运行一次，实时推送重要新闻

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_DIR/data"
CONFIG_DIR="$PROJECT_DIR/config"

# 创建必要的目录
mkdir -p "$DATA_DIR"
mkdir -p "$CONFIG_DIR"

echo -e "${YELLOW}========================================"
echo "   AI 新闻实时监控系统"
echo "========================================${NC}"
echo -e "${YELLOW}⏰ 启动时间: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""

# 1. 初始化配置（如果不存在）
if [ ! -f "$CONFIG_DIR/sources.json" ]; then
    echo -e "${YELLOW}📝 初始化配置文件...${NC}"
    cat > "$CONFIG_DIR/sources.json" << EOF
{
  "arxiv_categories": [
    "cs.AI",
    "cs.CL",
    "cs.CV",
    "cs.LG",
    "cs.NE"
  ],
  "blogs": [
    {
      "name": "OpenAI Blog",
      "url": "https://openai.com/blog/rss.xml"
    },
    {
      "name": "Google DeepMind",
      "url": "https://deepmind.google/blog/feed/"
    },
    {
      "name": "Anthropic",
      "url": "https://www.anthropic.com/news/rss"
    },
    {
      "name": "MIT Technology Review AI",
      "url": "https://www.technologyreview.com/feed/"
    }
  ],
  "update_interval_minutes": 5,
  "importance_threshold": 10,
  "enable_notification": true
}
EOF
    echo -e "${GREEN}✓ 配置文件已创建${NC}\n"
fi

# 2. 采集新闻
echo -e "${YELLOW}📡 步骤 1: 采集 AI 新闻...${NC}"
python3 "$SCRIPT_DIR/collect.py" \
    --config "$CONFIG_DIR/sources.json" \
    --output "$DATA_DIR/news_raw.json"

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ 采集失败${NC}"
    exit 1
fi

# 3. 评分和过滤
echo -e "${YELLOW}🎯 步骤 2: 评分和过滤...${NC}"
python3 "$SCRIPT_DIR/score.py" \
    --input "$DATA_DIR/news_raw.json" \
    --output "$DATA_DIR/news_scored.json" \
    --config "$CONFIG_DIR/sources.json" \
    --threshold 10

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ 评分失败${NC}"
    exit 1
fi

# 4. 生成摘要
echo -e "${YELLOW}📝 步骤 3: 生成摘要...${NC}"
python3 "$SCRIPT_DIR/summarize.py" \
    --input "$DATA_DIR/news_scored.json" \
    --output "$DATA_DIR/news_digest.md" \
    --format digest

if [ $? -ne 0 ]; then
    echo -e "${RED}✗ 摘要生成失败${NC}"
    exit 1
fi

# 5. 检查是否有极重要新闻
CRITICAL_COUNT=$(python3 -c "
import json
with open('$DATA_DIR/news_scored.json', 'r') as f:
    data = json.load(f)
    critical = [n for n in data.get('news', []) if n.get('category') == '🔴 极重要']
    print(len(critical))
")

# 6. 推送通知
if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo ""
    echo -e "${RED}🚨 发现 $CRITICAL_COUNT 条极重要新闻！${NC}"
    echo ""
    
    # 显示极重要新闻
    python3 << EOF
import json
with open('$DATA_DIR/news_scored.json', 'r') as f:
    data = json.load(f)
    critical = [n for n in data.get('news', []) if n.get('category') == '🔴 极重要']
    
    for i, news in enumerate(critical, 1):
        print(f"\n{i}. {news.get('title')}")
        print(f"   来源: {news.get('source')}")
        print(f"   评分: {news.get('importance_score')}/20")
        print(f"   链接: {news.get('url')}")
EOF
    
    echo ""
    echo -e "${YELLOW}📢 准备推送通知...${NC}"
    
    # 这里可以调用推送脚本
    # bash "$SCRIPT_DIR/notify.sh" "$DATA_DIR/news_scored.json"
else
    echo -e "${GREEN}✓ 无极重要新闻${NC}"
fi

# 7. 显示统计
echo ""
echo -e "${GREEN}========================================"
echo "   监控完成"
echo "========================================${NC}"

python3 << EOF
import json
with open('$DATA_DIR/news_scored.json', 'r') as f:
    data = json.load(f)
    news_list = data.get('news', [])
    critical = len([n for n in news_list if n.get('category') == '🔴 极重要'])
    important = len([n for n in news_list if n.get('category'] == '🟡 重要'])
    
    print(f"📊 采集统计:")
    print(f"   总计: {len(news_list)} 条")
    print(f"   🔴 极重要: {critical} 条")
    print(f"   🟡 重要: {important} 条")
    print(f"   🟢 一般: {len(news_list) - critical - important} 条")
EOF

echo ""
echo -e "${GREEN}✓ 下次运行: $(date -d '+5 minutes' '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""

# 保存运行日志
echo "$(date '+%Y-%m-%d %H:%M:%S') - 监控完成" >> "$DATA_DIR/monitor.log"
