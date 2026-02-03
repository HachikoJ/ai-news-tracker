#!/bin/bash

# AI 新闻监控系统 - 快速启动脚本

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}========================================"
echo "   AI 新闻监控系统 - 启动"
echo "========================================${NC}"
echo ""

# 1. 创建必要的目录
mkdir -p "$SCRIPT_DIR/data"
mkdir -p "$SCRIPT_DIR/logs"
mkdir -p "$SCRIPT_DIR/config"

# 2. 初始化配置（如果不存在）
if [ ! -f "$SCRIPT_DIR/config/sources.json" ]; then
    echo -e "${YELLOW}📝 初始化配置文件...${NC}"
    cp "$SCRIPT_DIR/assets/sources.json.template" "$SCRIPT_DIR/config/sources.json"
fi

# 3. 安装依赖检查
echo -e "${YELLOW}🔍 检查依赖...${NC}"
python3 -c "import feedparser, requests, bs4" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Python 依赖未完全安装，尝试安装...${NC}"
    yum install -y python3-feedparser python3-requests python3-beautifulsoup4 python3-lxml >/dev/null 2>&1
fi

# 4. 启动监控
echo -e "${GREEN}✓ 启动监控...${NC}"
cd "$SCRIPT_DIR"
bash scripts/monitor.sh

echo ""
echo -e "${GREEN}✓ 监控系统已启动！${NC}"
echo ""
echo -e "${BLUE}📊 查看结果：${NC}"
echo "  - 数据文件: $SCRIPT_DIR/data/"
echo "  - 运行日志: $SCRIPT_DIR/logs/monitor.log"
echo ""
echo -e "${BLUE}⏰ 定时任务：${NC}"
echo "  - 监控频率: 每 10 分钟"
echo "  - 通知频率: 每 30 分钟"
echo "  - 查看任务: crontab -l"
echo ""
echo -e "${BLUE}🛑 停止监控：${NC}"
echo "  - 删除定时任务: crontab -e (删除相关行)"
echo "  - 杀死进程: pkill -f monitor.sh"
echo ""
