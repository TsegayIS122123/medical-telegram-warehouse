{{ config(materialized='table', schema='marts') }}

SELECT
    m.message_id,
    c.channel_key,
    EXTRACT(YEAR FROM m.message_date)*10000 + 
    EXTRACT(MONTH FROM m.message_date)*100 + 
    EXTRACT(DAY FROM m.message_date) as date_key,
    m.message_text,
    m.message_length,
    m.views as view_count,
    m.forwards as forward_count,
    m.has_image
FROM {{ ref('stg_telegram_messages') }} m
LEFT JOIN {{ ref('dim_channels') }} c ON m.channel_name = c.channel_name
