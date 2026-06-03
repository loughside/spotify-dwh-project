
import uuid
from ingestion.clients.spotify_api_client import SpotifyClient
from ingestion.loaders.sql_loader import SqlLoader

def run_saved_tracks_pipeline():
  client = SpotifyClient()
  loader = SqlLoader()
  batch_id = str(uuid.uuid4())

  total = 0
  params = {"limit": 50}

  while True:
    response = client.get("me/tracks", params=params)
    result = response["items"]
    total += len(result)            
    print(f"Fetched {len(result)} saved tracks so far...")
    loader.load_saved_tracks(result, batch_id=batch_id)

    if response['next'] is None:
      break
    params["offset"] = params.get("offset", 0) + 50

if __name__ == "__main__":
  run_saved_tracks_pipeline()