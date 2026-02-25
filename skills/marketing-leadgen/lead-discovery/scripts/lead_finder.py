#!/usr/bin/env python3
"""
Lead Finder — Discovers and scores potential B2B customers for 3D printing services.
Used by the Lead Discovery skill for targeted business prospecting.
"""

import argparse
import json
import csv
import sys
from datetime import datetime
from dataclasses import dataclass, asdict, field

TARGET_INDUSTRIES = [
    "architecture", "product design", "education", "medical devices",
    "dental", "jewelry", "film/entertainment", "automotive",
    "real estate", "startups"
]

# Sample leads database (in production, populated by web search)
SAMPLE_LEADS = [
    {
        "company": "Morphosis Architects",
        "industry": "architecture",
        "location": "Culver City, CA",
        "employees": 150,
        "website": "morphosis.com",
        "email": "info@morphosis.com",
        "phone": "(310) 555-0101",
        "linkedin": "linkedin.com/company/morphosis-architects",
        "why_3d_printing": "Award-winning firm known for complex geometries. Currently uses foam-core models.",
        "pitch_angle": "Your Pritzker Prize-winning designs deserve models that match their complexity. We can print 1:100 scale models in 48 hours.",
        "score_breakdown": {"industry_fit": 15, "location": 10, "company_size": 10, "website": 5, "need_indicators": 25, "accessibility": 20},
    },
    {
        "company": "JFAK Architects",
        "industry": "architecture",
        "location": "Downtown LA",
        "employees": 45,
        "website": "jfrankarchitects.com",
        "email": "studio@jfak.net",
        "phone": "(213) 555-0202",
        "linkedin": "linkedin.com/company/jfak-architects",
        "why_3d_printing": "Specializes in mixed-use developments. Job posting mentions physical modeling.",
        "pitch_angle": "Mixed-use development models with removable floors for client presentations — printed next-day.",
        "score_breakdown": {"industry_fit": 15, "location": 10, "company_size": 10, "website": 5, "need_indicators": 20, "accessibility": 20},
    },
    {
        "company": "Prototype Studios LA",
        "industry": "product design",
        "location": "Arts District, LA",
        "employees": 12,
        "website": "prototypestudiosla.com",
        "email": "hello@prototypestudiosla.com",
        "phone": "(323) 555-0303",
        "linkedin": "linkedin.com/company/prototype-studios-la",
        "why_3d_printing": "Product design consultancy currently outsourcing prototyping to a shop in OC.",
        "pitch_angle": "Cut your prototyping turnaround from 2 weeks to 2 days — we're right here in the Arts District.",
        "score_breakdown": {"industry_fit": 15, "location": 10, "company_size": 10, "website": 5, "need_indicators": 25, "accessibility": 25},
    },
    {
        "company": "SoCal STEM Academy",
        "industry": "education",
        "location": "Pasadena, CA",
        "employees": 35,
        "website": "socalstemacademy.edu",
        "email": "admin@socalstemacademy.edu",
        "phone": "(626) 555-0404",
        "linkedin": None,
        "why_3d_printing": "STEM-focused school with robotics program but no 3D printing lab yet.",
        "pitch_angle": "Launch your 3D printing lab with our education bundle — printer, materials, and curriculum support for under $500.",
        "score_breakdown": {"industry_fit": 15, "location": 10, "company_size": 10, "website": 5, "need_indicators": 20, "accessibility": 15},
    },
    {
        "company": "MedTech Innovations",
        "industry": "medical devices",
        "location": "El Segundo, CA",
        "employees": 28,
        "website": "medtechinnovations.io",
        "email": "contact@medtechinnovations.io",
        "phone": "(310) 555-0505",
        "linkedin": "linkedin.com/company/medtech-innovations",
        "why_3d_printing": "Medical device startup prototyping surgical guides. Currently sends to Shapeways (slow, expensive).",
        "pitch_angle": "Local surgical guide prototyping with biocompatible resins — same-day turnaround, half the cost of Shapeways.",
        "score_breakdown": {"industry_fit": 15, "location": 10, "company_size": 10, "website": 5, "need_indicators": 25, "accessibility": 25},
    },
    {
        "company": "BrightSmile Dental Group",
        "industry": "dental",
        "location": "Santa Monica, CA",
        "employees": 20,
        "website": "brightsmilela.com",
        "email": "office@brightsmilela.com",
        "phone": "(310) 555-0606",
        "linkedin": None,
        "why_3d_printing": "Multi-location dental practice, currently outsourcing all dental models.",
        "pitch_angle": "Bring dental model production in-house — our resin printers pay for themselves in 3 months.",
        "score_breakdown": {"industry_fit": 15, "location": 10, "company_size": 10, "website": 5, "need_indicators": 15, "accessibility": 15},
    },
    {
        "company": "Phantom Props Studio",
        "industry": "film/entertainment",
        "location": "Burbank, CA",
        "employees": 8,
        "website": "phantomprops.com",
        "email": "info@phantomprops.com",
        "phone": "(818) 555-0707",
        "linkedin": "linkedin.com/company/phantom-props",
        "why_3d_printing": "Prop and costume house for film/TV. Uses CNC but not yet 3D printing.",
        "pitch_angle": "From concept art to screen-ready prop in 72 hours — no minimum order, any shape, any size.",
        "score_breakdown": {"industry_fit": 15, "location": 10, "company_size": 5, "website": 5, "need_indicators": 20, "accessibility": 20},
    },
    {
        "company": "FastTrack AutoParts",
        "industry": "automotive",
        "location": "Torrance, CA",
        "employees": 55,
        "website": "fasttrackautoparts.com",
        "email": "b2b@fasttrackautoparts.com",
        "phone": "(310) 555-0808",
        "linkedin": "linkedin.com/company/fasttrack-autoparts",
        "why_3d_printing": "Aftermarket auto parts company, exploring 3D printed jigs and custom brackets.",
        "pitch_angle": "Replace expensive machined jigs with printed alternatives at 1/10th the cost — perfect for short-run custom brackets.",
        "score_breakdown": {"industry_fit": 15, "location": 10, "company_size": 10, "website": 5, "need_indicators": 15, "accessibility": 20},
    },
]


