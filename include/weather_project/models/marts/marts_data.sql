WITH cte AS (
  SELECT *  FROM {{ ref('src_data') }}
)

SELECT
 city, max(temperature) as max_temp,min(temperature) as min_temp,round(avg(temperature),2) as avg_temp,date_
 from cte
 group by city,country,date_