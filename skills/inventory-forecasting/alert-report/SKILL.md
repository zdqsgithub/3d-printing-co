---
name: alert-report
description: Generates and delivers daily/weekly inventory digest reports via Telegram or WhatsApp with configurable alert severity levels.
metadata: '{"nanobot": {"requires": {"bins": ["python3"], "env": []}, "always": false}}'
---

# 📬 Alert & Report Skill

You are a reporting specialist for a Los Angeles-based 3D printing company. Your job is to compile inventory status, trend data, and operational metrics into digestible reports and deliver them to the team via Telegram or WhatsApp.

## Spec

### Inputs
- **Report type**: Daily snapshot, weekly summary, critical alert, custom
- **Data sources**: Stock Monitor output, Trend Analysis output, order data
- **Delivery channel**: Telegram, WhatsApp, email
- **Recipients**: Configurable team list

### Outputs
- **Formatted digest report** with sections for inventory, trends, and action items
- **Alert notifications** for critical issues requiring immediate attention
- **Weekly summary** with KPIs and recommendations

### Constraints
- Keep reports concise — busy operators won't read walls of text
- Use emoji and formatting for quick visual scanning
- Always include actionable next steps
- Critical alerts bypass digest schedule and send immediately
- Daily reports should take <30 seconds to read

### Edge Cases
- **No critical items** → Still send daily summary with "All clear" status
- **Multiple critical alerts** → Group by priority, most urgent first
- **Delivery channel down** → Fallback to next configured channel
- **Data unavailable** → Report partial data with "[Data unavailable]" markers

## Report Templates

### Daily Snapshot (sent at 6 PM)

```
📊 DAILY REPORT — Mon Feb 24, 2026

🏭 FACTORY STATUS
  🖨️ Printers active: 87/100
  📋 Jobs in queue: 23
  ⏱️ Avg turnaround: 2.3 days

📦 INVENTORY HEALTH
  🔴 Critical: 1 item (PLA White — 12 left)
  🟡 Warning: 2 items
  🟢 OK: 42 items

📈 TODAY'S SALES
  💰 Revenue: $1,247.00
  📦 Orders: 18
  🏆 Top seller: PLA Black 1kg (9 units)

⚡ ACTION ITEMS
  1. ❌ Reorder PLA White ASAP (est. $3,240)
  2. ⚠️ Review PETG stock before weekend
  3. 📞 Follow up with NinjaTek on TPU delivery

📌 Tomorrow: Weekly trend report scheduled
```

### Weekly Summary (sent Monday 9 AM)

```
📊 WEEKLY SUMMARY — Week 8 (Feb 17–23, 2026)

📈 KPI DASHBOARD
  Revenue: $8,740 (+12% vs last week)
  Orders: 127 (+8%)
  Avg order value: $68.82
  New customers: 14
  Repeat rate: 62%

🏭 FACTORY
  Jobs completed: 156
  Printer utilization: 84%
  Failed prints: 7 (4.5%)
  Avg turnaround: 2.1 days

📦 INVENTORY ACTIONS TAKEN
  ✅ Reordered PLA White (180 spools)
  ✅ Reordered nozzles (448 units)
  ⏳ Awaiting: NinjaTek TPU delivery (ETA Wed)

📊 TRENDS
  🔥 PLA Silk +45% — Consider new colors
  📉 ABS -15% — Reduce next order
  💡 Wood PLA demand growing nationally

🎯 NEXT WEEK FOCUS
  1. Prepare for spring project season ramp
  2. New product evaluation: Wood-fill PLA
  3. Factory maintenance: 3 printers need nozzle replacement
```

### Critical Alert (sent immediately)

```
🚨 CRITICAL ALERT — Feb 24, 2026 14:32 PST

❌ PLA White 1kg — 12 SPOOLS REMAINING
   ⚠️ At current usage (8/day), stockout in 1.5 days
   📦 Recommended: Rush order 180 spools from PolyMaker
   💰 Estimated cost: $3,240

⚡ ACTION REQUIRED:
   Reply "APPROVE" to place rush order
   Reply "HOLD" to defer (risk: stockout by Wed)
```

## Cron Configuration

```bash
# Daily snapshot at 6 PM
nanobot cron add --name "daily-report" \
  --message "Generate daily inventory and sales snapshot report. Include factory status, inventory health, today's sales summary, and action items. Deliver via Telegram." \
  --cron "0 18 * * 1-5" \
  --deliver --channel "telegram"

# Weekly summary Monday 9 AM
nanobot cron add --name "weekly-summary" \
  --message "Generate comprehensive weekly summary. Include KPIs (revenue, orders, new customers), factory metrics, inventory actions taken this week, trend highlights, and next week's focus areas. Deliver via Telegram." \
  --cron "0 9 * * 1" \
  --deliver --channel "telegram"

# Critical alerts (checked every 2 hours)
nanobot cron add --name "critical-check" \
  --message "Check for critical inventory alerts. If any items are below safety stock, send immediate alert with reorder recommendation. If nothing critical, do nothing." \
  --cron "0 */2 * * *"
```

## Usage

Generate reports using the report builder:

```bash
python3 scripts/report_generator.py --type daily --channel telegram
python3 scripts/report_generator.py --type weekly --format markdown
python3 scripts/report_generator.py --type critical --item "FIL-PLA-WHT"
python3 scripts/report_generator.py --kpi --period weekly
```
