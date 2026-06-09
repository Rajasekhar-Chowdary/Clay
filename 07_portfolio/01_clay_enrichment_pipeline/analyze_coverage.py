#!/usr/bin/env python3
"""
Clay waterfall coverage analyzer.

Reads a Clay table export (CSV) and computes the metrics that actually matter
for a portfolio case study: overall coverage rate, per-provider contribution,
and credit efficiency. Prints a recruiter-ready breakdown table.

Expected columns (rename via --source-col / --email-col if yours differ):
    email_final    -- consolidated email (empty if not found)
    email_source   -- which provider found it: Apollo / Prospeo / Findymail / Dropcontact / Not found

Usage:
    python analyze_coverage.py clay_export.csv
    python analyze_coverage.py clay_export.csv --credits-used 280
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter

# Credit cost per provider position in the waterfall (1 attempt each).
WATERFALL_ORDER = ["Apollo", "Prospeo", "Findymail", "Dropcontact"]


def load_rows(path: str, email_col: str, source_col: str) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit(f"ERROR: {path} has no data rows.")
    header = rows[0].keys()
    for col in (email_col, source_col):
        if col not in header:
            sys.exit(f"ERROR: column '{col}' not found. Available: {', '.join(header)}")
    return rows


def analyze(rows: list[dict[str, str]], email_col: str, source_col: str,
            credits_used: int | None) -> None:
    total = len(rows)
    found = sum(1 for r in rows if str(r.get(email_col) or "").strip())
    coverage = found / total * 100 if total else 0.0

    sources = Counter(
        (str(r.get(source_col) or "Not found").strip() or "Not found")
        for r in rows
    )

    print("\n" + "=" * 56)
    print("  CLAY WATERFALL COVERAGE ANALYSIS")
    print("=" * 56)
    print(f"  Total rows        : {total}")
    print(f"  Emails found      : {found}")
    print(f"  Coverage rate     : {coverage:.1f}%")
    print("-" * 56)
    print(f"  {'Provider':<14}{'Found':>7}{'% total':>10}{'Cumulative':>13}")
    print("-" * 56)

    cumulative = 0
    for provider in WATERFALL_ORDER:
        n = sources.get(provider, 0)
        cumulative += n
        print(f"  {provider:<14}{n:>7}{n/total*100:>9.1f}%{cumulative/total*100:>12.1f}%")
    not_found = sources.get("Not found", 0)
    print(f"  {'Not found':<14}{not_found:>7}{not_found/total*100:>9.1f}%{'—':>13}")
    print("-" * 56)

    if credits_used:
        cpl = credits_used / found if found else float("inf")
        print(f"  Credits used      : {credits_used}")
        print(f"  Credits / lead    : {cpl:.2f}   (target < 3.0)")
        print("-" * 56)

    verdict = (
        "excellent (expert bar)" if coverage >= 90
        else "good waterfall design" if coverage >= 80
        else "acceptable" if coverage >= 60
        else "REVIEW input data / ICP — coverage is low"
    )
    print(f"  Verdict           : {verdict}")
    print("=" * 56 + "\n")


def main() -> None:
    p = argparse.ArgumentParser(description="Analyze Clay waterfall coverage")
    p.add_argument("csv_path", help="Clay table export CSV")
    p.add_argument("--email-col", default="email_final")
    p.add_argument("--source-col", default="email_source")
    p.add_argument("--credits-used", type=int, default=None,
                   help="total credits spent, to compute credits/lead")
    args = p.parse_args()

    rows = load_rows(args.csv_path, args.email_col, args.source_col)
    analyze(rows, args.email_col, args.source_col, args.credits_used)


if __name__ == "__main__":
    main()
