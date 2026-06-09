# Module 4.1 — Clay API: Programmatic Table Management

**Time:** 90–120 minutes  
**Prerequisite:** Phases 1–3 complete, Python basics, n8n familiarity  
**Focus:** Adding rows to Clay programmatically, triggering enrichment via API, reading results

---

## Why the Clay API Matters

Without the API, your workflow is:
1. Manually prepare CSV
2. Upload to Clay
3. Run enrichment
4. Export results
5. Process in n8n/Supabase

With the API:
1. Signal detected in n8n (funding news, job change, etc.)
2. n8n POSTs to Clay API → adds row to table
3. Clay auto-enriches (auto-enrich ON for production)
4. Clay webhook fires when enrichment complete
5. n8n receives enriched row → writes to Supabase + HubSpot

Total elapsed time: 5–10 minutes from signal to CRM. Zero manual steps.

---

## Clay API Authentication

### Getting Your API Key

1. Clay account → Settings → API
2. Generate API key
3. Store in `.env` or secret manager — never in code

```bash
CLAY_API_KEY=clay_live_abc123...
CLAY_TABLE_ID=tbl_xyz789...
```

### Base URL and Headers

```python
BASE_URL = "https://api.clay.com/v1"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('CLAY_API_KEY')}",
    "Content-Type": "application/json"
}
```

---

## Core API Operations

### 1. List Tables

```python
import requests
import os

def list_tables() -> list[dict]:
    response = requests.get(
        f"{BASE_URL}/tables",
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()["tables"]

# Returns list of tables with their IDs and names
tables = list_tables()
for table in tables:
    print(f"{table['name']} — {table['id']}")
```

### 2. Get Table Schema

Before adding rows, understand what columns exist:

```python
def get_table_columns(table_id: str) -> list[dict]:
    response = requests.get(
        f"{BASE_URL}/tables/{table_id}/columns",
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()["columns"]

columns = get_table_columns(TABLE_ID)
for col in columns:
    print(f"{col['name']} ({col['type']}) — ID: {col['id']}")
```

### 3. Add a Single Row

```python
def add_lead_to_clay(lead: dict, table_id: str) -> dict:
    """Add one lead row to a Clay table."""
    payload = {
        "data": {
            "first_name": lead["first_name"],
            "last_name": lead["last_name"],
            "company_name": lead.get("company_name", ""),
            "company_domain": lead.get("company_domain", ""),
            "linkedin_url": lead.get("linkedin_url", ""),
            "job_title": lead.get("job_title", ""),
            # Add custom columns by their exact Clay column name
            "signal_source": lead.get("signal_source", ""),
            "signal_date": lead.get("signal_date", "")
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/tables/{table_id}/rows",
        headers=HEADERS,
        json=payload
    )
    response.raise_for_status()
    return response.json()

# Example usage
lead = {
    "first_name": "Jane",
    "last_name": "Smith",
    "company_name": "Acme Corp",
    "company_domain": "acmecorp.com",
    "signal_source": "Series B funding",
    "signal_date": "2026-06-01"
}

result = add_lead_to_clay(lead, TABLE_ID)
print(f"Row created: {result['row']['id']}")
```

### 4. Add Multiple Rows (Batch)

```python
def add_leads_batch(leads: list[dict], table_id: str, batch_size: int = 10) -> list[dict]:
    """Add multiple leads in batches to avoid rate limits."""
    results = []
    
    for i in range(0, len(leads), batch_size):
        batch = leads[i:i + batch_size]
        
        for lead in batch:
            try:
                result = add_lead_to_clay(lead, table_id)
                results.append({"status": "success", "row_id": result["row"]["id"], "lead": lead})
            except requests.HTTPError as e:
                results.append({"status": "error", "error": str(e), "lead": lead})
        
        # Rate limit: Clay allows ~100 requests/minute
        if i + batch_size < len(leads):
            time.sleep(0.6)  # ~100 req/min = 1 req per 0.6s
    
    return results

# Usage
import time
leads = [...]  # your list of 100 leads
results = add_leads_batch(leads, TABLE_ID)
print(f"Added: {sum(1 for r in results if r['status'] == 'success')}")
print(f"Failed: {sum(1 for r in results if r['status'] == 'error')}")
```

### 5. Get Row Data (Read Back Enriched Results)

After Clay enriches a row (you can wait for the webhook, or poll):

```python
def get_row(row_id: str, table_id: str) -> dict:
    response = requests.get(
        f"{BASE_URL}/tables/{table_id}/rows/{row_id}",
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()["row"]

row = get_row(row_id, TABLE_ID)
print(f"Email: {row['data'].get('email_final', 'Not found')}")
print(f"ICP Score: {row['data'].get('icp_score', 'N/A')}")
```

### 6. Search Rows (Filter by Column Value)

