# GoHighLevel API v2 Reference: Marketing & Finance

## Forms & Surveys API

Retrieve forms, surveys, and their submissions.

**Required Scopes:** `forms.readonly`, `surveys.readonly`

### Get Forms
- **Endpoint:** `GET /forms/`
- **Query Params:** `locationId` (required), `skip`, `limit`, `type`
- **Response:** Returns list of forms.

### Get Form Submissions
- **Endpoint:** `GET /forms/submissions`
- **Query Params:** `locationId` (required), `formId` (optional), `page`, `limit`, `startAt`, `endAt`
- **Response:** Returns list of form submissions.

### Get Surveys
- **Endpoint:** `GET /surveys/`
- **Query Params:** `locationId` (required), `skip`, `limit`, `type`
- **Response:** Returns list of surveys.

### Get Survey Submissions
- **Endpoint:** `GET /surveys/submissions`
- **Query Params:** `locationId` (required), `surveyId` (optional), `page`, `limit`, `startAt`, `endAt`
- **Response:** Returns list of survey submissions.

---

## Invoices API

Manage invoices, payments, and billing settings.

**Required Scopes:** `invoices.readonly`, `invoices.write`

### List Invoices
- **Endpoint:** `GET /invoices/`
- **Query Params:** `altId` (required, usually locationId), `altType` (required, usually "location"), `limit`, `offset`
- **Response:** Returns list of invoices.

### Get Invoice
- **Endpoint:** `GET /invoices/{invoiceId}`
- **Query Params:** `altId` (required), `altType` (required)
- **Response:** Returns invoice details including `status`, `amountDue`, `invoiceItems`.

### Create Invoice
- **Endpoint:** `POST /invoices/`
- **Body:**
  ```json
  {
    "altId": "LOCATION_ID",
    "altType": "location",
    "name": "Consulting Services",
    "currency": "USD",
    "items": [
      {
        "name": "1 Hour Consultation",
        "price": 150.00,
        "quantity": 1
      }
    ],
    "issueDate": "2026-04-26",
    "sentTo": "CONTACT_ID",
    "liveMode": true
  }
  ```

### Send Invoice
- **Endpoint:** `POST /invoices/{invoiceId}/send`
- **Body:** Include `altId`, `altType`, `userId`, `action`, `liveMode`.

### Record Manual Payment
- **Endpoint:** `POST /invoices/{invoiceId}/record-payment`
- **Body:** Include `altId`, `altType`, `mode`, `notes`.

---

## Social Planner API

Manage social media posts across platforms (Facebook, Instagram, LinkedIn, Twitter, Google My Business, TikTok, YouTube, Pinterest).

**Required Scopes:** `socialplanner/post.readonly`, `socialplanner/post.write`, `socialplanner/account.readonly`

### Get Accounts
- **Endpoint:** `GET /social-media-posting/{locationId}/accounts`
- **Response:** Returns connected social media accounts.

### Get Posts
- **Endpoint:** `POST /social-media-posting/{locationId}/posts/list`
- **Body:** Include `type`, `accounts`, `skip`, `limit`, `fromDate`, `toDate`.

### Create Post
- **Endpoint:** `POST /social-media-posting/{locationId}/posts`
- **Body:**
  ```json
  {
    "accountIds": ["ACCOUNT_ID_1", "ACCOUNT_ID_2"],
    "type": "text",
    "summary": "Check out our new services! #marketing",
    "status": "scheduled",
    "scheduleDate": "2026-05-01T10:00:00Z"
  }
  ```

### Edit Post
- **Endpoint:** `PUT /social-media-posting/{locationId}/posts/{id}`
- **Body:** Include fields to update (e.g., `summary`, `scheduleDate`, `status`).

### Delete Post
- **Endpoint:** `DELETE /social-media-posting/{locationId}/posts/{id}`

---

## Email Marketing (Campaigns) API

Manage email campaigns.

**Required Scopes:** `emails/schedule.readonly`, `emails/schedule.write`

### List Email Campaigns
- **Endpoint:** `GET /emails/public/v2/locations/{locationId}/campaigns/emails`
- **Query Params:** `limit`, `offset`, `search`, `status`
- **Response:** Returns list of email campaigns.

### Create Email Campaign
- **Endpoint:** `POST /emails/public/v2/locations/{locationId}/campaigns/email-campaign`
- **Body:**
  ```json
  {
    "name": "May Newsletter",
    "editorType": "builder",
    "timeZone": "America/Los_Angeles",
    "userId": "USER_ID"
  }
  ```

### Update Email Campaign
- **Endpoint:** `PATCH /emails/public/v2/locations/{locationId}/campaigns/{campaignId}`
- **Body:** Include fields to update (e.g., `name`, `editorContent`).

### Delete Email Campaign
- **Endpoint:** `DELETE /emails/public/v2/locations/{locationId}/campaigns/{campaignId}`
