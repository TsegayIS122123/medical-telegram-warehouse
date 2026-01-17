{{ config(materialized='table', schema='marts') }}

SELECT
    ROW_NUMBER() OVER (ORDER BY channel_name) as channel_key,
    channel_name,
    CASE 
        WHEN channel_name = 'lobelia4cosmetics' THEN 'Cosmetics'
        WHEN channel_name = 'tikvahpharma' THEN 'Pharmaceutical'
        ELSE 'Medical'
    END as channel_type,
    COUNT(*) as total_posts,
    AVG(views)::integer as avg_views
FROM {{ ref('stg_telegram_messages') }}
GROUP BY channel_name
