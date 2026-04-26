---
name: gohighlevel
description: "Comprehensive GoHighLevel API v2 integration skill. Use for: managing contacts, opportunities, pipelines, calendars, webhooks, users, locations, workflows, invoices, forms, surveys, social planner, and email campaigns via API v2 using Private Integration Tokens. Compatible with OpenClaw and Claude Code."
---

# GoHighLevel API Skill

This skill provides the necessary tools and references to interact with the GoHighLevel (GHL) API v2. It enables AI agents to fully manage client businesses across all major GHL modules.

## Prerequisites

To use this skill, you need a **Private Integration Token** from the GoHighLevel sub-account.

1. In GoHighLevel, navigate to **Settings > Private Integrations**.
2. Click **Create new Integration**.
3. Select the necessary scopes (e.g., `contacts.write`, `opportunities.write`, `calendars.readonly`, `invoices.write`, etc.).
4. Copy the generated token.

Set the token as an environment variable before running scripts:
```bash
export GHL_API_TOKEN="your_private_integration_token"
```

## Available Resources

### 1. API Helper Script (`scripts/ghl_api.py`)

A comprehensive Python helper script is provided to interact with the GHL API easily. It handles authentication, headers, and endpoints for all major modules.

**Usage:**
```bash
# Get a contact
python3 /home/ubuntu/skills/gohighlevel/scripts/ghl_api.py get_contact --id "CONTACT_ID"

# Search contacts in a location
python3 /home/ubuntu/skills/gohighlevel/scripts/ghl_api.py get_contacts --location "LOCATION_ID"

# Get pipelines
python3 /home/ubuntu/skills/gohighlevel/scripts/ghl_api.py get_pipelines --location "LOCATION_ID"

# Get calendars
python3 /home/ubuntu/skills/gohighlevel/scripts/ghl_api.py get_calendars --location "LOCATION_ID"

# List invoices
python3 /home/ubuntu/skills/gohighlevel/scripts/ghl_api.py list_invoices --location "LOCATION_ID"
```

You can also import this script into your own Python code:
```python
import sys
sys.path.append('/home/ubuntu/skills/gohighlevel/scripts')
from ghl_api import GoHighLevelAPI

api = GoHighLevelAPI(token="YOUR_TOKEN")
contact = api.get_contact("CONTACT_ID")
```

### 2. API References

For detailed information on endpoints, request bodies, and webhook structures, refer to the domain-specific API reference documents:

- **Core CRM:** `references/api_reference.md` (Contacts, Opportunities, Webhooks)
- **Communication:** `references/conversations_calendars.md` (Conversations, Calendars, Appointments)
- **Admin:** `references/users_locations_workflows.md` (Users, Locations, Workflows)
- **Marketing & Finance:** `references/marketing_finance.md` (Forms, Surveys, Invoices, Social Planner, Email Campaigns)

**Read a reference:**
```bash
cat /home/ubuntu/skills/gohighlevel/references/marketing_finance.md
```

## Common Workflows

### Managing Contacts & Pipelines

1. **Search for a contact:** Use `get_contacts` with the `locationId` and an optional `query` (email, phone, or name).
2. **Create Opportunity:** Use `create_opportunity` with the `pipelineId`, `locationId`, `contactId`, `name`, and `stageId`.
3. **Move Opportunity:** Use `update_opportunity` to change the `stageId` or `status` (open, won, lost, abandoned).

### Managing Appointments

1. **Get Calendars:** Fetch calendars for the location using `get_calendars`.
2. **Check Availability:** Use `get_free_slots` to find open times.
3. **Book Appointment:** Use `create_appointment` with the `calendarId`, `locationId`, `contactId`, `startTime`, and `endTime`.

### Handling Webhooks

GoHighLevel can send real-time updates to your application.
1. Set up a webhook endpoint in your application.
2. In GHL, configure the Private Integration to send webhooks to your URL.
3. Verify the webhook authenticity using the `X-GHL-Signature` header (Ed25519 signature).
4. See `references/api_reference.md` for payload examples.

## Important Notes

- **API Version:** This skill uses GoHighLevel API v2 (`Version: 2021-07-28`).
- **Authentication:** Always use the `Authorization: Bearer <TOKEN>` header.
- **Rate Limits:** Be mindful of GoHighLevel API rate limits (typically 100 requests per 10 seconds per location).
