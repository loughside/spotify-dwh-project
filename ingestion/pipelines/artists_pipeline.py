
import uuid
import json
from ingestion.clients.spotify_api_client import SpotifyClient
from ingestion.loaders.sql_loader import SqlLoader

def run_artists_pipeline():
    client = SpotifyClient()
    loader = SqlLoader()
    batch_id = str(uuid.uuid4())

    # Query bronze.top_artists for distinct artist IDs
    cursor = loader.cnxn.cursor()
    cursor.execute("SELECT raw_json FROM bronze.top_artists")

    rows = cursor.fetchall()

    # Extract distinct artist IDs
    artist_ids = set()
    for row in rows:
        artist = json.loads(row[0])
        artist_ids.add(artist["id"])

    print(f"Found {len(artist_ids)} distinct artists to fetch")

    total = 0
    for artist_id in artist_ids:
        response = client.get(f"artists/{artist_id}")
        loader.load_artists(response, batch_id=batch_id)
        total += 1
        if total % 50 == 0:
            print(f"Loaded {total} artists...")

    print(f"Done — {total} artists loaded")

if __name__ == "__main__":
    run_artists_pipeline()