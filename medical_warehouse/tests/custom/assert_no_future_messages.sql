-- Tests that no messages have unreasonable future dates (beyond 1 day from now)
SELECT 
    message_id,
    channel_name,
    message_date
FROM {{ ref('stg_telegram_messages') }}
WHERE message_date > CURRENT_TIMESTAMP + INTERVAL '1 day'
