# GoHighLevel API Skill for AI Agents

A **Manus skill** that enables AI agents to manage client businesses through the [GoHighLevel](https://www.gohighlevel.com/) CRM platform via the official API v2. Compatible with **Manus**, **OpenClaw**, and **Claude Code**.

## What This Skill Does

This skill provides AI agents with the tools and knowledge to:

- Manage **contacts** (create, search, update, tag)
- Manage **sales pipelines and opportunities** (create deals, move stages, update status)
- Manage **calendars and appointments** (list calendars, view bookings)
- Handle **webhooks** (receive real-time events from GoHighLevel)

## Directory Structure

```
gohighlevel/
├── SKILL.md                  # Main skill instructions (loaded by AI agent)
├── README.md                 # This file (for GitHub)
├── scripts/
│   └── ghl_api.py            # Python API helper class
└── references/
    └── api_reference.md      # Detailed API endpoint reference
```

## Quick Start

### 1. Get a Private Integration Token

1. In GoHighLevel, go to **Settings > Private Integrations**.
2. Click **Create new Integration**.
3. Select the required scopes (e.g., `contacts.write`, `opportunities.write`, `calendars.readonly`).
4. Copy the generated token.

### 2. Set the Token

```bash
export GHL_API_TOKEN="your_private_integration_token"
```

### 3. Use the Python Helper

```python
from scripts.ghl_api import GoHighLevelAPI

api = GoHighLevelAPI()  # Reads GHL_API_TOKEN from environment

# Search contacts
contacts = api.search_contacts(location_id="YOUR_LOCATION_ID")

# Create a contact
new_contact = api.create_contact(
    location_id="YOUR_LOCATION_ID",
    contact_data={
        "firstName": "Jane",
        "lastName": "Smith",
        "email": "jane@example.com",
        "phone": "+1234567890"
    }
)

# Get pipelines
pipelines = api.get_pipelines(location_id="YOUR_LOCATION_ID")

# Create an opportunity
opp = api.create_opportunity(
    pipeline_id="PIPELINE_ID",
    location_id="LOCATION_ID",
    contact_id="CONTACT_ID",
    name="New Deal",
    stage_id="STAGE_ID",
    value=1500.00
)
```

### 4. Command-Line Usage

```bash
# Get a contact
python3 scripts/ghl_api.py get_contact --id "CONTACT_ID"

# Search contacts
python3 scripts/ghl_api.py search_contacts --location "LOCATION_ID"

# Get pipelines
python3 scripts/ghl_api.py get_pipelines --location "LOCATION_ID"

# Get calendars
python3 scripts/ghl_api.py get_calendars --location "LOCATION_ID"
```

## API Reference

See [references/api_reference.md](references/api_reference.md) for a full reference of all supported endpoints, request formats, and webhook payloads.

## Authentication

This skill uses **Private Integration Tokens** (GHL API v2). These are static tokens scoped to specific permissions, ideal for AI agents operating on behalf of a client sub-account.

| Feature | Private Integration Token | OAuth 2.0 |
|---|---|---|
| Setup | Simple (UI-generated) | Complex (OAuth flow) |
| Refresh | Manual rotation | Auto-refresh daily |
| Best for | AI agents, automation | Multi-tenant apps |

## Supported API Modules

| Module | Scope(s) | Description |
|---|---|---|
| Contacts | `contacts.readonly`, `contacts.write` | CRM contact management |
| Opportunities | `opportunities.readonly`, `opportunities.write` | Sales pipeline management |
| Calendars | `calendars.readonly` | Calendar and appointment access |
| Webhooks | Varies | Real-time event notifications |

## Compatibility

This skill is designed to work with:
- **[Manus](https://manus.im/)** - Drop the `gohighlevel/` folder into your `skills/` directory.
- **[OpenClaw](https://github.com/openclaw)** - Follow OpenClaw skill installation instructions.
- **[Claude Code](https://docs.anthropic.com/claude-code)** - Reference `SKILL.md` in your system prompt or project context.

## Contributing

Contributions are welcome! If you find a missing endpoint, a bug, or want to add a new workflow, please open an issue or submit a pull request.

## License

MIT License — free to use, modify, and distribute.

## Resources

- [GoHighLevel API v2 Documentation](https://marketplace.gohighlevel.com/docs/)
- [GoHighLevel Developer Portal](https://developers.gohighlevel.com/)
- [GoHighLevel API GitHub Docs](https://github.com/GoHighLevel/highlevel-api-docs)
