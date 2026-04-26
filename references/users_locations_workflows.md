# GoHighLevel API v2 Reference: Users, Locations & Workflows

## Users & Teams API

Manage user accounts and team members within GoHighLevel.

**Required Scopes:** `users.readonly`, `users.write`

### Get User
- **Endpoint:** `GET /users/{userId}`
- **Response:** Returns user details including `name`, `email`, `phone`, `permissions`, `roles`.

### Get Users by Location
- **Endpoint:** `GET /users/`
- **Query Params:** `locationId` (required)
- **Response:** Returns list of users for the location.

### Create User
- **Endpoint:** `POST /users/`
- **Body:**
  ```json
  {
    "companyId": "COMPANY_ID",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "password": "SecurePassword123!",
    "phone": "+1234567890",
    "type": "account",
    "role": "user",
    "locationIds": ["LOCATION_ID"]
  }
  ```

### Update User
- **Endpoint:** `PUT /users/{userId}`
- **Body:** Include fields to update (e.g., `firstName`, `phone`, `role`, `locationIds`). Note: Email updates are deprecated for security reasons.

### Delete User
- **Endpoint:** `DELETE /users/{userId}`

---

## Sub-Account / Location Management API

Manage business locations (sub-accounts).

**Required Scopes:** `locations.readonly`, `locations.write`

### Get Location
- **Endpoint:** `GET /locations/{locationId}`
- **Response:** Returns location details including `name`, `phone`, `address`, `settings`.

### Create Location (Sub-Account)
- **Endpoint:** `POST /locations/`
- **Body:**
  ```json
  {
    "name": "New Client Business",
    "phone": "+1234567890",
    "companyId": "COMPANY_ID",
    "address": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "country": "US",
    "postalCode": "12345",
    "timezone": "America/Los_Angeles"
  }
  ```
  *Note: "Create Sub-Account" feature is only available on the Agency Pro ($497) plan.*

### Update Location
- **Endpoint:** `PUT /locations/{locationId}`
- **Body:** Include fields to update (e.g., `name`, `phone`, `address`, `settings`).

### Delete Location
- **Endpoint:** `DELETE /locations/{locationId}`
- **Query Params:** `deleteTwilioAccount` (optional boolean)

---

## Workflows API

Retrieve automation workflows.

**Required Scopes:** `workflows.readonly`

### Get Workflows
- **Endpoint:** `GET /workflows/`
- **Query Params:** `locationId` (required)
- **Response:** Returns list of workflows for the location.
- *Note: Currently, there is no direct API endpoint to create or modify workflows. The available API is limited to retrieving workflow information.*
