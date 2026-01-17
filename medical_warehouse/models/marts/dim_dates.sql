{{ config(materialized='table', schema='public_marts') }}

WITH date_series AS (
    SELECT 
        generate_series(
            (SELECT MIN(DATE(message_date)) FROM {{ ref('stg_telegram_messages') }}),
            (SELECT MAX(DATE(message_date)) FROM {{ ref('stg_telegram_messages') }}),
            '1 day'::interval
        )::date as full_date
)

SELECT
    TO_CHAR(full_date, 'YYYYMMDD')::integer as date_key,
    full_date,
    EXTRACT(DOW FROM full_date) as day_of_week,
    CASE EXTRACT(DOW FROM full_date)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as day_name,
    EXTRACT(WEEK FROM full_date) as week_of_year,
    EXTRACT(MONTH FROM full_date) as month,
    TO_CHAR(full_date, 'Month') as month_name,
    EXTRACT(QUARTER FROM full_date) as quarter,
    EXTRACT(YEAR FROM full_date) as year,
    CASE 
        WHEN EXTRACT(DOW FROM full_date) IN (0, 6) THEN TRUE 
        ELSE FALSE 
    END as is_weekend
FROM date_series
ORDER BY full_date
