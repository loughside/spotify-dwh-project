
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'audio_features' AND schema_id = SCHEMA_ID('bronze'))
  EXEC('
    CREATE TABLE bronze.audio_features (
      id INT IDENTITY(1,1),
      raw_json NVARCHAR(MAX),
      ingested_at DATETIME2 DEFAULT GETUTCDATE(),
      api_endpoint NVARCHAR(100) NOT NULL,
      CONSTRAINT pk_audio_features PRIMARY KEY (id))
    ')

