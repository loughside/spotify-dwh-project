
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
          
    def load_fixtures(self, fixtures):
        # Create a cursor
        cursor = self.cnxn.cursor()
        ingested_at = dt.datetime.now(dt.timezone.utc)

        # Write the MERGE T-SQL query
        merge_sql = (
            """
            MERGE INTO 
              bronze.fixtures AS target
            USING 
              (VALUES (?, ?, ?, ?)) AS source (fixture_id, json_response, ingested_at, api_endpoint)
            ON 
              target.fixture_id = source.fixture_id
            WHEN MATCHED THEN UPDATE 
              SET 
                target.json_response = source.json_response,
                target.ingested_at = source.ingested_at,
                target.api_endpoint = source.api_endpoint
            WHEN NOT MATCHED THEN
                INSERT (fixture_id, json_response, ingested_at, api_endpoint)
                  VALUES (
                    source.fixture_id,
                    source.json_response,
                    source.ingested_at,
                    source.api_endpoint);
            """
        )

        for fixture in fixtures:
          values = (
              fixture["fixture"]["id"],
              json.dumps(fixture),
              ingested_at,
              "fixtures"
          )
          cursor.execute(merge_sql, values)

        self.cnxn.commit()