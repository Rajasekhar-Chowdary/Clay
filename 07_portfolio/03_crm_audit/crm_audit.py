#!/usr/bin/env python3
"""
HubSpot CRM Data-Quality Audit
==============================

Scores every contact in a HubSpot portal on three data-quality dimensions —
completeness, consistency, and freshness — and writes a ranked CSV report plus
a console summary. Built to run weekly (cron / GitHub Action) as a standing
data-quality monitor for a GTM team.

Why this exists: GTM automation (sequences, scoring, routing) silently breaks on
dirty CRM data. This surfaces the rot before it costs pipeline.

Usage:
    export HUBSPOT_TOKEN="pat-na1-xxxx"        # Private App token, scope: crm.objects.contacts.read
    python crm_audit.py                         # full portal
    python crm_audit.py --limit 500             # first 500 contacts
    python crm_audit.py --out reports/audit.csv

No paid dependencies. Standard library + requests.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterator

import requests

HUBSPOT_BASE = "https://api.hubapi.com"
CONTACTS_ENDPOINT = f"{HUBSPOT_BASE}/crm/v3/objects/contacts"

# Properties we pull and the weight each completeness field carries.
COMPLETENESS_FIELDS: dict[str, int] = {
    "email": 25,
    "firstname": 10,
    "lastname": 10,
    "jobtitle": 15,
    "company": 15,
    "phone": 10,
    "hs_linkedin_url": 15,
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
# Free / personal domains are a consistency red flag on a B2B contact.
PERSONAL_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
    "icloud.com", "aol.com", "protonmail.com", "live.com",
}
FRESHNESS_WARN_DAYS = 90   # not touched in 90 days -> stale
FRESHNESS_FAIL_DAYS = 180  # not touched in 180 days -> rotting


@dataclass
class ContactAudit:
    contact_id: str
    email: str
    completeness: int = 0           # 0-100
    consistency_issues: list[str] = field(default_factory=list)
    freshness_days: int | None = None
    freshness_status: str = "unknown"

    @property
    def consistency_score(self) -> int:
        """100 minus 20 per issue, floored at 0."""
        return max(0, 100 - 20 * len(self.consistency_issues))

    @property
    def freshness_score(self) -> int:
        if self.freshness_days is None:
            return 50  # unknown -> neutral
        if self.freshness_days <= FRESHNESS_WARN_DAYS:
            return 100
        if self.freshness_days <= FRESHNESS_FAIL_DAYS:
            return 60
        return 20

    @property
    def total_score(self) -> int:
        """Weighted: completeness 50%, consistency 30%, freshness 20%."""
        return round(
            0.50 * self.completeness
            + 0.30 * self.consistency_score
            + 0.20 * self.freshness_score
        )

    @property
    def grade(self) -> str:
        s = self.total_score
        if s >= 85:
            return "A"
        if s >= 70:
            return "B"
        if s >= 50:
            return "C"
        return "D"


def get_token() -> str:
    token = os.getenv("HUBSPOT_TOKEN")
    if not token:
        sys.exit(
            "ERROR: HUBSPOT_TOKEN not set.\n"
            "Create a Private App in HubSpot (Settings → Integrations → Private Apps) "
            "with scope crm.objects.contacts.read, then:\n"
            '  export HUBSPOT_TOKEN="pat-na1-..."'
        )
    return token


def fetch_contacts(token: str, limit: int | None) -> Iterator[dict[str, Any]]:
    """Page through the contacts API, yielding raw contact objects."""
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    properties = list(COMPLETENESS_FIELDS) + ["lastmodifieddate", "notes_last_updated"]
    after: str | None = None
    fetched = 0

    while True:
        params: dict[str, Any] = {
            "limit": 100,
            "properties": ",".join(properties),
        }
        if after:
            params["after"] = after

        resp = session.get(CONTACTS_ENDPOINT, params=params, timeout=30)
        if resp.status_code == 401:
            sys.exit("ERROR: 401 Unauthorized — check token and scopes.")
        if resp.status_code == 429:
            sys.exit("ERROR: 429 rate-limited — wait and re-run, or add backoff.")
        resp.raise_for_status()

        payload = resp.json()
        for contact in payload.get("results", []):
            yield contact
            fetched += 1
            if limit and fetched >= limit:
                return

        paging = payload.get("paging", {}).get("next", {})
        after = paging.get("after")
        if not after:
            return


def score_completeness(props: dict[str, Any]) -> int:
    earned = sum(
        weight for fieldname, weight in COMPLETENESS_FIELDS.items()
        if str(props.get(fieldname) or "").strip()
    )
    total = sum(COMPLETENESS_FIELDS.values())
    return round(earned / total * 100)


def check_consistency(props: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    email = str(props.get("email") or "").strip().lower()

    if email and not EMAIL_RE.match(email):
        issues.append("malformed_email")
    if email and EMAIL_RE.match(email):
        domain = email.split("@", 1)[1]
        if domain in PERSONAL_DOMAINS:
            issues.append("personal_email_on_b2b_contact")

    # Name sanity: ALL CAPS or all-lowercase names signal unclean imports.
    for name_field in ("firstname", "lastname"):
        val = str(props.get(name_field) or "").strip()
        if val and (val.isupper() or val.islower()) and len(val) > 1:
            issues.append(f"{name_field}_casing")

    # Company present but no email domain match is a soft signal; flag missing company on titled contact.
    if str(props.get("jobtitle") or "").strip() and not str(props.get("company") or "").strip():
        issues.append("title_without_company")

    return issues


def compute_freshness(props: dict[str, Any]) -> tuple[int | None, str]:
    raw = props.get("lastmodifieddate") or props.get("notes_last_updated")
    if not raw:
        return None, "unknown"
    try:
        # HubSpot returns ISO-8601 with Z.
        modified = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return None, "unknown"
    days = (datetime.now(timezone.utc) - modified).days
    if days <= FRESHNESS_WARN_DAYS:
        status = "fresh"
    elif days <= FRESHNESS_FAIL_DAYS:
        status = "stale"
    else:
        status = "rotting"
    return days, status


def audit_contact(contact: dict[str, Any]) -> ContactAudit:
    props = contact.get("properties", {}) or {}
    freshness_days, freshness_status = compute_freshness(props)
    return ContactAudit(
        contact_id=str(contact.get("id", "")),
        email=str(props.get("email") or "").strip().lower(),
        completeness=score_completeness(props),
        consistency_issues=check_consistency(props),
        freshness_days=freshness_days,
        freshness_status=freshness_status,
    )


def write_report(audits: list[ContactAudit], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            "contact_id", "email", "total_score", "grade",
            "completeness", "consistency_score", "freshness_score",
            "freshness_days", "freshness_status", "consistency_issues",
        ])
        for a in sorted(audits, key=lambda x: x.total_score):  # worst first
            writer.writerow([
                a.contact_id, a.email, a.total_score, a.grade,
                a.completeness, a.consistency_score, a.freshness_score,
                a.freshness_days if a.freshness_days is not None else "",
                a.freshness_status, "|".join(a.consistency_issues),
            ])


def print_summary(audits: list[ContactAudit], out_path: str) -> None:
    n = len(audits)
    if n == 0:
        print("No contacts audited.")
        return
    avg = sum(a.total_score for a in audits) / n
    grades = {g: sum(1 for a in audits if a.grade == g) for g in "ABCD"}
    missing_email = sum(1 for a in audits if not a.email)
    personal = sum(1 for a in audits if "personal_email_on_b2b_contact" in a.consistency_issues)
    rotting = sum(1 for a in audits if a.freshness_status == "rotting")

    print("\n" + "=" * 52)
    print("  HUBSPOT CRM DATA-QUALITY AUDIT")
    print("=" * 52)
    print(f"  Contacts audited        : {n}")
    print(f"  Average quality score   : {avg:.1f} / 100")
    print(f"  Grade distribution      : A={grades['A']}  B={grades['B']}  C={grades['C']}  D={grades['D']}")
    print(f"  Missing email           : {missing_email} ({missing_email/n*100:.0f}%)")
    print(f"  Personal email on B2B   : {personal} ({personal/n*100:.0f}%)")
    print(f"  Rotting (>180d untouched): {rotting} ({rotting/n*100:.0f}%)")
    print("-" * 52)
    print(f"  Full report written to  : {out_path}")
    print(f"  ({grades['C'] + grades['D']} contacts need attention — see bottom of CSV)")
    print("=" * 52 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="HubSpot CRM data-quality audit")
    parser.add_argument("--limit", type=int, default=None, help="max contacts to audit")
    parser.add_argument("--out", default="reports/crm_audit.csv", help="output CSV path")
    args = parser.parse_args()

    token = get_token()
    print("Fetching contacts from HubSpot…")
    audits = [audit_contact(c) for c in fetch_contacts(token, args.limit)]

    write_report(audits, args.out)
    print_summary(audits, args.out)


if __name__ == "__main__":
    main()
