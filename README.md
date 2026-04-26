# GoHighLevel API Skill for AI Agents

A **comprehensive Manus skill** that enables AI agents to fully manage client businesses through the [GoHighLevel](https://www.gohighlevel.com/) CRM platform via the official API v2. Compatible with **Manus**, **OpenClaw**, and **Claude Code**.

## What This Skill Does

This skill provides AI agents with the tools and knowledge to manage every major aspect of a GoHighLevel sub-account:

| Module | Capabilities |
|---|---|
| **Contacts** | Create, search, update, delete, upsert, add/remove tags, notes, tasks, workflows |
| **Opportunities** | Create deals, move pipeline stages, update status (won/lost), search by pipeline |
| **Calendars & Appointments** | List calendars, check free slots, book/update/delete appointments |
| **Conversations** | Create threads, send SMS/email messages, get message history |
| **Users & Teams** | Create, update, delete users; list team members by location |
| **Locations (Sub-Accounts)** | Create, update, delete sub-account locations |
| **Workflows** | List automation workflows for a location |
| **Invoices** | Create, send, void, record payments, list invoices |
| **Forms & Surveys** | List forms/surveys, retrieve submissions |
| **Social Planner** | Get connected accounts, list/create/delete social media posts |
| **Email Campaigns** | List, create, update, delete email campaigns |
| **Blogs** | List blogs, get/create/update blog posts |
| **Custom Fields V2** | Get, create, update, delete custom fields |
| **Webhooks** | Receive and verify real-time events (Ed25519 signature) |

## Directory Structure

```
gohighlevel/
├── SKILL.md                              # Main skill instructions (loaded by AI agent)
├── README.md                             # This file (for GitHub)
├── LICENSE                               # MIT License
├── scripts/
│   └── ghl_api.py                        # Comprehensive Python API client
└── references/
    ├── api_reference.md                  # Core CRM: Contacts, Opportunities, Webhooks
    ├── conversations_calendars.md        # Conversations, Calendars, Appointments
    ├── users_locations_workflows.md      # Users, Locations, Workflows
    └── marketing_finance.md             # Forms, Surveys, Invoices, Social Planner, Email
```

## Quick Start

### 1. Get a Private Integration Token

1. In GoHighLevel, go to **Settings > Private Integrations**.
2. Click **Create new Integration**.
3. Select the required scopes (see table below).
4. Copy the generated token.

### 2. Set the Token

```bash
export GHL_API_TOKEN="your_private_integration_token"
```

### 3. Use the Python Helper

```python
from scripts.ghl_api import GoHighLevelAPI

api = GoHighLevelAPI()  # Reads GHL_API_TOKEN from environment

# --- Contacts ---
contacts = api.get_contacts(location_id="LOC_ID", query="john@example.com")
new_contact = api.create_contact("LOC_ID", {"firstName": "Jane", "lastName": "Smith", "email": "jane@example.com"})
api.add_contact_tags("CONTACT_ID", ["vip", "hot-lead"])

# --- Opportunities ---
pipelines = api.get_pipelines("LOC_ID")
opp = api.create_opportunity("PIPELINE_ID", "LOC_ID", "CONTACT_ID", "New Deal", "STAGE_ID", value=1500)
api.move_opportunity_stage("OPP_ID", "NEW_STAGE_ID")
api.update_opportunity_status("OPP_ID", "won")

# --- Calendars ---
slots = api.get_free_slots("CAL_ID", start_date_ms=1746057600000, end_date_ms=1746316800000)
appt = api.create_appointment("CAL_ID", "LOC_ID", "CONTACT_ID", "2026-05-01T10:00:00Z", "2026-05-01T10:30:00Z")

# --- Conversations ---
conv = api.create_conversation("LOC_ID", "CONTACT_ID")
api.send_message(conv["conversation"]["id"], "SMS", "Hello! Your appointment is confirmed.")

# --- Invoices ---
invoice = api.create_invoice("LOC_ID", {"name": "Consulting", "currency": "USD", "items": [{"name": "1hr", "price": 150, "quantity": 1}], "issueDate": "2026-04-26"})
api.send_invoice(invoice["_id"], "LOC_ID", "USER_ID")

# --- Social Planner ---
accounts = api.get_social_accounts("LOC_ID")
api.create_social_post("LOC_ID", ["ACCOUNT_ID"], "New post content! #marketing", schedule_date="2026-05-01T10:00:00Z")
```

### 4. Command-Line Usage

```bash
python3 scripts/ghl_api.py get_contacts --location "LOCATION_ID"
python3 scripts/ghl_api.py get_pipelines --location "LOCATION_ID"
python3 scripts/ghl_api.py get_calendars --location "LOCATION_ID"
python3 scripts/ghl_api.py list_invoices --location "LOCATION_ID"
python3 scripts/ghl_api.py get_workflows --location "LOCATION_ID"
python3 scripts/ghl_api.py get_social_accounts --location "LOCATION_ID"
python3 scripts/ghl_api.py get_users_by_location --location "LOCATION_ID"
```

## Required API Scopes

| Module | Scopes |
|---|---|
| Contacts | `contacts.readonly`, `contacts.write` |
| Opportunities | `opportunities.readonly`, `opportunities.write` |
| Calendars | `calendars.readonly`, `calendars.write` |
| Conversations | `conversations.readonly`, `conversations.write` |
| Users | `users.readonly`, `users.write` |
| Locations | `locations.readonly`, `locations.write` |
| Workflows | `workflows.readonly` |
| Invoices | `invoices.readonly`, `invoices.write` |
| Forms | `forms.readonly` |
| Surveys | `surveys.readonly` |
| Social Planner | `socialplanner/post.readonly`, `socialplanner/post.write`, `socialplanner/account.readonly` |
| Email Campaigns | `emails/schedule.readonly`, `emails/schedule.write` |
| Custom Fields | `locations/customFields.readonly`, `locations/customFields.write` |

## Webhook Verification

Webhooks include signature headers to verify authenticity:

- `X-GHL-Signature`: Ed25519 signature (Current standard — use this)
- `X-WH-Signature`: RSA-SHA256 signature (Legacy, deprecated July 2026)

## Compatibility

This skill is designed to work with:
- **[Manus](https://manus.im/)** — Drop the `gohighlevel/` folder into your `skills/` directory.
- **[OpenClaw](https://github.com/openclaw)** — Follow OpenClaw skill installation instructions.
- **[Claude Code](https://docs.anthropic.com/claude-code)** — Reference `SKILL.md` in your system prompt or project context.

## Contributing

Contributions are welcome! If you find a missing endpoint, a bug, or want to add a new workflow, please open an issue or submit a pull request.

## License

MIT License — free to use, modify, and distribute.

## Resources

- [GoHighLevel API v2 Documentation](https://marketplace.gohighlevel.com/docs/)
- [GoHighLevel Developer Portal](https://developers.gohighlevel.com/)
- [GoHighLevel API GitHub Docs](https://github.com/GoHighLevel/highlevel-api-docs)
