import os
import json
import requests
from typing import Dict, Any, Optional, List

class GoHighLevelAPI:
    """
    Helper class for interacting with the GoHighLevel API v2.
    Uses Private Integration Tokens for authentication.
    """
    BASE_URL = "https://services.leadconnectorhq.com"
    API_VERSION = "2021-07-28"

    def __init__(self, token: str = None):
        """
        Initialize the API client.
        
        Args:
            token: Private Integration Token. If not provided, looks for GHL_API_TOKEN env var.
        """
        self.token = token or os.environ.get("GHL_API_TOKEN")
        if not self.token:
            raise ValueError("GoHighLevel API token is required. Set GHL_API_TOKEN environment variable or pass it directly.")
            
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Version": self.API_VERSION,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict[str, Any]:
        """Make an HTTP request to the GHL API."""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data,
            params=params
        )
        
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = f"API Error: {e}"
            try:
                error_details = response.json()
                error_msg += f" - Details: {json.dumps(error_details)}"
            except:
                error_msg += f" - Response: {response.text}"
            raise Exception(error_msg)

    # --- Contacts ---
    
    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get a contact by ID."""
        return self._request("GET", f"contacts/{contact_id}")
        
    def search_contacts(self, location_id: str, query: str = None, limit: int = 20) -> Dict[str, Any]:
        """Search contacts in a location."""
        params = {"locationId": location_id, "limit": limit}
        if query:
            params["query"] = query
        return self._request("GET", "contacts/", params=params)
        
    def create_contact(self, location_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new contact."""
        data = {"locationId": location_id, **contact_data}
        return self._request("POST", "contacts/", data=data)
        
    def update_contact(self, contact_id: str, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing contact."""
        return self._request("PUT", f"contacts/{contact_id}", data=contact_data)

    # --- Opportunities ---
    
    def get_pipelines(self, location_id: str) -> Dict[str, Any]:
        """Get all pipelines for a location."""
        return self._request("GET", f"opportunities/pipelines?locationId={location_id}")
        
    def search_opportunities(self, location_id: str, pipeline_id: str = None) -> Dict[str, Any]:
        """Search opportunities."""
        params = {"location_id": location_id}
        if pipeline_id:
            params["pipeline_id"] = pipeline_id
        return self._request("GET", "opportunities/search", params=params)
        
    def create_opportunity(self, pipeline_id: str, location_id: str, contact_id: str, 
                          name: str, stage_id: str, status: str = "open", value: float = 0) -> Dict[str, Any]:
        """Create a new opportunity."""
        data = {
            "pipelineId": pipeline_id,
            "locationId": location_id,
            "contactId": contact_id,
            "name": name,
            "stageId": stage_id,
            "status": status,
            "monetaryValue": value
        }
        return self._request("POST", "opportunities/", data=data)
        
    def update_opportunity(self, opportunity_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an opportunity (e.g., change stage or status)."""
        return self._request("PUT", f"opportunities/{opportunity_id}", data=data)

    # --- Calendars & Appointments ---
    
    def get_calendars(self, location_id: str) -> Dict[str, Any]:
        """Get all calendars for a location."""
        return self._request("GET", f"calendars/?locationId={location_id}")
        
    def get_appointments(self, location_id: str, calendar_id: str = None) -> Dict[str, Any]:
        """Get appointments."""
        params = {"locationId": location_id}
        if calendar_id:
            params["calendarId"] = calendar_id
        return self._request("GET", "calendars/events/appointments", params=params)

if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="GoHighLevel API Helper")
    parser.add_argument("--token", help="Private Integration Token (or set GHL_API_TOKEN env var)")
    parser.add_argument("action", choices=["get_contact", "search_contacts", "get_pipelines", "get_calendars"], 
                        help="Action to perform")
    parser.add_argument("--id", help="ID for the specific resource (contact_id, etc.)")
    parser.add_argument("--location", help="Location ID (required for searches)")
    
    args = parser.parse_args()
    
    try:
        api = GoHighLevelAPI(args.token)
        
        if args.action == "get_contact":
            if not args.id:
                print("Error: --id is required for get_contact")
                sys.exit(1)
            result = api.get_contact(args.id)
            print(json.dumps(result, indent=2))
            
        elif args.action == "search_contacts":
            if not args.location:
                print("Error: --location is required for search_contacts")
                sys.exit(1)
            result = api.search_contacts(args.location)
            print(json.dumps(result, indent=2))
            
        elif args.action == "get_pipelines":
            if not args.location:
                print("Error: --location is required for get_pipelines")
                sys.exit(1)
            result = api.get_pipelines(args.location)
            print(json.dumps(result, indent=2))
            
        elif args.action == "get_calendars":
            if not args.location:
                print("Error: --location is required for get_calendars")
                sys.exit(1)
            result = api.get_calendars(args.location)
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
