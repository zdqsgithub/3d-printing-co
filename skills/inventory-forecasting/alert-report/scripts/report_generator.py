#!/usr/bin/env python3
"""
Report Generator — Builds and formats inventory, sales, and trend digest reports.
Used by the Alert & Report skill for scheduled report delivery.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

# Simulated KPI data
DAILY_KPIS = {
    "printers_active": 87,
    "printers_total": 100,
    "jobs_in_queue": 23,
    "avg_turnaround_days": 2.3,
    "critical_items": 1,
    "warning_items": 2,
    "ok_items": 42,
    "daily_revenue": 1247.00,
    "daily_orders": 18,
    "top_seller": "PLA Black 1kg",
    "top_seller_units": 9,
}

WEEKLY_KPIS = {
    "revenue": 8740.00,
    "revenue_change_pct": 12.0,
    "orders": 127,
    "orders_change_pct": 8.0,
    "avg_order_value": 68.82,
    "new_customers": 14,
    "repeat_rate_pct": 62.0,
    "jobs_completed": 156,
    "printer_utilization_pct": 84.0,
    "failed_prints": 7,
    "fail_rate_pct": 4.5,
    "avg_turnaround_days": 2.1,
}

ACTION_ITEMS = [
    {"priority": "critical", "action": "Reorder PLA White ASAP", "detail": "Est. cost: $3,240 for 180 spools"},
    {"priority": "warning", "action": "Review PETG stock before weekend", "detail": "45 spools, approaching reorder point"},
    {"priority": "info", "action": "Follow up with NinjaTek on TPU delivery", "detail": "Expected delivery: Wed"},
]


def generate_daily_report(kpis: dict, actions: list[dict]) -> str:
    """Generate daily snapshot report."""
    now = datetime.now()
    date_str = now.strftime("%a %b %d, %Y")

    report = f"""📊 DAILY REPORT — {date_str}

🏭 FACTORY STATUS
  🖨️ Printers active: {kpis['printers_active']}/{kpis['printers_total']}
  📋 Jobs in queue: {kpis['jobs_in_queue']}
  ⏱️ Avg turnaround: {kpis['avg_turnaround_days']} days

📦 INVENTORY HEALTH
  🔴 Critical: {kpis['critical_items']} item(s)
  🟡 Warning: {kpis['warning_items']} item(s)
  🟢 OK: {kpis['ok_items']} items

📈 TODAY'S SALES
  💰 Revenue: ${kpis['daily_revenue']:,.2f}
  📦 Orders: {kpis['daily_orders']}
  🏆 Top seller: {kpis['top_seller']} ({kpis['top_seller_units']} units)

⚡ ACTION ITEMS"""

    for i, item in enumerate(actions, 1):
        icon = {"critical": "❌", "warning": "⚠️", "info": "📌"}.get(item["priority"], "•")
        report += f"\n  {i}. {icon} {item['action']}"
        if item.get("detail"):
            report += f" ({item['detail']})"

    return report


def generate_weekly_report(kpis: dict) -> str:
    """Generate weekly summary report."""
    now = datetime.now()
    week_num = now.isocalendar()[1]
    week_start = (now - timedelta(days=now.weekday() + 7)).strftime("%b %d")
    week_end = (now - timedelta(days=now.weekday() + 1)).strftime("%b %d, %Y")

    rev_arrow = "📈" if kpis["revenue_change_pct"] > 0 else "📉"
    ord_arrow = "📈" if kpis["orders_change_pct"] > 0 else "📉"

    report = f"""📊 WEEKLY SUMMARY — Week {week_num} ({week_start}–{week_end})

{rev_arrow} KPI DASHBOARD
  Revenue: ${kpis['revenue']:,.2f} ({'+' if kpis['revenue_change_pct'] > 0 else ''}{kpis['revenue_change_pct']:.0f}% vs last week)
  Orders: {kpis['orders']} ({'+' if kpis['orders_change_pct'] > 0 else ''}{kpis['orders_change_pct']:.0f}%)
  Avg order value: ${kpis['avg_order_value']:.2f}
  New customers: {kpis['new_customers']}
  Repeat rate: {kpis['repeat_rate_pct']:.0f}%

🏭 FACTORY PERFORMANCE
  Jobs completed: {kpis['jobs_completed']}
  Printer utilization: {kpis['printer_utilization_pct']:.0f}%
  Failed prints: {kpis['failed_prints']} ({kpis['fail_rate_pct']:.1f}%)
  Avg turnaround: {kpis['avg_turnaround_days']} days"""

    return report


def generate_critical_alert(item_name: str, current_stock: int, daily_usage: float, recommended_order: int, cost: float) -> str:
    """Generate a critical stock alert."""
    days_left = current_stock / daily_usage if daily_usage > 0 else float("inf")
    now = datetime.now().strftime("%b %d, %Y %H:%M %Z")

    return f"""🚨 CRITICAL ALERT — {now}

❌ {item_name} — {current_stock} REMAINING
   ⚠️ At current usage ({daily_usage:.0f}/day), stockout in {days_left:.1f} days
   📦 Recommended: Rush order {recommended_order} units
   💰 Estimated cost: ${cost:,.2f}

⚡ ACTION REQUIRED:
   Reply "APPROVE" to place rush order
   Reply "HOLD" to defer"""


def main():
    parser = argparse.ArgumentParser(description="Inventory & Sales Report Generator")
    parser.add_argument("--type", type=str, required=True, choices=["daily", "weekly", "critical"],
                        help="Report type to generate")
    parser.add_argument("--channel", type=str, default="console", choices=["console", "telegram", "whatsapp"],
                        help="Delivery channel")
    parser.add_argument("--format", type=str, default="text", choices=["text", "markdown", "json"])
    parser.add_argument("--item", type=str, help="Item SKU for critical alerts")
    parser.add_argument("--kpi", action="store_true", help="Show KPI data only")
    parser.add_argument("--period", type=str, default="daily", choices=["daily", "weekly"])
    args = parser.parse_args()

    if args.kpi:
        kpis = DAILY_KPIS if args.period == "daily" else WEEKLY_KPIS
        if args.format == "json":
            print(json.dumps(kpis, indent=2))
        else:
            for k, v in kpis.items():
                print(f"  {k}: {v}")
        return

    if args.type == "daily":
        report = generate_daily_report(DAILY_KPIS, ACTION_ITEMS)
    elif args.type == "weekly":
        report = generate_weekly_report(WEEKLY_KPIS)
    elif args.type == "critical":
        report = generate_critical_alert(
            item_name="PLA White 1kg",
            current_stock=12,
            daily_usage=8,
            recommended_order=180,
            cost=3240.00,
        )
    else:
        parser.print_help()
        return

    if args.format == "json":
        print(json.dumps({"report_type": args.type, "channel": args.channel, "content": report}, indent=2))
    else:
        print(report)

    if args.channel != "console":
        print(f"\n📤 Report would be delivered to: {args.channel}")


if __name__ == "__main__":
    main()
