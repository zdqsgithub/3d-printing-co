#!/usr/bin/env python3
"""
Content Drafter — Generates social media, newsletter, and blog content drafts.
Used by the Content Generation skill for automated marketing content.
"""

import argparse
import json
import sys
from datetime import datetime
from dataclasses import dataclass, asdict

CONTENT_CALENDAR = {
    1: "Product Spotlight",
    2: "How-To / Tutorial",
    3: "Customer Story",
    4: "Industry / Trend",
}

PLATFORM_LIMITS = {
    "instagram": {"chars": 2200, "hashtags": 30},
    "linkedin": {"chars": 3000, "hashtags": 5},
    "twitter": {"chars": 280, "hashtags": 3},
    "blog": {"words_min": 600, "words_max": 1200},
    "newsletter": {"sections": 4, "read_time_max": 5},
}

HASHTAG_BANK = {
    "general": ["#3DPrinting", "#3DPrinterLA", "#MadeInLA", "#Maker", "#MakerMovement", "#3DPrintingCommunity"],
    "filament": ["#PLA", "#PETG", "#ABS", "#Filament", "#FilamentDrop", "#3DPrintMaterial"],
    "resin": ["#ResinPrinting", "#SLA", "#Miniatures", "#DetailedPrints"],
    "service": ["#3DPrintingService", "#RapidPrototyping", "#CustomParts", "#MadeToOrder"],
    "education": ["#STEM", "#Education", "#MakerEd", "#LearnByDoing"],
    "business": ["#B2B", "#Prototyping", "#ProductDesign", "#Manufacturing"],
}


@dataclass
class ContentDraft:
    content_type: str
    platform: str
    topic: str
    draft: str
    hashtags: list
    image_suggestion: str
    cta: str
    word_count: int
    created: str


def generate_instagram_post(topic: str) -> ContentDraft:
    """Generate an Instagram post draft."""
    draft = f"""🔥 [HOOK about {topic} — make it scroll-stopping]

[2-3 sentences about {topic} — what makes it exciting, who it's for]

[Social proof: "Our customers are loving..." or stat]

[CTA: Price + "link in bio" or "DM us for a quote"]

.
.
.

{' '.join(HASHTAG_BANK['general'][:5])}
{' '.join(HASHTAG_BANK['filament'][:3])}"""

    return ContentDraft(
        content_type="social_media",
        platform="instagram",
        topic=topic,
        draft=draft,
        hashtags=HASHTAG_BANK["general"][:5] + HASHTAG_BANK["filament"][:3],
        image_suggestion=f"Close-up or lifestyle shot of {topic}. Bright lighting, clean background, maybe a timelapse of printing.",
        cta="Link in bio to shop. Free local delivery in LA on orders over $50!",
        word_count=len(draft.split()),
        created=datetime.now().isoformat(),
    )


def generate_linkedin_post(topic: str) -> ContentDraft:
    """Generate a LinkedIn post draft."""
    draft = f"""[Bold opening question or statement about {topic}]

In the 3D printing world, [explain the topic's significance in 2-3 sentences].

Here's what we're seeing at our LA factory:

• [Key insight 1]
• [Key insight 2]  
• [Key insight 3]

For businesses in the LA area, this means [business value proposition].

[Soft CTA: "Curious how 3D printing could help your business? Let's chat."]

#3DPrinting #Manufacturing #LosAngeles"""

    return ContentDraft(
        content_type="social_media",
        platform="linkedin",
        topic=topic,
        draft=draft,
        hashtags=["#3DPrinting", "#Manufacturing", "#LosAngeles"],
        image_suggestion=f"Professional photo related to {topic} — factory floor, finished parts, or team at work.",
        cta="DM us or visit our website for a free consultation.",
        word_count=len(draft.split()),
        created=datetime.now().isoformat(),
    )


