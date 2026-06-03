
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'top_artists' AND schema_id = SCHEMA_ID('bronze'))
  EXEC('
    CREATE TABLE bronze.top_artists (
      id INT IDENTITY(1,1),
      time_range NVARCHAR(20),
      rank INT,
      raw_json NVARCHAR(MAX),
      ingested_at DATETIME2 DEFAULT GETUTCDATE(),
      api_endpoint NVARCHAR(100) NOT NULL,
      batch_id NVARCHAR(100) NOT NULL,
      CONSTRAINT pk_top_artists PRIMARY KEY (id))
    ')