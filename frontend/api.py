import requests
import pandas as pd

API_BASE_URL = "http://127.0.0.1:8000"

class ReflectaClient:
    """
    A simple wrapper around the Reflecta API for the Streamlit Frontend.
    """

    def get_dashboard_stats(self):
        """Fetch analytics data for the dashboard."""
        try:
            response = requests.get(f"{API_BASE_URL}/analytics/dashboard")
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def create_entry(self, content: str):
        """Send a raw thought to the backend."""
        payload = {"raw_content": content}
        try:
            response = requests.post(f"{API_BASE_URL}/entries/", json=payload)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def get_entries(self):
        """Fetch all history."""
        try:
            response = requests.get(f"{API_BASE_URL}/entries/")
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []

    def get_todos(self):
        """Fetch all active tasks."""
        try:
            response = requests.get(f"{API_BASE_URL}/todos/")
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []

    def delete_todo(self, todo_id: int):
        """Delete a task."""
        try:
            requests.delete(f"{API_BASE_URL}/todos/{todo_id}")
            return True
        except:
            return False

    def create_todo(self, title: str):
        """Create a manual task."""
        payload = {"title": title}
        try:
            requests.post(f"{API_BASE_URL}/todos/", json=payload)
            return True
        except:
            return False
