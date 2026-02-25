# 3D Printing Co — AI Agent Skills

> 9 nanobot-ai skills across 3 AI-powered solutions for a Los Angeles-based 3D printing company.

## Quick Start

```bash
pip install nanobot-ai pyyaml pytest
```

Copy skills to your nanobot workspace:
```bash
cp -r skills/* ~/.nanobot/workspace/skills/
```

## Solutions Overview

### 🤖 Solution 1: AI Sales & Customer Support Agent
24/7 sales assistant and support rep on website, Telegram, or WhatsApp.

| Skill | Description |
|-------|-------------|
| **Product Recommender** | Matches customers to printers, filament, and materials based on needs |
| **Order & Quote** | Instant pricing for DIY printing service requests |
| **FAQ & Troubleshooting** | Answers questions about materials, settings, and machine issues |

### 📦 Solution 2: AI Inventory & Demand Forecasting Agent
Scheduled agent monitoring stock, analyzing trends, and alerting the team.

| Skill | Description |
|-------|-------------|
| **Stock Monitor** | Polls inventory at intervals, triggers reorder alerts |
| **Trend Analysis** | Detects demand spikes via order history + web search |
| **Alert & Report** | Daily/weekly digest reports via Telegram/WhatsApp |

### 📣 Solution 3: AI Marketing & Lead Generation Agent
Autonomous agent for online presence, B2B prospecting, and outreach.

| Skill | Description |
|-------|-------------|
| **Lead Discovery** | Finds LA-area businesses needing 3D printing |
| **Content Generation** | Auto-drafts social media, newsletters, blog articles |
| **Outreach Scheduler** | Cron-based cold outreach email sequences |

## Testing

```bash
# Run all structural + functional tests
python -m pytest tests/test_specs.py -v

# Run Agent-as-Judge evaluation
python tests/agent_judge.py --all --threshold 4.0
```

## Architecture

Each skill follows the nanobot skill format:
```
skill-name/
├── SKILL.md              # Instructions + spec + examples
├── scripts/              # Helper scripts
│   └── helper.py
└── resources/            # Data files
    └── data.json
```

## LLM Configuration

All skills use **Claude via OpenRouter** as the underlying LLM. Configure in `~/.nanobot/config.json`.
