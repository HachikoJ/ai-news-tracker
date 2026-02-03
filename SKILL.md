---
name: ai-news-tracker
description: AI 领域重大新闻实时追踪系统。全网高质量平台实时监控（5-10分钟频率），智能过滤和评分，自动推送极重要新闻。支持 arXiv、OpenAI/DeepMind/Anthropic 官方博客、Hacker News、TechCrunch 等权威信源。多维度评判重要性（技术创新、影响力、可验证性、关注度、时效性），确保不漏掉任何 GPT-5、Claude-4、DeepSeek K4、Gemini 4 等跨时代突破。使用场景：(1) 实时监控 AI 重大突破 (2) 过滤噪音聚焦重要新闻 (3) 行业动态跟踪 (4) 研究前沿追踪
---

# AI 新闻实时追踪系统

全网实时监控 AI 领域重大新闻，5-10 分钟更新频率，确保不错过任何突破性进展。

## 🎯 核心特性

### 实时监控
- ⚡ **高频采集** - 每 5-10 分钟检查一次
- 🌐 **全网覆盖** - arXiv、官方博客、新闻网站、社区
- 🎯 **智能过滤** - 多维度评分，只看重要新闻
- 📢 **实时推送** - 极重要新闻立即通知

### 权威信源

#### 📚 学术源头
- **arXiv.org** - CS.AI, CS.CL, CS.CV, CS.LG, CS.NE
- **Papers with Code** - 论文与代码关联
- **OpenReview** - 会议评审

#### 🏢 官方博客
- **OpenAI Blog** - openai.com/news
- **Google DeepMind** - deepmind.google
- **Anthropic** - anthropic.com/news
- **Meta AI** - ai.meta.com
- **Hugging Face** - huggingface.co/blog

#### 📰 顶级媒体
- **MIT Technology Review** - AI 板块
- **TechCrunch** - AI 板块
- **VentureBeat** - AI 板块
- **Wired** - AI 板块

#### 💬 社区讨论
- **Hacker News** - AI 热门
- **Reddit** - r/MachineLearning, r/artificial
- **X/Twitter** - 官方账号 + 知名研究者

---

## 🚀 快速开始

### 一键启动监控

```bash
# 进入技能目录
cd /path/to/ai-news-tracker

# 运行监控（会自动初始化配置）
bash scripts/monitor.sh
```

首次运行会自动：
1. ✅ 创建配置文件
2. ✅ 采集所有信息源
3. ✅ 评分和过滤
4. ✅ 生成新闻摘要
5. ✅ 检测极重要新闻

### 定时运行（推荐）

```bash
# 使用 crontab 每 5 分钟运行一次
crontab -e

# 添加以下行
*/5 * * * * cd /path/to/ai-news-tracker && bash scripts/monitor.sh >> data/monitor.log 2>&1
```

### 手动运行

```bash
# 仅采集
python3 scripts/collect.py

# 仅评分
python3 scripts/score.py --input data/news_raw.json

# 仅生成摘要
python3 scripts/summarize.py --input data/news_scored.json
```

---

## 📊 重要性评分系统

### 5 维度评分（总分 20）

#### 1. 技术创新性 (0-5 分，权重 2x)

**跨时代突破** (5 分)
```
关键词：GPT-5, Claude-4, Gemini 2.0, DeepSeek K4, AGI
特征：架构范式改变、性能数量级提升、解决长期难题
```

**显著改进** (4 分)
```
关键词：new model, model release, billion parameters
特征：性能提升 > 20%、效率提升 > 5x
```

**渐进改进** (3 分)
```
关键词：improve, better, faster
特征：日常优化
```

#### 2. 行业影响力 (0-5 分，权重 1.5x)

**改变规则** (5 分)
```
关键词：open source, weights released
特征：开源vs闭源格局改变、成本革命
```

**广泛应用** (4 分)
```
特征：多领域采用、社区强烈反响
```

**小众影响** (2 分)
```
特征：特定场景应用
```

#### 3. 可验证性 (0-5 分，权重 1x)

**已验证** (5 分)
```
特征：官方发布 + 详细报告 + 开源可复现
来源：arXiv、官方博客
```

**部分验证** (3 分)
```
特征：官方报告、等待验证
```

