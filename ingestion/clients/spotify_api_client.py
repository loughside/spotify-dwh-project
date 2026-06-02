import base64
import os

import requests
from dotenv import load_dotenv


class SpotifyClient:
    ACCOUNTS_URL = "https://accounts.spotify.com/api/token"
    BASE_URL = "https://api.spotify.com/v1"

    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

        # Get an access token immediately so the client is ready to use
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        """Exchange the refresh token for a fresh access token."""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }

        try:
            response = requests.post(self.ACCOUNTS_URL, headers=headers, data=data)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error during token refresh: {e}")

        if response.status_code != 200:
            raise Exception(
                f"Token refresh failed: {response.status_code} {response.text}"
            )

        return response.json()["access_token"]

    def get(self, endpoint, params=None):
        """Make an authenticated GET request to the Spotify Web API."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, headers=headers, params=params)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error calling {endpoint}: {e}")

        if response.status_code != 200:
            raise Exception(
                f"API error {response.status_code} on {endpoint}: {response.text}"
            )

        return response.json()