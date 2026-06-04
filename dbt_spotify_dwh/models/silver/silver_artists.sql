
{{ config(materialized='table', schema='silver') }}

WITH CTE_Data AS (
  SELECT 
    id bronze_id,
    ingested_at,
    JSON_VALUE(raw_json, '$.id') artist_id,
    JSON_VALUE(raw_json, '$.name') artist_name,
    JSON_VALUE(raw_json, '$.images[0].url') image_url
  FROM
    {{source('bronze', 'artists')}}),

CTE_Ranked AS (
  SELECT
    ROW_NUMBER() OVER(PARTITION BY artist_id ORDER BY ingested_at DESC) ranking,
    ingested_at,
    bronze_id,
    artist_id,
    artist_name,
    image_url
  FROM
    CTE_Data
)

SELECT
  artist_id,
  artist_name,
  image_url,
  GETUTCDATE() updated_at 
FROM
  CTE_Ranked
WHERE
  ranking = 1