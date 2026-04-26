"""
GoHighLevel API v2 Helper
=========================
Comprehensive Python client for the GoHighLevel API v2.
Supports Private Integration Tokens and OAuth Access Tokens.

Compatible with: Manus, OpenClaw, Claude Code

Usage:
    export GHL_API_TOKEN="your_private_integration_token"
    python3 ghl_api.py <action> [options]

Or import into your own code:
    from ghl_api import GoHighLevelAPI
    api = GoHighLevelAPI()
"""

import os
import json
import sys
import argparse
import requests
from typing import Dict, Any, Optional, List


class GoHighLevelAPI:
    """
    Comprehensive GoHighLevel API v2 client.
    Handles authentication, headers, and all major API modules.
    """

    BASE_URL = "https://services.leadconnectorhq.com"
    API_VERSION = "2021-07-28"

    def __init__(self, token: str = None):
        """
        Initialize the API client.

        Args:
            token: Private Integration Token or OAuth Access Token.
                   If not provided, reads from GHL_API_TOKEN environment variable.
        """
        self.token = token or os.environ.get("GHL_API_TOKEN")
        if not self.token:
            raise ValueError(
                "GoHighLevel API token is required. "
                "Set GHL_API_TOKEN environment variable or pass it directly."
            )
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Version": self.API_VERSION,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Dict = None,
        params: Dict = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the GHL API."""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data,
            params=params,
        )
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = f"API Error {response.status_code}: {e}"
            try:
                error_details = response.json()
                error_msg += f"\nDetails: {json.dumps(error_details, indent=2)}"
            except Exception:
                error_msg += f"\nResponse: {response.text}"
            raise Exception(error_msg)

    # =========================================================================
    # CONTACTS
    # Scopes: contacts.readonly, contacts.write
    # =========================================================================

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get a contact by ID."""
        return self._request("GET", f"contacts/{contact_id}")

    def get_contacts(self, location_id: str, query: str = None, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        """Search/list contacts in a location."""
        params = {"locationId": location_id, "limit": limit, "skip": skip}
        if query:
            params["query"] = query
        return self._request("GET", "contacts/", params=params)

    def create_contact(self, location_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new contact.
        contact_data fields: firstName, lastName, email, phone, tags, customFields, etc.
        """
        data = {"locationId": location_id, **contact_data}
        return self._request("POST", "contacts/", data=data)

    def update_contact(self, contact_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing contact."""
        return self._request("PUT", f"contacts/{contact_id}", data=contact_data)

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete a contact."""
        return self._request("DELETE", f"contacts/{contact_id}")

    def upsert_contact(self, location_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a contact (upsert by email/phone)."""
        data = {"locationId": location_id, **contact_data}
        return self._request("POST", "contacts/upsert", data=data)

    def add_contact_tags(self, contact_id: str, tags: List[str]) -> Dict[str, Any]:
        """Add tags to a contact."""
        return self._request("POST", f"contacts/{contact_id}/tags", data={"tags": tags})

    def remove_contact_tags(self, contact_id: str, tags: List[str]) -> Dict[str, Any]:
        """Remove tags from a contact."""
        return self._request("DELETE", f"contacts/{contact_id}/tags", data={"tags": tags})

    def get_contact_tasks(self, contact_id: str) -> Dict[str, Any]:
        """Get tasks for a contact."""
        return self._request("GET", f"contacts/{contact_id}/tasks")

    def create_contact_task(self, contact_id: str, title: str, due_date: str, assigned_to: str = None) -> Dict[str, Any]:
        """Create a task for a contact."""
        data = {"title": title, "dueDate": due_date, "completed": False}
        if assigned_to:
            data["assignedTo"] = assigned_to
        return self._request("POST", f"contacts/{contact_id}/tasks", data=data)

    def get_contact_notes(self, contact_id: str) -> Dict[str, Any]:
        """Get notes for a contact."""
        return self._request("GET", f"contacts/{contact_id}/notes")

    def create_contact_note(self, contact_id: str, body: str, user_id: str = None) -> Dict[str, Any]:
        """Create a note for a contact."""
        data = {"body": body}
        if user_id:
            data["userId"] = user_id
        return self._request("POST", f"contacts/{contact_id}/notes", data=data)

    def add_contact_to_workflow(self, contact_id: str, workflow_id: str) -> Dict[str, Any]:
        """Add a contact to a workflow."""
        return self._request("POST", f"contacts/{contact_id}/workflow/{workflow_id}")

    def remove_contact_from_workflow(self, contact_id: str, workflow_id: str) -> Dict[str, Any]:
        """Remove a contact from a workflow."""
        return self._request("DELETE", f"contacts/{contact_id}/workflow/{workflow_id}")

    # =========================================================================
    # OPPORTUNITIES (SALES PIPELINE)
    # Scopes: opportunities.readonly, opportunities.write
    # =========================================================================

    def get_pipelines(self, location_id: str) -> Dict[str, Any]:
        """Get all pipelines for a location."""
        return self._request("GET", "opportunities/pipelines", params={"locationId": location_id})

    def search_opportunities(
        self,
        location_id: str,
        pipeline_id: str = None,
        stage_id: str = None,
        status: str = None,
        contact_id: str = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Search opportunities with optional filters."""
        params = {"location_id": location_id, "limit": limit}
        if pipeline_id:
            params["pipeline_id"] = pipeline_id
        if stage_id:
            params["pipeline_stage_id"] = stage_id
        if status:
            params["status"] = status
        if contact_id:
            params["contact_id"] = contact_id
        return self._request("GET", "opportunities/search", params=params)

    def get_opportunity(self, opportunity_id: str) -> Dict[str, Any]:
        """Get a single opportunity by ID."""
        return self._request("GET", f"opportunities/{opportunity_id}")

    def create_opportunity(
        self,
        pipeline_id: str,
        location_id: str,
        contact_id: str,
        name: str,
        stage_id: str,
        status: str = "open",
        value: float = 0,
        assigned_to: str = None,
    ) -> Dict[str, Any]:
        """Create a new opportunity."""
        data = {
            "pipelineId": pipeline_id,
            "locationId": location_id,
            "contactId": contact_id,
            "name": name,
            "stageId": stage_id,
            "status": status,
            "monetaryValue": value,
        }
        if assigned_to:
            data["assignedTo"] = assigned_to
        return self._request("POST", "opportunities/", data=data)

    def update_opportunity(self, opportunity_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an opportunity.
        Common updates: stageId, status (open/won/lost/abandoned), monetaryValue.
        """
        return self._request("PUT", f"opportunities/{opportunity_id}", data=data)

    def delete_opportunity(self, opportunity_id: str) -> Dict[str, Any]:
        """Delete an opportunity."""
        return self._request("DELETE", f"opportunities/{opportunity_id}")

    def update_opportunity_status(self, opportunity_id: str, status: str) -> Dict[str, Any]:
        """
        Shortcut to update opportunity status.
        status: 'open', 'won', 'lost', 'abandoned'
        """
        return self.update_opportunity(opportunity_id, {"status": status})

    def move_opportunity_stage(self, opportunity_id: str, stage_id: str) -> Dict[str, Any]:
        """Shortcut to move an opportunity to a different pipeline stage."""
        return self.update_opportunity(opportunity_id, {"stageId": stage_id})

    # =========================================================================
    # CALENDARS & APPOINTMENTS
    # Scopes: calendars.readonly, calendars.write
    # =========================================================================

    def get_calendars(self, location_id: str) -> Dict[str, Any]:
        """Get all calendars for a location."""
        return self._request("GET", "calendars/", params={"locationId": location_id})

    def get_calendar(self, calendar_id: str) -> Dict[str, Any]:
        """Get a specific calendar by ID."""
        return self._request("GET", f"calendars/{calendar_id}")

    def create_calendar(self, location_id: str, name: str, extra: Dict = None) -> Dict[str, Any]:
        """Create a new calendar."""
        data = {"locationId": location_id, "name": name}
        if extra:
            data.update(extra)
        return self._request("POST", "calendars/", data=data)

    def update_calendar(self, calendar_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a calendar."""
        return self._request("PUT", f"calendars/{calendar_id}", data=data)

    def delete_calendar(self, calendar_id: str) -> Dict[str, Any]:
        """Delete a calendar."""
        return self._request("DELETE", f"calendars/{calendar_id}")

    def get_free_slots(
        self,
        calendar_id: str,
        start_date_ms: int,
        end_date_ms: int,
        timezone: str = None,
    ) -> Dict[str, Any]:
        """
        Get available booking slots for a calendar.
        start_date_ms and end_date_ms are Unix timestamps in milliseconds.
        Date range cannot exceed 31 days.
        """
        params = {"startDate": start_date_ms, "endDate": end_date_ms}
        if timezone:
            params["timezone"] = timezone
        return self._request("GET", f"calendars/{calendar_id}/free-slots", params=params)

    def get_appointments(self, location_id: str, calendar_id: str = None) -> Dict[str, Any]:
        """Get appointments for a location or specific calendar."""
        params = {"locationId": location_id}
        if calendar_id:
            params["calendarId"] = calendar_id
        return self._request("GET", "calendars/events/appointments", params=params)

    def create_appointment(
        self,
        calendar_id: str,
        location_id: str,
        contact_id: str,
        start_time: str,
        end_time: str,
        title: str = None,
        assigned_user_id: str = None,
    ) -> Dict[str, Any]:
        """
        Create an appointment.
        start_time and end_time should be ISO 8601 strings (e.g., '2026-05-01T10:00:00Z').
        """
        data = {
            "calendarId": calendar_id,
            "locationId": location_id,
            "contactId": contact_id,
            "startTime": start_time,
            "endTime": end_time,
        }
        if title:
            data["title"] = title
        if assigned_user_id:
            data["assignedUserId"] = assigned_user_id
        return self._request("POST", "calendars/events/appointments", data=data)

    def update_appointment(self, event_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an appointment."""
        return self._request("PUT", f"calendars/events/appointments/{event_id}", data=data)

    def delete_appointment(self, event_id: str) -> Dict[str, Any]:
        """Delete an appointment."""
        return self._request("DELETE", f"calendars/events/appointments/{event_id}")

    # =========================================================================
    # CONVERSATIONS (SMS, EMAIL, CALLS)
    # Scopes: conversations.readonly, conversations.write
    # =========================================================================

    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """Get a conversation by ID."""
        return self._request("GET", f"conversations/{conversation_id}")

    def create_conversation(self, location_id: str, contact_id: str) -> Dict[str, Any]:
        """Create a new conversation thread."""
        return self._request(
            "POST",
            "conversations/",
            data={"locationId": location_id, "contactId": contact_id},
        )

    def update_conversation(self, conversation_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a conversation (e.g., mark as read, star)."""
        return self._request("PUT", f"conversations/{conversation_id}", data=data)

    def delete_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """Delete a conversation."""
        return self._request("DELETE", f"conversations/{conversation_id}")

    def send_message(
        self,
        conversation_id: str,
        message_type: str,
        message: str,
        html: str = None,
        subject: str = None,
        from_name: str = None,
        from_email: str = None,
        to: str = None,
    ) -> Dict[str, Any]:
        """
        Send a message in a conversation.
        message_type: 'SMS', 'Email', 'WhatsApp', 'GMB', 'IG', 'FB', 'Custom', 'Live_Chat'
        """
        data = {"type": message_type, "message": message, "conversationId": conversation_id}
        if html:
            data["html"] = html
        if subject:
            data["subject"] = subject
        if from_name:
            data["fromName"] = from_name
        if from_email:
            data["from"] = from_email
        if to:
            data["to"] = to
        return self._request("POST", "conversations/messages", data=data)

    def get_messages(self, conversation_id: str) -> Dict[str, Any]:
        """Get messages in a conversation."""
        return self._request("GET", f"conversations/{conversation_id}/messages")

    # =========================================================================
    # USERS & TEAMS
    # Scopes: users.readonly, users.write
    # =========================================================================

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get a user by ID."""
        return self._request("GET", f"users/{user_id}")

    def get_users_by_location(self, location_id: str) -> Dict[str, Any]:
        """Get all users for a location."""
        return self._request("GET", "users/", params={"locationId": location_id})

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user.
        Required fields: companyId, firstName, lastName, email, password, type, role, locationIds
        """
        return self._request("POST", "users/", data=user_data)

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a user. Note: email updates are deprecated."""
        return self._request("PUT", f"users/{user_id}", data=user_data)

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete a user."""
        return self._request("DELETE", f"users/{user_id}")

    # =========================================================================
    # LOCATIONS (SUB-ACCOUNTS)
    # Scopes: locations.readonly, locations.write
    # =========================================================================

    def get_location(self, location_id: str) -> Dict[str, Any]:
        """Get a location (sub-account) by ID."""
        return self._request("GET", f"locations/{location_id}")

    def create_location(self, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new sub-account location.
        Required: name, phone, companyId. Agency Pro plan required.
        """
        return self._request("POST", "locations/", data=location_data)

    def update_location(self, location_id: str, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a location."""
        return self._request("PUT", f"locations/{location_id}", data=location_data)

    def delete_location(self, location_id: str) -> Dict[str, Any]:
        """Delete a location."""
        return self._request("DELETE", f"locations/{location_id}")

    # =========================================================================
    # WORKFLOWS
    # Scopes: workflows.readonly
    # =========================================================================

    def get_workflows(self, location_id: str) -> Dict[str, Any]:
        """Get all workflows for a location."""
        return self._request("GET", "workflows/", params={"locationId": location_id})

    # =========================================================================
    # INVOICES
    # Scopes: invoices.readonly, invoices.write
    # =========================================================================

    def list_invoices(self, location_id: str, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """List invoices for a location."""
        return self._request(
            "GET",
            "invoices/",
            params={"altId": location_id, "altType": "location", "limit": limit, "offset": offset},
        )

    def get_invoice(self, invoice_id: str, location_id: str) -> Dict[str, Any]:
        """Get a specific invoice."""
        return self._request(
            "GET",
            f"invoices/{invoice_id}",
            params={"altId": location_id, "altType": "location"},
        )

    def create_invoice(self, location_id: str, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new invoice.
        invoice_data fields: name, currency, items (list), issueDate, sentTo, liveMode
        """
        data = {"altId": location_id, "altType": "location", **invoice_data}
        return self._request("POST", "invoices/", data=data)

    def send_invoice(self, invoice_id: str, location_id: str, user_id: str, action: str = "send") -> Dict[str, Any]:
        """Send an invoice to the contact."""
        return self._request(
            "POST",
            f"invoices/{invoice_id}/send",
            data={"altId": location_id, "altType": "location", "userId": user_id, "action": action},
        )

    def void_invoice(self, invoice_id: str, location_id: str) -> Dict[str, Any]:
        """Void an invoice."""
        return self._request(
            "POST",
            f"invoices/{invoice_id}/void",
            data={"altId": location_id, "altType": "location"},
        )

    def record_invoice_payment(self, invoice_id: str, location_id: str, mode: str, notes: str = None) -> Dict[str, Any]:
        """Record a manual payment for an invoice."""
        data = {"altId": location_id, "altType": "location", "mode": mode}
        if notes:
            data["notes"] = notes
        return self._request("POST", f"invoices/{invoice_id}/record-payment", data=data)

    # =========================================================================
    # FORMS & SURVEYS
    # Scopes: forms.readonly, surveys.readonly
    # =========================================================================

    def get_forms(self, location_id: str, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        """Get forms for a location."""
        return self._request("GET", "forms/", params={"locationId": location_id, "limit": limit, "skip": skip})

    def get_form_submissions(self, location_id: str, form_id: str = None, limit: int = 20) -> Dict[str, Any]:
        """Get form submissions."""
        params = {"locationId": location_id, "limit": limit}
        if form_id:
            params["formId"] = form_id
        return self._request("GET", "forms/submissions", params=params)

    def get_surveys(self, location_id: str, limit: int = 20, skip: int = 0) -> Dict[str, Any]:
        """Get surveys for a location."""
        return self._request("GET", "surveys/", params={"locationId": location_id, "limit": limit, "skip": skip})

    def get_survey_submissions(self, location_id: str, survey_id: str = None, limit: int = 20) -> Dict[str, Any]:
        """Get survey submissions."""
        params = {"locationId": location_id, "limit": limit}
        if survey_id:
            params["surveyId"] = survey_id
        return self._request("GET", "surveys/submissions", params=params)

    # =========================================================================
    # SOCIAL PLANNER
    # Scopes: socialplanner/post.readonly, socialplanner/post.write, socialplanner/account.readonly
    # =========================================================================

    def get_social_accounts(self, location_id: str) -> Dict[str, Any]:
        """Get connected social media accounts."""
        return self._request("GET", f"social-media-posting/{location_id}/accounts")

    def get_social_posts(self, location_id: str, from_date: str = None, to_date: str = None, limit: int = 20) -> Dict[str, Any]:
        """List social media posts."""
        body = {"limit": str(limit)}
        if from_date:
            body["fromDate"] = from_date
        if to_date:
            body["toDate"] = to_date
        return self._request("POST", f"social-media-posting/{location_id}/posts/list", data=body)

    def create_social_post(self, location_id: str, account_ids: List[str], content: str, post_type: str = "text", schedule_date: str = None) -> Dict[str, Any]:
        """
        Create a social media post.
        post_type: 'text', 'image', 'video', 'reel', 'story'
        schedule_date: ISO 8601 string, e.g. '2026-05-01T10:00:00Z'
        """
        data = {
            "accountIds": account_ids,
            "type": post_type,
            "summary": content,
            "status": "scheduled" if schedule_date else "draft",
        }
        if schedule_date:
            data["scheduleDate"] = schedule_date
        return self._request("POST", f"social-media-posting/{location_id}/posts", data=data)

    def delete_social_post(self, location_id: str, post_id: str) -> Dict[str, Any]:
        """Delete a social media post."""
        return self._request("DELETE", f"social-media-posting/{location_id}/posts/{post_id}")

    # =========================================================================
    # EMAIL CAMPAIGNS
    # Scopes: emails/schedule.readonly, emails/schedule.write
    # =========================================================================

    def list_email_campaigns(self, location_id: str, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """List email campaigns for a location."""
        return self._request(
            "GET",
            f"emails/public/v2/locations/{location_id}/campaigns/emails",
            params={"limit": limit, "offset": offset},
        )

    def create_email_campaign(self, location_id: str, name: str, user_id: str, timezone: str = "UTC", extra: Dict = None) -> Dict[str, Any]:
        """Create a new email campaign."""
        data = {"name": name, "editorType": "builder", "timeZone": timezone, "userId": user_id}
        if extra:
            data.update(extra)
        return self._request("POST", f"emails/public/v2/locations/{location_id}/campaigns/email-campaign", data=data)

    def delete_email_campaign(self, location_id: str, campaign_id: str) -> Dict[str, Any]:
        """Delete an email campaign."""
        return self._request("DELETE", f"emails/public/v2/locations/{location_id}/campaigns/{campaign_id}")

    # =========================================================================
    # BLOGS
    # =========================================================================

    def get_blogs(self, location_id: str) -> Dict[str, Any]:
        """Get all blogs for a location."""
        return self._request("GET", "blogs/site/all", params={"locationId": location_id})

    def get_blog_posts(self, blog_id: str) -> Dict[str, Any]:
        """Get all posts for a blog."""
        return self._request("GET", "blogs/posts/all", params={"blogId": blog_id})

    def create_blog_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new blog post."""
        return self._request("POST", "blogs/posts", data=post_data)

    def update_blog_post(self, post_id: str, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a blog post."""
        return self._request("PUT", f"blogs/posts/{post_id}", data=post_data)

    # =========================================================================
    # CUSTOM FIELDS V2
    # Scopes: locations/customFields.readonly, locations/customFields.write
    # =========================================================================

    def get_custom_field(self, field_id: str) -> Dict[str, Any]:
        """Get a custom field by ID."""
        return self._request("GET", f"custom-fields/{field_id}")

    def create_custom_field(self, location_id: str, field_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a custom field."""
        data = {"locationId": location_id, **field_data}
        return self._request("POST", "custom-fields/", data=data)

    def update_custom_field(self, field_id: str, field_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a custom field."""
        return self._request("PUT", f"custom-fields/{field_id}", data=field_data)

    def delete_custom_field(self, field_id: str) -> Dict[str, Any]:
        """Delete a custom field."""
        return self._request("DELETE", f"custom-fields/{field_id}")


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="GoHighLevel API v2 CLI Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ghl_api.py get_contact --id CONTACT_ID
  python3 ghl_api.py get_contacts --location LOCATION_ID
  python3 ghl_api.py get_pipelines --location LOCATION_ID
  python3 ghl_api.py get_calendars --location LOCATION_ID
  python3 ghl_api.py get_workflows --location LOCATION_ID
  python3 ghl_api.py list_invoices --location LOCATION_ID
  python3 ghl_api.py get_forms --location LOCATION_ID
  python3 ghl_api.py get_social_accounts --location LOCATION_ID
  python3 ghl_api.py get_users_by_location --location LOCATION_ID
        """
    )
    parser.add_argument("--token", help="Private Integration Token (or set GHL_API_TOKEN env var)")
    parser.add_argument("action", help="Action to perform (see examples above)")
    parser.add_argument("--id", help="Resource ID (contact_id, opportunity_id, etc.)")
    parser.add_argument("--location", help="Location ID")
    parser.add_argument("--query", help="Search query string")

    args = parser.parse_args()

    try:
        api = GoHighLevelAPI(args.token)
        result = None

        if args.action == "get_contact":
            result = api.get_contact(args.id)
        elif args.action == "get_contacts":
            result = api.get_contacts(args.location, query=args.query)
        elif args.action == "get_pipelines":
            result = api.get_pipelines(args.location)
        elif args.action == "get_calendars":
            result = api.get_calendars(args.location)
        elif args.action == "get_workflows":
            result = api.get_workflows(args.location)
        elif args.action == "list_invoices":
            result = api.list_invoices(args.location)
        elif args.action == "get_forms":
            result = api.get_forms(args.location)
        elif args.action == "get_surveys":
            result = api.get_surveys(args.location)
        elif args.action == "get_social_accounts":
            result = api.get_social_accounts(args.location)
        elif args.action == "get_users_by_location":
            result = api.get_users_by_location(args.location)
        elif args.action == "get_location":
            result = api.get_location(args.location)
        elif args.action == "get_appointments":
            result = api.get_appointments(args.location)
        else:
            print(f"Unknown action: {args.action}")
            print("Run with --help to see available actions.")
            sys.exit(1)

        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
