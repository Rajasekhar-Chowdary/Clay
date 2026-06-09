#!/usr/bin/env python3
"""
Signal-Triggered Personalization Engine
=======================================

Generates a personalized cold-email opener per lead using the Claude API, with a
confidence score the downstream pipeline uses to gate auto-send. This is the AI
brain of the signal-triggered system: Clay enriches → this scores + writes →
n8n routes by confidence → SendGrid sends / HubSpot logs.

Uses structured outputs so every call returns a validated {opener, confidence,
used_signal} object — no fragile string parsing.

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python personalize.py --demo                 # 3 sample leads, no CSV needed
    python personalize.py leads.csv              # enrich a Clay export
    python personalize.py leads.csv --threshold 0.65 --out scored.csv

Model note: defaults to Claude Haiku 4.5 — the right tier for high-volume,
short-output personalization (cheap, fast), matching the GTM stack's documented
choice. Override with --model claude-opus-4-8 for higher-stakes accounts.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from dataclasses import dataclass

try:
    import anthropic
    from pydantic import BaseModel, Field
except ImportError:
    sys.exit("Install deps first:  pip install anthropic pydantic")

DEFAULT_MODEL = "claude-haiku-4-5"

SYSTEM_PROMPT = """You write the opening line of a cold B2B email for a GTM/RevOps \
software seller. You write ONE sentence that a busy operator would actually read.

Hard rules:
- Reference the SPECIFIC signal or tech stack given — never a generic "I saw your company".
- Connect to a GTM data, enrichment, or pipeline challenge their role would care about.
- Sound like a human peer who did real research, not a template bot.
- No greeting (no "Hi {name}"), no "I hope this finds you well", no "I wanted to reach out".
- Max 25 words.

You also rate your confidence (0.0-1.0) that this opener is specific and send-worthy:
- 0.8-1.0: references a concrete, recent signal (funding, hire, post) — send it.
- 0.5-0.79: references tech stack or role context only — usable.
- below 0.5: you had little to work with — the opener is generic, hold for review."""


class Opener(BaseModel):
    """Structured result returned by the model."""
    opener: str = Field(description="The one-sentence cold email opener, max 25 words.")
    confidence: float = Field(ge=0.0, le=1.0, description="0-1 confidence this is specific and send-worthy.")
    used_signal: bool = Field(description="True if a concrete signal (funding/hire/post) was used.")


@dataclass
class Lead:
    first_name: str
    last_name: str
    job_title: str
    company_name: str
    signal: str
    crm: str
    industry: str

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "Lead":
        g = lambda k: str(row.get(k) or "").strip()
        return cls(
            first_name=g("first_name"),
            last_name=g("last_name"),
            job_title=g("job_title"),
            company_name=g("company_name"),
            signal=g("primary_signal_text") or g("signal") or g("gtm_signal"),
            crm=g("crm_detected") or g("tech_stack_crm"),
            industry=g("industry"),
        )

    def to_prompt(self) -> str:
        return (
            f"Contact: {self.first_name} {self.last_name}, {self.job_title} at {self.company_name}\n"
            f"Signal: {self.signal or 'none found'}\n"
            f"CRM in use: {self.crm or 'unknown'}\n"
            f"Industry: {self.industry or 'unknown'}\n\n"
            "Write the opener. If the signal is empty, use the CRM or industry as the hook "
            "and lower your confidence accordingly."
        )


def personalize(client: anthropic.Anthropic, lead: Lead, model: str) -> Opener:
    """Generate a confidence-scored opener for one lead via structured output."""
    response = client.messages.parse(
        model=model,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": lead.to_prompt()}],
        output_format=Opener,
    )
    # parsed_output is None on a refusal or max_tokens truncation — treat as hold-for-review.
    if response.parsed_output is None:
        return Opener(opener="", confidence=0.0, used_signal=False)
    return response.parsed_output


def run_csv(client: anthropic.Anthropic, path: str, model: str, threshold: float, out: str) -> None:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        sys.exit(f"ERROR: {path} has no rows.")

    results: list[dict[str, str]] = []
    sent, held = 0, 0
    for i, row in enumerate(rows, 1):
        lead = Lead.from_row(row)
        try:
            result = personalize(client, lead, model)
        except anthropic.APIStatusError as e:
            print(f"  [{i}] API error for {lead.company_name}: {e.status_code}")
            result = Opener(opener="", confidence=0.0, used_signal=False)

        decision = "SEND" if result.confidence >= threshold else "HOLD"
        sent += decision == "SEND"
        held += decision == "HOLD"
        results.append({
            **row,
            "ai_opener": result.opener,
            "ai_confidence": f"{result.confidence:.2f}",
            "ai_used_signal": str(result.used_signal),
            "ai_decision": decision,
        })
        print(f"  [{i}/{len(rows)}] {decision} ({result.confidence:.2f}) {lead.company_name}")

    fieldnames = list(results[0].keys())
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone. {sent} SEND / {held} HOLD (threshold {threshold}). Written to {out}")


def run_demo(client: anthropic.Anthropic, model: str, threshold: float) -> None:
    demo_leads = [
        Lead("Marcus", "Bragg", "VP of Sales", "Acme Corp",
             "FUNDING: Series B $25M Q1 2026", "Salesforce", "B2B SaaS"),
        Lead("Lena", "Ortiz", "Head of RevOps", "Northwind",
             "HIRING: Revenue Operations Manager", "HubSpot", "Fintech"),
        Lead("Sunita", "Patel", "Director of Sales Ops", "Globex",
             "", "", "Logistics SaaS"),  # no signal — should produce lower confidence
    ]
    print(f"Running demo with {model} (threshold {threshold})\n")
    for lead in demo_leads:
        result = personalize(client, lead, model)
        decision = "SEND" if result.confidence >= threshold else "HOLD"
        print(f"[{decision}] confidence={result.confidence:.2f} signal_used={result.used_signal}")
        print(f"  {lead.first_name} @ {lead.company_name}: \"{result.opener}\"\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Signal-triggered personalization engine")
    parser.add_argument("csv_path", nargs="?", help="Clay export CSV (omit with --demo)")
    parser.add_argument("--demo", action="store_true", help="run 3 sample leads, no CSV")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Claude model ID")
    parser.add_argument("--threshold", type=float, default=0.65, help="confidence gate for SEND")
    parser.add_argument("--out", default="reports/scored_leads.csv")
    args = parser.parse_args()

    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit('ERROR: set ANTHROPIC_API_KEY first.\n  export ANTHROPIC_API_KEY="sk-ant-..."')

    client = anthropic.Anthropic()

    if args.demo or not args.csv_path:
        run_demo(client, args.model, args.threshold)
    else:
        run_csv(client, args.csv_path, args.model, args.threshold, args.out)


if __name__ == "__main__":
    main()
