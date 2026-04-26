# GoHighLevel API v2 Reference: Conversations & Calendars

## Conversations API

Manage SMS, email, and call messaging threads.

**Required Scopes:** `conversations.readonly`, `conversations.write`

### Get Conversation
- **Endpoint:** `GET /conversations/{conversationId}`
- **Response:** Returns conversation details including `contactId`, `locationId`, `type` (1=Phone, 2=Email, 3=FB Messenger, 4=Review, 5=Group SMS), `unreadCount`, `assignedTo`.

### Create Conversation
- **Endpoint:** `POST /conversations/`
- **Body:**
  ```json
  {
    "locationId": "LOCATION_ID",
    "contactId": "CONTACT_ID"
  }
  ```

### Update Conversation
- **Endpoint:** `PUT /conversations/{conversationId}`
- **Body:**
  ```json
  {
    "locationId": "LOCATION_ID",
    "unreadCount": 0,
    "starred": true
  }
  ```

### Delete Conversation
- **Endpoint:** `DELETE /conversations/{conversationId}`

---

## Calendars & Appointments API

Schedule appointments and manage calendar events.

**Required Scopes:** `calendars.readonly`, `calendars.write`

### Get Calendars
- **Endpoint:** `GET /calendars/`
- **Query Params:** `locationId` (required), `groupId` (optional)
- **Response:** Returns list of calendars for the location.

### Get Free Slots
- **Endpoint:** `GET /calendars/{calendarId}/free-slots`
- **Query Params:** `startDate` (required, ms timestamp), `endDate` (required, ms timestamp), `timezone` (optional)
- **Response:** Returns availability map keyed by date.

### Create Calendar
- **Endpoint:** `POST /calendars/`
- **Body:**
  ```json
  {
    "locationId": "LOCATION_ID",
    "name": "Consultation Call",
    "description": "30 min intro call",
    "slotDuration": 30,
    "slotDurationUnit": "mins"
  }
  ```

### Update Calendar
- **Endpoint:** `PUT /calendars/{calendarId}`
- **Body:** Include fields to update (e.g., `isActive`, `name`, `slotDuration`).

### Delete Calendar
- **Endpoint:** `DELETE /calendars/{calendarId}`
