{{ config(materialized='table') }}

with date_range as (
    select 
        generate_series(
            '2024-01-01'::date,
            '2025-12-31'::date,
            '1 day'::interval
        ) as full_date
)

select
    to_char(full_date, 'YYYYMMDD')::integer as date_key,
    full_date,
    extract(dow from full_date) as day_of_week,
    to_char(full_date, 'Day') as day_name,
    extract(week from full_date) as week_of_year,
    extract(month from full_date) as month,
    to_char(full_date, 'Month') as month_name,
    extract(quarter from full_date) as quarter,
    extract(year from full_date) as year,
    case 
        when extract(dow from full_date) in (0, 6) then true 
        else false 
    end as is_weekend
from date_range