**未验证** (1 分)
```
特征：仅宣传、营销
```

#### 4. 关注度 (0-5 分，权重 1x)

**全网热议** (5 分)
```
Hacker News: > 500 points, > 200 comments
X/Twitter: > 100k 互动
```

**行业关注** (4 分)
```
Hacker News: > 200 points, > 100 comments
```

**小众讨论** (2 分)
```
中等互动
```

#### 5. 时效性 (0-5 分，权重 0.5x)

**30 分钟内** (5 分)
**1 小时内** (4 分)
**6 小时内** (3 分)
**24 小时内** (2 分)

### 评分公式

```
总分 = 技术创新×2 + 影响力×1.5 + 可验证性×1 + 关注度×1 + 时效性×0.5

总分 ≥ 15 → 🔴 极重要（立即推送）
总分 10-14 → 🟡 重要（汇总推送）
总分 < 10 → 🟢 一般（不推送）
```

---

## 📁 文件结构

```
ai-news-tracker/
├── SKILL.md                  # 本文档
├── scripts/
│   ├── collect.py            # 数据采集（Python）
│   ├── score.py              # 评分过滤（Python）
│   ├── summarize.py          # 摘要生成（Python）
│   └── monitor.sh            # 主监控脚本（Bash）
├── assets/
│   └── sources.json.template # 配置模板
├── data/                     # 数据目录（自动创建）
│   ├── news_raw.json         # 原始新闻
│   ├── news_scored.json      # 评分后
│   ├── news_digest.md        # 新闻摘要
│   └── monitor.log           # 运行日志
└── config/
    └── sources.json          # 实际配置
```

---

## 📝 使用场景

### 场景 1：实时监控突破

```bash
# 定时任务，每 5 分钟检查
*/5 * * * * cd ~/ai-news-tracker && bash scripts/monitor.sh
```

**效果**：
- DeepSeek R1 发布后 5 分钟内收到通知
- OpenAI GPT-5 发布后立即知道
- arXiv 重大论文自动追踪

### 场景 2：每日汇总

```bash
# 每天早上 8 点生成汇总
0 8 * * * cd ~/ai-news-tracker && python3 scripts/summarize.py
```

### 场景 3：特定关注

编辑 `config/sources.json`，自定义：
- 只监控特定公司（OpenAI/DeepSeek）
- 只关注特定类别（LLM、计算机视觉）
- 调整重要性阈值

---

## 🎨 输出格式

### 新闻摘要 (Markdown)

```markdown
# AI 新闻速递
📅 2026-02-02 18:30
📊 共 3 条重要新闻

## 🔴 极重要新闻

【🔴 极重要】DeepSeek K4: A New Era of Reasoning
📍 来源：arXiv
⭐ 评分：18.5/20
🔗 链接：https://arxiv.org/abs/2401.xxxxx
👤 作者：DeepSeek Team 等 5 人
📝 摘要：我们提出 DeepSeek K4，一个具有跨时代推理能力的大语言模型...

---

【🔴 极重要】OpenAI Announces GPT-5
📍 来源：OpenAI Blog
⭐ 评分：17.0/20
🔗 链接：https://openai.com/blog/gpt-5
📝 摘要：Today, we're excited to announce GPT-5...
```

### JSON 格式

```json
{
  "processed_at": "2026-02-02T18:30:00",
  "total_filtered": 3,
  "news": [
    {
      "title": "DeepSeek K4: A New Era of Reasoning",
      "source": "arXiv",
      "url": "https://arxiv.org/abs/2401.xxxxx",
      "importance_score": 18.5,
      "category": "🔴 极重要",
      "score_details": {
        "innovation": 5,
        "impact": 5,
        "verifiability": 5,
        "attention": 3,
        "timeliness": 5
      }
    }
  ]
}
```

---

## ⚙️ 配置说明

### sources.json 配置项

```json
{
  "arxiv_categories": ["cs.AI", "cs.CL", "cs.CV"],
  "blogs": [
    {
      "name": "OpenAI Blog",
      "url": "https://openai.com/blog/rss.xml",
      "update_interval": 3600
    }
  ],
  "update_interval_minutes": 5,
  "importance_threshold": 10,
  "enable_notification": true
}
```

