---
name: gohighlevel
description: "GoHighLevel API integration skill. Use for: managing contacts, opportunities, pipelines, calendars, and webhooks in GoHighLevel via API v2 using Private Integration Tokens. Compatible with OpenClaw and Claude Code."
---

# GoHighLevel API Skill

This skill provides the necessary tools and references to interact with the GoHighLevel (GHL) API v2. It enables AI agents to manage client businesses, including contacts, sales pipelines, appointments, and webhooks.

## Prerequisites

To use this skill, you need a **Private Integration Token** from the GoHighLevel sub-account.

1. In GoHighLevel, navigate to **Settings > Private Integrations**.
2. Click **Create new Integration**.
3. Select the necessary scopes (e.g., `contacts.readonly`, `contacts.write`, `opportunities.readonly`, `opportunities.write`, `calendars.readonly`).
4. Copy the generated token.

Set the token as an environment variable before running scripts:
```bash
export GHL_API_TOKEN="your_private_integration_token"
```

## Available Resources

### 1. API Helper Script (`scripts/ghl_api.py`)

A Python helper script is provided to interact with the GHL API easily. It handles authentication, headers, and common endpoints.

**Usage:**
```bash
# Get a contact
python3 /home/ubuntu/skills/gohighlevel/scripts/ghl_api.py get_contact --id "CONTACT_ID"

# Search contacts in a location
python3 /home/ubuntu/skills/gohighlevel/scripts/ghl_api.py search_contacts --location "LOCATION_ID"

# Get pipelines
python3 /home/ubuntu/skills/gohighlevel/scripts/ghl_api.py get_pipelines --location "LOCATION_ID"

# Get calendars
python3 /home/ubuntu/skills/gohighlevel/scripts/ghl_api.py get_calendars --location "LOCATION_ID"
```

You can also import this script into your own Python code:
```python
import sys
sys.path.append('/home/ubuntu/skills/gohighlevel/scripts')
from ghl_api import GoHighLevelAPI

api = GoHighLevelAPI(token="YOUR_TOKEN")
contact = api.get_contact("CONTACT_ID")
```

### 2. API Reference (`references/api_reference.md`)

For detailed information on endpoints, request bodies, and webhook structures, refer to the API reference document.

**Read the reference:**
```bash
cat /home/ubuntu/skills/gohighlevel/references/api_reference.md
```

## Common Workflows

### Managing Contacts

1. **Search for a contact:** Use `search_contacts` with the `locationId` and an optional `query` (email, phone, or name).
2. **Create a contact:** Use the `create_contact` method in the Python script, providing `locationId`, `firstName`, `lastName`, `email`, etc.
3. **Update a contact:** Use the `update_contact` method with the `contactId` and the fields to update.

### Managing Opportunities (Sales Pipeline)

1. **Get Pipelines:** First, fetch the pipelines for the location using `get_pipelines` to get the `pipelineId` and `stageId`s.
2. **Create Opportunity:** Use `create_opportunity` with the `pipelineId`, `locationId`, `contactId`, `name`, and `stageId`.
3. **Move Opportunity:** Use `update_opportunity` to change the `stageId` or `status` (open, won, lost, abandoned).

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
location).
