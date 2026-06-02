
from dotenv import load_dotenv
from ingestion.clients.spotify_api_client import SpotifyClient

#============== Check API response ====================#

# Instantiates the client
client = SpotifyClient()

# Calls the API to return my personal account information
result = client.get("me")
print(result)
