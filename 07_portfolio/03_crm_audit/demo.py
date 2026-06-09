#!/usr/bin/env python3
"""
Offline demo of the CRM audit scoring engine.

Lets anyone (a recruiter, a hiring manager) run the audit logic in 5 seconds
without a HubSpot account — using synthetic contacts that exercise every
quality rule. Proves the scoring works; the live version (crm_audit.py) runs
the same logic against a real portal.

    python demo.py
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from crm_audit import audit_contact, print_summary, write_report

NOW = datetime.now(timezone.utc)


def iso(days_ago: int) -> str:
    return (NOW - timedelta(days=days_ago)).isoformat().replace("+00:00", "Z")


# Synthetic contacts engineered to hit each rule: clean, personal-email,
# stale, rotting, missing fields, bad casing, title-without-company.
SYNTHETIC = [
    {"id": "1", "properties": {
        "email": "jane.smith@acme.com", "firstname": "Jane", "lastname": "Smith",
        "jobtitle": "VP Revenue Operations", "company": "Acme", "phone": "+1-555-0100",
        "hs_linkedin_url": "linkedin.com/in/janesmith", "lastmodifieddate": iso(5)}},
    {"id": "2", "properties": {
        "email": "bob@gmail.com", "firstname": "bob", "lastname": "CHEN",
        "jobtitle": "Head of Growth", "company": "", "lastmodifieddate": iso(120)}},
    {"id": "3", "properties": {
        "email": "not-an-email", "firstname": "Sunita", "lastname": "Patel",
        "jobtitle": "", "company": "Globex", "lastmodifieddate": iso(220)}},
    {"id": "4", "properties": {
        "email": "", "firstname": "Marcus", "lastname": "Bragg",
        "lastmodifieddate": iso(15)}},
    {"id": "5", "properties": {
        "email": "lena@northwind.io", "firstname": "Lena", "lastname": "Ortiz",
        "jobtitle": "CRO", "company": "Northwind", "phone": "+44-20-7946-0000",
        "hs_linkedin_url": "linkedin.com/in/lenaortiz", "lastmodifieddate": iso(45)}},
]


def main() -> None:
    audits = [audit_contact(c) for c in SYNTHETIC]
    out = "reports/demo_audit.csv"
    write_report(audits, out)
    print_summary(audits, out)
    print("Per-contact grades:")
    for a in sorted(audits, key=lambda x: x.total_score):
        issues = ", ".join(a.consistency_issues) or "none"
        print(f"  {a.grade}  {a.total_score:>3}  {a.email or '<no email>':<28} issues: {issues}")
    print()


if __name__ == "__main__":
    main()
