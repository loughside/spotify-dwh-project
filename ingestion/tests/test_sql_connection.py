
import os
from dotenv import load_dotenv
import pyodbc

#============== Check Azure SQL connection ====================#

# Load environment variables from .env file
load_dotenv()

# Driver hardcoded — not a secret, just infrastructure config
SQL_DRIVER = "ODBC Driver 18 for SQL Server"
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

# pyodbc expects this exact connection string format for Azure SQL
cnxn_string = (
    f"Driver={{{SQL_DRIVER}}};"
    f"Server={SQL_SERVER};"
    f"Database={SQL_DATABASE};"
    f"UID={SQL_USERNAME};"
    f"PWD={SQL_PASSWORD};"
    "Encrypt=yes;TrustServerCertificate=no;"
)

try:
    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()

    # Simple query to confirm the connection is live and return the SQL Server version
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print(row[0])
    print("Connection successful!")

    # Always close in test scripts — free tier has a low connection limit
    cnxn.close()

except Exception as e:
    print(f"Failed: {e}")