```python
def search_rows(table_id: str, filter_column: str, filter_value: str) -> list[dict]:
    response = requests.get(
        f"{BASE_URL}/tables/{table_id}/rows",
        headers=HEADERS,
        params={
            "filter[column]": filter_column,
            "filter[value]": filter_value
        }
    )
    response.raise_for_status()
    return response.json()["rows"]

# Find all Tier A leads
tier_a_rows = search_rows(TABLE_ID, "icp_tier", "Tier A")
```

### 7. Update a Row

```python
def update_row(row_id: str, table_id: str, updates: dict) -> dict:
    response = requests.patch(
        f"{BASE_URL}/tables/{table_id}/rows/{row_id}",
        headers=HEADERS,
        json={"data": updates}
    )
    response.raise_for_status()
    return response.json()["row"]

# Mark a row as processed
update_row(row_id, TABLE_ID, {"processing_status": "sent_to_hubspot"})
```

---

## n8n Integration: HTTP Request Node

For n8n users, the Clay API is accessed via HTTP Request nodes.

**Add row to Clay from n8n:**

```json
{
  "method": "POST",
  "url": "https://api.clay.com/v1/tables/{{$env.CLAY_TABLE_ID}}/rows",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "httpBearerAuth",
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "data",
        "value": "={{ { first_name: $json.first_name, last_name: $json.last_name, company_domain: $json.domain, signal_source: $json.signal } }}"
      }
    ]
  }
}
```

---

## Full Real-Time Pipeline (Python)

This script simulates a production signal-triggered pipeline:

```python
import requests
import os
import time
from datetime import datetime

CLAY_API_KEY = os.getenv("CLAY_API_KEY")
CLAY_TABLE_ID = os.getenv("CLAY_TABLE_ID")
BASE_URL = "https://api.clay.com/v1"

HEADERS = {
    "Authorization": f"Bearer {CLAY_API_KEY}",
    "Content-Type": "application/json"
}

def process_funding_signal(company: dict) -> None:
    """
    Called when a company raises funding.
    Adds 3 key contacts to Clay for enrichment.
    """
    target_roles = ["CEO", "CTO", "VP Sales", "Head of Revenue Operations"]
    
    # In production, you'd look these up from Apollo or LinkedIn
    # For demo: we're adding placeholder rows that Clay will enrich
    for role in target_roles[:3]:  # Top 3 roles
        lead = {
            "company_name": company["name"],
            "company_domain": company["domain"],
            "job_title": role,
            "signal_source": f"Series {company['round']} funding",
            "signal_date": datetime.now().isoformat(),
            "signal_amount": company.get("amount", ""),
        }
        
        result = add_lead_to_clay(lead, CLAY_TABLE_ID)
        print(f"  Added {role} at {company['name']}: {result['row']['id']}")
        time.sleep(0.3)


def add_lead_to_clay(lead: dict, table_id: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/tables/{table_id}/rows",
        headers=HEADERS,
        json={"data": lead}
    )
    response.raise_for_status()
    return response.json()


# Simulate receiving a funding signal
funding_event = {
    "name": "Acme Corp",
    "domain": "acmecorp.com",
    "round": "B",
    "amount": "$25M"
}

print(f"Processing funding signal: {funding_event['name']} raised Series {funding_event['round']}")
process_funding_signal(funding_event)
print("Done — Clay will auto-enrich these rows.")
```

---

## API Rate Limits and Error Handling

### Rate Limits
- Clay API: ~100 requests/minute on Starter plan
- Batch operations: add `time.sleep(0.6)` between rows
- If you hit rate limit: Clay returns 429 → implement exponential backoff

```python
def add_lead_with_retry(lead: dict, table_id: str, max_retries: int = 3) -> dict:
    for attempt in range(max_retries):
        try:
            return add_lead_to_clay(lead, table_id)
        except requests.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = (2 ** attempt) * 1  # 1s, 2s, 4s
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries")
```

### Common API Errors

| Status | Meaning | Fix |
|--------|---------|-----|
| 401 | Invalid API key | Check env variable loading |
| 404 | Table not found | Verify TABLE_ID is correct |
| 422 | Invalid field names | Column names must match exactly as in Clay UI |
| 429 | Rate limited | Add sleep / exponential backoff |
| 500 | Clay server error | Retry after 30 seconds |

---

## Anki Cards to Create

```
Q: What is the Clay API base URL?
A: https://api.clay.com/v1

Q: What is Clay's API rate limit (Starter plan)?
A: ~100 requests/minute — add time.sleep(0.6) between row additions

Q: How do you add a row to Clay via API?
A: POST to /tables/{table_id}/rows with {"data": {column_name: value, ...}}

Q: What HTTP status code means you're rate limited?
A: 429 — implement exponential backoff: wait 1s, 2s, 4s on successive retries

Q: What is the production pattern for a signal-triggered pipeline?
A: Signal detected → n8n/Python POSTs to Clay API → Clay auto-enriches → Clay webhook fires → n8n routes enriched data to Supabase + HubSpot
```

---

## Next Module

→ [04_expert/02_cost_optimization.md](./02_cost_optimization.md) — Credit optimization, audit techniques, and budget planning for production
