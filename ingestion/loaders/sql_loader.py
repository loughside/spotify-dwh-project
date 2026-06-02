
import os
from dotenv import load_dotenv
import pyodbc
import datetime as dt
import json

# load environment variables from .env file
load_dotenv()

SQL_DRIVER = "ODBC Driver 18 for SQL Server"
SQL_SERVER = os.getenv("SQL_SERVER") 
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME") 
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

# Define the SqlLoader class
class SqlLoader:
    def __init__(self):
        # Construct the connection string
        cnxn_string = (
          f"Driver={{{SQL_DRIVER}}};"
          f"Server={SQL_SERVER};"
          f"Database={SQL_DATABASE};"
          f"UID={SQL_USERNAME};"
          f"PWD={SQL_PASSWORD};"
          "Encrypt=yes;TrustServerCertificate=no;"
        )
        # Connect to the database
        self.cnxn = pyodbc.connect(cnxn_string)
          
    def load_top_tracks(self, tracks: list, time_range: str, batch_id: str):
        # Create a cursor
        cursor = self.cnxn.cursor()

        # Set variable values
        ingested_at = dt.datetime.now(dt.timezone.utc)

        # Write the MERGE T-SQL query
        merge_sql = (
            """
            INSERT INTO bronze.top_tracks 
              (time_range, rank, raw_json, ingested_at, api_endpoint, batch_id)
            VALUES 
              (?, ?, ?, ?, ?, ?) 
            """
        )

        for rank, track in enumerate(tracks, start=1):
          values = (
              time_range,
              rank,
              json.dumps(track),
              ingested_at,
              "me/top/tracks",
              batch_id
          )
          cursor.execute(merge_sql, values)

        self.cnxn.commit()

    def load_top_artists(self, artists: list, time_range: str, batch_id: str):
        # Create a cursor
        cursor = self.cnxn.cursor()

        # Set variable values
        ingested_at = dt.datetime.now(dt.timezone.utc)

        # Write the MERGE T-SQL query
        merge_sql = (
            """
            INSERT INTO bronze.top_artists
              (time_range, rank, raw_json, ingested_at, api_endpoint, batch_id)
            VALUES 
              (?, ?, ?, ?, ?, ?) 
            """
        )

        for rank, artist in enumerate(artists, start=1):
          values = (
              time_range,
              rank,
              json.dumps(artist),
              ingested_at,
              "me/top/artists",
              batch_id
          )
          cursor.execute(merge_sql, values)

        self.cnxn.commit()

    def load_recently_played(self, tracks: list, batch_id: str):
        # Create a cursor
        cursor = self.cnxn.cursor()

        # Set variable values
        ingested_at = dt.datetime.now(dt.timezone.utc)

        # Write the MERGE T-SQL query
        merge_sql = (
            """
            INSERT INTO bronze.recently_played
              (raw_json, played_at, ingested_at, api_endpoint, batch_id)
            VALUES 
              (?, ?, ?, ?, ?) 
            """
        )

        for track in tracks:
          values = (
              json.dumps(track),
              track["played_at"],
              ingested_at,
              "me/player/recently-played",
              batch_id
          )
          cursor.execute(merge_sql, values)

        self.cnxn.commit()