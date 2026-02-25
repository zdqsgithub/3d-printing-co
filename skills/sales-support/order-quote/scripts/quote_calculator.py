#!/usr/bin/env python3
"""
Quote Calculator — Generates itemized price quotes for 3D printing service requests.
Used by the Order & Quote skill to provide instant, accurate pricing.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

# Pricing tables
MATERIAL_RATES = {
    "PLA": {"cost_per_gram": 0.03, "machine_rate": 12.00},
    "ABS": {"cost_per_gram": 0.04, "machine_rate": 14.00},
    "PETG": {"cost_per_gram": 0.04, "machine_rate": 13.00},
    "TPU": {"cost_per_gram": 0.06, "machine_rate": 15.00},
    "Nylon": {"cost_per_gram": 0.08, "machine_rate": 16.00},
    "Resin": {"cost_per_gram": 0.07, "machine_rate": 10.00},
}

QUALITY_MODIFIERS = {
    "draft": 0.80,      # -20% time
    "standard": 1.00,
    "fine": 1.25,        # +25% time
    "ultra-fine": 1.60,  # +60% time
}

URGENCY_MODIFIERS = {
    "standard": 1.00,
    "rush": 1.50,        # +50%
    "same-day": 2.00,    # +100%
}

URGENCY_DAYS = {
    "standard": "3–5 business days",
    "rush": "1–2 business days",
    "same-day": "Same day (if ordered before 10 AM)",
}

LABOR_COST_PER_PART = 5.00
MINIMUM_ORDER = 10.00


@dataclass
class Quote:
    quote_id: str
    material: str
    dimensions: str
    weight_grams: float
    print_hours: float
    quality: str
    quantity: int
    urgency: str
    material_cost: float
    machine_cost: float
    labor_cost: float
    subtotal: float
    discount_rate: float
    discount_amount: float
    urgency_surcharge: float
    total: float
    turnaround: str
    valid_until: str


def estimate_weight_from_dimensions(dims_str: str, infill: float = 0.20) -> float:
    """Rough estimate of print weight from LxWxH dimensions string."""
    parts = dims_str.lower().replace("mm", "").split("x")
    if len(parts) != 3:
        raise ValueError(f"Dimensions must be in LxWxH format, got: {dims_str}")
    l, w, h = float(parts[0]), float(parts[1]), float(parts[2])
    volume_cm3 = (l * w * h) / 1000  # mm³ → cm³
    # Assume ~20% infill, 1.24 g/cm³ density (PLA-like)
    weight = volume_cm3 * infill * 1.24
    return round(weight, 1)


def estimate_print_time(weight_grams: float, quality: str) -> float:
    """Rough estimate of print time in hours based on weight."""
    # ~15g/hour at standard quality
    base_rate = 15.0
    modifier = QUALITY_MODIFIERS.get(quality, 1.0)
    hours = (weight_grams / base_rate) * modifier
    return round(max(0.5, hours), 1)  # Minimum 30 min


def get_bulk_discount(quantity: int) -> float:
    """Return bulk discount rate based on quantity."""
    if quantity >= 50:
        return 0.20  # Custom, but start at 20%
    elif quantity >= 25:
        return 0.15
    elif quantity >= 10:
        return 0.10
    return 0.0


def calculate_quote(
    material: str,
    weight_grams: float,
    print_hours: float,
    quality: str = "standard",
    quantity: int = 1,
    urgency: str = "standard",
    dimensions: str = "",
) -> Quote:
    """Calculate a full itemized quote."""
    material = material.upper() if material.upper() != "NYLON" else "Nylon"
    # Normalize material name
    mat_key = material if material in MATERIAL_RATES else material.upper()
    for k in MATERIAL_RATES:
        if k.upper() == mat_key.upper():
            mat_key = k
            break

    if mat_key not in MATERIAL_RATES:
        raise ValueError(f"Unknown material: {material}. Options: {list(MATERIAL_RATES.keys())}")

    rates = MATERIAL_RATES[mat_key]
    quality_mod = QUALITY_MODIFIERS.get(quality.lower(), 1.0)

    material_cost = weight_grams * rates["cost_per_gram"]
    machine_cost = print_hours * rates["machine_rate"] * quality_mod
    labor_cost = LABOR_COST_PER_PART
    per_unit = material_cost + machine_cost + labor_cost
    subtotal = per_unit * quantity

    discount_rate = get_bulk_discount(quantity)
    discount_amount = subtotal * discount_rate
    after_discount = subtotal - discount_amount

    urgency_mod = URGENCY_MODIFIERS.get(urgency.lower(), 1.0)
    urgency_surcharge = after_discount * (urgency_mod - 1.0)
    total = after_discount + urgency_surcharge

    total = max(total, MINIMUM_ORDER)

    quote_id = f"QT-{datetime.now().strftime('%Y%m%d')}-{abs(hash(f'{material}{dimensions}{quantity}')) % 1000:03d}"
    valid_until = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    return Quote(
        quote_id=quote_id,
        material=mat_key,
        dimensions=dimensions or "N/A",
        weight_grams=weight_grams,
        print_hours=print_hours,
        quality=quality,
        quantity=quantity,
        urgency=urgency,
        material_cost=round(material_cost, 2),
        machine_cost=round(machine_cost, 2),
        labor_cost=round(labor_cost, 2),
        subtotal=round(subtotal, 2),
        discount_rate=discount_rate,
        discount_amount=round(discount_amount, 2),
        urgency_surcharge=round(urgency_surcharge, 2),
        total=round(total, 2),
        turnaround=URGENCY_DAYS.get(urgency.lower(), "3–5 business days"),
        valid_until=valid_until,
    )


def format_quote(q: Quote) -> str:
    """Format quote for display."""
    lines = [
        f"📋 Quote #{q.quote_id}",
        f"{'='*40}",
        f"Material: {q.material} | Quality: {q.quality}",
        f"Dimensions: {q.dimensions} | Weight: {q.weight_grams}g",
        f"Print time: {q.print_hours}hr | Quantity: {q.quantity}",
        f"",
        f"  Material cost:    ${q.material_cost:>8.2f}",
        f"  Machine time:     ${q.machine_cost:>8.2f}",
        f"  Setup & finish:   ${q.labor_cost:>8.2f}",
    ]
    if q.quantity > 1:
        lines.append(f"  × {q.quantity} units:      ${q.subtotal:>8.2f}")
    if q.discount_rate > 0:
        lines.append(f"  Bulk discount ({q.discount_rate:.0%}): -${q.discount_amount:>7.2f}")
    if q.urgency_surcharge > 0:
        lines.append(f"  {q.urgency.title()} surcharge: +${q.urgency_surcharge:>7.2f}")
    lines.extend([
        f"  {'─'*30}",
        f"  TOTAL:            ${q.total:>8.2f}",
        f"",
        f"  ⏱️  Turnaround: {q.turnaround}",
        f"  📅 Valid until: {q.valid_until}",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="3D Printing Quote Calculator")
    parser.add_argument("--material", type=str, required=True, help="Material: PLA, ABS, PETG, TPU, Nylon, Resin")
    parser.add_argument("--dimensions", type=str, help="Dimensions in LxWxH mm (e.g., 80x60x40)")
    parser.add_argument("--weight", type=float, help="Weight in grams (if known)")
    parser.add_argument("--hours", type=float, help="Print time in hours (if known)")
    parser.add_argument("--quality", type=str, default="standard", choices=["draft", "standard", "fine", "ultra-fine"])
    parser.add_argument("--quantity", type=int, default=1, help="Number of copies")
    parser.add_argument("--urgency", type=str, default="standard", choices=["standard", "rush", "same-day"])
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    # Determine weight and time
    weight = args.weight
    hours = args.hours

    if weight is None and args.dimensions:
        weight = estimate_weight_from_dimensions(args.dimensions)
    if weight is None:
        print("Error: Provide either --dimensions or --weight", file=sys.stderr)
        sys.exit(1)
    if hours is None:
        hours = estimate_print_time(weight, args.quality)

    quote = calculate_quote(
        material=args.material,
        weight_grams=weight,
        print_hours=hours,
        quality=args.quality,
        quantity=args.quantity,
        urgency=args.urgency,
        dimensions=args.dimensions or "",
    )

    if args.json:
        print(json.dumps(asdict(quote), indent=2))
    else:
        print(format_quote(quote))


if __name__ == "__main__":
    main()
