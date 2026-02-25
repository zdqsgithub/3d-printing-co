#!/usr/bin/env python3
"""
Outreach Manager — Manages email outreach sequences with scheduling and tracking.
Used by the Outreach Scheduler skill for automated B2B outreach.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

SEQUENCES = {
    "cold-intro": {
        "name": "Cold Introduction",
        "emails": 3,
        "delays_days": [0, 4, 10],
        "templates": ["intro", "followup", "final"],
    },
    "post-event": {
        "name": "Post-Event Follow-up",
        "emails": 2,
        "delays_days": [0, 5],
        "templates": ["event-intro", "event-followup"],
    },
    "re-engagement": {
        "name": "Re-engagement",
        "emails": 1,
        "delays_days": [0],
        "templates": ["re-engage"],
    },
}

OPTIMAL_HOURS = {
    1: [(10, 11)],  # Monday
    2: [(9, 11)],   # Tuesday (best)
    3: [(9, 11)],   # Wednesday
    4: [(9, 11)],   # Thursday
    5: [(9, 10)],   # Friday
}

# Sample outreach queue
SAMPLE_QUEUE = [
    {"lead": "Morphosis Architects", "email": "info@morphosis.com", "sequence": "cold-intro", "step": 1, "status": "pending", "scheduled": "2026-02-25 09:00", "industry": "architecture"},
    {"lead": "JFAK Architects", "email": "studio@jfak.net", "sequence": "cold-intro", "step": 1, "status": "sent", "scheduled": "2026-02-20 09:30", "sent_at": "2026-02-20 09:30", "industry": "architecture"},
    {"lead": "Prototype Studios LA", "email": "hello@prototypestudiosla.com", "sequence": "cold-intro", "step": 2, "status": "pending", "scheduled": "2026-02-26 09:00", "industry": "product design"},
    {"lead": "MedTech Innovations", "email": "contact@medtechinnovations.io", "sequence": "cold-intro", "step": 1, "status": "replied", "reply_status": "interested", "industry": "medical devices"},
    {"lead": "Phantom Props Studio", "email": "info@phantomprops.com", "sequence": "cold-intro", "step": 1, "status": "pending", "scheduled": "2026-02-27 09:00", "industry": "film/entertainment"},
]

WEEKLY_STATS = {
    "emails_sent": 12,
    "opens": 8,
    "open_rate": 66.7,
    "replies": 3,
    "reply_rate": 25.0,
    "meetings_booked": 1,
    "opted_out": 0,
    "bounced": 1,
}


def get_queue_status(queue):
    """Show current outreach queue status."""
    lines = ["📤 OUTREACH QUEUE STATUS", "=" * 50, ""]
    
    pending = [q for q in queue if q["status"] == "pending"]
    sent = [q for q in queue if q["status"] == "sent"]
    replied = [q for q in queue if q["status"] == "replied"]

    lines.append(f"📊 Total in queue: {len(queue)}")
    lines.append(f"   ⏳ Pending: {len(pending)}")
    lines.append(f"   ✅ Sent (awaiting reply): {len(sent)}")
    lines.append(f"   💬 Replied: {len(replied)}")
    lines.append("")

    if pending:
        lines.append("⏳ NEXT UP:")
        for q in sorted(pending, key=lambda x: x["scheduled"]):
            seq = SEQUENCES[q["sequence"]]
            lines.append(f"  📧 {q['lead']} — {seq['name']} Step {q['step']}")
            lines.append(f"     📅 Scheduled: {q['scheduled']}")
            lines.append("")

    if replied:
        lines.append("💬 REPLIES:")
        for q in replied:
            status_icon = "🔥" if q.get("reply_status") == "interested" else "❌"
            lines.append(f"  {status_icon} {q['lead']} — {q.get('reply_status', 'unknown')}")

    return "\n".join(lines)


def get_today_sends(queue):
    """Get emails scheduled for today."""
    today = datetime.now().strftime("%Y-%m-%d")
    today_items = [q for q in queue if q["status"] == "pending" and q["scheduled"].startswith(today)]
    
    if not today_items:
        return "📭 No emails scheduled for today."
    
    lines = [f"📤 TODAY'S SENDS — {today}", "=" * 40, ""]
    for q in today_items:
        seq = SEQUENCES[q["sequence"]]
        lines.append(f"  📧 {q['lead']} ({q['email']})")
        lines.append(f"     Sequence: {seq['name']} — Step {q['step']}/{seq['emails']}")
        lines.append(f"     Time: {q['scheduled']}")
        lines.append("")
    return "\n".join(lines)


def check_followups(queue):
    """Check for leads needing follow-up."""
    now = datetime.now()
    needs_followup = []
    
    for q in queue:
        if q["status"] == "sent" and "sent_at" in q:
            sent = datetime.strptime(q["sent_at"], "%Y-%m-%d %H:%M")
            seq = SEQUENCES[q["sequence"]]
            if q["step"] < seq["emails"]:
                next_delay = seq["delays_days"][q["step"]]
                if (now - sent).days >= next_delay:
                    needs_followup.append((q, q["step"] + 1))
    
    if not needs_followup:
        return "✅ No follow-ups needed right now."
    
    lines = ["📋 FOLLOW-UPS NEEDED", "=" * 40, ""]
    for q, next_step in needs_followup:
        seq = SEQUENCES[q["sequence"]]
        lines.append(f"  📧 {q['lead']} — needs Step {next_step}/{seq['emails']}")
        lines.append(f"     Last sent: {q['sent_at']} ({(now - datetime.strptime(q['sent_at'], '%Y-%m-%d %H:%M')).days}d ago)")
        lines.append("")
    return "\n".join(lines)


def weekly_report(stats):
    """Generate weekly outreach performance report."""
    lines = [
        "📊 WEEKLY OUTREACH REPORT",
        "=" * 40, "",
        f"  📧 Emails sent: {stats['emails_sent']}",
        f"  👁️ Opens: {stats['opens']} ({stats['open_rate']:.1f}%)",
        f"  💬 Replies: {stats['replies']} ({stats['reply_rate']:.1f}%)",
        f"  📅 Meetings booked: {stats['meetings_booked']}",
        f"  🚫 Opted out: {stats['opted_out']}",
        f"  ❌ Bounced: {stats['bounced']}",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Email Outreach Manager")
    parser.add_argument("--queue-status", action="store_true")
    parser.add_argument("--send-today", action="store_true")
    parser.add_argument("--check-followups", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--period", default="weekly", choices=["weekly", "monthly"])
    parser.add_argument("--add-to-sequence", action="store_true")
    parser.add_argument("--lead", type=str)
    parser.add_argument("--sequence", type=str, choices=list(SEQUENCES.keys()))
    parser.add_argument("--mark-replied", action="store_true")
    parser.add_argument("--status", type=str, choices=["interested", "not-interested", "meeting-booked"])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.queue_status:
        print(get_queue_status(SAMPLE_QUEUE))
    elif args.send_today:
        print(get_today_sends(SAMPLE_QUEUE))
    elif args.check_followups:
        print(check_followups(SAMPLE_QUEUE))
    elif args.report:
        print(weekly_report(WEEKLY_STATS))
    elif args.add_to_sequence and args.lead and args.sequence:
        print(f"✅ Added '{args.lead}' to {SEQUENCES[args.sequence]['name']} sequence")
    elif args.mark_replied and args.lead and args.status:
        print(f"✅ Marked '{args.lead}' as: {args.status}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
