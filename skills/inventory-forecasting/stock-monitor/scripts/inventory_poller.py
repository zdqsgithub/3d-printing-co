#!/usr/bin/env python3
"""
Inventory Poller — Monitors stock levels and generates reorder alerts.
Used by the Stock Monitor skill for automated inventory tracking.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from pathlib import Path

# Sample inventory data (in production, this would connect to Shopify/DB API)
SAMPLE_INVENTORY = [
    {"sku": "FIL-PLA-WHT", "name": "PLA White 1kg", "category": "filament", "current_stock": 12, "avg_daily_usage": 8, "lead_time_days": 5, "safety_factor": 1.5, "max_stock": 200, "unit_cost": 18.00, "supplier": "PolyMaker"},
    {"sku": "FIL-PLA-BLK", "name": "PLA Black 1kg", "category": "filament", "current_stock": 95, "avg_daily_usage": 10, "lead_time_days": 5, "safety_factor": 1.5, "max_stock": 200, "unit_cost": 18.00, "supplier": "PolyMaker"},
    {"sku": "FIL-PETG-BLK", "name": "PETG Black 1kg", "category": "filament", "current_stock": 45, "avg_daily_usage": 3, "lead_time_days": 5, "safety_factor": 1.5, "max_stock": 200, "unit_cost": 20.00, "supplier": "eSun"},
    {"sku": "FIL-ABS-GRY", "name": "ABS Grey 1kg", "category": "filament", "current_stock": 68, "avg_daily_usage": 2, "lead_time_days": 5, "safety_factor": 1.5, "max_stock": 150, "unit_cost": 22.00, "supplier": "eSun"},
    {"sku": "FIL-TPU-BLU", "name": "TPU Blue 1kg", "category": "filament", "current_stock": 30, "avg_daily_usage": 1, "lead_time_days": 7, "safety_factor": 1.5, "max_stock": 50, "unit_cost": 28.00, "supplier": "NinjaTek"},
    {"sku": "RES-STD-GRY", "name": "Standard Resin Grey 1L", "category": "resin", "current_stock": 25, "avg_daily_usage": 2, "lead_time_days": 7, "safety_factor": 1.5, "max_stock": 100, "unit_cost": 25.00, "supplier": "Elegoo"},
    {"sku": "ACC-NZL-04", "name": "0.4mm Brass Nozzles", "category": "parts", "current_stock": 52, "avg_daily_usage": 4, "lead_time_days": 3, "safety_factor": 1.2, "max_stock": 500, "unit_cost": 1.50, "supplier": "Generic"},
    {"sku": "ACC-PEI-235", "name": "PEI Sheet 235x235mm", "category": "parts", "current_stock": 40, "avg_daily_usage": 1, "lead_time_days": 7, "safety_factor": 1.5, "max_stock": 100, "unit_cost": 12.00, "supplier": "Generic"},
    {"sku": "ACC-PTFE-TUBE", "name": "PTFE Tube 1m", "category": "parts", "current_stock": 85, "avg_daily_usage": 2, "lead_time_days": 5, "safety_factor": 1.5, "max_stock": 200, "unit_cost": 3.00, "supplier": "Capricorn"},
]


@dataclass
class StockAlert:
    sku: str
    name: str
    category: str
    current_stock: int
    reorder_point: int
    safety_stock: int
    avg_daily_usage: float
    lead_time_days: int
    recommended_order: int
    estimated_cost: float
    severity: str  # "critical", "warning", "ok"
    days_until_stockout: float
    supplier: str


def calculate_reorder_point(item: dict) -> tuple[int, int, int]:
    """Calculate safety stock, reorder point, and recommended order quantity."""
    safety_stock = int(item["avg_daily_usage"] * item["lead_time_days"] * item["safety_factor"])
    reorder_point = safety_stock + int(item["avg_daily_usage"] * item["lead_time_days"])
    reorder_qty = max(0, item["max_stock"] - item["current_stock"] + safety_stock)
    return safety_stock, reorder_point, reorder_qty


def check_stock(inventory: list[dict]) -> list[StockAlert]:
    """Check all inventory items against thresholds."""
    alerts = []
    for item in inventory:
        safety_stock, reorder_point, reorder_qty = calculate_reorder_point(item)

        if item["avg_daily_usage"] > 0:
            days_left = item["current_stock"] / item["avg_daily_usage"]
        else:
            days_left = float("inf")

        if item["current_stock"] == 0:
            severity = "emergency"
        elif item["current_stock"] <= safety_stock:
            severity = "critical"
        elif item["current_stock"] <= reorder_point:
            severity = "warning"
        else:
            severity = "ok"

        alerts.append(StockAlert(
            sku=item["sku"],
            name=item["name"],
            category=item["category"],
            current_stock=item["current_stock"],
            reorder_point=reorder_point,
            safety_stock=safety_stock,
            avg_daily_usage=item["avg_daily_usage"],
            lead_time_days=item["lead_time_days"],
            recommended_order=reorder_qty,
            estimated_cost=round(reorder_qty * item["unit_cost"], 2),
            severity=severity,
            days_until_stockout=round(days_left, 1),
            supplier=item["supplier"],
        ))
    return alerts


def format_alerts(alerts: list[StockAlert], critical_only: bool = False) -> str:
    """Format alerts for display."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M %Z")
    lines = [f"📊 STOCK REPORT — {now}", "=" * 50, ""]

    emergency = [a for a in alerts if a.severity == "emergency"]
    critical = [a for a in alerts if a.severity == "critical"]
    warning = [a for a in alerts if a.severity == "warning"]
    ok = [a for a in alerts if a.severity == "ok"]

    if emergency:
        lines.append("🆘 EMERGENCY (Out of Stock):")
        for a in emergency:
            lines.append(f"  💀 {a.name} ({a.sku}) — ZERO STOCK")
            lines.append(f"     ⚡ Recommended order: {a.recommended_order} units (${a.estimated_cost:.2f})")
            lines.append("")

    if critical:
        lines.append("🚨 CRITICAL (Below Safety Stock):")
        for a in critical:
            lines.append(f"  ❌ {a.name} ({a.sku}) — {a.current_stock} left")
            lines.append(f"     Usage: {a.avg_daily_usage}/day | Stockout in: {a.days_until_stockout} days")
            lines.append(f"     ⚡ Recommended order: {a.recommended_order} units (${a.estimated_cost:.2f})")
            lines.append("")

    if not critical_only:
        if warning:
            lines.append("⚠️ WARNING (Approaching Reorder Point):")
            for a in warning:
                lines.append(f"  ⚠️ {a.name} ({a.sku}) — {a.current_stock} left")
                lines.append(f"     Usage: {a.avg_daily_usage}/day | Reorder at: {a.reorder_point}")
                lines.append(f"     📦 Recommended order: {a.recommended_order} units (${a.estimated_cost:.2f})")
                lines.append("")

        lines.append(f"✅ OK: {len(ok)} items within normal range")

    total_cost = sum(a.estimated_cost for a in alerts if a.severity in ("emergency", "critical", "warning"))
    lines.extend(["", f"💰 Total reorder cost estimate: ${total_cost:,.2f}"])

    return "\n".join(lines)


