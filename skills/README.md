# 🖨️ 3D Printing Co — AI Agent Skills

> **9 production-ready [nanobot-ai](https://github.com/nanobot-ai/nanobot) skills** across 3 AI-powered solutions for an LA-based 3D printing company operating 100 printers. Each skill is spec-driven, test-covered, and designed for deployment via Telegram, WhatsApp, or web chat.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [Solution 1: AI Sales & Customer Support Agent](#-solution-1-ai-sales--customer-support-agent)
- [Solution 2: AI Inventory & Demand Forecasting Agent](#-solution-2-ai-inventory--demand-forecasting-agent)
- [Solution 3: AI Marketing & Lead Generation Agent](#-solution-3-ai-marketing--lead-generation-agent)
- [Testing & Quality Assurance](#-testing--quality-assurance)
- [Cron Scheduling](#-cron-scheduling)
- [Customization Guide](#-customization-guide)
- [Skill Architecture](#-skill-architecture)

---

## Prerequisites

- **Python 3.11+**
- **nanobot-ai** — the agent runtime framework
- **Claude API access** via [OpenRouter](https://openrouter.ai/) (or direct Anthropic key)
- **Messaging channel** — Telegram and/or WhatsApp (optional, for live deployment)

## Installation & Setup

### 1. Install dependencies

```bash
pip install nanobot-ai pyyaml pytest
```

### 2. Configure nanobot

Create or edit your nanobot config at `~/.nanobot/config.json`:

```json
{
  "llm": {
    "provider": "openrouter",
    "model": "anthropic/claude-sonnet-4-20250514",
    "api_key": "sk-or-v1-YOUR_OPENROUTER_KEY"
  },
  "channels": {
    "telegram": {
      "bot_token": "YOUR_TELEGRAM_BOT_TOKEN"
    }
  }
}
```

### 3. Copy skills to your nanobot workspace

```bash
# Copy all 9 skills to nanobot's skill directory
cp -r skills/* ~/.nanobot/workspace/skills/

# Or symlink for easier development
ln -s $(pwd)/skills/* ~/.nanobot/workspace/skills/
```

### 4. Verify skills are loaded

```bash
nanobot skills list
```

You should see all 9 skills listed: `product-recommender`, `order-quote`, `faq-troubleshooting`, `stock-monitor`, `trend-analysis`, `alert-report`, `lead-discovery`, `content-generation`, `outreach-scheduler`.

### 5. Start chatting

```bash
# Interactive CLI chat with all skills available
nanobot chat

# Or start the Telegram bot
nanobot serve --channel telegram
```

---

## Project Structure

```
3d-printing-co/
├── skills/
│   ├── sales-support/                    # Solution 1
│   │   ├── product-recommender/
│   │   │   ├── SKILL.md                  # Decision logic + material matrix
│   │   │   ├── scripts/
│   │   │   │   └── product_catalog.py    # Product search & filter engine
│   │   │   └── resources/
│   │   │       └── catalog.json          # 17-product catalog database
│   │   ├── order-quote/
│   │   │   ├── SKILL.md                  # Pricing model + quote templates
│   │   │   └── scripts/
│   │   │       └── quote_calculator.py   # Instant pricing engine
│   │   └── faq-troubleshooting/
│   │       ├── SKILL.md                  # Decision trees + escalation rules
│   │       └── resources/
│   │           └── faq_knowledge_base.json  # 12-entry FAQ database
│   │
│   ├── inventory-forecasting/            # Solution 2
│   │   ├── stock-monitor/
│   │   │   ├── SKILL.md                  # Reorder logic + alert thresholds
│   │   │   └── scripts/
│   │   │       └── inventory_poller.py   # Stock level polling engine
│   │   ├── trend-analysis/
│   │   │   ├── SKILL.md                  # Forecasting framework + seasonal calendar
│   │   │   └── scripts/
│   │   │       └── trend_analyzer.py     # Order trend detection engine
│   │   └── alert-report/
│   │       ├── SKILL.md                  # Report templates + delivery rules
│   │       └── scripts/
│   │           └── report_generator.py   # Daily/weekly report compiler
│   │
│   ├── marketing-leadgen/                # Solution 3
│   │   ├── lead-discovery/
│   │   │   ├── SKILL.md                  # Industry targeting + scoring rubric
│   │   │   └── scripts/
│   │   │       └── lead_finder.py        # Lead scoring & export engine
│   │   ├── content-generation/
│   │   │   ├── SKILL.md                  # Brand voice + platform templates
│   │   │   └── scripts/
│   │   │       └── content_drafter.py    # Multi-platform content generator
│   │   └── outreach-scheduler/
│   │       ├── SKILL.md                  # Email sequences + send timing
│   │       └── scripts/
│   │           └── outreach_manager.py   # Outreach queue manager
│   └── README.md                         # ← You are here
│
├── tests/
│   ├── test_specs.py                     # 80 structural & functional tests
│   └── agent_judge.py                    # Agent-as-Judge evaluation (21 scenarios)
├── success_criteria.md                   # Pass/fail criteria per skill
└── ralph_evaluation.md                   # RALPH loop tracking
```

---

## 🤖 Solution 1: AI Sales & Customer Support Agent

A 24/7 conversational agent that handles product inquiries, generates instant quotes, and troubleshoots common 3D printing issues. Designed for deployment on Telegram, WhatsApp, or website chat.

---

### 1. Product Recommender

**What it does:** Recommends printers, filaments, resins, and accessories based on the customer's project type, experience level, budget, and technical requirements. Includes a material compatibility matrix and decision tree logic.

**When to use:** A customer asks "What printer should I buy?" or "Which filament works for outdoor parts?"

**Example conversations:**

```
Customer: "I'm a teacher looking for a 3D printer for my classroom, budget around $300"
Agent:    Recommends beginner-friendly FDM printers (Ender-3 V3) with PLA starter kit,
          explains why PLA is safest for classrooms, suggests education bundle.

Customer: "I need to print flexible phone cases"
Agent:    Recommends TPU filament, explains need for direct-drive extruder,
          suggests compatible printers, provides print settings.
```

**Helper script — `product_catalog.py`:**

```bash
# Search products by keyword
python scripts/product_catalog.py --search "PLA"

# Filter by category and budget
python scripts/product_catalog.py --category filament --budget 30

# List all printers
python scripts/product_catalog.py --category printer

# JSON output for integration
python scripts/product_catalog.py --search "resin" --json
```

**Data:** `resources/catalog.json` contains 17 products across categories: printers, filament, resin, accessories, and services.

---

### 2. Order & Quote

**What it does:** Generates instant price quotes for 3D printing service requests based on material type, part dimensions (LxWxH), quantity, quality tier, and urgency. Includes bulk discounts, rush surcharges, and automatic print time estimation.

**When to use:** A customer asks "How much to print this part?" or uploads an STL and wants pricing.

**Example conversations:**

```
Customer: "How much to print a 100x80x50mm enclosure in PETG?"
Agent:    Calculates material weight, estimates print time, applies PETG rate,
          returns quote with turnaround time and validity date.

Customer: "Need 25 copies of a small gear in ABS, rush delivery"
Agent:    Applies bulk discount (15% for 25+), adds rush surcharge (1.5x),
          returns total with expedited timeline.
```

**Helper script — `quote_calculator.py`:**

```bash
# Basic quote
python scripts/quote_calculator.py --material PETG --dimensions 80x60x40 --quantity 1

# With quality tier and rush
python scripts/quote_calculator.py --material ABS --dimensions 50x50x30 --quantity 25 --quality fine --rush

# JSON output
python scripts/quote_calculator.py --material PLA --dimensions 100x100x50 --json
```

**Pricing model:** Base rate per gram varies by material (PLA $0.04/g, PETG $0.05/g, ABS $0.06/g, etc.) + machine time ($13/hr) + setup fee. Quality tiers multiply base: Draft (0.8x), Standard (1.0x), Fine (1.3x), Ultra (1.6x).

---

### 3. FAQ & Troubleshooting

**What it does:** Answers frequently asked questions about 3D printing materials, settings, machine issues, and company policies. Uses troubleshooting decision trees to diagnose problems step-by-step and escalates to human support when needed.

**When to use:** A customer reports "My prints keep warping" or asks "What's your return policy?"

**Example conversations:**

```
Customer: "My PLA prints keep warping off the bed"
Agent:    Walks through decision tree: check bed temp (60°C), check leveling,
          suggest adhesion aids (glue stick, hairspray), check for drafts.

Customer: "Is 3D printing safe for my 8-year-old?"
Agent:    Explains PLA is non-toxic, warns about hot end temperatures,
          recommends adult supervision, suggests enclosed printers.
```

**Data:** `resources/faq_knowledge_base.json` contains 12 FAQ entries organized by category (materials, settings, troubleshooting, policies). Each entry has tags for smart matching.

**Escalation rules:** The skill escalates to human support if the issue involves safety, refund disputes, damaged equipment, or after 3 unsuccessful troubleshooting steps.

---

## 📦 Solution 2: AI Inventory & Demand Forecasting Agent

An automated agent that runs on schedules (cron) to monitor stock levels, detect demand trends, and deliver reports to the team via Telegram or WhatsApp. Designed to prevent stockouts and optimize purchasing.

---

### 4. Stock Monitor

**What it does:** Polls inventory levels at configurable intervals, calculates dynamic reorder points based on daily consumption rates, and triggers tiered alerts (low stock, critical, stockout risk). Uses safety stock formulas with lead time consideration.

**When to use:** Runs automatically via cron. Team asks "What items are running low?" or "When will PLA White run out?"

**Example output:**

```
📊 STOCK REPORT
  🔴 CRITICAL: PLA White — 12 spools left (1.5 days to stockout)
  🟡 LOW: PETG Black — 28 spools left (reorder point: 35)
  🟢 OK: ABS Red — 85 spools left
```

**Helper script — `inventory_poller.py`:**

```bash
# Check all inventory items
python scripts/inventory_poller.py --check-all

# Check specific item
python scripts/inventory_poller.py --item "PLA White"

# Show only critical items
python scripts/inventory_poller.py --critical-only

# JSON output for dashboards
python scripts/inventory_poller.py --check-all --json
```

**Reorder formula:** `Reorder Point = (Daily Usage × Lead Time Days) + Safety Stock`, where Safety Stock = Daily Usage × Safety Buffer Days (default: 7).

---

### 5. Trend Analysis

**What it does:** Analyzes internal order history to detect demand spikes, seasonal patterns, and growth trends. Combines internal data with web search results to identify emerging market trends (e.g., new materials gaining popularity, industry events driving demand). Includes a seasonal demand calendar for proactive inventory planning.

**When to use:** Weekly analysis runs. Team asks "What's trending?" or "Should we stock up for back-to-school season?"

**Example output:**

```
📈 TREND REPORT
  🔥 PLA Silk: +340% growth (15→66 orders/month) — HIGH confidence
  📈 PETG:     +45% growth (sustained 3 months) — MEDIUM confidence
  📉 ABS:      -12% decline (possible seasonal) — LOW confidence
  🌐 Web trend: "TPU flexible filament" search volume up 200%
```

**Helper script — `trend_analyzer.py`:**

```bash
# Full trend report
python scripts/trend_analyzer.py --report

# Analyze specific product
python scripts/trend_analyzer.py --product "PLA Silk"

# Seasonal forecast
python scripts/trend_analyzer.py --seasonal

# JSON output
python scripts/trend_analyzer.py --report --json
```

**Seasonal calendar:** Built-in awareness of demand modifiers: back-to-school (Aug–Sep, +30%), holiday season (Nov–Dec, +45%), trade shows, maker faires, etc.

---

### 6. Alert & Report

**What it does:** Compiles and delivers formatted reports at scheduled intervals — daily operational summaries, weekly strategic digests, and critical alerts for urgent inventory or operational issues. Reports are delivered via Telegram or WhatsApp with clear formatting and action items.

**When to use:** Runs automatically. Team asks "Send me today's report" or triggered by critical events.

**Report types:**

| Type | Schedule | Contents |
|------|----------|----------|
| **Daily** | Every morning 7 AM | Factory status, inventory health, yesterday's orders, today's action items |
| **Weekly** | Friday 5 PM | Weekly sales summary, top products, inventory trends, forecasts, recommendations |
| **Critical** | Triggered by events | Stockout warnings, equipment issues, urgent orders requiring attention |

**Helper script — `report_generator.py`:**

```bash
# Generate daily report
python scripts/report_generator.py --type daily

# Generate weekly digest
python scripts/report_generator.py --type weekly

# Generate critical alert
python scripts/report_generator.py --type critical

# JSON output
python scripts/report_generator.py --type daily --json
```

---

## 📣 Solution 3: AI Marketing & Lead Generation Agent

An autonomous marketing agent that discovers potential B2B customers in the LA area, generates on-brand content for social media and email, and manages automated outreach email sequences with optimal timing.

---

### 7. Lead Discovery

**What it does:** Finds and qualifies local businesses that could benefit from 3D printing services using structured web search queries. Scores leads on a 100-point rubric across three dimensions: Company Fit (40 pts), Need Indicators (35 pts), and Accessibility (25 pts). Generates customized pitch angles for each lead based on their industry.

**When to use:** Weekly prospecting runs. Team asks "Find architecture firms in LA that need 3D printing."

**Target industries:** Architecture, Product Design, Education, Medical Devices, Dental, Jewelry, Film/Entertainment, Automotive, Real Estate, Startups.

**Scoring tiers:**

| Score | Tier | Action |
|-------|------|--------|
| 80–100 | 🔥 Hot Lead | Immediate outreach |
| 60–79 | 🟡 Warm Lead | Weekly outreach batch |
| 40–59 | 🔵 Cool Lead | Nurture with content |
| <40 | ⚪ Low Priority | Monitor only |

**Helper script — `lead_finder.py`:**

```bash
# Find architecture leads in LA
python scripts/lead_finder.py --industry architecture --location "Los Angeles"

# Top 5 leads across all industries
python scripts/lead_finder.py --all-industries --top 5

# Filter by minimum score
python scripts/lead_finder.py --industry "product design" --min-score 70

# Export to CSV for CRM import
python scripts/lead_finder.py --all-industries --export csv --output leads.csv

# JSON output
python scripts/lead_finder.py --industry dental --json
```

**Data:** Ships with 8 sample LA-area leads across industries. In production, replace with web search API integration for live prospecting.

---

### 8. Content Generation

**What it does:** Auto-drafts marketing content optimized for each platform — Instagram posts (with hashtags and image suggestions), LinkedIn articles (professional tone), blog outlines (SEO-optimized), and email newsletters. Follows brand voice guidelines: enthusiastic, helpful, maker-culture, LA-local.

**When to use:** Weekly content batch runs. Team asks "Draft an Instagram post about our new silk PLA."

**Content calendar rotation:**

| Week | Theme | Deliverables |
|------|-------|-------------|
| 1 | Product Spotlight | Instagram carousel + blog + newsletter |
| 2 | How-To/Tutorial | Instagram reel script + blog + LinkedIn |
| 3 | Customer Story | Instagram post + LinkedIn + email case study |
| 4 | Industry/Trend | Twitter thread + blog analysis + newsletter |

**Helper script — `content_drafter.py`:**

```bash
# Instagram post
python scripts/content_drafter.py --type instagram --topic "new silk PLA filament"

# LinkedIn post
python scripts/content_drafter.py --type linkedin --topic "3D printing in architecture"

# Blog outline with SEO keywords
python scripts/content_drafter.py --type blog --topic "PLA vs PETG" --seo-keywords "PLA vs PETG,best filament"

# Newsletter
python scripts/content_drafter.py --type newsletter --topic "February product roundup"

# View content calendar
python scripts/content_drafter.py --calendar --month 3

# JSON output
python scripts/content_drafter.py --type instagram --topic "resin printing" --json
```

---

### 9. Outreach Scheduler

**What it does:** Manages personalized cold outreach email sequences with optimal send timing. Supports 3-email cold introduction sequences (intro → follow-up → final), post-event follow-ups, and re-engagement campaigns. Tracks response status and enforces CAN-SPAM compliance (unsubscribe, opt-out tracking).

**When to use:** After Lead Discovery generates scored leads. Runs on cron for automated sending and follow-up reminders.

**Send timing optimization:**

| Day | Best Window (PST) | Expected Performance |
|-----|:------------------:|---------------------|
| Tuesday | 9–11 AM | 🏆 Highest open rate |
| Wednesday | 9–11 AM | 🥈 Second best |
| Thursday | 9–11 AM | 🥉 Third best |

**3-email cold sequence:**
1. **Day 0 — Introduction**: Personalized intro with industry-specific pitch + free sample offer
2. **Day 4 — Follow-up**: Brief bump with relevant case study
3. **Day 10 — Final**: Graceful close with bookmark CTA

**Helper script — `outreach_manager.py`:**

```bash
# View queue status (pending, sent, replied)
python scripts/outreach_manager.py --queue-status

# See today's scheduled sends
python scripts/outreach_manager.py --send-today

# Check for leads needing follow-up
python scripts/outreach_manager.py --check-followups

# Add a lead to a sequence
python scripts/outreach_manager.py --add-to-sequence --lead "Morphosis Architects" --sequence cold-intro

# Mark a lead as replied
python scripts/outreach_manager.py --mark-replied --lead "JFAK Architects" --status interested

# Weekly performance report
python scripts/outreach_manager.py --report --period weekly
```

---

## 🧪 Testing & Quality Assurance

### Structural & Functional Tests (80 tests)

Validates SKILL.md structure, YAML frontmatter, resource files, and script functionality:

```bash
cd 3d-printing-co
python -m pytest tests/test_specs.py -v
```

**What's tested:**
- All 9 SKILL.md files have valid frontmatter (`name`, `description`, `metadata`)
- All specs include Inputs, Outputs, Constraints, and Edge Cases
- All 8 helper scripts compile without syntax errors
- All scripts accept `--help` without crashing
- `catalog.json` has valid products with required fields
- `faq_knowledge_base.json` has valid Q&A entries

### Agent-as-Judge Evaluation (21 scenarios)

Scores skill quality across 5 dimensions using a rubric:

```bash
# Set encoding for emoji output on Windows
$env:PYTHONIOENCODING='utf-8'

# Evaluate all skills (pass threshold: 4.0/5.0)
python tests/agent_judge.py --all --threshold 4.0

# Evaluate a specific skill
python tests/agent_judge.py --skill product-recommender

# View the rubric
python tests/agent_judge.py --rubric

# List all test scenarios
python tests/agent_judge.py --scenarios
```

**Rubric dimensions:**

| Dimension | Weight | Description |
|-----------|:------:|-------------|
| Accuracy | 25% | Information is factually correct |
| Relevance | 25% | Response addresses the user's actual need |
| Completeness | 20% | All important details included |
| Clarity | 15% | Easy to understand, well-formatted |
| Brand Alignment | 15% | Matches company tone (helpful, enthusiastic, LA-local) |

### RALPH Loop

The iterative quality improvement process: **R**eview → **A**djust → **L**oop → **P**olish → **H**alt. Run tests, fix failures, repeat until all skills score ≥ 4.0. See `ralph_evaluation.md` for the tracking template.

---

## ⏰ Cron Scheduling

Each skill includes ready-to-use cron schedules. Set them up with `nanobot cron add`:

```bash
# Inventory check every 4 hours
nanobot cron add --name "stock-check" \
  --message "Run inventory check on all items. Report critical and low stock." \
  --cron "0 */4 * * *" \
  --deliver --channel "telegram"

# Daily report every morning at 7 AM
nanobot cron add --name "daily-report" \
  --message "Generate and deliver today's daily operations report." \
  --cron "0 7 * * *" \
  --deliver --channel "telegram"

# Weekly lead discovery on Tuesdays at 10 AM
nanobot cron add --name "weekly-leads" \
  --message "Find top 10 leads in this week's target industry." \
  --cron "0 10 * * 2" \
  --deliver --channel "telegram"

# Weekly content batch on Sundays at 6 PM
nanobot cron add --name "weekly-content" \
  --message "Generate this week's content: 1 Instagram post, 1 LinkedIn post, 1 blog outline." \
  --cron "0 18 * * 0" \
  --deliver --channel "telegram"

# Outreach sending Tue–Thu at 9 AM
nanobot cron add --name "outreach-send" \
  --message "Process outreach queue and send today's scheduled emails." \
  --cron "0 9 * * 2-4"

# Manage cron jobs
nanobot cron list
nanobot cron remove --name "stock-check"
nanobot cron enable --name "daily-report"
```

---

## 🔧 Customization Guide

### Updating the Product Catalog

Edit `sales-support/product-recommender/resources/catalog.json` to add, remove, or update products:

```json
{
  "id": "PROD-018",
  "name": "Your New Product",
  "category": "filament",
  "material": "PLA+",
  "price": 24.99,
  "in_stock": true,
  "description": "Enhanced PLA with better layer adhesion"
}
```

### Adjusting Pricing

Edit the `RATES` dictionary in `sales-support/order-quote/scripts/quote_calculator.py`:

```python
RATES = {
    "PLA":   {"per_gram": 0.04, "hr_rate": 13.00},
    "PETG":  {"per_gram": 0.05, "hr_rate": 13.00},
    # Add your custom materials here
}
```

### Adding FAQ Entries

Add entries to `sales-support/faq-troubleshooting/resources/faq_knowledge_base.json`:

```json
{
  "id": "faq-013",
  "question": "Your new question?",
  "answer": "Detailed answer here.",
  "category": "materials",
  "tags": ["keyword1", "keyword2"]
}
```

### Connecting Real Data Sources

The helper scripts ship with sample data. To connect real APIs:

1. **Inventory**: Replace the `SAMPLE_INVENTORY` dict in `inventory_poller.py` with your actual inventory API calls
2. **Orders**: Replace `SAMPLE_ORDERS` in `trend_analyzer.py` with your order management system API
3. **Leads**: Replace `SAMPLE_LEADS` in `lead_finder.py` with web search API (e.g., Google Custom Search, SerpAPI)
4. **Outreach**: Replace `SAMPLE_QUEUE` in `outreach_manager.py` with your CRM/email platform API

---

## 🏗️ Skill Architecture

Each skill follows the [nanobot-ai skill format](https://github.com/nanobot-ai/nanobot):

```
skill-name/
├── SKILL.md              # Main instruction file (YAML frontmatter + Markdown)
├── scripts/              # Helper Python scripts (called by the agent)
│   └── helper.py
└── resources/            # Static data files (JSON, CSV)
    └── data.json
```

**SKILL.md anatomy:**

```yaml
---
name: skill-name              # Unique identifier
description: What it does      # One-line summary
metadata: '{"nanobot": {...}}' # Runtime requirements
---

# Skill Title
[Agent instructions in Markdown]

## Spec
### Inputs        — What the skill accepts
### Outputs       — What it produces
### Constraints   — Rules and limits
### Edge Cases    — How to handle unusual situations

## [Domain Logic]  — Decision trees, formulas, templates
## Usage           — CLI commands for helper scripts
## Cron Schedule   — Automated scheduling examples
```

**LLM:** All skills use **Claude** (via OpenRouter or direct API) as the underlying language model. The model reads the SKILL.md instructions and uses the helper scripts as tools to look up data, calculate values, and generate structured output.
