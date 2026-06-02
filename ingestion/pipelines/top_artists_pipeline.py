
import uuid
from ingestion.clients.spotify_api_client import SpotifyClient
from ingestion.loaders.sql_loader import SqlLoader

# Define list of time ranges
TIME_RANGES = ['short_term', 'medium_term', 'long_term']

def run_top_artists_pipeline():
  client = SpotifyClient()
  loader = SqlLoader()
  batch_id = str(uuid.uuid4())
  for time_range in TIME_RANGES:  
    response = client.get("me/top/artists", params={"limit": 50, "time_range": time_range})
    result = response["items"]            
    print(f"Fetched {len(result)} artists for {time_range} time range")
    loader.load_top_artists(result, time_range=time_range, batch_id=batch_id)

if __name__ == "__main__":
  run_top_artists_pipeline()