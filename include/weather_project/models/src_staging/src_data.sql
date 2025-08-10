WITH raw AS (
    SELECT  *
    FROM {{ source('raw_source', 'weather') }}
)

SELECT
    city,country,temperature,split_part(observed_time,' ',1) as date_
FROM raw