def generate_blog_outline(topic: str, seo_keywords: list = None) -> ContentDraft:
    """Generate a blog article outline."""
    keywords = seo_keywords or [topic, "3D printing", "LA"]
    keyword_str = ", ".join(keywords)

    draft = f"""# [SEO Title about {topic} — 55-60 chars, include "{keywords[0]}"]

**Meta description**: [150-160 chars summarizing the article, include "{keywords[0]}"]
**Target keywords**: {keyword_str}

## Introduction
[Hook the reader — pose a question or surprising fact about {topic}. 100 words.]

## [Main Section: What Is {topic}?]
[Explain the concept clearly for beginners. 200-300 words. Include comparison table if relevant.]

## [Practical Guide: How to {topic}]
[Step-by-step instructions or numbered tips. 200-300 words.]

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Step 4]
5. [Step 5]

## [Why This Matters for Your Projects]
[Connect to reader's needs — hobbyist, business, education angles. 150 words.]

## Get Started with [Topic]
[Mention our products/services that relate. Soft sell. 100 words.]

**CTA**: [Shop now / Get a quote / Visit our showroom]

---
**Related Products**: [3 product suggestions from catalog]
**Related Articles**: [2-3 internal links to other blog posts]"""

    return ContentDraft(
        content_type="blog",
        platform="blog",
        topic=topic,
        draft=draft,
        hashtags=[],
        image_suggestion=f"Hero image for {topic} — high quality, original photo or well-edited stock.",
        cta="Shop our products or get a free quote for our printing service.",
        word_count=len(draft.split()),
        created=datetime.now().isoformat(),
    )


def generate_newsletter(topic: str = None, sections: int = 4) -> ContentDraft:
    """Generate a newsletter draft."""
    draft = f"""**Subject**: 🖨️ [Compelling subject line about {topic or 'this month in 3D printing'}]
**Preview**: [25-50 char preview text]

---

## 🌟 Featured: [Main story about {topic or 'our latest product/service'}]
[150 words max — the hero content piece]

---

## 🛒 Product Spotlight
[100 words — feature a product with image, price, and direct link]

---

## 💡 Quick Tip
[75 words — practical 3D printing tip readers can use immediately]

---

## 📢 Community & Events
[50 words — customer spotlight, upcoming workshops, or local maker events in LA]

---

**[CTA BUTTON: "Shop New Arrivals" / "Get a Free Quote"]**

---
📍 Visit our LA showroom | 📧 support@3dprintco.com
[Social icons] [Unsubscribe link]"""

    return ContentDraft(
        content_type="newsletter",
        platform="email",
        topic=topic or "Monthly Newsletter",
        draft=draft,
        hashtags=[],
        image_suggestion="Header banner with brand colors. Product photos for spotlight section.",
        cta="Shop New Arrivals or Get a Free Quote",
        word_count=len(draft.split()),
        created=datetime.now().isoformat(),
    )


def show_calendar(month: int = None) -> str:
    """Show content calendar for the month."""
    month = month or datetime.now().month
    month_name = datetime(2026, month, 1).strftime("%B %Y")

    lines = [f"📅 CONTENT CALENDAR — {month_name}", "=" * 40, ""]
    for week, theme in CONTENT_CALENDAR.items():
        lines.append(f"  Week {week}: {theme}")
        if theme == "Product Spotlight":
            lines.append("    📸 Instagram carousel + Blog deep-dive + Newsletter")
        elif theme == "How-To / Tutorial":
            lines.append("    🎬 Instagram reel script + Blog + LinkedIn article")
        elif theme == "Customer Story":
            lines.append("    📱 Instagram post + LinkedIn + Email case study")
        elif theme == "Industry / Trend":
            lines.append("    🐦 Twitter thread + Blog analysis + Newsletter")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Marketing Content Drafter")
    parser.add_argument("--type", type=str, choices=["instagram", "linkedin", "twitter", "blog", "newsletter"],
                        help="Content type to generate")
    parser.add_argument("--topic", type=str, help="Content topic")
    parser.add_argument("--seo-keywords", type=str, help="Comma-separated SEO keywords")
    parser.add_argument("--sections", type=int, default=4, help="Newsletter sections")
    parser.add_argument("--calendar", action="store_true", help="Show content calendar")
    parser.add_argument("--month", type=int, help="Month for calendar (1-12)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    if args.calendar:
        print(show_calendar(args.month))
        return

    topic = args.topic or "3D printing"

    if args.type == "instagram":
        draft = generate_instagram_post(topic)
    elif args.type == "linkedin":
        draft = generate_linkedin_post(topic)
    elif args.type == "blog":
        keywords = args.seo_keywords.split(",") if args.seo_keywords else None
        draft = generate_blog_outline(topic, keywords)
    elif args.type == "newsletter":
        draft = generate_newsletter(topic, args.sections)
    else:
        parser.print_help()
        return

    if args.json:
        print(json.dumps(asdict(draft), indent=2))
    else:
        print(f"📝 {draft.platform.upper()} DRAFT — {draft.topic}")
        print("=" * 50)
        print(draft.draft)
        print("\n" + "-" * 50)
        print(f"📸 Image suggestion: {draft.image_suggestion}")
        print(f"🎯 CTA: {draft.cta}")
        print(f"📊 Word count: {draft.word_count}")


if __name__ == "__main__":
    main()
