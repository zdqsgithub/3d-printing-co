#!/usr/bin/env python3
"""
Product Catalog Helper — Searches and filters the 3D printing product catalog.
Used by the Product Recommender skill to look up real-time product data.
"""

import argparse
import json
import sys
from pathlib import Path

CATALOG_PATH = Path(__file__).parent.parent / "resources" / "catalog.json"


def load_catalog() -> list[dict]:
    """Load the product catalog from JSON."""
    if not CATALOG_PATH.exists():
        print(f"Error: Catalog not found at {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def search_products(catalog: list[dict], query: str) -> list[dict]:
    """Search products by name, category, or description."""
    query_lower = query.lower()
    results = []
    for product in catalog:
        searchable = f"{product['name']} {product['category']} {product['description']} {' '.join(product.get('tags', []))}".lower()
        if query_lower in searchable:
            results.append(product)
    return results


def filter_by_category(catalog: list[dict], category: str) -> list[dict]:
    """Filter products by category."""
    return [p for p in catalog if p["category"].lower() == category.lower()]


def filter_by_budget(products: list[dict], max_price: float) -> list[dict]:
    """Filter products by maximum price."""
    return [p for p in products if p["price"] <= max_price]


def filter_by_experience(products: list[dict], level: str) -> list[dict]:
    """Filter products by experience level."""
    return [p for p in products if level.lower() in [l.lower() for l in product.get("experience_levels", ["all"])]]


def format_product(product: dict) -> str:
    """Format a single product for display."""
    lines = [
        f"  📦 {product['name']}",
        f"     Category: {product['category']}",
        f"     Price: ${product['price']:.2f}",
        f"     Description: {product['description']}",
    ]
    if product.get("in_stock") is not None:
        status = "✅ In Stock" if product["in_stock"] else "❌ Out of Stock"
        lines.append(f"     Status: {status}")
    if product.get("tags"):
        lines.append(f"     Tags: {', '.join(product['tags'])}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="3D Printing Product Catalog Search")
    parser.add_argument("--search", type=str, help="Search query (name, category, description)")
    parser.add_argument("--category", type=str, choices=["printers", "filament", "resin", "accessories", "services"],
                        help="Filter by category")
    parser.add_argument("--budget", type=float, help="Maximum price filter")
    parser.add_argument("--list", action="store_true", help="List all products")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    catalog = load_catalog()
    results = catalog

    if args.search:
        results = search_products(results, args.search)
    if args.category:
        results = filter_by_category(results, args.category)
    if args.budget:
        results = filter_by_budget(results, args.budget)
    if not args.list and not args.search and not args.category:
        parser.print_help()
        return

    if not results:
        print("No products found matching your criteria.")
        return

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n🔍 Found {len(results)} product(s):\n")
        for product in results:
            print(format_product(product))
            print()


if __name__ == "__main__":
    main()
