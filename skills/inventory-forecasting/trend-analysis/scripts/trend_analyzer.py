#!/usr/bin/env python3
"""
Trend Analyzer — Detects demand spikes and market trends for 3D printing products.
Used by the Trend Analysis skill for market intelligence.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Optional

# Simulated order history data (in production, this connects to your order database)
SAMPLE_ORDER_HISTORY = [
    {"date": "2026-02-17", "sku": "FIL-PLA-WHT", "product": "PLA White 1kg", "category": "filament", "quantity": 45, "revenue": 810.00},
    {"date": "2026-02-17", "sku": "FIL-PLA-BLK", "product": "PLA Black 1kg", "category": "filament", "quantity": 52, "revenue": 936.00},
    {"date": "2026-02-17", "sku": "FIL-PETG-BLK", "product": "PETG Black 1kg", "category": "filament", "quantity": 18, "revenue": 396.00},
    {"date": "2026-02-17", "sku": "RES-STD-GRY", "product": "Standard Resin Grey 1L", "category": "resin", "quantity": 12, "revenue": 300.00},
    {"date": "2026-02-17", "sku": "SVC-DIY", "product": "DIY Printing Service", "category": "services", "quantity": 8, "revenue": 320.00},
    {"date": "2026-02-10", "sku": "FIL-PLA-WHT", "product": "PLA White 1kg", "category": "filament", "quantity": 38, "revenue": 684.00},
    {"date": "2026-02-10", "sku": "FIL-PLA-BLK", "product": "PLA Black 1kg", "category": "filament", "quantity": 48, "revenue": 864.00},
    {"date": "2026-02-10", "sku": "FIL-PETG-BLK", "product": "PETG Black 1kg", "category": "filament", "quantity": 22, "revenue": 484.00},
    {"date": "2026-02-10", "sku": "RES-STD-GRY", "product": "Standard Resin Grey 1L", "category": "resin", "quantity": 9, "revenue": 225.00},
    {"date": "2026-02-10", "sku": "SVC-DIY", "product": "DIY Printing Service", "category": "services", "quantity": 6, "revenue": 240.00},
    {"date": "2026-02-03", "sku": "FIL-PLA-WHT", "product": "PLA White 1kg", "category": "filament", "quantity": 32, "revenue": 576.00},
    {"date": "2026-02-03", "sku": "FIL-PLA-BLK", "product": "PLA Black 1kg", "category": "filament", "quantity": 41, "revenue": 738.00},
    {"date": "2026-02-03", "sku": "FIL-PETG-BLK", "product": "PETG Black 1kg", "category": "filament", "quantity": 20, "revenue": 440.00},
    {"date": "2026-02-03", "sku": "RES-STD-GRY", "product": "Standard Resin Grey 1L", "category": "resin", "quantity": 7, "revenue": 175.00},
    {"date": "2026-02-03", "sku": "SVC-DIY", "product": "DIY Printing Service", "category": "services", "quantity": 5, "revenue": 200.00},
]

SEASONAL_TRENDS = {
    1: {"label": "Post-Holiday Slow", "modifier": 0.75, "note": "Reduced demand after holiday season"},
    2: {"label": "Winter Projects", "modifier": 0.85, "note": "Indoor projects, still slow"},
    3: {"label": "Spring Rising", "modifier": 1.00, "note": "Project season starting"},
    4: {"label": "Spring Peak", "modifier": 1.10, "note": "School projects, spring builds"},
    5: {"label": "School Projects", "modifier": 1.15, "note": "End-of-year school projects"},
    6: {"label": "Summer Start", "modifier": 1.10, "note": "Maker season beginning"},
    7: {"label": "Maker Peak", "modifier": 1.25, "note": "Peak maker/hobbyist season"},
    8: {"label": "Late Summer", "modifier": 1.20, "note": "Still high, conventions"},
    9: {"label": "Back to School", "modifier": 1.10, "note": "Education + Halloween prep"},
    10: {"label": "Halloween/Fall", "modifier": 1.15, "note": "Costume parts, props, etc."},
    11: {"label": "Holiday Ramp", "modifier": 1.30, "note": "Gift buying begins"},
    12: {"label": "Holiday Peak", "modifier": 1.40, "note": "Maximum gift season"},
}


@dataclass
class TrendResult:
    product: str
    sku: str
    category: str
    current_period_qty: int
    previous_period_qty: int
    growth_rate_pct: float
    direction: str  # "up", "down", "stable"
    confidence: str  # "HIGH", "MEDIUM", "LOW"
    action: str


def analyze_trends(orders: list[dict], period_days: int = 7) -> list[TrendResult]:
    """Analyze order trends by comparing current and previous periods."""
    now = datetime.strptime("2026-02-24", "%Y-%m-%d")
    current_start = now - timedelta(days=period_days)
    previous_start = current_start - timedelta(days=period_days)

    results = []
    products = set((o["sku"], o["product"], o["category"]) for o in orders)

    for sku, product, category in products:
        current_qty = sum(
            o["quantity"] for o in orders
            if o["sku"] == sku and datetime.strptime(o["date"], "%Y-%m-%d") >= current_start
        )
        previous_qty = sum(
            o["quantity"] for o in orders
            if o["sku"] == sku and previous_start <= datetime.strptime(o["date"], "%Y-%m-%d") < current_start
        )

        if previous_qty > 0:
            growth = ((current_qty - previous_qty) / previous_qty) * 100
        elif current_qty > 0:
            growth = 100.0
        else:
            growth = 0.0

        if growth > 20:
            direction = "up"
            confidence = "HIGH" if abs(growth) > 30 else "MEDIUM"
            action = "Increase stock levels, consider promotional push"
        elif growth < -20:
            direction = "down"
            confidence = "HIGH" if abs(growth) > 30 else "MEDIUM"
            action = "Reduce reorder quantity, investigate cause"
        else:
            direction = "stable"
            confidence = "HIGH"
            action = "Maintain current levels"

        results.append(TrendResult(
            product=product,
            sku=sku,
            category=category,
            current_period_qty=current_qty,
            previous_period_qty=previous_qty,
            growth_rate_pct=round(growth, 1),
            direction=direction,
            confidence=confidence,
            action=action,
        ))

    return sorted(results, key=lambda x: abs(x.growth_rate_pct), reverse=True)


def format_trend_report(trends: list[TrendResult], period: str = "weekly") -> str:
    """Format trend analysis as a readable report."""
    now = datetime.now().strftime("%Y-%m-%d")
    lines = [f"📈 {period.upper()} TREND REPORT — {now}", "=" * 50, ""]

    up_trends = [t for t in trends if t.direction == "up"]
    down_trends = [t for t in trends if t.direction == "down"]
    stable = [t for t in trends if t.direction == "stable"]

    if up_trends:
        lines.append("🔥 TRENDING UP:")
        for t in up_trends:
            lines.append(f"  📊 {t.product} — +{t.growth_rate_pct:.0f}% (Confidence: {t.confidence})")
            lines.append(f"     This period: {t.current_period_qty} | Previous: {t.previous_period_qty}")
            lines.append(f"     Action: {t.action}")
            lines.append("")

    if down_trends:
        lines.append("📉 TRENDING DOWN:")
        for t in down_trends:
            lines.append(f"  📊 {t.product} — {t.growth_rate_pct:.0f}% (Confidence: {t.confidence})")
            lines.append(f"     This period: {t.current_period_qty} | Previous: {t.previous_period_qty}")
            lines.append(f"     Action: {t.action}")
            lines.append("")

    if stable:
        lines.append(f"➡️ STABLE: {len(stable)} items with <20% change")

    # Seasonal note
    month = datetime.now().month
    seasonal = SEASONAL_TRENDS.get(month, {})
    if seasonal:
        lines.extend([
            "",
            f"📅 SEASONAL NOTE ({seasonal['label']}):",
            f"   Demand modifier: {seasonal['modifier']:.0%} of baseline",
            f"   {seasonal['note']}",
        ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="3D Printing Trend Analyzer")
    parser.add_argument("--period", type=str, default="weekly", choices=["weekly", "monthly", "quarterly"])
    parser.add_argument("--product", type=str, help="Filter by product name")
    parser.add_argument("--history", type=int, default=30, help="Days of history to analyze")
    parser.add_argument("--seasonal", action="store_true", help="Show seasonal forecast")
    parser.add_argument("--month", type=int, help="Month for seasonal forecast (1-12)")
    parser.add_argument("--format", type=str, default="report", choices=["report", "json"])
    args = parser.parse_args()

    if args.seasonal:
        month = args.month or datetime.now().month
        s = SEASONAL_TRENDS[month]
        print(f"📅 Seasonal Forecast for Month {month}: {s['label']}")
        print(f"   Demand modifier: {s['modifier']:.0%}")
        print(f"   {s['note']}")
        return

    orders = SAMPLE_ORDER_HISTORY
    if args.product:
        orders = [o for o in orders if args.product.lower() in o["product"].lower()]

    period_days = {"weekly": 7, "monthly": 30, "quarterly": 90}[args.period]
    trends = analyze_trends(orders, period_days)

    if args.format == "json":
        print(json.dumps([asdict(t) for t in trends], indent=2))
    else:
        print(format_trend_report(trends, args.period))


if __name__ == "__main__":
    main()
