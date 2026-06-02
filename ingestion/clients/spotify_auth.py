
import base64
import os
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
 
import requests
from dotenv import load_dotenv, set_key
 
load_dotenv()
 
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
 
# Scopes required for personal listening history
SCOPES = "user-read-recently-played user-top-read user-library-read"
 
# Will be populated by the local callback server
auth_code = None
 
 
def build_auth_url():
    """Build the Spotify authorisation URL to open in the browser."""
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    }
    return "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
 
 
class CallbackHandler(BaseHTTPRequestHandler):
    """Handles the single redirect request from Spotify after user login."""
 
    def do_GET(self):
        global auth_code
        # Extract the 'code' query parameter from the redirect URL
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
 
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Auth successful. You can close this tab.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing code parameter.")
 
    def log_message(self, format, *args):
        # Suppress default server log output
        pass
 
 
def exchange_code_for_tokens(code):
    """Exchange the one-time auth code for access + refresh tokens."""
    # Spotify requires client credentials as HTTP Basic Auth
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()
 
    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
 
    response = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=data
    )
    response.raise_for_status()
    return response.json()
 
 
def save_refresh_token(token):
    """Write the refresh token back into .env so pipelines can use it."""
    env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    env_path = os.path.normpath(env_path)
    set_key(env_path, "SPOTIFY_REFRESH_TOKEN", token)
    print(f"Refresh token saved to {env_path}")
 
 
def main():
    # Step 1 — open browser to Spotify login
    url = build_auth_url()
    print(f"Opening browser for Spotify login...\n{url}")
    webbrowser.open(url)
 
    # Step 2 — start local server to catch the redirect
    server = HTTPServer(("127.0.0.1", 8888), CallbackHandler)
    print("Waiting for Spotify callback on http://127.0.0.1:8888/callback ...")
    server.handle_request()  # handles exactly one request then stops
 
    if not auth_code:
        print("ERROR: No auth code received.")
        return
 
    # Step 3 — exchange code for tokens
    print("Exchanging auth code for tokens...")
    tokens = exchange_code_for_tokens(auth_code)
 
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
 
    print(f"\nAccess token:  {access_token}")
    print(f"Refresh token: {refresh_token}")
 
    # Step 4 — persist refresh token to .env
    if refresh_token:
        save_refresh_token(refresh_token)
    else:
        print("WARNING: No refresh token returned.")
 
 
if __name__ == "__main__":
    main()