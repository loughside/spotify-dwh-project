
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'artists' AND schema_id = SCHEMA_ID('bronze'))
  EXEC('
    CREATE TABLE bronze.artists (
      id INT IDENTITY(1,1),
      raw_json NVARCHAR(MAX),
      ingested_at DATETIME2 DEFAULT GETUTCDATE(),
      api_endpoint NVARCHAR(100) NOT NULL,
      batch_id NVARCHAR(100) NOT NULL,
      CONSTRAINT pk_artists PRIMARY KEY (id))
    ')