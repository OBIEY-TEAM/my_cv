import os
import requests
import logging

logger = logging.getLogger(__name__)

class GoogleJulesClient:
    """
    Client for interacting with Google's Jules API.
    Supports real HTTP API requests using X-Goog-Api-Key as well as a Mock mode for development/testing.
    """
    BASE_URL = os.getenv("JULES_API_BASE_URL", "https://jules.googleapis.com/v1alpha")

    def __init__(self, api_key=None, mock_mode=None):
        self.api_key = api_key or os.getenv("JULES_API_KEY", "")
        if mock_mode is None:
            mock_mode = os.getenv("JULES_API_MOCK_MODE", "true").lower() in ("true", "1", "yes")
        self.mock_mode = mock_mode

    def _get_headers(self):
        return {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
        }

    def create_session(self, prompt, repo_name=""):
        if self.mock_mode or not self.api_key:
            logger.info("Using mock mode for Jules create_session")
            return {
                "name": "sessions/mock-session-123",
                "id": "mock-session-123",
                "prompt": prompt,
                "status": "active"
            }

        url = f"{self.BASE_URL}/sessions"
        payload = {
            "prompt": prompt,
        }
        if repo_name:
            payload["repository"] = repo_name

        response = requests.post(url, json=payload, headers=self._get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    def list_activities(self, session_name):
        if self.mock_mode or not self.api_key:
            logger.info("Using mock mode for Jules list_activities")
            return {
                "activities": [
                    {
                        "name": f"{session_name}/activities/act-1",
                        "id": "act-1",
                        "type": "plan_generated",
                        "content": {"summary": "Generated CV and Motivation Letter customization plan"},
                        "plan_approved": True
                    }
                ]
            }

        url = f"{self.BASE_URL}/{session_name}/activities"
        response = requests.get(url, headers=self._get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    def approve_plan(self, session_name, activity_id):
        if self.mock_mode or not self.api_key:
            logger.info("Using mock mode for Jules approve_plan")
            return {"status": "approved", "activity_id": activity_id}

        url = f"{self.BASE_URL}/{session_name}/activities/{activity_id}:approvePlan"
        response = requests.post(url, headers=self._get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    def send_message(self, session_name, message):
        if self.mock_mode or not self.api_key:
            logger.info("Using mock mode for Jules send_message")
            return {
                "name": f"{session_name}/activities/msg-reply",
                "id": "msg-reply",
                "type": "message",
                "content": {"text": f"Mock Jules response to: {message}"}
            }

        url = f"{self.BASE_URL}/{session_name}:sendMessage"
        payload = {"text": message}
        response = requests.post(url, json=payload, headers=self._get_headers(), timeout=30)
        response.raise_for_status()
        return response.json()
