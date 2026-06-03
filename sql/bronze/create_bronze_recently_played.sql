
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'recently_played' AND schema_id = SCHEMA_ID('bronze'))
  EXEC('
    CREATE TABLE bronze.recently_played (
      id INT IDENTITY(1,1),
      raw_json NVARCHAR(MAX),
      played_at DATETIME2,
      ingested_at DATETIME2 DEFAULT GETUTCDATE(),
      api_endpoint NVARCHAR(100) NOT NULL,
      batch_id NVARCHAR(100) NOT NULL,
      CONSTRAINT pk_recently_played PRIMARY KEY (id))
    ')