def consumption_report(inventory: list[dict], days: int = 7) -> str:
    """Generate consumption trend report."""
    lines = [f"📈 CONSUMPTION REPORT ({days}-day projection)", "=" * 50, ""]
    lines.append(f"{'Item':<30} {'Daily':>6} {f'{days}d Total':>10} {'Stock':>7} {'Days Left':>10}")
    lines.append("-" * 70)

    for item in sorted(inventory, key=lambda x: x["avg_daily_usage"], reverse=True):
        projected = item["avg_daily_usage"] * days
        days_left = item["current_stock"] / item["avg_daily_usage"] if item["avg_daily_usage"] > 0 else float("inf")
        flag = " ⚠️" if days_left < days else ""
        lines.append(
            f"{item['name']:<30} {item['avg_daily_usage']:>6.1f} {projected:>10.0f} {item['current_stock']:>7} {days_left:>9.1f}d{flag}"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Inventory Stock Monitor")
    parser.add_argument("--check-all", action="store_true", help="Check all inventory levels")
    parser.add_argument("--category", type=str, help="Filter by category: filament, resin, parts")
    parser.add_argument("--threshold", action="store_true", help="Show reorder thresholds")
    parser.add_argument("--critical-only", action="store_true", help="Show only critical/emergency items")
    parser.add_argument("--consumption-report", action="store_true", help="Show consumption trend report")
    parser.add_argument("--days", type=int, default=7, help="Days for consumption projection")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    inventory = SAMPLE_INVENTORY
    if args.category:
        inventory = [i for i in inventory if i["category"] == args.category]

    if args.consumption_report:
        print(consumption_report(inventory, args.days))
        return

    if args.check_all or args.critical_only or args.category:
        alerts = check_stock(inventory)
        if args.json:
            print(json.dumps([asdict(a) for a in alerts], indent=2))
        else:
            print(format_alerts(alerts, critical_only=args.critical_only))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
