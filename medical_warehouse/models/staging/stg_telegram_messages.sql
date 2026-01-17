{{ config(materialized='view', schema='staging') }}

SELECT
    message_id,
    channel_name,
    CAST(message_date AS TIMESTAMP) as message_date,
    message_text,
    has_media,
    image_path,
    views,
    forwards,
    scraped_at,
    -- Simple transformations
    LENGTH(message_text) as message_length,
    CASE WHEN image_path IS NOT NULL THEN TRUE ELSE FALSE END as has_image
FROM {{ source('raw', 'telegram_messages') }}
WHERE message_date IS NOT NULL
