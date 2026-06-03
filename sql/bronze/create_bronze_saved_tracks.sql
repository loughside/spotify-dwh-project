
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'saved_tracks' AND schema_id = SCHEMA_ID('bronze'))
  EXEC('
    CREATE TABLE bronze.saved_tracks (
      id INT IDENTITY(1,1),
      raw_json NVARCHAR(MAX),
      added_at DATETIME2,
      ingested_at DATETIME2 DEFAULT GETUTCDATE(),
      api_endpoint NVARCHAR(100) NOT NULL,
      batch_id NVARCHAR(100) NOT NULL,
      CONSTRAINT pk_saved_tracks PRIMARY KEY (id))
    ')
