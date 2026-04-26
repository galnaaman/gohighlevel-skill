# GoHighLevel API v2 Reference

This document provides a quick reference for the most common GoHighLevel API v2 endpoints used for managing client businesses.

## Authentication

All API requests require a Private Integration Token (or OAuth Access Token) passed in the `Authorization` header, along with the `Version` header.

```http
Authorization: Bearer <YOUR_PRIVATE_INTEGRATION_TOKEN>
Version: 2021-07-28
Accept: application/json
Content-Type: application/json
```

**Base URL:** `https://services.leadconnectorhq.com`

## Contacts API

Manage contacts, leads, and customer data.

### Get Contact
- **Endpoint:** `GET /contacts/{contactId}`
- **Scope:** `contacts.readonly`
- **Response:** Returns full contact details including custom fields and tags.

### Search Contacts
- **Endpoint:** `GET /contacts/`
- **Query Params:** `locationId` (required), `query` (optional), `limit` (optional)
- **Scope:** `contacts.readonly`

### Create Contact
- **Endpoint:** `POST /contacts/`
- **Scope:** `contacts.write`
- **Body:**
  ```json
  {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "locationId": "LOCATION_ID",
    "tags": ["new lead", "api"]
  }
  ```

### Update Contact
- **Endpoint:** `PUT /contacts/{contactId}`
- **Scope:** `contacts.write`
- **Body:** Same structure as Create Contact, but only include fields to update.

## Opportunities API

Track sales pipeline, manage deals, and automate opportunity workflows.

### Get Pipelines
- **Endpoint:** `GET /opportunities/pipelines`
- **Query Params:** `locationId` (required)
- **Scope:** `opportunities.readonly`
- **Response:** Returns list of pipelines and their stages for the location.

### Search Opportunities
- **Endpoint:** `GET /opportunities/search`
- **Query Params:** `location_id` (required), `pipeline_id` (optional)
- **Scope:** `opportunities.readonly`

### Create Opportunity
- **Endpoint:** `POST /opportunities/`
- **Scope:** `opportunities.write`
- **Body:**
  ```json
  {
    "pipelineId": "PIPELINE_ID",
    "locationId": "LOCATION_ID",
    "name": "New Deal",
    "contactId": "CONTACT_ID",
    "status": "open",
    "stageId": "STAGE_ID",
    "monetaryValue": 500.00
  }
  ```

### Update Opportunity
- **Endpoint:** `PUT /opportunities/{opportunityId}`
- **Scope:** `opportunities.write`
- **Body:** Include fields to update (e.g., `status`: "won", "lost", "abandoned", or `stageId` to move pipeline stages).

## Calendars & Appointments API

Schedule appointments and manage calendar events.

### Get Calendars
- **Endpoint:** `GET /calendars/`
- **Query Params:** `locationId` (required)
- **Scope:** `calendars.readonly`

### Get Appointments
- **Endpoint:** `GET /calendars/events/appointments`
- **Query Params:** `locationId` (required), `calendarId` (optional)
- **Scope:** `calendars.readonly`

## Webhooks

Real-time notifications for events in GoHighLevel.

### Setting up Webhooks
1. Create a Private Integration or Marketplace App.
2. Define the required scopes.
3. Configure the Webhook URL in the integration settings.
4. Subscribe to specific events (e.g., `ContactCreate`, `OpportunityStatusUpdate`).

### Webhook Verification
Webhooks include signature headers to verify authenticity:
- `X-GHL-Signature`: Ed25519 signature (Current standard)
- `X-WH-Signature`: RSA-SHA256 signature (Legacy, deprecated July 2026)

### Common Webhook Payload Structure
```json
{
  "type": "ContactCreate",
  "timestamp": "2025-01-28T14:35:00.000Z",
  "webhookId": "test-123",
  "locationId": "LOCATION_ID",
  "data": {
    "id": "CONTACT_ID",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com"
  }
}
```