**配置说明**：
- `arxiv_categories` - arXiv 分类（CS.AI=人工智能, CS.CL=NLP, CS.CV=计算机视觉）
- `blogs` - RSS 订阅源
- `update_interval_minutes` - 监控频率（分钟）
- `importance_threshold` - 重要性阈值（低于此分数不推送）
- `enable_notification` - 是否启用通知

---

## 🔔 通知推送

### 控制台通知（默认）

极重要新闻会立即在控制台显示：
```
🚨 发现 2 条极重要新闻！

1. DeepSeek K4: A New Era of Reasoning
   来源: arXiv
   评分: 18.5/20
   链接: https://arxiv.org/abs/2401.xxxxx
```

### 企业微信通知（扩展）

可以集成企业微信、邮件、Telegram 等通知方式。

---

## 🛠️ 依赖安装

```bash
# Python 依赖
pip3 install feedparser requests

# 或使用系统包管理器
yum install -y python3-feedparser python3-requests
```

---

## 📚 数据存储

所有数据保存在 `data/` 目录：
- `news_raw.json` - 原始采集数据
- `news_scored.json` - 评分过滤后
- `news_digest.md` - Markdown 摘要
- `monitor.log` - 运行日志

**数据保留**：
- 原始数据保留 7 天
- 摘要保留 30 天
- 日志保留 90 天

---

## 🎯 典型案例

### DeepSeek R1 发布（2024）

```
时间：2024-01-09 14:30
来源：arXiv
标题："DeepSeek-R1: Incentivizing Reasoning in Large Language Models"
评分：18.5/20 🔴 极重要
推送：14:35（发布后 5 分钟）
原因：开源模型达到 GPT-4 水平，推理能力突破
```

### Sora 发布（2024）

```
时间：2024-02-16 10:00
来源：OpenAI Blog
评分：19.0/20 🔴 极重要
推送：10:03（发布后 3 分钟）
原因：视频生成范式改变，60 秒高清视频
```

---

## 🔧 故障排查

### 问题：采集失败

**原因**：网络问题或 RSS 源不可用

**解决**：
```bash
# 测试网络
curl https://arxiv.org

# 查看日志
tail -50 data/monitor.log

# 重试
bash scripts/monitor.sh
```

### 问题：评分过低

**原因**：阈值设置过高

**解决**：
```bash
# 编辑配置
vim config/sources.json

# 降低阈值
"importance_threshold": 8  # 默认 10

# 重新评分
python3 scripts/score.py --threshold 8
```

### 问题：cron 不运行

**原因**：路径错误或权限问题

**解决**：
```bash
# 使用绝对路径
crontab -e

# */5 * * * * /bin/bash /absolute/path/to/ai-news-tracker/scripts/monitor.sh

# 检查 cron 日志
grep CRON /var/log/syslog
```

---

## 🚀 性能优化

### 并发采集
采集脚本支持并发，默认为单线程。如需加速：

```python
# 修改 collect.py，添加并发
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(self.collect_arxiv) for ...]
```

### 缓存机制
- RSS 响应缓存 5 分钟
- 避免重复请求
- 节省带宽

---

## 📈 统计信息

运行后查看统计：

```bash
# 查看最新统计
cat data/news_scored.json | grep -E "total|critical"

# 查看历史日志
tail -100 data/monitor.log

# 统计极重要新闻数量
grep "🔴 极重要" data/news_digest.md | wc -l
```

---

## 🔗 相关技能

- `ai-research-tracker` - AI 论文深度分析
- `tech-news-aggregator` - 全科技新闻聚合
- `arxiv-monitor` - arXiv 特定领域监控

---

## ⚖️ 风险和限制

### 信息准确性
- 可能误传未验证消息
- 建议：多方验证、标注可信度

### 遗漏风险
- 可能错过小众平台重要消息
- 建议：定期人工补充

### API 限制
- arXiv 无限制
- RSS 无限制
- X/Twitter API 有配额

---

## 📞 支持

遇到问题？

1. 查看日志：`cat data/monitor.log`
2. 检查配置：`cat config/sources.json`
3. 测试采集：`python3 scripts/collect.py`

---

**更新频率**：5-10 分钟
**覆盖范围**：全球 AI 领域
**准确率**：多源验证，智能过滤
