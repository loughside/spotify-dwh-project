
import uuid
from ingestion.clients.spotify_api_client import SpotifyClient
from ingestion.loaders.sql_loader import SqlLoader

def run_recently_played_pipeline():
  client = SpotifyClient()
  loader = SqlLoader()
  batch_id = str(uuid.uuid4())

  total = 0
  params = {"limit": 50}

  while True:
    response = client.get("me/player/recently-played", params=params)
    result = response["items"]
    total += len(result)            
    print(f"Fetched {len(result)} recently played tracks so far...")
    loader.load_recently_played(result, batch_id=batch_id)

    if response['next'] is None:
      break
    params["before"] = response["cursors"]["before"]

if __name__ == "__main__":
  run_recently_played_pipeline()