@dataclass
class ScoredLead:
    company: str
    industry: str
    location: str
    employees: int
    website: str
    email: str
    phone: str
    score: int
    tier: str
    why_3d_printing: str
    pitch_angle: str


def score_lead(lead: dict) -> ScoredLead:
    """Calculate total score and tier for a lead."""
    breakdown = lead.get("score_breakdown", {})
    total = sum(breakdown.values())
    
    if total >= 80:
        tier = "🔥 Hot"
    elif total >= 60:
        tier = "🟡 Warm"
    elif total >= 40:
        tier = "🔵 Cool"
    else:
        tier = "⚪ Low"

    return ScoredLead(
        company=lead["company"],
        industry=lead["industry"],
        location=lead["location"],
        employees=lead["employees"],
        website=lead["website"],
        email=lead["email"],
        phone=lead["phone"],
        score=total,
        tier=tier,
        why_3d_printing=lead["why_3d_printing"],
        pitch_angle=lead["pitch_angle"],
    )


def format_lead_report(leads: list[ScoredLead], industry: str = "All") -> str:
    """Format scored leads as a report."""
    now = datetime.now().strftime("%b %d, %Y")
    lines = [
        f"🔍 LEAD DISCOVERY REPORT — {industry.title()}, LA Area",
        f"Generated: {now} | Leads found: {len(leads)}",
        ""
    ]

    hot = [l for l in leads if l.score >= 80]
    warm = [l for l in leads if 60 <= l.score < 80]
    cool = [l for l in leads if 40 <= l.score < 60]

    if hot:
        lines.append("🔥 HOT LEADS (Score 80+):\n")
        for i, l in enumerate(hot, 1):
            lines.extend([
                f"  {i}. {l.company} (Score: {l.score})",
                f"     📍 {l.location} | 👥 {l.employees} employees",
                f"     🌐 {l.website} | 📧 {l.email}",
                f"     💡 Why: {l.why_3d_printing}",
                f"     📝 Pitch: \"{l.pitch_angle}\"",
                ""
            ])

    if warm:
        lines.append("🟡 WARM LEADS (Score 60-79):\n")
        for i, l in enumerate(warm, 1):
            lines.extend([
                f"  {i}. {l.company} (Score: {l.score}) — {l.location}",
                f"     📧 {l.email} | 💡 {l.why_3d_printing}",
                ""
            ])

    if cool:
        lines.append(f"🔵 COOL LEADS: {len(cool)} leads scored 40-59 (nurture via content)")

    return "\n".join(lines)


def export_csv(leads: list[ScoredLead], output_path: str):
    """Export leads to CSV."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Company", "Industry", "Location", "Employees", "Score", "Tier", "Email", "Phone", "Website", "Pitch"])
        for l in leads:
            writer.writerow([l.company, l.industry, l.location, l.employees, l.score, l.tier, l.email, l.phone, l.website, l.pitch_angle])
    print(f"✅ Exported {len(leads)} leads to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="B2B Lead Finder for 3D Printing")
    parser.add_argument("--industry", type=str, help=f"Target industry: {', '.join(TARGET_INDUSTRIES)}")
    parser.add_argument("--location", type=str, default="Los Angeles", help="Location filter")
    parser.add_argument("--count", type=int, default=10, help="Max leads to return")
    parser.add_argument("--min-score", type=int, default=0, help="Minimum lead score")
    parser.add_argument("--all-industries", action="store_true", help="Search all target industries")
    parser.add_argument("--top", type=int, help="Show top N leads across all industries")
    parser.add_argument("--export", type=str, choices=["csv", "json"], help="Export format")
    parser.add_argument("--output", type=str, help="Export file path")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    leads_data = SAMPLE_LEADS
    if args.industry:
        leads_data = [l for l in leads_data if l["industry"] == args.industry]

    scored = [score_lead(l) for l in leads_data]
    scored = [l for l in scored if l.score >= args.min_score]
    scored.sort(key=lambda x: x.score, reverse=True)

    if args.top:
        scored = scored[:args.top]
    elif args.count:
        scored = scored[:args.count]

    if args.export == "csv" and args.output:
        export_csv(scored, args.output)
    elif args.json or args.export == "json":
        print(json.dumps([asdict(l) for l in scored], indent=2))
    else:
        industry_label = args.industry or "All Industries"
        print(format_lead_report(scored, industry_label))


if __name__ == "__main__":
    main()
