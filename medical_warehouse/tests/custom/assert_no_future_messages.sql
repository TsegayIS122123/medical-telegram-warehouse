-- Test to ensure no messages have future dates
select 
    message_id,
    channel_name,
    message_date
from {{ ref('stg_telegram_messages') }}
where message_date > current_timestamp
